import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QListWidget, QMessageBox, QHBoxLayout, QStatusBar
)
from PyQt5.QtGui import QIcon
import matplotlib.pyplot as plt
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(700, 300, 1000, 600)
        self.setWindowTitle("Expense Tracker - No Transactions")
        self.setWindowIcon(QIcon())  # Optional: Add an icon if needed
        self.initUI()
        
    def initUI(self):
        try:
            # Central Widget
            central_widget = QWidget()
            self.setCentralWidget(central_widget)

            # Main Layout
            layout = QVBoxLayout()

            # Input Form
            self.task_input = QFormLayout()
            self.input_title = QLineEdit()
            self.input_title.setPlaceholderText("Enter title here...")
            self.input_amount = QLineEdit()
            self.input_amount.setPlaceholderText("Enter amount in numbers...")
            self.input_category = QLineEdit()
            self.input_category.setPlaceholderText("Enter category...")

            # Adding Labels to Form
            self.task_input.addRow("Title: ", self.input_title)
            self.task_input.addRow("Amount: ", self.input_amount)
            self.task_input.addRow("Category: ", self.input_category)

            # Add Button and Show Graph Button
            self.button_add = QPushButton("Add Transaction")
            self.button_graph = QPushButton("Show Graph")

            # Expense List
            self.expense_list = QListWidget()

            # Adding Widgets to Layout
            layout.addWidget(self.expense_list)
            layout.addLayout(self.task_input)
            
            button_layout = QHBoxLayout()
            button_layout.addWidget(self.button_add)
            button_layout.addWidget(self.button_graph)
            layout.addLayout(button_layout)

            central_widget.setLayout(layout)

            # Connect Buttons to Functions
            self.button_add.clicked.connect(self.func_add)
            self.button_graph.clicked.connect(self.show_graph)

            # Initialize expense data
            self.transactions = []

            # Status Bar with Transaction Count
            self.status_bar = QStatusBar()
            self.setStatusBar(self.status_bar)

        except Exception as e:
            self.show_message(f"An error occurred while initializing the application: {str(e)}", "Initialization Error", QMessageBox.Critical)

    # Function to Add Transactions
    def func_add(self):
        try:
            title = self.input_title.text()
            category = self.input_category.text()
            amount = self.input_amount.text()

            # Check if fields are empty
            if not title:
                self.show_message("Please enter a title for the transaction.", "Field Missing", QMessageBox.Warning)
                return
            if not category:
                self.show_message("Please enter a category for the transaction.", "Field Missing", QMessageBox.Warning)
                return
            if not amount:
                self.show_message("Please enter an amount for the transaction.", "Field Missing", QMessageBox.Warning)
                return

            # Input Validation for Amount
            if not amount.isdigit():
                self.show_message("Amount must be a number.", "Invalid Input", QMessageBox.Warning)
                return

            # Add Transaction
            self.transactions.append({"title": title, "category": category, "amount": int(amount)})
            self.expense_list.addItem(f"{len(self.transactions)}. {title}\n   Category: {category}\n   Amount: {amount}")
            self.input_title.clear()
            self.input_category.clear()
            self.input_amount.clear()

            # Update Status Bar
            self.update_status_bar()

            # Success Message
            self.show_message("Transaction Added!", "Success", QMessageBox.Information)

        except Exception as e:
            self.show_message(f"An error occurred while adding the transaction: {str(e)}", "Error", QMessageBox.Critical)

    # Function to Show Graph
    def show_graph(self):
        try:
            if not self.transactions:
                self.show_message("No transactions to show graph.", "No Data", QMessageBox.Warning)
                return
            
            # Prepare Data for Graph
            categories = [txn['category'] for txn in self.transactions]
            amounts = [txn['amount'] for txn in self.transactions]

            # Creating the Plot
            plt.figure(figsize=(8, 5))
            plt.bar(categories, amounts, color='skyblue')

            # Add Labels and Title
            plt.title("Transaction Breakdown")
            plt.xlabel("Categories")
            plt.ylabel("Amount")
            plt.xticks(rotation=45, ha='right')

            # Show the plot
            plt.tight_layout()
            plt.show()

        except Exception as e:
            self.show_message(f"An error occurred while generating the graph: {str(e)}", "Graph Error", QMessageBox.Critical)

    # Function to Update the Status Bar
    def update_status_bar(self):
        try:
            num_transactions = len(self.transactions)
            self.setWindowTitle(f"Expense Tracker - {num_transactions} Transactions")
            self.status_bar.showMessage(f"{num_transactions} Transaction(s) Recorded", 3000)

        except Exception as e:
            self.show_message(f"An error occurred while updating the status bar: {str(e)}", "Status Bar Error", QMessageBox.Critical)

    # Function to Show Pop-up Messages (Error, Success, Info)
    def show_message(self, message, title, icon_type):
        try:
            # Correct usage of QMessageBox with buttons and icons
            if icon_type == QMessageBox.Information:
                QMessageBox.information(self, title, message, QMessageBox.Ok, QMessageBox.NoButton)
            elif icon_type == QMessageBox.Warning:
                QMessageBox.warning(self, title, message, QMessageBox.Ok, QMessageBox.NoButton)
            elif icon_type == QMessageBox.Critical:
                QMessageBox.critical(self, title, message, QMessageBox.Ok, QMessageBox.NoButton)
            else:
                # Default fallback for unhandled icon types
                QMessageBox.information(self, title, message, QMessageBox.Ok, QMessageBox.NoButton)
        except Exception as e:
            # Catch any exception that may occur during message display
            print(f"Error displaying message: {e}")

# Main Application Loop
if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)
