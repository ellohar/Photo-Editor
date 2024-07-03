"""
This module defines a dialog for drawing a blue rectangle on an image
"""
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QLabel, QVBoxLayout


class RectangleDialog(QDialog):
    """
    A dialog for specifying the coordinates and dimensions of a blue rectangle.

    Attributes:
        max_width (int): The maximum width of the rectangle.
        max_height (int): The maximum height of the rectangle.
        layout (QVBoxLayout): The layout of the dialog.
        line_edit1 (QLineEdit): Input field for the x-coordinate.
        line_edit2 (QLineEdit): Input field for the y-coordinate.
        line_edit3 (QLineEdit): Input field for the width.
        line_edit4 (QLineEdit): Input field for the height.
        button_box (QDialogButtonBox): The box containing OK and Cancel buttons.
    """
    def __init__(self, max_width, max_height, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Draw Blue Rectangle")

        self.max_width = max_width
        self.max_height = max_height

        self.layout = QVBoxLayout(self)

        self.label1 = QLabel("Enter X-coordinate of top-left corner (0 to {}):".format(self.max_width), self)
        self.line_edit1 = QLineEdit(self)
        self.line_edit1.setText("0")
        self.line_edit1.setValidator(QIntValidator(0, self.max_width, self))
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.line_edit1)

        self.label2 = QLabel("Enter Y-coordinate of top-left corner (0 to {}):".format(self.max_height), self)
        self.line_edit2 = QLineEdit(self)
        self.line_edit2.setText("0")
        self.line_edit2.setValidator(QIntValidator(0, self.max_height, self))
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.line_edit2)

        self.label3 = QLabel("Enter width of the rectangle:", self)
        self.line_edit3 = QLineEdit(self)
        self.line_edit3.setText("100")
        self.line_edit3.setValidator(QIntValidator(1, self.max_width, self))
        self.layout.addWidget(self.label3)
        self.layout.addWidget(self.line_edit3)

        self.label4 = QLabel("Enter height of the rectangle:", self)
        self.line_edit4 = QLineEdit(self)
        self.line_edit4.setText("100")
        self.line_edit4.setValidator(QIntValidator(1, self.max_height, self))
        self.layout.addWidget(self.label4)
        self.layout.addWidget(self.line_edit4)

        self.buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(self.buttons)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
        self.layout.addWidget(self.button_box)

        self.line_edit1.textChanged.connect(self.validate_input)
        self.line_edit2.textChanged.connect(self.validate_input)
        self.line_edit3.textChanged.connect(self.validate_input)
        self.line_edit4.textChanged.connect(self.validate_input)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def validate_input(self):
        """
        Validate the input in the line edit fields.
        Enables the OK button if the input values are valid and within the specified range.
        """
        x = self.line_edit1.text()
        y = self.line_edit2.text()
        width = self.line_edit3.text()
        height = self.line_edit4.text()

        if x.isdigit() and y.isdigit() and width.isdigit() and height.isdigit():
            x = int(x)
            y = int(y)
            width = int(width)
            height = int(height)
            if 0 <= x <= self.max_width - width and 0 <= y <= self.max_height - height:
                self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
                return
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)

    def get_rectangle_params(self):
        """
        Get the rectangle parameters entered by the user.

        Returns:
            tuple: The x, y coordinates and width, height of the rectangle.
        """
        x = int(self.line_edit1.text())
        y = int(self.line_edit2.text())
        width = int(self.line_edit3.text())
        height = int(self.line_edit4.text())
        return x, y, width, height
