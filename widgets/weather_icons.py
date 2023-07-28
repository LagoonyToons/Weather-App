import sys
import requests
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QWidget, QApplication, QLabel
from PyQt6.QtGui import *
from backend.weather import WeatherData

# create widget to display an icon of the current weather
class iconWidget(QWidget):
    def __init__(self, weather_data: WeatherData = None):
        super().__init__()

        # create instance of WeatherData class
        self.wd = weather_data if weather_data != None else WeatherData()
        self.icon_id = self.wd.get_current_weather()["icon"]
        
        
        # create dictionary mapping each weather description to an icon
        image_url = "http://openweathermap.org/img/wn/%s@2x.png" % (self.icon_id)
        image = QImage()
        image.loadFromData(requests.get(image_url).content)

        # styling the widget
        self.setWindowTitle("Current Weather Icon")

        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
            
        self.label1.setText(f"Today's Weather Icon: \n")
        self.label2.setPixmap(QPixmap(image))
            
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label1.setStyleSheet("border: 2px solid black; padding: 20px;")
        self.label2.move(20, 80)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.label2.setStyleSheet('background-color:#cdf7ed')

# Run file individually to test widget in isolation
if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = iconWidget()
    widget.resize(400, 300)
    widget.show()

    sys.exit(app.exec())
