'''
    uvNotify.py
    Notifies user if the UV index in their area rises
    above certain threshold
'''

from types import FunctionType
from PyQt6.QtWidgets import QMessageBox, QApplication
import sys
from widgets.notification import Notification
from backend.weather import WeatherData
import time


class UVCheck(Notification):
    '''
        Notification with UV information
    '''
    def __init__(self, msg: str = 'UV Index Alert', icon=None, buttons=None, threshold=9, weather_data: WeatherData = None):
        super().__init__()
        
        # create instance of WeatherData class if None was given
        self.wd = weather_data if weather_data != None else WeatherData()
        self.threshold = threshold

        # check weather every 15 minutes
        while True:
            self.check_index()
            time.sleep(350)


    # Retrieve current UV index
    def get_uvi(self):
        self.uvi = self.wd.get_current_uvi()

    # Check if notification must be sent out
    def check_index(self):
        self.get_uvi()
        if self.uvi >= self.threshold:
            self.setMessage("UV index is dangerously high!\n UV Index: %d" % self.uvi)
            self.notify()
        else:
            print("UV at a healthy %d" % self.uvi)

        

# To test functionality individually
if __name__ == "__main__":
    app = QApplication(sys.argv)

    uv_notif = UVCheck()
    uv_notif.check_index()

    sys.exit(app.exec())