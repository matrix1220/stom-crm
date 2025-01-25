import sys
import asyncio

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QComboBox
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtCore import Qt
from qasync import QEventLoop

from constants import names

#from excel.com import save_new_record
#save_new_record = None
from printer import print_cheque
from datetime import datetime
import csv


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

    def open_payment_window(self):
        if self.payment_window is None:
            self.payment_window = PaymentWindow(self)

        result = self.payment_window.exec_()  # Use exec_() for PyQt5

        if result == QDialog.Accepted:
            pass
        else:
            pass



if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Integrate asyncio with PyQt5 event loop
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)  

    window = MainWindow()
    window.show()

    with loop:
        loop.run_forever()

