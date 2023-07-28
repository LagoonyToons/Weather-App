import sys
from datetime import date
import calendar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QWidget

from backend.weather import WeatherData
from helpers.temperature import KelvinToFahrenheit

class DaysWidget(QWidget):
  def __init__(self, weather_data: WeatherData = None):
    super().__init__()

    self.wd = weather_data if weather_data != None else WeatherData()
    self.wd.get_weather()
    curr_date = date.today()
    self.tempString = ""
    self.daytempString = ""
    self.weekdayString = ""

    for ind, day in enumerate(self.wd.weather['daily']):
      self.weekdayString = self.weekdayString + calendar.day_name[(curr_date.weekday()+ind)%7] +\
        ': ' + '\n'

    for ind, day in enumerate(self.wd.weather['daily']):
      self.daytempString = self.daytempString + str(int(KelvinToFahrenheit(day['temp']['day']))) + ' °F\n'

    lableNames = QLabel(self.weekdayString, self)
    lableNames.move(15, 10)

    labelTemps = QLabel(self.daytempString, self)
    labelTemps.move(160, 10)

    lableTitle = QLabel("This Week", self)
    lableTitle.move(98, 30)

    self.setWindowTitle("Weather for the Week")
    self.label = QLabel(self)
    self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.setStyleSheet("margin-bottom: 25px;")

    lableNames.setStyleSheet(
            "border-radius: 35px;"
            "border-bottom-right-radius: 0px;"
            "border-top-right-radius: 0px;"
            "padding: 22px;"
            "padding-top: 40px;"
            "background-color: #58a5f0;"
            "font-weight: normal;"
            "font-size: 18px;"
            "font-family: Verdana;"
            "margin: 10px 10px 10px 10px;"
            )
    labelTemps.setStyleSheet(
            "border-radius: 35px;"
            "border-bottom-left-radius: 0px;"
            "border-top-left-radius: 0px;"
            "padding: 22px;"
            "padding-top: 40px;"
            "background-color: #58a5f0;"
            "font-weight: normal;"
            "font-size: 18px;"
            "font-family: Verdana;"
            "margin: 10px 10px 10px 10px;"
            )
    lableTitle.setStyleSheet(
            "font-weight: bold;"
            "font-size: 18px;"
            "font-family: Verdana;"
    )

    # adding icon
    self.pixmap = QPixmap('icons/cloudy.png')
    self.pixmap = self.pixmap.scaledToWidth(80)
    self.light = QLabel(self)
    self.light.setPixmap(self.pixmap)
    self.light.move(195,230)

# Run file individually to test widget in isolation
if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = DaysWidget()
    widget.resize(400, 500)
    widget.show()

    sys.exit(app.exec())
