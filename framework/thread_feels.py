#!python
# -*- coding: UTF-8 -*-
import logging, time
import weather, stoppable_thread, database, settings

#
# This File Handles updating the 'feels-like' display.
# This is the small window in the top-right of the index page
# that show what the weather currently 'feels like.'
class thread_feels_like(stoppable_thread.stoppable_thread):
	def run(self):
		self.check_db()
		while self.RUN:
			self.update_feels_like()
			time.sleep(settings.how_often_to_update_feels_like)
	
	def update_feels_like(self):
		parsed_json = weather.fetchWeather('conditions')
		weather.closeURL()
		
		NOW_URL = parsed_json['current_observation']['icon_url']
		NOW_FEEL = float(parsed_json['current_observation']['feelslike_f'])
		
		database.Table_Sensors.selectBy(int_id="Feels_URL").getOne().value_string = NOW_URL
		database.Table_Sensors.selectBy(int_id="Feels_value").getOne().value = NOW_FEEL
		
		logging.getLogger("thread-feels").info(" Updated feels like info.")
	
	# Handles making sure all the feel-like entries exist in the database
	def check_db(self):
		database.database_verify_group("Feels", "Feels Like")
		database.database_verify_sensor("Feels_URL", "URL of the Feels like Image", "Feels", '', '')
		database.database_verify_sensor("Feels_value", "Temp of feels like", "Feels", '', u"\u00b0F")