#!python
import urllib2, json

from settings import *

#This becomes the global url handle
f = "error"

def fetchWeather(type):
	global f
	url = 'http://api.wunderground.com/api/' + key + '/geolookup/' + type +  '/q/' + zip + '.json'
	f = urllib2.urlopen(url)
	json_string = f.read()
	return json.loads(json_string)

def closeURL():
	f.close()