
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QComboBox
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtCore import Qt
from qasync import QEventLoop

from constants import names, percentage

from printer import print_cheque
from datetime import datetime
import csv
import os.path

from labor_share_window import LaborShareWindow
from other_expences_window import OtherExpensesWindow
from payment_window import PaymentWindow


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

        open_labor_share_button = QPushButton("Register labor share")
        open_labor_share_button.clicked.connect(self.open_labor_share_window)
        layout.addWidget(open_labor_share_button)
        self.labor_share_window = None

        open_other_expenses_button = QPushButton("Open other expenses")  # New button
        open_other_expenses_button.clicked.connect(self.open_other_expenses_window)  # Connect
        layout.addWidget(open_other_expenses_button)  # Add to layout
        self.other_expenses_window = None
    
    def open_other_expenses_window(self): # New method to open the new window
        if self.other_expenses_window is None:
            self.other_expenses_window = OtherExpensesWindow(self)
        self.other_expenses_window.exec_()
        

    def open_payment_window(self):
        if self.payment_window is None:
            self.payment_window = PaymentWindow(self)

        result = self.payment_window.exec_()  # Use exec_() for PyQt5

        # if result == QDialog.Accepted:
        #     pass
        # else:
        #     pass
    
    def open_labor_share_window(self): # New function in MainWindow
        if self.labor_share_window is None:
            self.labor_share_window = LaborShareWindow(self) # Instance of labor_share window
        self.labor_share_window.exec_()

