from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QComboBox
from PyQt5.QtWidgets import QMainWindow, QDialog, QTableView, QAbstractItemView
from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionButton, QStyle
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from qasync import QEventLoop

from constants import names, percentage, files_location  # Import files_location

from printer import print_cheque
from datetime import datetime
import csv
import os.path

from labor_share_window import LaborShareWindow
from other_expences_window import OtherExpensesWindow
from payment_window import PaymentWindow

class ButtonDelegate(QStyledItemDelegate):
    def __init__(self, table, click_handler):
        super().__init__(table)
        self.table = table
        self.click_handler = click_handler

    def paint(self, painter, option, index):  # Draw the button
        if not self.table.indexWidget(index): # Don't override existing widgets
            button = QStyleOptionButton()
            button.rect = option.rect  # Set button size to cell size
            button.text = "Delete"  # Button text
            QApplication.style().drawControl(QStyle.CE_PushButton, button, painter)

    def createEditor(self, parent, option, index):
        return None  # Don't create editor for button (it's not editable)

    def editorEvent(self, event, model, option, index): # Handle clicks
        if event.type() == event.MouseButtonRelease and event.button() == Qt.LeftButton:
            if option.rect.contains(event.pos()):  # Check if click is within button
                self.click_handler.buttonClicked(index.row())  # Emit custom signal
                return True
        return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")

        self.setMinimumSize(600, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a QTableView widget
        self.table_view = QTableView(self)
        layout.addWidget(self.table_view)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Make read-only


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

        self.load_payment_data()
    
    def load_payment_data(self):
        try:
            with open(files_location + 'payments.csv', 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                
                # Skip empty lines
                data = [row for row in reader if any(cell.strip() for cell in row)]

                model = QStandardItemModel(0, 5, self)
                for row in data:
                    row_items = [QStandardItem(item) for item in row]
                    model.appendRow(row_items)

                # Set horizontal header labels
                model.setHorizontalHeaderLabels(["Date/Time", "Doctor", "Patient Name", "Amount", "Action"])  # Example headers

                self.table_view.setModel(model)
                
                # Resize the last column to fill the rest of the space
                self.table_view.resizeColumnsToContents()
                header = self.table_view.horizontalHeader()
                header.setStretchLastSection(True)

                delegate = ButtonDelegate(self.table_view, self) # Create delegate
                self.table_view.setItemDelegateForColumn(4, delegate) # Add button to column 4
                self.table_view.setColumnWidth(4, 80)  # Adjust column width

        except FileNotFoundError:
            print("payments.csv not found.")  # Handle the case where the file doesn't exist
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def buttonClicked(self, row):
        # Get the model and the item from the clicked row
        model = self.table_view.model()
        item = model.item(row, 0)  # Get the first item in the row (you might need to adjust the column index)

        if item is not None:  # Check if an item was found
            # Display the confirmation dialog
            reply = QMessageBox.question(self, 'Delete Record',
                                           f"Are you sure you want to delete this record?<br><br>{item.text()}", # Display info about the record
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                # Remove the row from the model
                model.removeRow(row)

                # Save the updated data to CSV (optional but recommended)
                self.save_payment_data()
    
    def save_payment_data(self): # New method to save the CSV data
        try:
            with open(files_location + 'payments.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                model = self.table_view.model()
                for row in range(model.rowCount()):
                    row_data = []
                    for column in range(model.columnCount() -1 ): # Exclude the button column
                        item = model.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append("") # Add empty string if item is None
                    writer.writerow(row_data)

        except Exception as e:
            print(f"Error saving to CSV: {e}")
    
    def open_other_expenses_window(self): # New method to open the new window
        if self.other_expenses_window is None:
            self.other_expenses_window = OtherExpensesWindow(self)
        self.other_expenses_window.exec_()
        

    def open_payment_window(self):
        if self.payment_window is None:
            self.payment_window = PaymentWindow(self)

        result = self.payment_window.exec_()  # Use exec_() for PyQt5

        if result == QDialog.Accepted: # Refresh only if the dialog was closed with 'Accepted' (or similar successful condition if you have one).
            self.load_payment_data() # Reload after new payment registered

    def open_labor_share_window(self): # New function in MainWindow
        if self.labor_share_window is None:
            self.labor_share_window = LaborShareWindow(self) # Instance of labor_share window
        self.labor_share_window.exec_()

