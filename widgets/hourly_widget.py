from PyQt6.QtWidgets import QGridLayout, QGroupBox, QWidget, QLabel, QApplication, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
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

        groupbox = QGroupBox("Hourly Temps")
        layout = QGridLayout()
        layout.addWidget(groupbox)

        vbox0 = QVBoxLayout()
        groupbox.setLayout(vbox0)
        self.hour0 = QLabel(self)
        self.hour0.setText(str(self.hourly_temp[0]))
        
        self.hour1 = QLabel(self)
        self.hour1.setText(str(self.hourly_temp[1]))

        #self.label = QLabel(self)
        #self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        #self.label.setStyleSheet("border: 2px solid black; padding: 4px;")
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    widget = HourlyWeatherWidget()
    widget.resize(600, 200)
    widget.show()

    sys.exit(app.exec())