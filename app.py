import sys
import asyncio

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QComboBox
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtCore import Qt
from qasync import QEventLoop

from constants import names, percentage

#from excel.com import save_new_record
#save_new_record = None
from printer import print_cheque
from datetime import datetime
import csv
import os.path


class PaymentWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("To'lov qilish")
        self.layout = QVBoxLayout(self)

        self.setMinimumSize(400, 300)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.label = QLabel("Malumotlarni kiriting:")
        self.layout.addWidget(self.label)

        self.combo1 = QComboBox()
        self.combo1.addItems(names)
        self.label1 = QLabel("Doktor:")
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.combo1)

        self.input2 = QLineEdit()
        self.label2 = QLabel("Ism Familia:")
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.input2)

        self.input3 = QLineEdit()
        self.label3 = QLabel("Summa:")
        self.layout.addWidget(self.label3)
        self.layout.addWidget(self.input3)

        self.button = QPushButton("To'lov")
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.process_inputs)

        self.layout.addSpacing(10)

    def process_inputs(self):
        doctor = self.combo1.currentText()
        patient_name = self.input2.text()
        amount = self.input3.text()
        date_today = datetime.now().strftime("%Y-%m-%d")  # Get today's date

        print(f"To'lov amalga oshmoqda: {doctor}, {patient_name}, {amount}")
        print_cheque(patient_name, amount, date_today, doctor) # Use today's date
        

        try:
            with open('payments.csv', 'a', newline='', encoding='utf-8') as csvfile:  # 'a' mode appends
                writer = csv.writer(csvfile)
                now = datetime.now()
                date_time_string = now.strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([date_time_string, doctor, patient_name, amount])  # Include time
        except Exception as e:
            print(f"Error saving to CSV: {e}")  # Handle potential errors
        
        print(f"To'lov qilindi: {doctor}, {patient_name}, {amount}")

        self.close()  # Close the payment window after successful payment

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")

        self.setMinimumSize(600, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        label = QLabel("This is the main window.")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        open_payment_button = QPushButton("Open Payment Window")
        open_payment_button.clicked.connect(self.open_payment_window)
        layout.addWidget(open_payment_button)
        self.payment_window = None

        open_payroll_button = QPushButton("Open Payroll Window")
        open_payroll_button.clicked.connect(self.open_payroll_window)
        layout.addWidget(open_payroll_button)
        self.payroll_window = None

        

    def open_payment_window(self):
        if self.payment_window is None:
            self.payment_window = PaymentWindow(self)

        result = self.payment_window.exec_()  # Use exec_() for PyQt5

        # if result == QDialog.Accepted:
        #     pass
        # else:
        #     pass
    
    def open_payroll_window(self): # New function in MainWindow
        if self.payroll_window is None:
            self.payroll_window = PayrollWindow(self) # Instance of payroll window
        self.payroll_window.exec_()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Integrate asyncio with PyQt5 event loop
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)  

    window = MainWindow()
    window.show()

    with loop:
        loop.run_forever()

