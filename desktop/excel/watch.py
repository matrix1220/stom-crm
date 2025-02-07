


    

# import os
# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler

# class ExcelChangeHandler(FileSystemEventHandler):
#     def __init__(self, excel_filepath, callback_function):
#         self.excel_filepath = excel_filepath
#         self.callback = callback_function  # Store the callback function

#     def on_modified(self, event):
#         if event.src_path == self.excel_filepath:
#             try:
#                 print(f"Change detected in {self.excel_filepath} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
#                 self.callback(self.excel_filepath)  # Call the provided callback function
#             except Exception as e:
#                 print(f"An error occurred during processing: {e}")


# def watch_excel_changes(excel_filepath, callback_function):
#     """Watches an Excel file for changes and calls a callback function when a change is detected.

#     Args:
#         excel_filepath (str): The path to the Excel file to watch.
#         callback_function (function): The function to call when a change is detected.
#                                       This function should accept the excel_filepath as an argument.
#     """
#     event_handler = ExcelChangeHandler(excel_filepath, callback_function)
#     observer = Observer()
#     observer.schedule(event_handler, os.path.dirname(excel_filepath), recursive=False)
#     observer.start()

#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()


# # Example callback function (replace this with your actual logic):
# def process_excel_data(filepath):
#     """
#     This function will be called when a change is detected in the Excel file.
#     """
#     try:
#         print(f"Processing Excel data from: {filepath}")
#     except Exception as e:
#         print(f"Error processing Excel file: {e}")


# # Example usage:
# excel_file = "your_excel_file.xlsx"  # Replace with your actual file path
# watch_excel_changes(excel_file, process_excel_data)








# import pythoncom
# import win32com.client

# class ExcelEventHandler:
#     def OnSheetChange(self, sh, target):
#         print(f"Change detected in sheet: {sh.Name}, cell: {target.Address}")
#         print(f"New value: {target.Value}")

# # Start Excel and open a workbook
# excel = win32com.client.DispatchWithEvents("Excel.Application", ExcelEventHandler)
# excel.Visible = True  # Show Excel window

# # Open an existing workbook or create a new one
# wb = excel.Workbooks.Open(r"your_file.xlsx")

# # Keep the script running to listen for events
# print("Listening for events... Press Ctrl+C to stop.")
# while True:
#     pythoncom.PumpWaitingMessages()