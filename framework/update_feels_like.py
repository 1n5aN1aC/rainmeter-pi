#!python
import logging
from database import *
from weather import *

#
# This File Handles updating the 'feels-like' display.
# This is the small window in the top-right of the index page
# that show what the weather currently 'feels like.'
#

# Gets the Weather data from the internet.
def update_feels_like():
	parsed_json = fetchWeather('conditions')
	closeURL()
	
	NOW_URL = parsed_json['current_observation']['icon_url']
	NOW_Feel = float(parsed_json['current_observation']['feelslike_f'])
	
	now = Table_Now.get(1)
	now.Now_URL = NOW_URL
	now.Now_Feel = NOW_Feel
	logging.getLogger("thread_feelsLike").info(" Updated Feels Like Data.")