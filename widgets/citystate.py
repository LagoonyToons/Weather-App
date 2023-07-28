import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt
from backend.weather import WeatherData

class HighLowWidget(QWidget):
    '''
        Widget displays the high and low temperatures
        in Celsius for the given day
    '''
    def __init__(self, date = None, weather_data: WeatherData = None):
        super().__init__()

        self.wd = weather_data if weather_data != None else WeatherData()
        self.wd.get_weather()
        self.wd.get_city()

        # Display text with name of city and state
        self.label = QLabel(self)
        self.label.setText(f"Location: {self.wd.city}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("border: 2px solid black; padding: 20px;")

# Test code to view widget
if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = HighLowWidget()
    widget.resize(200, 200)
    widget.show()

    sys.exit(app.exec()) 