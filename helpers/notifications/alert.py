from typing import Union
from PyQt6.QtWidgets import QMessageBox
from widgets.notification import Notification
from backend.weather import WeatherData

def notify_thunder(wd: WeatherData) -> Union[Notification, None]:
    '''Returns a Notification if it is thundering'''
    # Get the description and checks if it is tundering
    description = wd.get_current_weather()["description"]

    if 'thunder' in description.lower():
        return Notification(msg='Warning: Thundering')

    return None
