"""
This script initializes and runs the Photo Editor application.

The application allows users to load, display, and edit images using various features such as:
- Displaying red, green, and blue color channels separately;
- Resizing the image;
- Adjusting brightness;
- Drawing a blue rectangle on the image.

Usage:
    To run the application, execute this script.

    Example:
        python main.py
"""
import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
