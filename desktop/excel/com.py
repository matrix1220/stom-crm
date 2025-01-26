import win32com.client

from constants import names, file_path, sheet_name


try:
    excel = win32com.client.GetActiveObject("Excel.Application") # Get running Excel instance
except Exception as e: # Handle case where Excel isn't running
    print(f"Error: Could not get Excel application. Is Excel running? {e}")

for wb in excel.Workbooks:
    if wb.FullName == file_path:  # Use FullName for reliable path comparison
        print("Workbook is already open. Reusing it.")
        ws = wb.Worksheets(sheet_name)
        break # Exit the loop since we found the workbook
else:
    # Workbook not found, open it
    print("Workbook is not open. Opening it now.")
    wb = excel.Workbooks.Open(file_path)
    ws = wb.Worksheets(sheet_name)

def read_excel_data():
    if excel is None:
        return None # Or raise an exception, depending on your needs

    try:

        data = {}
        for col in range(1, 17):
            for row in range(9, 24):
                actual_row = row - 8
                cell_value = ws.Cells(row, col * 2).Value
                if cell_value:
                    doctor_name = names[col - 1]
                    if doctor_name not in data:
                        data[doctor_name] = {}
                    data[doctor_name][actual_row] = cell_value
        #wb.Close(SaveChanges=False) # Close without saving changes since we're only reading
        return data
    
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        #if wb: wb.Close(SaveChanges=False)
        return None # or handle the error as needed

data = read_excel_data()

import time
def save_new_record(doctor, amount):
    if doctor in data:
        new_row = len(data[doctor]) + 1
    else:
        data[doctor] = {}
        new_row = 1
    
    data[doctor][new_row] = amount

    col = (names.index(doctor) + 1)*2
    
    actual_row = 9 + new_row - 1
    
    try:
        ws.Cells(actual_row, col).Value = amount  # Write the new amount to the cell
        wb.Save()  # Save the changes

        # Give Excel a moment to process (hacky, but sometimes necessary)
        time.sleep(0.5) # Adjust delay if needed.

    except Exception as e:  # Handle errors
        print(f"Error modifying Excel file: {e}")
    finally:
        wb.Close() # Close the workbook