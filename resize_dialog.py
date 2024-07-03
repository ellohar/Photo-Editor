"""
This module defines a dialog for resizing an image.
"""
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QLabel, QVBoxLayout


class ResizeDialog(QDialog):
    """
    A dialog for resizing an image.

    Attributes:
    current_width (int): The current width of the image.
    current_height (int): The current height of the image.
    aspect_ratio (float): The aspect ratio of the image (width / height).
    """
    def __init__(self, current_width, current_height, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Resize Image")
        self.setMinimumWidth(300)

        self.current_width = current_width
        self.current_height = current_height
        self.aspect_ratio = self.current_width / self.current_height

        self.width_edit = QLineEdit(str(self.current_width))
        self.height_edit = QLineEdit(str(self.current_height))

        min_value = 100
        max_width = parent.image_label.width()
        max_height = parent.image_label.height()
        width_range = f"({min_value} - {max_width})"
        height_range = f"({min_value} - {max_height})"
        self.width_validator = QIntValidator(min_value, max_width, self)
        self.height_validator = QIntValidator(min_value, max_height, self)

        self.width_edit.setValidator(self.width_validator)
        self.height_edit.setValidator(self.height_validator)

        self.width_edit.textChanged.connect(self.on_width_changed)
        self.height_edit.textChanged.connect(self.on_height_changed)

        self.block_signals = False

        # Layout setup
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Enter new dimensions:"))
        form_layout.addWidget(QLabel(f"Width {width_range}:"))
        form_layout.addWidget(self.width_edit)
        form_layout.addWidget(QLabel(f"Height {height_range}:"))
        form_layout.addWidget(self.height_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        self.ok_button = button_box.button(QDialogButtonBox.Ok)
        self.ok_button.setEnabled(False)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)

    def on_width_changed(self):
        """
        Handle changes to the width input field.
        Adjusts the height to maintain the aspect ratio and validates the input
        """
        if self.block_signals:
            return

        self.block_signals = True
        try:
            width = int(self.width_edit.text())
            height = int(width / self.aspect_ratio)
            self.height_edit.setText(str(height))
        except ValueError:
            pass
        self.block_signals = False
        self.validate_input()

    def on_height_changed(self):
        """
        Handle changes to the height input field.
        Adjusts the width to maintain the aspect ratio and validates the input
        """
        if self.block_signals:
            return

        self.block_signals = True
        try:
            height = int(self.height_edit.text())
            width = int(height * self.aspect_ratio)
            self.width_edit.setText(str(width))
        except ValueError:
            pass
        self.block_signals = False
        self.validate_input()

    def validate_input(self):
        """
        Validate the width and height input fields.
        Enables the OK button if both inputs are valid
        """
        is_width_valid = self.width_validator.validate(self.width_edit.text(), 0)[0] == QIntValidator.Acceptable
        is_height_valid = self.height_validator.validate(self.height_edit.text(), 0)[0] == QIntValidator.Acceptable

        self.ok_button.setEnabled(is_width_valid and is_height_valid)

    def get_new_dimensions(self):
        """
        Get the new dimensions entered by the user.

        Returns:
            tuple: The new width and height as integers.
        """
        new_width = int(self.width_edit.text())
        new_height = int(self.height_edit.text())
        return new_width, new_height

    def update_validators(self, max_width, max_height):
        """Update the range of the validators for the width and height input fields"""
        self.width_validator.setRange(100, max_width)
        self.height_validator.setRange(100, max_height)
