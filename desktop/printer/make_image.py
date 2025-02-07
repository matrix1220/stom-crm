import os
from jinja2 import Template
import imgkit
#import pdfkit

# Determine script's directory to construct absolute paths
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set output path to the script's directory
output_path = os.path.join(script_dir, "cheque.jpg") # Absolute path to cheque1.jpg

def make_image(template_path, data, options={'width': '576'}):
    with open(os.path.join(script_dir, template_path), "r") as f:  # Use absolute template path
        template = Template(f.read())
    
    rendered_html = template.render(**data)
    options['quiet'] = ''
    imgkit.from_string(rendered_html, output_path, options=options)
    return output_path



def make_double_cheque_image(payee, amount, date, doctor):
    with open(os.path.join(script_dir, "2x_cheque_template.html"), "r") as f:  # Use absolute template path
        template = Template(f.read())

    rendered_html = template.render(payee=payee, amount=amount, date=date, doctor=doctor)
    options = {
        'height': '576',
        #'width': '2374',
        #'width': '576',
        #'height': '2374',
        # 'format': 'jpeg',
        # 'quality': '100',
        'quiet': '',
    }

    imgkit.from_string(rendered_html, output_path, options=options)
    return output_path

def make_cheque_image(payee, amount, date, doctor):
    with open(os.path.join(script_dir, "cheque_template.html"), "r") as f:  # Use absolute template path
        template = Template(f.read())

    rendered_html = template.render(payee=payee, amount=amount, date=date, doctor=doctor)
    options = {
        'width': '576',
        'quiet': '',
    }

    imgkit.from_string(rendered_html, output_path, options=options)
    return output_path

def make_doctor_cheque_image(doctor, date, payments, labor_shares, total):
    with open(os.path.join(script_dir, "doctor_cheque_template.html"), "r") as f:  # Use absolute template path
        template = Template(f.read())

    rendered_html = template.render(doctor=doctor, date=date, payments=payments, labor_shares=labor_shares, total=total)
    options = {
        'width': '576',
        'quiet': '',
    }

    imgkit.from_string(rendered_html, output_path, options=options)
    return output_path



