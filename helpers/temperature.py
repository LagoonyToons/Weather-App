'''
    Implements functions that perform unit
    conversions for given temperatures
'''

def KelvinToCelsius(temp, precision=0):
    '''
        Converts temperature from Kelvin to Celsius
    '''
    temp = (temp - 273.15)
    return round(temp, precision)

def KelvinToFahrenheit(temp, precision=0):
    '''
        Temperature conversion from Kelvin to Fahrenheit
    '''
    celsuis = temp - 273.15
    temp = (celsuis * 9/5) + 32
    return round(temp, precision)

def CelsiusToFahrenheit(temp, precision=0):
    '''
        Temperature conversion from Celsius to Fahrenheit
    '''
    temp = (temp * 9/5) + 32
    return round(temp, precision)

def FahrenheitToCelsius(temp, precision=0):
    '''
        Temperature conversion from Fahrenheit to Celsius
    '''
    temp = (temp - 32) * 5/9
    return round(temp, precision)