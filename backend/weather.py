import requests, json
from datetime import datetime
import helpers.temperature as temperature
from backend.secure_API_key import getKey
from geopy.geocoders import Nominatim
import os
import time

path = "UD"

def open_json(URL):
    """Gets json from web URL
    @param URL string with the full URL
    @return Json dictionary or False (if failed to open)"""
    response = requests.get(URL)
    if response.status_code == 200: return response.json()

    print("Error in the HTTP request")
    return False

class WeatherData:
    def __init__(self):
        try:
            self.API_KEY = getKey("OWM_KEY")
        except:
            print("API key not found, terminating program")
            exit()
        
        self.LOCATION_URL = "http://ipinfo.io/json"
        self.coords = [float(-1),float(-1)]
        self.WEATHER_URL = ""
        self.weather = ""
        self.city = ""

        self.get_weather()
    
    def get_weather(self, given_name="na"):
        """ get current location  and weather information
        no return
        """
        data = -1

        used_name = given_name #set to a function variable to avoid modifications persisting
        if (used_name == "na"):
            #check for cached data?
            folder = os.listdir(path)
            if not folder == []:
                greatest = 0
                for file in os.listdir(path):
                    if int(greatest) < int(file):
                        greatest = file
                f = open(path + "/" + greatest)
                lines = f.readlines()
                # print(lines)
                self.city = lines[1]
                try: #sometimes there is an extra newline in self.city which throws an error
                    self.coords[0] = float(lines[2])
                    self.coords[1] = float(lines[3])
                except:
                    self.coords[0] = float(lines[3])
                    self.coords[1] = float(lines[4])
            else:
            #default knoxville maybe?
                used_name = "Knoxville"

            #request input/auto location?
        data = self.find_coords(used_name)
        if (data == -1):
            pass
            #try again may be simple timeout
            #if it keeps happening set data to 0
        
        if(data == 0):
            #they messed up and need an error message
            #temporary print, swap to a display message in the gui#
            print("failed to find %s", used_name)
            data = self.find_coords("Knoxville")
        if (data == 1 or used_name=="na"):
            self.WEATHER_URL = "https://pro.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}".format(*self.coords, self.API_KEY)
            self.weather = open_json(self.WEATHER_URL)
            if (self.weather == False): print("Failed to load weather at URL " + self.WEATHER_URL)
            else:
                self.get_city()
                self.save_location()
    def get_location_weather(self):
        self.location = open_json(self.LOCATION_URL)
        if (self.location == False): print("Failed to get location at URL " + self.LOCATION_URL)
        self.coords = self.location['loc'].split(',')
        self.WEATHER_URL = "https://pro.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}".format(*self.coords, self.API_KEY)
        self.weather = open_json(self.WEATHER_URL)
        if (self.weather == False): print("Failed to load weather at URL " + self.WEATHER_URL)
        else:
            self.get_city()
            self.save_location()
    def get_city(self):
        geolocator = Nominatim(user_agent="default")
        # coordinates = ("%s,%s", self.coords[0], self.coords[1])
        location = geolocator.reverse(self.coords, language='en')
        loc = location.address
        # print(loc)
        self.city = loc

    def save_location(self):
        timechange = round(time.time())
        fo = open(path + "/" + str(timechange), "w")
        fo.write("Custom location name here\n")
        fo.write(self.city + "\n")
        fo.write(str(self.coords[0]) + "\n")
        fo.write(str(self.coords[1]) + "\n")
        fo.close()

    def find_coords(self, name):
        """Input can be regions, countries, states, cities, etc
        returns an int of 0, 1, or -1
        0 -> failure to find given name
        1 -> successfully found name and updated self.coords
        -1 -> The API failed to retrieve results (possibly just a time out)
        """
        try:
            geolocator = Nominatim(user_agent="default")
            result = geolocator.geocode(name)
        except:
            return -1
        
        if (result != None):
            self.coords = [result.latitude, result.longitude]
            return 1
        else:
            return 0

    def get_city_list(self, name):
        """Input can be regions, countries, states, cities, etc
        returns a list of location strings"""
        try:
            geolocator = Nominatim(user_agent="default")
            result = geolocator.geocode(name, exactly_one=False)
        except:
            print("Failed to get location")
            return []
        
        if (result != None):
            temp = []
            for location in result:
               temp.append(location.address)
            return temp
        else:
            # print("empty")
            return []

    def get_current(self):
        """return hourly weather dictionary\n
        returned dictionary has keys:\n
        dt, sunrise, sunset, temp, feels_like, pressure, humidity, dew_point\n
        uvi, clouds, visibility, wind_speed, wind_deg\n
        weather[] - 0[] - id, main, description, icon
        """
        return self.weather['current']

    def get_minutely(self, key):
        """return minutely weather dictionary\n
        valid keys are '0' - '60' \n
        returned dictionary has keys:\n
        dt, precipitation"""
        return self.weather['minutely'][key]

    def get_hourly(self, key):
        """return hourly weather dictionary\n
        valid keys are '0' - '47' \n
        returned dictionary has keys:\n
        dt, temp, feels_like, pressure, humidity, dew_point, uvi\n
        clouds, visibility, wind_speed, wind_deg, wind_gust, pop\n
        weather[] - 0[] - id, main, description, icon"""
        return self.weather['hourly'][key]

    def get_daily(self, key):
        """return daily weather dictionary\n
        valid keys are '0' - '7' \n
        returned dictionary has keys:\n
        dt, sunrise, sunset, moonrise, moonset, moon_phase, pressure\n
        humidity, dew_point, wind_speed, wind_deg, wind_gust, clouds, pop, uvi\n
        temp[] - day, min, max, night, eve, morn\n
        feels_like[] - day, night, eve, morn\n
        weather[] - 0[] - id, main, description, icon"""
        return self.weather['daily'][key]
    
    def get_time(self, w, start=0, stop=6):
        """Converts the given dictionaries 'dt' unix_timestamp to a date list\n
        Given time follows format [Year, Month, Day, Hour, Minute, Second]\n
        optional arguments start  and stop choose the inclusive-exclusive range of values returned:
        0,6 gives full list: 3,5 gives [hours, minutes]\n """
        l = datetime.utcfromtimestamp(w['dt']+int(self.weather['timezone_offset'])).strftime('%A-%Y-%m-%d-%H-%M-%S').split('-')
        return l[start:stop]

    def get_current_dt(self, start=0, stop=6):
        """returns current time list\n
        Given time follows format [Year, Month, Day, Hour, Minute, Second]\n
        optional arguments start  and stop choose the inclusive-exclusive range of values returned:"""
        l = datetime.utcfromtimestamp(self.weather['current']['dt']+int(self.weather['timezone_offset'])).strftime('%A-%Y-%m-%d-%H-%M-%S').split('-')
        return l[start:stop]

    def get_current_sunrise(self, start=0, stop=6):
        """"returns current sunrise time list\n
        Given time follows format [Year, Month, Day, Hour, Minute, Second]\n
        optional arguments start  and stop choose the inclusive-exclusive range of values returned:"""
        l = datetime.utcfromtimestamp(self.weather['current']['sunrise']+int(self.weather['timezone_offset'])).strftime('%A-%Y-%m-%d-%H-%M-%S').split('-')
        return l[start:stop]
 
    def get_current_sunset(self, start=0, stop=6):
        """"returns current expected sunset time list\n
        Given time follows format [Year, Month, Day, Hour, Minute, Second]\n
        optional arguments start  and stop choose the inclusive-exclusive range of values returned:"""
        l = datetime.utcfromtimestamp(self.weather['current']['sunset']+int(self.weather['timezone_offset'])).strftime('%A-%Y-%m-%d-%H-%M-%S').split('-')
        return l[start:stop]

    def get_current_temp(self, mode = 0, precision = 0):
        """returns current temperature\n
        @mode can be 0(default: Fareinheit) or 1(Celcius)\n
        @precision can be 0-2  and represents precision past decimal\n
        example precision = 0 -> 5 ; precision=2 -> 5.00 """
        t =  int(self.weather['current']['temp'])
        if (mode == 0): return temperature.KelvinToFahrenheit(t, precision)
        return temperature.KelvinToCelsius(t, precision)

    def get_current_feelslike(self, mode = 0, precision = 0):
        """returns current feelslike temperature\n
        @mode can be 0(default: Fareinheit) or 1(Celcius)\n
        @precision can be 0-2  and represents precision past decimal\n
        example precision = 0 -> 5 ; precision=2 -> 5.00 """
        t =  int(self.weather['current']['feels_like'])
        if (mode == 0): return temperature.KelvinToFahrenheit(t, precision)
        return temperature.KelvinToCelsius(t, precision)

    def get_current_pressure(self):
        """returns current pressure in hPa"""
        return self.weather['current']['pressure']
    
    def get_current_humidity(self):
        """returns current humidity % (int 1-100)"""
        return self.weather['current']['humidity']

    def get_current_dewpoint(self, mode=0, precision=0):
        """returns current dewpoint temperature\n
        @mode can be 0(default: Fareinheit) or 1(Celcius)\n
        @precision can be 0-2  and represents precision past decimal\n
        example precision = 0 -> 5 ; precision=2 -> 5.00 """
        t =  int(self.weather['current']['dew_point'])
        if (mode == 0): return temperature.KelvinToFahrenheit(t, precision)
        return temperature.KelvinToCelsius(t, precision)

    def get_current_uvi(self):
        """returns current uvi float"""
        return self.weather['current']['uvi']
    
    def get_current_clouds(self):
        """returns current cloud coverage % (int 0-100)"""
        return self.weather['current']['clouds']

    def get_current_visibility(self):
        """returns current visibility int"""
        return self.weather['current']['visibility']

    def get_current_windspeed(self):
        """returns current windspeed in m/s"""
        return self.weather['current']['wind_speed']
    
    def get_current_winddeg(self):
        """returns wind direction in degrees"""
        return self.weather['current']['wind_deg']

    def get_current_weather(self):
        """returns current weather dictionary with keys\n
        id : int -> the current weather's id\n
        main : string -> weather's general description (Ex: Clear)\n
        description: string -> weather's more descriptive description (Ex: Clear Sky)\n
        icon : string -> weather's icon id
        """
        return self.weather['current']['weather'][0] 

    def get_minutely_dt(self, minute, start=0, stop=6):
        """returns time list at minute\n
        @param minute -> string between '0' - '60'\n
        Given time follows format [Year, Month, Day, Hour, Minute, Second]\n
        optional arguments start  and stop choose the inclusive-exclusive range of values returned:"""
        l = datetime.utcfromtimestamp(self.weather['minutely'][minute]['dt']+int(self.weather['timezone_offset'])).strftime('%A-%Y-%m-%d-%H-%M-%S').split('-')
        return l[start:stop]

    def get_minutely_precipitation(self, minute):
        """returns precipitation at minute in mm^3
        @param minute -> string between '0' - '60'"""
        return self.weather['minutely'][minute]['precipitation']

    def get_hourly_dt(self, hour, start=0, stop=6):
        """returns time list at given hour\n
        @param hour -> string between '0' - '47'\n
        Given time follows format [Year, Month, Day, Hour, Minute, Second]\n
        optional arguments start  and stop choose the inclusive-exclusive range of values returned:"""
        l = datetime.utcfromtimestamp(self.weather['hourly'][hour]['dt']+int(self.weather['timezone_offset'])).strftime('%A-%Y-%m-%d-%H-%M-%S').split('-')
        return l[start:stop]
    
    def get_hourly_temp(self, hour, mode=0, precision=0):
        """returns temperature for given hour\n
        @param hour -> string between '0' - '47'\n
        @mode can be 0(default: Fareinheit) or 1(Celcius)\n
        @precision can be 0-2  and represents precision past decimal
        Example: precision = 0 -> 5 ; precision=2 -> 5.00 """
        t =  int(self.weather['hourly'][hour]['temp'])
        if (mode == 0): return temperature.KelvinToFahrenheit(t, precision)
        return temperature.KelvinToCelsius(t, precision)

    def get_hourly_feelslike(self, hour, mode=0, precision=0):
        """returns feelslike temperature at given hour\n
        @param hour -> string between '0' - '47'\n
        @mode can be 0(default: Fareinheit) or 1(Celcius)\n
        @precision can be 0-2  and represents precision past decimal\n
        example precision = 0 -> 5 ; precision=2 -> 5.00 """
        t =  int(self.weather['hourly'][hour]['feels_like'])
        if (mode == 0): return temperature.KelvinToFahrenheit(t, precision)
        return temperature.KelvinToCelsius(t, precision)
    
    def get_hourly_pressure(self, hour):
        """returns pressure at given hour in hPa
        @param hour -> string between '0' - '47'\n"""
        return self.weather['hourly'][hour]['pressure']

    def get_hourly_humidity(self, hour):
        """returns humidity % at given hour (returns int 0-100)
        @param hour -> string between '0' - '47'\n"""
        return self.weather['hourly'][hour]['humidity']
    
    def get_hourly_dewpoint(self, hour, mode=0, precision=0):
        """returns dewpoint temperature at given hour\n
        @param hour -> string between '0' - '47'\n
        @mode can be 0(default: Fareinheit) or 1(Celcius)\n
        @precision can be 0-2  and represents precision past decimal\n
        example precision = 0 -> 5 ; precision=2 -> 5.00 """
        t =  int(self.weather['hourly'][hour]['dew_point'])
        if (mode == 0): return temperature.KelvinToFahrenheit(t, precision)
        return temperature.KelvinToCelsius(t, precision)
        
    def get_hourly_uvi(self, hour):
        """returns uvi float at given hour
        @param hour -> string between '0' - '47'\n"""
        return self.weather['hourly'][hour]['uvi']
    
    def get_hourly_clouds(self, hour):
        """returns cloud coverage % for given hour (int 0-100)
        @param hour -> string between '0' - '47'\n"""
        return self.weather['hourly'][hour]['clouds']

    def get_hourly_visibility(self, hour):
        """returns visibility for given hour as an int
        @param hour -> string between '0' - '47'\n"""
        return self.weather['hourly'][hour]['visibility']

    def get_hourly_windspeed(self, hour):
        """returns windspeed for given hour in m/s
        @param hour -> string between '0' - '47'\n"""
        return self.weather['hourly'][hour]['wind_speed']

    def get_hourly_winddeg(self, hour):
        """returns wind direction for given hour in degrees
        @param hour -> string between '0' - '47'\n"""
        return self.weather['hourly'][hour]['wind_deg']

    def get_hourly_windgust(self, hour):
        """returns wind gust for given hour in m/s
        @param hour -> string between '0' - '47'\n"""
        return self.weather['hourly'][hour]['wind_gust']

    def get_hourly_pop(self, hour):
        """returns precipitation chance for given hour as float (0-1)
        @param hour -> string between '0' - '47'\n"""
        return self.weather['hourly'][hour]['pop']*100

    def get_hourly_weather(self, hour):
        """returns weather dictionary at given hour with keys:\n
        id : int -> the weather's id at given hour\n
        main : string -> weather's general description (Ex: Clear)\n
        description: string -> weather's more descriptive description (Ex: Clear Sky)\n
        icon : string -> weather's icon id
        @param hour -> string between '0' - '47'\n
        """
        return self.weather['hourly'][hour]['weather']['0']

    def get_daily_dt(self, day, start=0, stop=6):
        """returns time as a list for given day\n
        @param day -> string between '0' - '7'\n
        Given time follows format [Year, Month, Day, Hour, Minute, Second]\n
        optional arguments start  and stop choose the inclusive-exclusive range of values returned:"""
        l = datetime.utcfromtimestamp(self.weather['daily'][day]['dt']+int(self.weather['timezone_offset'])).strftime('%A-%Y-%m-%d-%H-%M-%S').split('-')
        return l[start:stop]

    def get_daily_sunrise(self, day, start=0, stop=6):
        """returns sunrise time as a list for given day\n
        @param day -> string between '0' - '7'\n
        Given time follows format [Year, Month, Day, Hour, Minute, Second]\n
        optional arguments start  and stop choose the inclusive-exclusive range of values returned:"""
        l = datetime.utcfromtimestamp(self.weather['daily'][day]['sunrise']+int(self.weather['timezone_offset'])).strftime('%A-%Y-%m-%d-%H-%M-%S').split('-')
        return l[start:stop]

    def get_daily_sunset(self, day, start=0, stop=6):
        """returns sunset time as a list for given day\n
        @param day -> string between '0' - '7'\n
        Given time follows format [Year, Month, Day, Hour, Minute, Second]\n
        optional arguments start  and stop choose the inclusive-exclusive range of values returned:"""
        l = datetime.utcfromtimestamp(self.weather['daily'][day]['sunset']+int(self.weather['timezone_offset'])).strftime('%A-%Y-%m-%d-%H-%M-%S').split('-')
        return l[start:stop]

    def get_daily_moonrise(self, day, start=0, stop=0):
        """returns moonrise time as a list for given day\n
        @param day -> string between '0' - '7'\n
        Given time follows format [Year, Month, Day, Hour, Minute, Second]\n
        optional arguments start  and stop choose the inclusive-exclusive range of values returned:"""
        l = datetime.utcfromtimestamp(self.weather['daily'][day]['moonrise']+int(self.weather['timezone_offset'])).strftime('%A-%Y-%m-%d-%H-%M-%S').split('-')
        return l[start:stop]

    def get_daily_moonset(self, day, start=0, stop=6):
        """returns moonset time as a list for given day\n
        @param day -> string between '0' - '7'\n
        Given time follows format [Year, Month, Day, Hour, Minute, Second]\n
        optional arguments start  and stop choose the inclusive-exclusive range of values returned:"""
        l = datetime.utcfromtimestamp(self.weather['daily'][day]['moonset']+int(self.weather['timezone_offset'])).strftime('%A-%Y-%m-%d-%H-%M-%S').split('-')
        return l[start:stop]

    def get_daily_moonphase(self, day):
        """returns moonphase on given day as float (0-1)
        @param day -> string between '0' - '7'\n"""
        return self.weather['daily'][day]['moon_phase']

    def get_daily_pressure(self, day):
        """returns pressure on given in hPa
        @param day -> string between '0' - '7'\n"""
        return self.weather['daily'][day]['pressure']
    
    def get_daily_humidity(self, day):
        """returns humidity % at given day (returns int 0-100)
        @param day -> string between '0' - '7'\n"""
        return self.weather['daily'][day]['humidity']

    def get_daily_dewpoint(self, day, mode=0, precision=0):
        """returns dewpoint temperature at given day\n
        @param day -> string between '0' - '7'\n
        @mode can be 0(default: Fareinheit) or 1(Celcius)\n
        @precision can be 0-2  and represents precision past decimal\n
        example precision = 0 -> 5 ; precision=2 -> 5.00 """
        t =  int(self.weather['daily'][day]['dew_point'])
        if (mode == 0): return temperature.KelvinToFahrenheit(t, precision)
        return temperature.KelvinToCelsius(t, precision)

    def get_daily_windspeed(self, day):
        """returns windspeed for given day in m/s
        @param day -> string between '0' - '7'\n"""
        return self.weather['daily'][day]['wind_speed']
    
    def get_daily_winddeg(self, day):
        """returns wind direction for given day in degrees
        @param day -> string between '0' - '7'\n"""
        return self.weather['daily'][day]['wind_deg']

    def get_daily_windgust(self, day):
        """returns wind gust for given day in m/s
        @param day -> string between '0' - '7'\n"""
        return self.weather['daily'][day]['wind_gust']

    def get_daily_clouds(self, day):
        """returns cloud coverage % for given day (int 0-100)
        @param day -> string between '0' - '7'\n"""
        return self.weather['daily'][day]['clouds']

    def get_daily_pop(self, day):
        """returns precipitation chance for given day as float (0-1)
        @param day -> string between '0' - '7'\n"""
        return self.weather['daily'][day]['pop']*100

    def get_daily_uvi(self, day):
        """returns uvi float at given day
        @param day -> string between '0' - '7'\n"""
        return self.weather['daily'][day]['uvi']

    def get_daily_temp_day(self, day, mode = 0, precision = 0):
        """returns average temperature at given day\n
        @param day -> string between '0' - '7'\n
        @mode can be 0(default: Fareinheit) or 1(Celcius)\n
        @precision can be 0-2  and represents precision past decimal\n
        example precision = 0 -> 5 ; precision=2 -> 5.00 """
        t =  int(self.weather['daily'][day]['temp']['day'])
        if (mode == 0): return temperature.KelvinToFahrenheit(t, precision)
        return temperature.KelvinToCelsius(t, precision)

    def get_daily_temp_min(self, day, mode = 0, precision = 0):
        """returns minimum temperature at given day\n
        @param day -> string between '0' - '7'\n
        @mode can be 0(default: Fareinheit) or 1(Celcius)\n
        @precision can be 0-2  and represents precision past decimal\n
        example precision = 0 -> 5 ; precision=2 -> 5.00 """
        t =  int(self.weather['daily'][day]['temp']['min'])
        if (mode == 0): return temperature.KelvinToFahrenheit(t, precision)
        return temperature.KelvinToCelsius(t, precision)
    
    def get_daily_temp_max(self, day, mode = 0, precision = 0):
        """returns max temperature at given day\n
        @param day -> string between '0' - '7'\n
        @mode can be 0(default: Fareinheit) or 1(Celcius)\n
        @precision can be 0-2  and represents precision past decimal\n
        example precision = 0 -> 5 ; precision=2 -> 5.00 """
        t =  int(self.weather['daily'][day]['temp']['max'])
        if (mode == 0): return temperature.KelvinToFahrenheit(t, precision)
        return temperature.KelvinToCelsius(t, precision)

    def get_daily_temp_night(self, day, mode = 0, precision = 0):
        """returns night time temperature at given day\n
        @param day -> string between '0' - '7'\n
        @mode can be 0(default: Fareinheit) or 1(Celcius)\n
        @precision can be 0-2  and represents precision past decimal\n
        example precision = 0 -> 5 ; precision=2 -> 5.00 """
        t =  int(self.weather['daily'][day]['temp']['night'])
        if (mode == 0): return temperature.KelvinToFahrenheit(t, precision)
        return temperature.KelvinToCelsius(t, precision)

    def get_daily_temp_evening(self, day, mode = 0, precision = 0):
        """returns evening temperature at given day\n
        @param day -> string between '0' - '7'\n
        @mode can be 0(default: Fareinheit) or 1(Celcius)\n
        @precision can be 0-2  and represents precision past decimal\n
        example precision = 0 -> 5 ; precision=2 -> 5.00 """
        t =  int(self.weather['daily'][day]['temp']['eve'])
        if (mode == 0): return temperature.KelvinToFahrenheit(t, precision)
        return temperature.KelvinToCelsius(t, precision)

    def get_daily_temp_morning(self, day, mode = 0, precision = 0):
        """returns morning temperature at given day\n
        @param day -> string between '0' - '7'\n
        @mode can be 0(default: Fareinheit) or 1(Celcius)\n
        @precision can be 0-2  and represents precision past decimal\n
        example precision = 0 -> 5 ; precision=2 -> 5.00 """
        t =  int(self.weather['daily'][day]['temp']['morn'])
        if (mode == 0): return temperature.KelvinToFahrenheit(t, precision)
        return temperature.KelvinToCelsius(t, precision)

    def get_daily_feelslike_day(self, day, mode = 0, precision = 0):
        """returns feelslike daytime temperature at given day\n
        @param day -> string between '0' - '7'\n
        @mode can be 0(default: Fareinheit) or 1(Celcius)\n
        @precision can be 0-2  and represents precision past decimal\n
        example precision = 0 -> 5 ; precision=2 -> 5.00 """
        t =  int(self.weather['daily'][day]['feels_like']['day'])
        if (mode == 0): return temperature.KelvinToFahrenheit(t, precision)
        return temperature.KelvinToCelsius(t, precision)

    def get_daily_feelslike_night(self, day, mode = 0, precision = 0):
        """returns feelslike nighttime temperature at given day\n
        @param day -> string between '0' - '7'\n
        @mode can be 0(default: Fareinheit) or 1(Celcius)\n
        @precision can be 0-2  and represents precision past decimal\n
        example precision = 0 -> 5 ; precision=2 -> 5.00 """
        t =  int(self.weather['daily'][day]['feels_like']['night'])
        if (mode == 0): return temperature.KelvinToFahrenheit(t, precision)
        return temperature.KelvinToCelsius(t, precision)

    def get_daily_feelslike_evening(self, day, mode = 0, precision = 0):
        """returns feelslike evening temperature at given day\n
        @param day -> string between '0' - '7'\n
        @mode can be 0(default: Fareinheit) or 1(Celcius)\n
        @precision can be 0-2  and represents precision past decimal\n
        example precision = 0 -> 5 ; precision=2 -> 5.00 """
        t =  int(self.weather['daily'][day]['feels_like']['eve'])
        if (mode == 0): return temperature.KelvinToFahrenheit(t, precision)
        return temperature.KelvinToCelsius(t, precision)

    def get_daily_feelslike_morning(self, day, mode = 0, precision = 0):
        """returns feelslike morning temperature at given day\n
        @param day -> string between '0' - '7'\n
        @mode can be 0(default: Fareinheit) or 1(Celcius)\n
        @precision can be 0-2  and represents precision past decimal\n
        example precision = 0 -> 5 ; precision=2 -> 5.00 """
        t =  int(self.weather['daily'][day]['feels_like']['morn'])
        if (mode == 0): return temperature.KelvinToFahrenheit(t, precision)
        return temperature.KelvinToCelsius(t, precision)

    def get_daily_weather(self, day):
        """returns weather dictionary at given hour with keys:\n
        id : int -> the weather's id at given hour\n
        main : string -> weather's general description (Ex: Clear)\n
        description: string -> weather's more descriptive description (Ex: Clear Sky)\n
        icon : string -> weather's icon id
        @param day -> string between '0' - '7'\n
        """
        return self.weather['daily'][day]['weather'][0]



if __name__ == '__main__':
    w = WeatherData()
    print("\n")
    DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    i = DAYS.index(w.get_current_dt()[0])
    for x in range(0,8):
        print(DAYS[(x+i)%7][:3] + ": " + w.get_daily_weather(x)['description'])
        print(str(w.get_daily_pop(x)) + "% chance of precipitation")
        print("High: " + str(w.get_daily_temp_max(x)) + " Low: " + str(w.get_daily_temp_min(x)))
        print("")

    forecast = []
    for x in range(0,int(48/3)):
        t = "AM"
        h = int(w.get_hourly_dt(x*3)[4])
        if (int(h/12) >= 1): 
            t = "PM"
            h -= 12
        if (h==0):
            h=12
        spaced = str(h) + t + ": "
        forecast.append((str(h)+t))
        print(f"{spaced:>6}"+ f"{str(w.get_hourly_temp(x*3)):>3}" + " degrees with a " + f"{str(int(w.get_hourly_pop(x*3))):>3}" + "% chance of rain")

