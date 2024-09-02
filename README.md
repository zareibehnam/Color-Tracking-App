# Color Tracking App

This is a simple GUI application built using Python, OpenCV, and Tkinter that allows you to track specific colors in real-time through your webcam. The application identifies and highlights colors such as red, blue, yellow, green, white, and black, and displays a bounding box around the detected colors in the video stream.

## Features

- Real-time color tracking using the webcam.
- Supports tracking of multiple colors: Red, Light Red, Blue, Yellow, Green, White, and Black.
- Simple and intuitive GUI with buttons to start, stop, and exit the application.
- Logging system for tracking the application's activities and errors.
- Unit tests for the main functionalities.

## Requirements

- Python 3.x
- OpenCV
- NumPy
- Tkinter
- pytest (for testing)
- pytest-mock (for testing)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/color-tracking-app.git
    cd color-tracking-app
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    python color_tracking_app.py
    ```

4. Run the tests:

    ```bash
    pytest
    ```

## How to Use

1. Launch the application by running `python color_tracking_app.py`.
2. Click on the "Start" button to begin color tracking.
3. The application will start tracking colors in real-time using your webcam.
4. To stop the tracking, click the "Stop" button.
5. You can exit the application by clicking the "Exit" button.

## Logging

- The application logs its operations to `color_tracker.log`. This includes information about when tracking starts, stops, and any errors encountered.
- Logs are also printed to the console for real-time monitoring.

## Customization

You can customize the colors being tracked by modifying the `color_ranges` dictionary in the `track_colors` method. Each color range is defined by lower and upper bounds in the HSV color space.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
