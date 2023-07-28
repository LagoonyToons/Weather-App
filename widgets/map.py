import sys
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton
from pyqtlet import L, MapWidget
from backend.weather import WeatherData


class MapWindow(QWidget):
    def __init__(self, weather_data: WeatherData = None):
        # Setting up the widgets and layout
        super().__init__()
        self.mapWidget = MapWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.mapWidget)
        self.setLayout(self.layout)

        self.w = weather_data if weather_data != None else WeatherData()
        self.wd.get_weather()

        # Working with the maps with pyqtlet
        self.map = L.map(self.mapWidget)
        self.map.setView([float(self.w.coords[0]),float(self.w.coords[1])], 6)
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(self.map) #base layer dont remove

        #default and basemap member needs to only be made into a tileLayer once, auto enables this base layer
        self.precip = L.tileLayer("http://maps.openweathermap.org/maps/2.0/weather/PR0/{z}/{x}/{y}?opacity=.25&appid=" + self.w.API_KEY)
        self.precip.addTo(self.map)


        self.generate_basemaps()
        self.generate_overlays()

        L.control.layers(self.basemaps, self.overlays).addTo(self.map)


        self.marker = L.marker([float(self.w.coords[0]),float(self.w.coords[1])])
        self.marker.bindPopup('You')
        self.map.addLayer(self.marker)


        self.show()
    
    def generate_basemaps(self):
        self.basemaps = {
            "Precipitation" : self.precip,
            "Temp" : L.tileLayer('http://maps.openweathermap.org/maps/2.0/weather/TA2/{z}/{x}/{y}?fill_bound=true&appid='  + self.w.API_KEY),
            "Humidity" : L.tileLayer("http://maps.openweathermap.org/maps/2.0/weather/HRD0/{z}/{x}/{y}?fill_bound=true&appid=" + self.w.API_KEY),
            "Soil temp" : L.tileLayer("http://maps.openweathermap.org/maps/2.0/weather/TS0/{z}/{x}/{y}?fill_bound=true&appid=" + self.w.API_KEY),
        }
    def generate_overlays(self):
        self.overlays = {
            "Accumulated precipitation" : L.tileLayer("http://maps.openweathermap.org/maps/2.0/weather/PA0/{z}/{x}/{y}?fill_bound=true&appid=" + self.w.API_KEY),
            "Wind speed" : L.tileLayer("http://maps.openweathermap.org/maps/2.0/weather/WS10/{z}/{x}/{y}?fill_bound=true&appid=" + self.w.API_KEY),
            "Cloudiness" : L.tileLayer("http://maps.openweathermap.org/maps/2.0/weather/CL/{z}/{x}/{y}?fill_bound=true&appid=" + self.w.API_KEY),
            "Wind direction" : L.tileLayer("http://maps.openweathermap.org/maps/2.0/weather/WND/{z}/{x}/{y}?fill_bound=true&appid=" + self.w.API_KEY),
        }
    
    def generate_forecasts(self):
        self.forecast = []
        for x in range(0,13):
            self.forecast.append( L.tileLayer("http://maps.openweathermap.org/maps/2.0/weather/PR0/{z}/{x}/{y}?opacity=.25&appid=" + self.w.API_KEY + "&date=" + str(self.time + ((x-6) * 3600*3))))
    
    def iter_weather(self):
        self.map.removeLayer(self.forecast[self.lastIndex])
        self.map.addLayer(self.forecast[self.sl.value()])
        self.lastIndex = self.sl.value()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MapWindow()
    sys.exit(app.exec_())