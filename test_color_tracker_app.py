import unittest
from unittest.mock import patch, MagicMock
import cv2
import numpy as np
from color_tracking_app import ColorTrackerApp  # Assuming your script is named color_tracking_app.py

class TestColorTrackerApp(unittest.TestCase):
    
    @patch('cv2.VideoCapture')
    def test_start_tracking(self, mock_VideoCapture):
        # Create a MagicMock object for the VideoCapture object
        mock_cap = MagicMock()
        mock_VideoCapture.return_value = mock_cap
        mock_cap.isOpened.return_value = True
        
        # Initialize the ColorTrackerApp without a real Tkinter window
        app = ColorTrackerApp(None)
        
        with patch.object(app, 'track_colors', return_value=None) as mock_track_colors:
            app.start_tracking()
            self.assertTrue(app.tracking)
            mock_track_colors.assert_called_once()
            self.assertEqual(app.start_button.cget('state'), 'disabled')
            self.assertEqual(app.stop_button.cget('state'), 'normal')

    @patch('cv2.VideoCapture')
    def test_stop_tracking(self, mock_VideoCapture):
        # Create a MagicMock object for the VideoCapture object
        mock_cap = MagicMock()
        mock_VideoCapture.return_value = mock_cap
        
        # Initialize the ColorTrackerApp without a real Tkinter window
        app = ColorTrackerApp(None)
        app.cap = mock_cap
        app.tracking = True
        
        app.stop_tracking()
        
        mock_cap.release.assert_called_once()
        self.assertFalse(app.tracking)
        self.assertEqual(app.start_button.cget('state'), 'normal')
        self.assertEqual(app.stop_button.cget('state'), 'disabled')

    @patch('cv2.VideoCapture')
    @patch('cv2.imshow')
    def test_track_colors(self, mock_imshow, mock_VideoCapture):
        # Mock VideoCapture and isOpened
        mock_cap = MagicMock()
        mock_VideoCapture.return_value = mock_cap
        mock_cap.isOpened.return_value = True
        
        # Create a dummy frame (480x640 with 3 channels)
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_cap.read.return_value = (True, dummy_frame)
        
        # Initialize the ColorTrackerApp without a real Tkinter window
        app = ColorTrackerApp(None)
        app.cap = mock_cap
        app.tracking = True
        
        with patch.object(app, 'stop_tracking') as mock_stop_tracking:
            # Run track_colors in a way that it stops after one iteration
            with patch('cv2.waitKey', return_value=ord('q')):
                app.track_colors()
                
            mock_cap.read.assert_called()
            mock_imshow.assert_called_once_with("Color Tracking", dummy_frame)
            mock_stop_tracking.assert_called_once()

    def test_exit_app(self):
        app = ColorTrackerApp(None)
        
        with patch.object(app, 'stop_tracking') as mock_stop_tracking, \
             patch.object(app.master, 'quit') as mock_quit:
            
            app.tracking = True
            app.exit_app()
            
            mock_stop_tracking.assert_called_once()
            mock_quit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
