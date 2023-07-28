import sys
import time
from threading import Thread
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QScrollArea
from backend.location import Location
from backend.weather import WeatherData
from helpers.notifications.alert import notify_thunder
from helpers.notifications.rain import notify_rain
from widgets.sunriseSunset import SunriseSunsetWidget
from widgets.uvRays import UVradiationWidget
from widgets.weatherDays import DaysWidget
from widgets.weatherDes import weatherDescriptionWidget
from widgets.wind import WindWidget
from widgets.displayUserCoord import UserCoor
from widgets.humidity import HumidityWidget
from widgets.hourly_weather import HourlyWeatherWidget
from widgets.highlow import HighLowWidget
from widgets.displaycity import CityDisplay
from widgets.locationbutton import LocationButton
from widgets.currentTemp import CurrentTempWidget
from widgets.searchbox import SearchboxWidget
from widgets.weather_icons import iconWidget
from widgets.clouds import CloudCoverageWidget
from widgets.combineDes import weatherDescriptionWidget

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create Weather and Location Data
        self.wd = WeatherData()
        self.location = Location()
        self.unit = 'F'
        self.wd.get_location_weather()
        self.subWidgets = []
        self.keep_refreshing = True

        self.scroll = QScrollArea()
        central_widget = QWidget()
        grid = QGridLayout()

        central_widget.setLayout(grid)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(central_widget)
        self.setCentralWidget(self.scroll)

        # Add imported widgets here
        self.seven_day_display = DaysWidget(self.wd)
        self.wind_display = WindWidget(self.wd)
        self.user_coor_display = UserCoor(self.location)
        self.humidity = HumidityWidget(self.wd)
        self.hourly_temp = HourlyWeatherWidget(self.wd)
        self.sunriseSunset = SunriseSunsetWidget(self.wd)
        self.uvRays = UVradiationWidget(self.wd)
        self.weatherDes = weatherDescriptionWidget(self.wd, temp_unit=self.unit)
        self.highlow = HighLowWidget(self.wd)
        self.cityDisplay = CityDisplay(self.wd)
        self.locationButton = LocationButton(self.wd)
        self.curr_temp = CurrentTempWidget(self.wd, self.unit)
        self.searchbox = SearchboxWidget(self.wd)
        self.iconWidget = iconWidget(self.wd)
        self.CloudCoverageWidget = CloudCoverageWidget(self.wd)

        self.subWidgets.append(self.seven_day_display)
        self.subWidgets.append(self.wind_display)
        self.subWidgets.append(self.user_coor_display)
        self.subWidgets.append(self.humidity )
        self.subWidgets.append(self.hourly_temp)
        self.subWidgets.append(self.sunriseSunset)
        self.subWidgets.append(self.uvRays)
        self.subWidgets.append(self.weatherDes)
        self.subWidgets.append(self.highlow)
        self.subWidgets.append(self.cityDisplay)
        self.subWidgets.append(self.locationButton)
        self.subWidgets.append(self.curr_temp)
        self.subWidgets.append(self.searchbox)
        self.subWidgets.append(self.iconWidget)
        self.subWidgets.append(self.CloudCoverageWidget)

        #grid.addWidget(self.curr_temp, 0, 1)
        #grid.addWidget(self.iconWidget,2,1)
        #grid.addWidget(self.highlow, 0, 2)
        #grid.addWidget(self.user_coor_display, 2, 1)
        grid.addWidget(self.searchbox, 0, 4, 1, 2)
        grid.addWidget(self.cityDisplay, 0, 3)
        grid.addWidget(self.weatherDes, 1, 3, 2, 2)
        grid.addWidget(self.hourly_temp, 3, 1, 1, 4)
        grid.addWidget(self.seven_day_display, 0, 0, 2, 1)
        grid.addWidget(self.wind_display, 0, 1, 1, 1)
        grid.addWidget(self.humidity, 2, 1)
        grid.addWidget(self.sunriseSunset, 2, 0, 2, 1)
        grid.addWidget(self.uvRays, 1, 1, 1, 1)
        grid.addWidget(self.CloudCoverageWidget, 3, 0, 1, 1)
        #grid.addWidget(self.locationButton, 5, 0)

    def updateUI(self, wait_time: int):
        amount, curr = 60 * wait_time, 0
        while(self.keep_refreshing):
            if curr >= amount:
                curr = 0
                self.wd.get_location_weather()
                for widget in self.subWidgets:
                    widget.update()
            curr += 5
            time.sleep(5)

    def onStartUp(self):
        self.t = Thread(target=self.updateUI, args=(5,))
        self.t.start()
        if rain_noti := notify_rain(self.wd):
            rain_noti.notify()
        if thunder_noti := notify_thunder(self.wd):
            thunder_noti.notify()


def setAppBG(app: QApplication, wd: WeatherData) -> None:
    num = int(wd.get_current_weather()['id'])
    weather_des = 'clear-sunny'
    match num:
        case num if 200 <= num < 300:
            weather_des = 'thunderstorm'
        case num if 300 <= num < 400:
            weather_des = 'drizzle'
        case num if 400 <= num < 500:
            weather_des = 'clear-sunny'
        case num if 500 <= num < 600:
            weather_des = 'rain'
        case num if 600 <= num < 700:
            weather_des = 'snow'
        case num if 700 <= num < 800:
            weather_des = 'mist'
        case num if 800 == num:
            weather_des = 'clear-sunny'
        case num if num > 800:
            weather_des = 'few-clouds'
    app.setStyleSheet(f"""
        Window {{
            background-image: url(./images/{weather_des}.png);
        }}
    """)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Window()
    window.resize(1300, 800)
    setAppBG(app, window.wd)
    window.show()
    window.onStartUp()

    stat = app.exec()
    window.keep_refreshing = False
    window.t.join()
    sys.exit(stat)
