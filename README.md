# Photo Editor

Photo Editor is a simple photo editing application built with PyQt5 and OpenCV.
It allows you to resize images, adjust brightness, display individual color channel, and draw rectangles on images.

## Features

* Load an image from a file;
* Connect to camera and capture an image;
* Display individual color channels (Red, Green, Blue);
* Resize an image;
* Adjust image brightness;
* Draw blue rectangles on image.

## Requirements

- Git
- Python 3.8
- PyQt5
- OpenCV

## Installation

1. Ensure you have Python 3.8. You can download it from the [official Python website](https://www.python.org/downloads/release/python-3810/).

2. Clone the project repository:
    ```sh
    git clone https://github.com/ellohar/Photo-Editor.git
    cd Photo-Editor
    ```
3. Install py:
    ```sh
    pip install py
    ```
4. Create a virtual environment:
    ```sh
    py -3.8 -m newenv venv
    ```
5. Activate the virtual environment:
   On Windows:
     ```sh
     newenv\Scripts\activate
     ```
6. Upgrade pip:
   ```
   python -m pip install --upgrade pip
   ```
7. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. Navigate to the project directory if you are not already there:
    ```sh
    cd Photo-Editor
    ```
2. (If using a virtual environment, ensure it is activated.)
3. Run the application:
    ```sh
    python main.py
    ```

## Usage

- **Load an Image**: Click the "Load Image" button and select an image in PNG or JPG format.
- **Connect to Camera**: Click the "Connect to Camera" button to open the camera. Click again to take a photo.
- **Resize Image**: Click the "Resize Image" button, enter the new dimensions, and click "OK".
- **Adjust Brightness**: Click the "Decrease Brightness" button, select the brightness percentage, and click "OK".
- **Display Color Channels**: Click the corresponding button to display the red, green, or blue channel.
- **Draw Rectangles**: Click the "Draw Blue Rectangle" button, enter the coordinates and dimensions of the rectangle, and click "OK".

## Project Structure

- `main.py`: The entry point of the application.
- `main_window.py`: Contains the `MainWindow` class, which manages the main application window and its functionalities.
- `resize_dialog.py`: Module containing the `ResizeDialog` class for resizing images.
- `brightness_dialog.py`: Module containing the `BrightnessDialog` class for adjusting image brightness.
- `rectangle_dialog.py`: Module containing the `RectangleDialog` class for drawing rectangles.
