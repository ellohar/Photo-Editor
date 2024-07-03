"""
This module defines a dialog for adjusting the brightness of an image
"""
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialog, QLineEdit, QDialogButtonBox


class BrightnessDialog(QDialog):
    """
    A dialog for adjusting the brightness of an image.

    Attributes:
        layout (QVBoxLayout): The layout of the dialog.
        label (QLabel): The label that displays instructions.
        line_edit (QLineEdit): The input field for entering the brightness percentage.
        button_box (QDialogButtonBox): The box containing OK and Cancel buttons.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adjust Brightness")

        self.layout = QVBoxLayout(self)
        self.label = QLabel("Enter the percentage of brightness (0-100):", self)
        self.line_edit = QLineEdit(self)
        self.line_edit.setValidator(QIntValidator(0, 100, self))
        self.line_edit.setText("100")

        self.buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(self.buttons)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)

        self.line_edit.textChanged.connect(self.validate_input)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.button_box)

    def validate_input(self):
        """
        Validate the input in the line edit field.
        Enables the OK button if the input is a valid percentage (0-100).
        """
        text = self.line_edit.text()
        if text.isdigit() and 0 <= int(text) <= 100:
            self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)

    def get_percentage(self):
        return int(self.line_edit.text())
