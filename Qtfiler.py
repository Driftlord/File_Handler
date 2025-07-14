from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog,
    QLabel, QTextEdit, QVBoxLayout, QWidget, QMessageBox, QMenuBar
)
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Dialog Example")
        self.setGeometry(100, 100, 600, 400)

        # Widgets
        self.label = QLabel("No file opened yet.")
        self.text_edit = QTextEdit()
        
        # Buttons
        self.open_button = self.create_button("Open File", "Ctrl+O", self.open_file)
        self.save_button = self.create_button("Save File", "Ctrl+S", self.save_file)
        self.folder_button = self.create_button("Pick Folder", "Ctrl+F", self.pick_folder)

        # Layout Setup
        self.setup_layout()

        # Menu Bar
        self.setup_menu()

    def create_button(self, text, shortcut, handler):
        """Helper method to create buttons with shortcuts and handlers."""
        button = QPushButton(text)
        button.setShortcut(shortcut)
        button.clicked.connect(handler)
        return button

    def setup_layout(self):
        """Setup the layout of widgets in the window."""
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.open_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.folder_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def setup_menu(self):
        """Setup the menu bar with help option."""
        menu = self.menuBar()
        help_menu = menu.addMenu("Help")
        help_action = help_menu.addAction("Help is here")
        help_action.triggered.connect(self.show_help)

    def show_help(self):
        """Display help information."""
        QMessageBox.information(
            self,
            "Help",
            "You can open, save files, or pick a folder using the buttons or shortcuts like Ctrl+O, Ctrl+S, Ctrl+F."
        )

    def open_file(self):
        """Handle file opening with multiple file types support."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open File", 
            "", 
            "Text Files (*.txt);;PDF Files (*.pdf);;Image Files (*.jpg *.png);;All Files (*)"
        )
        if file_path:
            try:
                # Try to open the file as text (only works for text files)
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.text_edit.setText(content)
                    self.label.setText(f"Opened: {file_path}")
            except Exception as e:
                # If opening the file as text fails, show an error message
                self.show_error(f"Failed to open the file: {e}")

    def save_file(self):
        """Handle file saving."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            content = self.text_edit.toPlainText()
            try:
                with open(file_path, "w") as file:
                    file.write(content)
                    self.label.setText(f"Saved to: {file_path}")
            except Exception as e:
                self.show_error(f"Failed to save the file: {e}")

    def pick_folder(self):
        """Handle folder selection."""
        folder_path = QFileDialog.getExistingDirectory(self, "Choose Folder")
        if folder_path:
            self.label.setText(f"Folder selected: {folder_path}")
            print("You picked", folder_path)
        else:
            self.show_error("No folder selected!")

    def show_error(self, message):
        """Show error messages."""
        QMessageBox.critical(self, "Error", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
