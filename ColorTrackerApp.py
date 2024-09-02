import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
import threading
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("F:\cook\ColorTrackerApp\color_tracker.log"),
    logging.StreamHandler(sys.stdout)
])

class ColorTrackerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Color Tracking App")
        
        # Creating buttons
        self.start_button = tk.Button(master, text="Start", command=self.start_tracking)
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(master, text="Stop", command=self.stop_tracking, state=tk.DISABLED)
        self.stop_button.pack(pady=10)
        
        self.exit_button = tk.Button(master, text="Exit", command=self.exit_app)
        self.exit_button.pack(pady=10)
        
        self.cap = None
        self.tracking = False

    def start_tracking(self):
        try:
            self.tracking = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            logging.info("Color tracking started.")
            
            # Start the tracking in a new thread to avoid freezing the GUI
            threading.Thread(target=self.track_colors, daemon=True).start()
        except Exception as e:
            logging.error(f"Error starting tracking: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def track_colors(self):
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("Could not open webcam.")

            color_ranges = {
                "Red": ([0, 70, 50], [10, 255, 255], (0, 0, 255)),
                "Light Red": ([170, 70, 50], [180, 255, 255], (0, 0, 255)),
                "Blue": ([94, 80, 2], [126, 255, 255], (255, 0, 0)),
                "Yellow": ([15, 100, 100], [35, 255, 255], (0, 255, 255)),
                "Green": ([25, 52, 72], [102, 255, 255], (0, 255, 0)),
                "White": ([0, 0, 168], [172, 111, 255], (255, 255, 255)),
                "Black": ([0, 0, 0], [180, 255, 30], (0, 0, 0))
            }

            kernel = np.ones((5, 5), "uint8")

            while self.tracking:
                ret, img = self.cap.read()
                if not ret:
                    logging.warning("Failed to capture frame from webcam.")
                    break

                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

                for color_name, (lower, upper, color_bgr) in color_ranges.items():
                    lower = np.array(lower, np.uint8)
                    upper = np.array(upper, np.uint8)
                    mask = cv2.inRange(hsv, lower, upper)
                    mask = cv2.dilate(mask, kernel)

                    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    
                    for contour in contours:
                        area = cv2.contourArea(contour)
                        if area > 300:
                            x, y, w, h = cv2.boundingRect(contour)
                            cv2.rectangle(img, (x, y), (x + w, y + h), color_bgr, 2)
                            cv2.putText(img, f"{color_name} Colour", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_bgr, 2)

                cv2.imshow("Color Tracking", img)
                
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    logging.info("Exiting color tracking by user command.")
                    break

        except Exception as e:
            logging.error(f"Error during color tracking: {e}")
            messagebox.showerror("Error", f"An error occurred during tracking: {e}")
            self.stop_tracking()

        finally:
            self.stop_tracking()

    def stop_tracking(self):
        try:
            if self.cap:
                self.tracking = False
                self.cap.release()
                cv2.destroyAllWindows()
                logging.info("Color tracking stopped.")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
        except Exception as e:
            logging.error(f"Error stopping tracking: {e}")
            messagebox.showerror("Error", f"An error occurred while stopping: {e}")

    def exit_app(self):
        try:
            if self.tracking:
                self.stop_tracking()
            logging.info("Exiting application.")
            self.master.quit()
        except Exception as e:
            logging.error(f"Error exiting application: {e}")
            messagebox.showerror("Error", f"An error occurred while exiting: {e}")

# Creating the main application window
root = tk.Tk()
app = ColorTrackerApp(root)
root.mainloop()
