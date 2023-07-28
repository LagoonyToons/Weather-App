### Use weather API to import user's current coordinates
import requests
from backend.secure_API_key import getKey

def open_json(URL):
    '''
        Gets json from web URL
        @param URL string with the full URL
        @return Json dictionary or False (if failed to open)
    '''
    response = requests.get(URL)
    if response.status_code == 200: return response.json()

    print("Error in the HTTP request")
    return False

class CityInformation:
    '''
        Contains relevant information of saved cities
    '''
    def __init__(self, cityName = None, stateName = None, coord = [float(-1), float(-1)]):
        self.cityName = cityName
        self.stateName = stateName
        self.coordinates = coord

class Location:
    def __init__(self):
        self.API_KEY = getKey('OWM_KEY')
        
        self.LOCATION_URL = "http://ipinfo.io/json"
        self.coord = [float(-1), float(-1)]
        self.saved_cities = {}

    def get_user_coordinates(self):
        '''
            Fetch user coordinates and save to self.coord
        '''

        self.location = open_json(self.LOCATION_URL)
        if (self.location == False): print("Failed to get location at URL " + self.LOCATION_URL)
        self.coords = self.location['loc'].split(',')

    def add_new_city(self, cityName, stateName, coord):
        '''
            Adds new city to list of saved cities
        '''
        self.saved_cities[cityName] = CityInformation(cityName, stateName, coord)

    def clear_saved_cities(self):
        '''
            Clear up list of save cities
        '''
        self.saved_cities.clear()

    def set_city(self, cityName):
        '''
            Given a city name it sets the
        '''
        cur_city: CityInformation = self.saved_cities.get(cityName)
        if cur_city:
            self.coord = cur_city.coord
            print('Current city updated: %s' % cur_city.cityName)
            
        else:
            print('Error: Specified city has not been saved')
            return False
