"""
This script defines the main window for the Photo Editor application.
"""
import os
import cv2
import numpy as np
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, \
    QSizePolicy, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from resize_dialog import ResizeDialog
from brightness_dialog import BrightnessDialog
from rectangle_dialog import RectangleDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.take_photo_button = None
        self.current_pixmap = None
        self.original_pixmap = None
        self.cv_image = None
        self.original_image = None
        self.setWindowTitle("Photo Editor")

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_widget.setStyleSheet("background-color: #bdd3ce;")

        # Image display label
        self.image_label = QLabel(self)
        self.image_label.setStyleSheet("background-color: #fcf3e3;")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Buttons
        self.red_button = QPushButton("Display Red Channel")
        self.green_button = QPushButton("Display Green Channel")
        self.blue_button = QPushButton("Display Blue Channel")
        self.resize_button = QPushButton("Resize Image")
        self.brightness_button = QPushButton("Decrease Brightness")
        self.rectangle_button = QPushButton("Draw Blue Rectangle")

        buttons = [self.red_button, self.green_button, self.blue_button, self.resize_button, self.brightness_button,
                   self.rectangle_button]
        for button in buttons:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setStyleSheet(
                "font-size: 15px; font-family: Bahnschrift; font-weight: bold;"
                " background-color: #013d5a; color: #fcf3e3;")

        # Button layout
        self.button_layout = QVBoxLayout()
        for button in buttons:
            self.button_layout.addWidget(button)

        # Load and camera buttons
        self.load_button = QPushButton("Load Image")
        self.load_button.setStyleSheet(
            "font-size: 15px; font-family: Bahnschrift; font-weight: bold;"
            " background-color: #708c69; color: #fcf3e3;")
        self.camera_button = QPushButton("Connect to Camera")
        self.camera_button.setStyleSheet(
            "font-size: 15px; font-family: Bahnschrift; font-weight: bold;"
            " background-color: #708c69; color: #fcf3e3;")
        self.camera_button.setCheckable(True)

        self.load_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.camera_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Connect buttons to functions
        self.load_button.clicked.connect(self.load_image)
        self.camera_button.clicked.connect(self.toggle_camera)

        self.resize_button.clicked.connect(self.resize_image)
        self.red_button.clicked.connect(lambda: self.display_channel('R'))
        self.green_button.clicked.connect(lambda: self.display_channel('G'))
        self.blue_button.clicked.connect(lambda: self.display_channel('B'))
        self.brightness_button.clicked.connect(self.adjust_brightness)
        self.rectangle_button.clicked.connect(self.draw_rectangle)

        # Bottom button layout
        self.bottom_button_layout = QHBoxLayout()
        self.bottom_button_layout.addWidget(self.load_button)
        self.bottom_button_layout.addWidget(self.camera_button)

        self.bottom_container = QWidget()
        self.bottom_container.setLayout(self.bottom_button_layout)
        self.bottom_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Main layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.image_label, 3)
        self.main_layout.addLayout(self.button_layout, 1)

        self.final_layout = QVBoxLayout()
        self.final_layout.addLayout(self.main_layout, 7)
        self.final_layout.addWidget(self.bottom_container, 1)

        main_widget.setLayout(self.final_layout)

        self.resize(800, 600)

        # Timer for camera updates
        self.capture = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.cv_image = None

    def load_image(self):
        """Load an image from the filesystem and display it"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg)")
        if file_path:
            try:
                image = self.load_image_with_cv2(file_path)
                if image is not None:
                    self.cv_image = image
                    self.original_image = image.copy()
                    pixmap = self.convert_cvimage_to_qpixmap(image)
                    if pixmap is not None:
                        self.display_image(pixmap)
                    else:
                        QMessageBox.critical(self, "Error", "Failed to load image.")
                else:
                    QMessageBox.critical(self, "Error", "Failed to load image.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")

    @staticmethod
    def load_image_with_cv2(file_path):
        """Load an image using OpenCV"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found.")

        with open(file_path, 'rb') as f:
            image_data = np.frombuffer(f.read(), dtype=np.uint8)
            image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
            return image

    def convert_cvimage_to_qpixmap(self, image):
        """Convert a CV image to QPixmap"""
        if image is None:
            return None

        # Resize the image to fit the label
        label_width = self.image_label.width()
        label_height = self.image_label.height()

        h, w, ch = image.shape
        bytes_per_line = ch * w
        q_image = QImage(image.data, w, h, bytes_per_line, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(q_image).scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pixmap

    def display_image(self, pixmap):
        """Display the given QPixmap in the image label"""
        self.image_label.setPixmap(pixmap)
        self.image_label.adjustSize()
        self.current_pixmap = pixmap

    def toggle_camera(self):
        """Toggle the camera on and off"""
        if self.camera_button.isChecked():
            self.camera_button.setText("Take Photo")
            try:
                self.capture = cv2.VideoCapture(0)
                if not self.capture.isOpened():
                    raise Exception("Failed to open camera.")
                self.timer.start(10)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open camera: {str(e)}")
                self.camera_button.setChecked(False)
                self.camera_button.setText("Connect to Camera")
        else:
            self.camera_button.setText("Connect to Camera")
            if self.capture and self.capture.isOpened():
                self.timer.stop()
                self.capture.release()

    def update_frame(self):
        """Update the frame from the camera"""
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            scaled_image = image.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(QPixmap.fromImage(scaled_image))

            self.current_pixmap = QPixmap.fromImage(image)
            self.cv_image = frame
            self.take_photo()

    def take_photo(self):
        """Capture a photo from the camera and display it"""
        if hasattr(self, 'current_pixmap'):
            self.image_label.setPixmap(
                self.current_pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def closeEvent(self, event):
        """Handle the close event to release the camera"""
        if self.capture and self.capture.isOpened():
            self.timer.stop()
            self.capture.release()
        event.accept()

    def resize_image(self):
        """Resize the current image"""
        if not self.image_label.pixmap():
            QMessageBox.warning(self, "Warning", "Please load an image first.")
            return

        current_width = self.current_pixmap.width()
        current_height = self.current_pixmap.height()

        dialog = ResizeDialog(current_width, current_height, self)

        dialog.update_validators(self.image_label.width(), self.image_label.height())

        if dialog.exec_():
            new_width, new_height = dialog.get_new_dimensions()
            new_pixmap = self.current_pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(new_pixmap)

    def display_channel(self, channel):
        """Display the specified color channel of the image"""
        if self.cv_image is None:
            QMessageBox.warning(self, "Warning", "Please load an image first.")
            return

        red_channel, green_channel, blue_channel = cv2.split(self.cv_image)

        if channel == 'R':
            channel_image = cv2.merge((red_channel,
                                       np.zeros_like(red_channel),
                                       np.zeros_like(red_channel)))
        elif channel == 'G':
            channel_image = cv2.merge((np.zeros_like(green_channel),
                                       green_channel,
                                       np.zeros_like(green_channel)))
        elif channel == 'B':
            channel_image = cv2.merge((np.zeros_like(blue_channel),
                                       np.zeros_like(blue_channel),
                                       blue_channel))
        else:
            QMessageBox.warning(self, "Warning", "Invalid channel specified.")
            return

        h, w, ch = channel_image.shape
        bytes_per_line = ch * w
        q_image = QImage(channel_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        scaled_q_image = q_image.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(QPixmap.fromImage(scaled_q_image))

    def adjust_brightness(self):
        """Adjust the brightness of the current image"""
        if self.cv_image is None:
            QMessageBox.warning(self, "Warning", "Please load an image first.")
            return

        dialog = BrightnessDialog(self)
        if dialog.exec_():
            percentage = dialog.get_percentage()
            self.apply_brightness(percentage)

    def apply_brightness(self, percentage):
        """Apply the brightness adjustment to the image using OpenCV"""
        if self.original_image is None:
            QMessageBox.warning(self, "Warning", "Please load an image first.")
            return

        # Calculate the brightness factor
        factor = percentage / 100.0

        # Apply brightness adjustment based on the original image
        brightened_image = cv2.convertScaleAbs(self.original_image, alpha=factor, beta=0)

        # Convert the updated image back to QPixmap
        h, w, ch = brightened_image.shape
        bytes_per_line = ch * w
        q_image = QImage(brightened_image.data, w, h, bytes_per_line, QImage.Format_BGR888)

        scaled_image = q_image.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(QPixmap.fromImage(scaled_image))
        self.current_pixmap = QPixmap.fromImage(scaled_image)
        self.cv_image = brightened_image

    def draw_rectangle(self):
        """Draw a filled blue rectangle on the image"""
        if self.cv_image is None:
            QMessageBox.warning(self, "Warning", "Please load an image first.")
            return

        original_width = self.cv_image.shape[1]
        original_height = self.cv_image.shape[0]
        display_width = self.image_label.width()
        display_height = self.image_label.height()

        dialog = RectangleDialog(display_width, display_height, self)

        if dialog.exec_():
            x, y, width, height = dialog.get_rectangle_params()

            # Calculate scaling factors
            scale_x = original_width / display_width
            scale_y = original_height / display_height

            # Scale the rectangle coordinates and size to match the original image size
            x = int(x * scale_x)
            y = int(y * scale_y)
            width = int(width * scale_x)
            height = int(height * scale_y)

            # Draw filled rectangle on the cv_image using cv2
            rect_image = self.cv_image.copy()
            cv2.rectangle(rect_image, (x, y), (x + width, y + height), (255, 0, 0), -1)

            # Convert the updated image back to QPixmap
            h, w, ch = rect_image.shape
            bytes_per_line = ch * w
            q_image = QImage(rect_image.data, w, h, bytes_per_line, QImage.Format_BGR888)

            scaled_image = q_image.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(QPixmap.fromImage(scaled_image))
            self.current_pixmap = QPixmap.fromImage(scaled_image)
            self.cv_image = rect_image
