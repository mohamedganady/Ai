import cv2
import numpy as np
import pickle
import os


class PolylineManager:
    def __init__(self):
        self.polylines = []
        self.polyline_names = []
        self.points = []
        self.pickle_file = "polylines.pkl"
        self.load_polylines()

    def load_polylines(self):
        """Load polylines from a pickle file if it exists."""
        if os.path.exists(self.pickle_file):
            with open(self.pickle_file, 'rb') as f:
                self.polylines, self.polyline_names = pickle.load(f)

    def save_polylines(self):
        """Save polylines to a pickle file."""
        with open(self.pickle_file, 'wb') as f:
            pickle.dump((self.polylines, self.polyline_names), f)

    def clear_polylines(self):
        """Clear all polylines, names, and delete the pickle file."""
        self.polylines.clear()
        self.polyline_names.clear()
        if os.path.exists(self.pickle_file):
            os.remove(self.pickle_file)  # Remove the pickle file

    def add_point(self, point):
        """Add a point to the current list of points."""
        if len(self.points) < 4:
            self.points.append(point)

    def draw_polylines(self, frame):
        """Draw the polylines on the given frame."""
        for polyline in self.polylines:
            if len(polyline) >= 4:
                cv2.polylines(frame, [np.array(polyline)], isClosed=True, color=(255, 0, 0), thickness=2)
        for point in self.points:
            cv2.circle(frame, point, 5, (0, 0, 255), -1)
        return frame

    def get_polyline_names(self):
        """Return the names of the defined polylines."""
        return self.polyline_names

    def point_polygon_test(self, point, polyline_name):
        """Check if a point is inside a specific polyline by name."""
        if polyline_name in self.polyline_names:
            index = self.polyline_names.index(polyline_name)
            polyline = self.polylines[index]
            polyline_array = np.array(polyline, dtype=np.int32)
            return cv2.pointPolygonTest(polyline_array, point, False) >= 0  # Returns True if point is inside
        return False  # Return False if polyline name not found

    def handle_key_events(self):
        """Handle key events for saving, clearing, or exiting."""
        key = cv2.waitKey(1) & 0xFF
        if key == ord("e"):
            return False
        elif key == ord("s"):
            self.save_polylines()
        elif key == ord("d"):
            self.clear_polylines()  # Clear polylines and remove the pickle file
        elif len(self.points) == 4:
            polyline_name = input("Enter a name for the polyline: ")
            self.polyline_names.append(polyline_name)
            self.polylines.append(self.points.copy())
            self.points.clear()
        return True
