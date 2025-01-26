
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QComboBox
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtCore import Qt
from qasync import QEventLoop

from constants import names, percentage

from printer import print_cheque
from datetime import datetime
import csv
import os.path


class PayrollWindow(QDialog):  # New Payroll Window
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Payroll")  # Window title
        self.layout = QVBoxLayout(self)

        self.setMinimumSize(400, 300)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.label = QLabel("Enter Payroll Information:")  # Instructions
        self.layout.addWidget(self.label)

        self.combo1 = QComboBox()
        self.combo1.addItems(names)  # Use names from constants or another source
        self.label1 = QLabel("Doktor:")  # Employee selection
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.combo1)


        self.input3 = QLineEdit()
        self.label3 = QLabel("Amount:")   # Payroll amount
        self.layout.addWidget(self.label3)
        self.layout.addWidget(self.input3)

        self.combo1.currentIndexChanged.connect(self.update_payroll_records) # Connect to update function
        

        self.payroll_records_label = QLabel("") # Label to display records
        self.layout.addWidget(self.payroll_records_label)

        self.button = QPushButton("Process Payroll")  # Button text
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.process_payroll) # Connect to a different function


        self.layout.addSpacing(10)

        self.update_payroll_records()
    
    def update_payroll_records(self):
        employee = self.combo1.currentText()
        today = datetime.now().strftime("%Y-%m-%d")
        payroll_records = []
        payment_records = []  # List to store payment records
        total_payroll = 0  # Initialize total payroll
        total_payments = 0 # Initialize total payments

        try:
            if os.path.isfile("payroll.csv"):
                with open('payroll.csv', 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        date_string, payroll_employee, amount_str = row
                        date_obj = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").date()
                        if date_obj.strftime("%Y-%m-%d") == today and payroll_employee == employee:
                            try:
                                amount = float(amount_str)
                                total_payroll += amount # Add to total
                                payroll_records.append(row) # Append the row (or just the amount if that's all you need)
                            except ValueError:
                                print(f"Invalid payroll amount: {amount_str}") # Handle non-numeric data

            if os.path.isfile("payments.csv"):
                with open('payments.csv', 'r', newline='', encoding='utf-8') as csvfile: # Open payments.csv
                    reader = csv.reader(csvfile)
                    for row in reader:
                        date_string, payment_employee, patient, amount_str = row
                        date_obj = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").date()
                        if date_obj.strftime("%Y-%m-%d") == today and payment_employee == employee:
                            try:
                                amount = float(amount_str)
                                total_payments += amount
                                payment_records.append(row)
                            except ValueError:
                                print(f"Invalid payment amount: {amount_str}")


        except FileNotFoundError:
            pass  # Handle the case where the files don't exist

        records_text = ""
        if payroll_records:
            records_text += f"Today's Payroll:<br>"
            records_text += "<br>".join([", ".join(record) for record in payroll_records])

        if payment_records: # Add payment records to the output if available
            if records_text: # Add some spacing to separate from payroll records
                records_text += "<br><br>"
            records_text += f"Today's Payments received:<br>"
            records_text += "<br>".join([", ".join(record) for record in payment_records])



        if not records_text: # Check if any records were added (payroll or payment).
            records_text = f"No payroll or payment records found for {employee} today."
            
        records_text += "<br><br>"
        records_text += f"Total Payroll: {total_payroll:.2f}<br>"
        records_text += f"Total Payments received: {total_payments:.2f}*{percentage[employee]} = {total_payments*percentage[employee]}<br>"
        records_text += f"Difference: {total_payments*percentage[employee] - total_payroll:.2f}"  # Calculate and display the difference
        
        
        self.payroll_records_label.setText(records_text)


    def process_payroll(self):  # New function for payroll processing
        employee = self.combo1.currentText()
        amount = self.input3.text()
        date_today = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Include date and time

        try:
            with open('payroll.csv', 'a', newline='', encoding='utf-8') as csvfile:  # Separate CSV for payroll
                writer = csv.writer(csvfile)
                writer.writerow([date_today, employee, amount]) # Write to payroll CSV
        except Exception as e:
            print(f"Error saving payroll to CSV: {e}") # Error handling
            # Consider showing an error message to the user

        print(f"Payroll processed for: {employee}, Amount: {amount}")


        self.close()
