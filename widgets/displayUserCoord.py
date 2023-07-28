import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QApplication, QLabel
from backend.location import Location

# create widget to display user coordinates
class UserCoor(QWidget):
    def __init__(self, location: Location = None):
        super().__init__()

        # create instance of WeatherData class
        self.location = location if location != None else Location()

        # gets user coordinates
        self.location.get_user_coordinates()
        self.coordinates = self.location.coords

        self.setWindowTitle("User Coordinates")
        self.label = QLabel(self)
        self.label.setText(f"User is at {self.coordinates}.")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

# Application Execution
if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = UserCoor()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())