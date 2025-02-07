from jinja2 import Template
import tempfile
import os
import win32ui
import win32print
import win32con
from PIL import Image, ImageWin


def _print_image(path, portrait = True):
    img = Image.open(path)
    printer_name = "XP-80C" # win32print.GetDefaultPrinter() # remember to include this in dotenv file
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)

    if portrait:
        img = img.rotate(90, expand=True)
    mode = win32con.MM_ANISOTROPIC if portrait else win32con.MM_ISOTROPIC # this is not affecting?
    hDC.SetMapMode(mode) # MM_ANISOTROPIC for portrait.
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

