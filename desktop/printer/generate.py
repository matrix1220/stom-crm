from jinja2 import Template
import tempfile
import os
import win32ui
import win32print
import win32con
from PIL import Image, ImageWin

from html2image import Html2Image

hti = Html2Image(size=(200, 200))

def print_cheque(payee, amount, date, doctor):
    # Load HTML template
    with open("printer/template.html", "r") as f:
        template = Template(f.read())

    # Render template with dynamic data
    rendered_html = template.render(payee=payee, amount=amount, date=date, doctor=doctor)

    # # Generate PDF
    # with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmpfile:
    #     output_path = tmpfile.name  # Get the temporary file path
    #     print(output_path)
    #     hti.screenshot(html_str=rendered_html, save_as=output_path)
    
    # Print the generated JPG image
    output_path = "cheque.jpg"
    hti.screenshot(html_str=rendered_html, save_as=output_path)
    #os.startfile(output_path, "print")
    #os.startfile(output_path)
    img = Image.open(output_path)
    printer_name = win32print.GetDefaultPrinter()
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)

    # Set portrait orientation (corrected)
    hDC.SetMapMode(win32con.MM_ANISOTROPIC) # MM_ANISOTROPIC for portrait.
    hDC.SetViewportExt((img.width, img.height))  # Viewport matches image dimensions
    hDC.SetWindowExt((img.width, img.height))   # Window extents match image dimensions


    # Calculate scaling (if needed) - you might adjust this
    printable_area = hDC.GetDeviceCaps(win32con.HORZRES), hDC.GetDeviceCaps(win32con.VERTRES)
    scale_factor = min(printable_area[0] / img.width, printable_area[1] / img.height)  # Maintain aspect ratio

    scaled_width = int(img.width * scale_factor)
    scaled_height = int(img.height * scale_factor)


    hDC.StartDoc("Cheque")
    hDC.StartPage()

    dib = ImageWin.Dib(img)  # Create DIB from the original image
    dib.draw(hDC.GetHandleOutput(), (0, 0, scaled_width, scaled_height)) # Draw potentially scaled.

    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()

# Example usage
#generate_cheque_html("John Doe", "1500.00", "2025-01-22", "shufik", "cheque.jpg")