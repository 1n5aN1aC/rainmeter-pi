#!python
import logging, time
from weather import *
from Stoppable_Thread import *
import Now

#
# This File Handles updating the 'feels-like' display.
# This is the small window in the top-right of the index page
# that show what the weather currently 'feels like.'
class thread_feels_like(Stoppable_Thread):
	def run(self):
		while self.RUN:
			self.update_feels_like()
			time.sleep(how_often_to_update_feels_like)
	
	def update_feels_like(self):
		parsed_json = fetchWeather('conditions')
		closeURL()
		
		NOW_URL = parsed_json['current_observation']['icon_url']
		NOW_Feel = float(parsed_json['current_observation']['feelslike_f'])
		
		now = Now.get(1)
		now.Now_URL = NOW_URL
		now.Now_Feel = NOW_Feel
		logging.getLogger("thread-feels").info(" Updated feels like info.")