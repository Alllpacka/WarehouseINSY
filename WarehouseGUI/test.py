import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.uic import loadUiType

# Load the .ui file
Ui_MainWindow, QMainWindow = loadUiType('./ui/test.ui')

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)  # This sets up the UI defined in your .ui file

        self.setWindowTitle("My App")

        # You can access widgets defined in your .ui file directly
        self.setFixedSize(QSize(400, 300))

    def on_button_click(self):
        print("Button clicked!")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())