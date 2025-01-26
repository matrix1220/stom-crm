
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QComboBox
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtCore import Qt
from qasync import QEventLoop

from constants import names, percentage

from printer import print_cheque
from datetime import datetime
import csv
import os.path

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

        open_payment_button = QPushButton("Register payment")
        open_payment_button.clicked.connect(self.open_payment_window)
        layout.addWidget(open_payment_button)
        self.payment_window = None

        open_payroll_button = QPushButton("Register labor share")
        open_payroll_button.clicked.connect(self.open_payroll_window)
        layout.addWidget(open_payroll_button)
        self.payroll_window = None

        open_new_payment_button = QPushButton("Open other expenses")  # New button
        open_new_payment_button.clicked.connect(self.open_new_payment_window)  # Connect
        layout.addWidget(open_new_payment_button)  # Add to layout
        self.new_payment_window = None
    
    def open_new_payment_window(self): # New method to open the new window
        if self.new_payment_window is None:
            self.new_payment_window = NewPaymentWindow(self)
        self.new_payment_window.exec_()
        

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

