
import pdfkit

options = {
    'page-width': '80mm',  # Set page width
    'page-height': '297mm',  # Set page height (standard A4, optional)
    'margin-top': '4mm',
    'margin-right': '2mm',
    'margin-bottom': '2mm',
    'margin-left': '2mm',
}

# Generate PDF from HTML string
pdfkit.from_file('printer/template.html', 'output.pdf', options=options)