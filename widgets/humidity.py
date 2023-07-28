from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
import sys
from backend.weather import WeatherData

class HumidityWidget(QWidget):
    def __init__(self, weather_data: WeatherData = None):
        super().__init__()

        self.wd = weather_data if weather_data != None else WeatherData()
        self.label = QLabel(self)
        self.label.setText(" Humidity\n" + "    " + str(self.wd.get_current_humidity()) + "%")
        self.label.setStyleSheet("border: 2px solid black; padding: 4px;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Adding some style componenets such as background color, fonts, font size, etc.
        self.label.setStyleSheet(
            "border-radius: 35px;"
            "padding: 25px;"
            "padding-left: 25px;"
            "padding-right: 30px;"
            "background-color: #58a5f0;"
            "font-weight: normal;"
            "font-size: 22px;"
            "font-family: Verdana;"
            "margin: 10px 10px 10px 10px;"
            )

        # adding humid icon
        self.pixmap = QPixmap('icons/humidity.png')
        self.pixmap = self.pixmap.scaledToWidth(27)
        self.humid = QLabel(self)
        self.humid.setPixmap(self.pixmap)
        self.humid.move(43,63)

# Run file individually to test widget in isolation
if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = HumidityWidget()
    widget.resize(400, 400)
    widget.show()

    sys.exit(app.exec())
