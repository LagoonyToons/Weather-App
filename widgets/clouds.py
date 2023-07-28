import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QApplication, QLabel
from backend.weather import WeatherData

# create widget to display cloud coverage
class CloudCoverageWidget(QWidget):
    def __init__(self, weather_data: WeatherData = None):
        super().__init__()

        # create instance of WeatherData class
        self.wd = weather_data if weather_data != None else WeatherData()
        self.current_clouds = self.wd.get_current_clouds()

        # styling the widget
        self.setWindowTitle("Clouds")
        self.label = QLabel(self)
        font = self.font()
        font.setPointSize(30)
        self.label.setFont(font)
        self.label.setText(f"Cloud \nCoverage: \n  {int(self.current_clouds)}%")
        self.label.setStyleSheet("border: 2px solid black; padding: 20px;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Adding some style componenets such as background color, fonts, font size, etc.
        self.label.setStyleSheet(
            "border-radius: 35px;"
            "padding: 20px;"
            "padding-left: 30px;"
            "padding-right: 100px;"
            "background-color: #58a5f0;"
            "font-weight: normal;"
            "font-size: 22px;"
            "font-family: Verdana;"
            "margin: 10px 10px 10px 10px;"
        )

        # adding cloud icon
        self.pixmap = QPixmap('icons/clouds.png')
        self.pixmap = self.pixmap.scaledToWidth(75)
        self.clouds = QLabel(self)
        self.clouds.setPixmap(self.pixmap)
        self.clouds.move(165,33)


# Run file individually to test widget in isolation
if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = CloudCoverageWidget()
    widget.resize(400, 400)
    widget.show()

    sys.exit(app.exec())
