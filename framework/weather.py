#!python
import urllib2, json

import settings

#This becomes the global url handle
f = "error"

def fetchWeather(forecast_type):
    global f
    url = 'http://api.wunderground.com/api/' + settings.key + "/" + forecast_type +  '/q/' + settings.zipcode + '.json'
    f = urllib2.urlopen(url)
    json_string = f.read()
    return json.loads(json_string)

def closeURL():
    f.close()