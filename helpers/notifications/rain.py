from datetime import datetime, timedelta
from typing import Union
from widgets.notification import Notification
from backend.weather import WeatherData


def notify_rain(wd: WeatherData) -> Union[Notification, None]:
    current = datetime.now()

    rain_time = [{'hour': hour,
                  'prob': wd.get_hourly(hour)['pop'],
                  'amount': wd.get_hourly(hour)['rain']['1h']}
                 for hour in range(24) if 'rain' in wd.get_hourly(hour)]

    if first_rain := next((x for x in rain_time if x['prob'] >= 0.5), None):
        added_time = timedelta(hours=first_rain['hour'])
        current = current + added_time
        return Notification(f'It might rain at {current.strftime("%-I%p")} today. Might want to bring an umbrella')
    else:
        return None
