from jinja2 import Environment, FileSystemLoader
import datetime
import os
from jinja2 import Template
import imgkit
import csv
from collections import defaultdict
import pdfkit

from .print_image import _print_image
from .make_image import make_image

# Determine script's directory to construct absolute paths
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set output path to the script's directory
output_path = os.path.join(script_dir, "cheque.jpg")

output_pdf = os.path.join(script_dir, "report.pdf") # Absolute path to cheque1.jpg

from constants import payments_file, labor_share_file, other_expences_file

def get_daily_report_data(full=False):
    # data (dict): A dictionary containing the report data.
    # Should include:
    # - total_payments (int): Total payments received.
    # - payments (list): A list of payment dictionaries. Each payment dictionary should contain:
    #     - doctor (str): Doctor's name.
    #     - total (int): Total amount for the doctor.
    #     - payments (list, optional): A list of individual payment details. Each detail should contain:
    #         - payee (str): Payer's name.
    #         - amount (int): Payment amount.
    # - total_labor_shares (int): Total labor shares paid.
    # - labor_shares (list): A list of labor share dictionaries. Each dictionary should contain:
    #     - doctor (str): Doctor's name.
    #     - amount (int): Labor share amount.
    # - totally_left (int): Total amount left.
    date_str = datetime.date.today().strftime('%Y-%m-%d')
    data = {
        "date": date_str,
        "total_payments": 0,
        "payments": [],
        "total_labor_shares": 0,
        "labor_shares": [],
        "total_other_expenses": 0,  # New field for other expenses
        "other_expenses": [],  # New field for other expenses
        "totally_left": 0
    }

    # Read payments.csv
    payments_by_doctor = defaultdict(lambda: {"doctor": "", "total": 0, "items": 0, "payments": []})
    with open(payments_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            date_time_str, doctor, payee, amount_str = row
            try:
                date_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S").date()
                if date_obj.strftime("%Y-%m-%d") == date_str:
                    amount = float(amount_str)
                    data["total_payments"] += amount
                    payments_by_doctor[doctor]["doctor"] = doctor
                    payments_by_doctor[doctor]["total"] += amount
                    payments_by_doctor[doctor]["items"] += 1
                    if full:
                        payments_by_doctor[doctor]["payments"].append({"payee": payee, "amount": amount})
            except (ValueError, IndexError) as e:
                print(f"Error reading payments.csv row: {row}. Error: {e}")

    data["payments"] = list(payments_by_doctor.values())

    # Transpose payments for HTML table
    transposed_payments = []
    max_payments = max([len(doctor_data["payments"]) for doctor_data in data["payments"]]) if data["payments"] else 0

    for i in range(max_payments):
        row = []
        for doctor_data in data["payments"]:
            try:
                payment = doctor_data["payments"][i]
                row.append({"doctor": doctor_data["doctor"], "payee": payment["payee"], "amount": payment["amount"]})
            except IndexError:
                row.append({"doctor": doctor_data["doctor"], "payee": "", "amount": ""}) # Add empty cell if no payment
        transposed_payments.append(row)

    data["transposed_payments"] = transposed_payments



    # Read labor_share.csv
    with open(labor_share_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            date_time_str, doctor, amount_str = row
            try:
                date_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S").date()
                if date_obj.strftime("%Y-%m-%d") == date_str:
                    amount = float(amount_str)
                    data["total_labor_shares"] += amount
                    data["labor_shares"].append({"doctor": doctor, "amount": amount})
            except (ValueError, IndexError) as e:
                print(f"Error reading labor_share.csv row: {row}. Error: {e}")

    # Read other_expences.csv  (New)
    with open(other_expences_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header row (if exists)

        for row in reader:  # Corrected loop variable
            date_time_str, description, amount_str = row
            try:
                date_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S").date()
                if date_obj.strftime("%Y-%m-%d") == date_str:

                    amount = float(amount_str)
                    data["total_other_expenses"] += amount
                    data["other_expenses"].append({"description": description, "amount": amount})  # Corrected field name
            except (ValueError, IndexError) as e:
                print(f"Error reading other_expenses.csv row: {row}. Error: {e}")  # Corrected file name



    data["totally_left"] = data["total_payments"] - data["total_labor_shares"] - data["total_other_expenses"]  # Subtract expenses
    return data

def make_daily_report_image(full=False):
    data = get_daily_report_data(full)
    return make_image("daily_report_template.html", data)

def make_pdf(template_path, data):
    with open(os.path.join(script_dir, template_path), "r") as f:  # Use absolute template path
        template = Template(f.read())
    
    rendered_html = template.render(**data)
    options = {
        'page-size': 'A4',
        'margin-top': '0',
        'margin-right': '0',
        'margin-bottom': '0',
        'margin-left': '0',
        'quiet': '',
    }
    pdfkit.from_string(rendered_html, output_pdf, options=options)
    return output_pdf

def make_daily_A4_report_document(full=True):
    data = get_daily_report_data(full)
    return make_pdf("daily_A4_report_template.html", data)




# make_daily_A4_report_document()
# make_daily_report_image()
#_print_image(output_path, False)  # Print the cheque to the default printer using imgkit