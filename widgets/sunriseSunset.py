import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QGridLayout
from backend.weather import WeatherData

# create widget to display sunset and sunrise times
class SunriseSunsetWidget(QWidget):

    def __init__(self, weather_data: WeatherData = None):
        super().__init__()

        # create instance of WeatherData class
        self.wd = weather_data if weather_data != None else WeatherData()
        self.sunset = self.wd.get_current_sunset() 
        self.sunrise = self.wd.get_current_sunrise()

        # styling the widget
        self.setWindowTitle("Sunset Sunrise Data")

        self.label1 = QLabel(self)

        # adding sun icon
        self.pixmap = QPixmap('icons/sunrise.png')
        self.pixmap = self.pixmap.scaledToWidth(40)
        self.sun = QLabel(self)
        self.sun.setPixmap(self.pixmap)
        self.sun.move(22,32)

        # adding sunset icon
        self.pixmap = QPixmap('icons/sunset-2.png')
        self.pixmap = self.pixmap.scaledToWidth(40)
        self.sun = QLabel(self)
        self.sun.setPixmap(self.pixmap)
        self.sun.move(22,117)


        self.label1.setText(f"      SUNRISE: \n    {int(self.sunrise[4])}:{self.sunrise[5]} AM\n\n    SUNSET: \n    {int(self.sunset[4])-12}:{self.sunset[5]} PM")
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Adding some style componenets such as background color, fonts, font size, etc.
        self.label1.setStyleSheet(
            "border-radius: 35px;"
            "padding: 25px;"
            "padding-left: 25px;"
            "background-color: #58a5f0;"
            "font-weight: normal;"
            "font-size: 22px;"
            "font-family: Verdana;"
            "margin: 10px 10px 10px 10px;"
            )

# Run file individually to test widget in isolation
if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = SunriseSunsetWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())