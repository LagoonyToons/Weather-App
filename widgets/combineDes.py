import sys
from datetime import date
import requests
from PyQt6.QtCore import Qt
from typing import Union
from typing_extensions import Literal
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QWidget, QApplication, QLabel
from backend.weather import WeatherData
import datetime

# create widget to display the description for the current weather
class weatherDescriptionWidget(QWidget):
    def __init__(self, weather_data: WeatherData, temp_unit: Union[Literal['F'],Literal['C'], Literal['K']]):
        super().__init__()

        # create instance of WeatherData class
        self.wd = weather_data if weather_data != None else WeatherData()
        self.description = self.wd.get_current_weather()["description"]
        
        # description
        self.setWindowTitle("Weather Description")
        self.label = QLabel(self)
        self.label.setText(self.description)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(10, 22, 300, 300)

        # temperature
        self.label2 = QLabel(self)
        deg = "" if temp_unit == 'K' else u"\N{DEGREE SIGN}"
        self.label2.setText(f"{self.wd.get_current_temp()}°")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label2.move(25, 25)

        # weather icon
        self.icon_id = self.wd.get_current_weather()["icon"]
        # create dictionary mapping each weather description to an icon
        image_url = "http://openweathermap.org/img/wn/%s@2x.png" % (self.icon_id)
        image = QImage()
        image.loadFromData(requests.get(image_url).content)

        # weather icon placement
        self.label3 = QLabel(self)
        self.label3.setPixmap(QPixmap(image))
        self.label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label3.setGeometry(5, 65, 300, 300)

        # Get data from WeatherData class
        self.high = self.wd.get_daily_temp_max(datetime.datetime.today().weekday())
        self.low = self.wd.get_daily_temp_min(datetime.datetime.today().weekday())
        day_high = int(self.high)
        day_low = int(self.low)

        # Display text with highs/lows
        self.label4 = QLabel(self)
        self.label4.setText(f"High/Low: {day_high}/{day_low} °F")
        self.label4.move(73, 120)
        
        #stylesheets
        self.label4.setStyleSheet(
            "font-weight: normal;"
            "font-size: 12px;"
            "font-family: Verdana;"
            "padding: 25px;"
        )
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet(
            "font-weight: normal;"
            "font-size: 18px;"
            "font-family: Verdana;"
            "padding: 25px;"
        )
        self.label2.setStyleSheet(
            "font-weight: normal;"
            "font-size: 70px;"
            "font-family: Verdana;"
            "padding: 25px;"
        )

# Run file individually to test widget in isolation
if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = weatherDescriptionWidget(WeatherData(), 'F')
    widget.resize(400, 300)
    widget.show()

    sys.exit(app.exec())