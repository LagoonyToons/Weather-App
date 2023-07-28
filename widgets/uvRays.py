import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QApplication, QLabel
from backend.weather import WeatherData

# create widget to display UV rays
class UVradiationWidget(QWidget):
    def __init__(self, weather_data: WeatherData = None):
        super().__init__()

        # create instance of WeatherData class
        self.wd = weather_data if weather_data != None else WeatherData()
        self.uv = self.wd.get_current_uvi()

        #styling the widget
        self.setWindowTitle("UV Radiation Data")
        self.label = QLabel(self)
        self.label.setText(f"       CURRENT\nUVI \n{float(self.uv)}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label.setStyleSheet(
            "border-radius: 35px;"
             "padding: 25px;"
             "padding-left: 35px;"
             "background-color: #58a5f0;"
             "font-weight: normal;"
             "font-size: 22px;"
             "font-family: Verdana;"
             "margin: 10px 10px 10px 10px;"
        )

        # adding uv icon
        self.pixmap = QPixmap('icons/ray.png')
        self.pixmap = self.pixmap.scaledToWidth(65)
        self.ray = QLabel(self)
        self.ray.setPixmap(self.pixmap)
        self.ray.move(20,35)

        # adding uv icon
        self.pixmap = QPixmap('icons/hot.png')
        self.pixmap = self.pixmap.scaledToWidth(95)
        self.hot = QLabel(self)
        self.hot.setPixmap(self.pixmap)
        self.hot.move(150,70)

# Run file individually to test widget in isolation
if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = UVradiationWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())