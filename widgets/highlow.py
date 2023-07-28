import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt
from backend.weather import WeatherData
import datetime

class HighLowWidget(QWidget):
    '''
        Widget displays the high and low temperatures
        in Celsius for the given day
    '''
    def __init__(self, date = None, weather_data: WeatherData = None):
        super().__init__()

        self.wd = weather_data if weather_data != None else WeatherData()
        self.wd.get_weather()

        # Get data from WeatherData class
        self.high = self.wd.get_daily_temp_max(datetime.datetime.today().weekday())
        self.low = self.wd.get_daily_temp_min(datetime.datetime.today().weekday())
        day_high = int(self.high)
        day_low = int(self.low)

        # Display text with highs/lows
        self.label = QLabel(self)
        self.label.setText(f"High/Low: {day_high}/{day_low} °F")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label.setStyleSheet("border: 2px solid black; padding: 20px;")

# Test code to view widget
if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = HighLowWidget()
    widget.resize(200, 200)
    widget.show()

    sys.exit(app.exec()) 