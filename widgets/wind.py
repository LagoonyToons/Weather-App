import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QWidget

from backend.weather import WeatherData

class WindWidget(QWidget):
  def __init__(self, weather_data: WeatherData = None):
    super().__init__()

    self.wd = weather_data if weather_data != None else WeatherData()
    self.wd.get_weather()

    self.wind_speed = self.wd.weather['daily'][0]['wind_speed']
    self.wind_direction = self.wd.weather['daily'][0]['wind_deg']

    self.label = QLabel(self)
    self.label.setText(f"   Wind Direction: {self.wind_direction}\n   Wind Speed: {self.wind_speed}")
    self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)

    # Adding some style componenets such as background color, fonts, font size, etc.
    self.label.setStyleSheet(
        "border-radius: 35px;"
        "padding: 30px;"
        "padding-left: 15px;"
        "padding-right: 20px;"
        "background-color: #58a5f0;"
        "font-weight: normal;"
        "font-size: 18px;"
        "font-family: Verdana;"
        "margin: 10px 10px 10px 10px;"
        )

    # adding wind icon
    self.pixmap = QPixmap('icons/wind-3.png')
    self.pixmap = self.pixmap.scaledToWidth(35)
    self.wind = QLabel(self)
    self.wind.setPixmap(self.pixmap)
    self.wind.move(210,70)

    # adding another wind icon
    self.pixmap = QPixmap('icons/wind-4.png')
    self.pixmap = self.pixmap.scaledToWidth(42)
    self.wind2 = QLabel(self)
    self.wind2.setPixmap(self.pixmap)
    self.wind2.move(10,15)

# Run file individually to test widget in isolation
if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = WindWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
