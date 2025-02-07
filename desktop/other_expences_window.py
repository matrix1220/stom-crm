

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QComboBox
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtCore import Qt

from constants import names, percentage, files_location, other_expences_file


from printer import print_cheque
from datetime import datetime
import csv
import os.path



class OtherExpensesWindow(QDialog):  # New class for the new payment window
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Expence") # Set a different title
        self.layout = QVBoxLayout(self)

        self.setMinimumSize(400, 300)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.expenses_label = QLabel("Today's Expenses:<br>")  # Label to display expenses
        self.layout.addWidget(self.expenses_label)
        self.update_expenses() # Update initially and after adding new expenses

        self.label = QLabel("Enter Expence Information:")
        self.layout.addWidget(self.label)

        # Other input fields
        self.input2 = QLineEdit()  
        self.label2 = QLabel("Description:")
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.input2)

        self.input3 = QLineEdit()
        self.label3 = QLabel("Amount:")
        self.layout.addWidget(self.label3)
        self.layout.addWidget(self.input3)
        
        #... Add other necessary input fields


        self.button = QPushButton("Register Expense")
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.process_payment) # Connect to a function
    
    def update_expenses(self):
        today = datetime.now().strftime("%Y-%m-%d")
        expenses_records = []
        total_expenses = 0

        try:
            if os.path.isfile(other_expences_file):  # Ensure correct CSV file name
                with open(other_expences_file, 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader) # skip the header if it exists
                    for row in reader:
                        date_string, description, amount_str = row # corrected variable name
                        date_obj = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").date()

                        if date_obj.strftime("%Y-%m-%d") == today:
                            try:
                                amount = float(amount_str)
                                total_expenses += amount
                                expenses_records.append(f"{description}: {amount}") # Store description and amount
                            except ValueError:
                                print(f"Invalid expense amount: {amount_str}")
        except FileNotFoundError:
            pass

        if expenses_records:
            expenses_text = "<br>".join(expenses_records) + "<br><br>" # Display descriptions
            expenses_text += f"Total Expenses: {total_expenses:.2f}"  # Display total expenses
        else:
            expenses_text = "No expenses recorded for today."

        self.expenses_label.setText(expenses_text)


    def process_payment(self):
        # Get input values
        description = self.input2.text()
        amount = self.input3.text()

        try:
            with open(other_expences_file, 'a', newline='', encoding='utf-8') as csvfile:  # Use a different CSV file or same
                writer = csv.writer(csvfile)
                now = datetime.now()
                date_time_string = now.strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([date_time_string, description, amount]) 
        except Exception as e:
            print(f"Error saving to CSV: {e}")
        
        print(f"New Expence registered: Description - {description}, Amount - {amount}") # Updated message

        self.update_expenses()

        self.close()
