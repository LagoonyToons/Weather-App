import sys
from datetime import date
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QApplication, QLabel
from backend.weather import WeatherData

# create widget to display the description for the current weather
class weatherDescriptionWidget(QWidget):
    def __init__(self, weather_data: WeatherData = None):
        super().__init__()

        # create instance of WeatherData class
        self.wd = weather_data if weather_data != None else WeatherData()
        self.description = self.wd.get_current_weather()["description"]

        # styling the widget
        self.setWindowTitle("Weather Description")
        self.label = QLabel(self)
        # make the description have a capital letter for each word
        self.label.setText(f"Today's Weather: \n{self.description.title()}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("border: 2px solid black; padding: 20px;")

# Run file individually to test widget in isolation
if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = weatherDescriptionWidget()
    widget.resize(400, 300)
    widget.show()

    sys.exit(app.exec())