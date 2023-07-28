from PyQt6.QtWidgets import QWidget, QApplication, QPushButton
from PyQt6.QtCore import Qt
from backend.weather import WeatherData
import sys
import datetime

class LocationButton(QWidget):
    def __init__(self, weather_data: WeatherData = None) -> None:
        super().__init__()
            
        self.wd = weather_data if weather_data != None else WeatherData()
        # self.wd.get_weather()
        
        self.button = QPushButton('Get location automatically', self)
        self.button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        self.wd.get_location_weather()
        ##flag that everything needs to refresh since wd is changing
        
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    widget = LocationButton()
    widget.show()

    sys.exit(app.exec())
