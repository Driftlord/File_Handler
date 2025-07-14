from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog,
    QLabel, QTextEdit, QVBoxLayout, QWidget, QMessageBox
)
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Dialog Example")
        self.setGeometry(100, 100, 500, 300)

        # Widgets
        self.label = QLabel("No file opened yet.")
        self.text_edit = QTextEdit()

        # Menu Bar
        menu = self.menuBar()
        help_menu = menu.addMenu("Help!!!")

        help_action = help_menu.addAction("Help is here")
        help_action.triggered.connect(self.show_help)

        # Buttons
        self.open_button = QPushButton("Open File")
        self.save_button = QPushButton("Save File")
        self.folder_button = QPushButton("Pick Folder")
        
        # Shortcuts
        self.open_button.setShortcut("Ctrl+O")
        self.save_button.setShortcut("Ctrl+S")
        self.folder_button.setShortcut("Ctrl+F")
        
        # Signals
        self.open_button.clicked.connect(self.open_file)
        self.save_button.clicked.connect(self.save_file)
        self.folder_button.clicked.connect(self.pick_folder)        

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.open_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.folder_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_help(self):
        QMessageBox.information(
            self,
            "Help",
            "Yahan se aap file open, save ya folder pick kar sakte ho.\n"
            "Use buttons or shortcuts like Ctrl+O, Ctrl+S, Ctrl+F.\n"
            "Happy Life"
        )

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_edit.setText(content)
                self.label.setText(f"Opened: {file_path}")

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            content = self.text_edit.toPlainText()
            with open(file_path, "w") as file:
                file.write(content)
                self.label.setText(f"Saved to: {file_path}")

    def pick_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Choose Folder")
        if folder_path:
            self.label.setText(f"Folder selected: {folder_path}")
            print("You picked", folder_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
