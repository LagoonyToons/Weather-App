from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from PyQt6.QtCore import Qt
from backend.weather import WeatherData
import sys
import datetime

class CityDisplay(QWidget):
    def __init__(self, weather_data: WeatherData = None) -> None:
        super().__init__()
            
        self.wd = weather_data if weather_data != None else WeatherData()
        # self.wd.get_weather()
        self.wd.get_city()
        self.name = self.wd.city.split(",")[:3]
        

        self.label = QLabel(self)
        self.label.setText("".join(self.name))
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label.setStyleSheet("border: 2px solid black; padding: 4px;")
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    widget = CityDisplay()
    widget.show()

    sys.exit(app.exec())
