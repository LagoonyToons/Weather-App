from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from backend.weather import WeatherData
import sys
import datetime

class HourlyWeatherWidget(QWidget):
    def __init__(self, weather_data: WeatherData = None) -> None:
        super().__init__()
            
        self.wd = weather_data if weather_data != None else WeatherData()
        self.wd.get_weather()
        time = datetime.datetime.now()
  
        self.hourly_temp = [int(self.wd.get_hourly_temp(hour)) for hour in range(12)]
        
        temp_string = ""
        hour_string = ""
        for ind, temp in enumerate(self.hourly_temp):
            added = datetime.timedelta(hours=ind+1)
            current = time + added
            temp_string += f'{temp} F '
            temp_string += '  '
            
            #adjust spacing
            if ind == 0:
                temp_string += ' '
            if ind == 2:
                temp_string += ' '
            if ind == 6:
                temp_string += ' '
            if ind == 9:
                temp_string += ' '
            if ind == 10:
                temp_string += ' '
            
            try:
                hour_string += current.strftime('%I%p') + "  "
            except:
                hour_string += current.strftime('%I%p') + "   "

        self.label = QLabel(self)
        self.label.setText("    " + hour_string + '\n' + "       " + temp_string)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Adding some style componenets such as background color, fonts, font size, etc.
        self.label.setStyleSheet(
            "border-radius: 35px;"
            "padding: 25px;"
            "padding-left: 45px;"
            "background-color: #8aacc8;"
            "font-weight: normal;"
            "font-size: 22px;"
            "font-family: Verdana;"
            "margin: 10px 10px 10px 10px;"
        )

        # adding sunset icon
        self.pixmap = QPixmap('icons/clock.png')
        self.pixmap = self.pixmap.scaledToWidth(50)
        self.clock = QLabel(self)
        self.clock.setPixmap(self.pixmap)
        self.clock.move(35,35)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    widget = HourlyWeatherWidget()
    widget.resize(1000, 200)
    widget.show()

    sys.exit(app.exec())
