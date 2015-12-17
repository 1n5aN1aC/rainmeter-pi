#!python
import logging, pytz, time, datetime
import stoppable_thread, database, settings

#
# This Handles compiling the raw rain data, (which is time-of-tip based)
# to the format seen on the main screen (last day, last 24h, since reset.)
# If you want to know how the rain sub-system works, have a look at README-ADVANCED.txt
class thread_rain_compile(stoppable_thread.stoppable_thread):
	def run(self):
		self.check_db()
		while self.RUN:
			self.update_rain_compile()
			time.sleep(settings.how_often_to_compile_rain)
	
	def update_rain_compile(self):
		rain_24h = 0.0
		rain_today = 0.0
		rain_week = 0.0
		
		#This is blackmagic that uses timezone witchcraft to fine the utc is local midnight
		now = datetime.datetime.now()
		midnight = now.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone(settings.my_timezone)).replace(hour=0,minute=0,second=0,microsecond=0).astimezone(pytz.UTC).replace(tzinfo=None)
		
		#I'm sure theres a better way to do this, but the performance impact is minimal, so w/e
		rains = database.Table_Rain.select()
		for rain in rains:
			rain_week = rain_week + rain.quantity
			if (now - rain.time) < datetime.timedelta(hours = 24):
				rain_24h = rain_24h + rain.quantity
			if (rain.time > midnight):
				rain_today = rain_today + rain.quantity
		
		database.Table_Sensors.selectBy(int_id="Rain_Today").getOne().value = rain_today
		database.Table_Sensors.selectBy(int_id="Rain_24h").getOne().value = rain_24h
		database.Table_Sensors.selectBy(int_id="Rain_week").getOne().value = rain_week
		
		logging.getLogger("thread-rain_compile").info(" Compiled rain pulse data.")
	
	def check_db(self):
		database.database_verify_group("Rain", "Rain Info")
		database.database_verify_sensor("Rain_Since_Reset", "Rain Since Reset", "Rain", '', 'in')
		database.database_verify_sensor("Rain_Today", "Rain Since Midnight", "Rain", '', 'in')
		database.database_verify_sensor("Rain_24h", "Rain last 24 Hours", "Rain", '', 'in')
		database.database_verify_sensor("Rain_week", "Rain This Week", "Rain", '', 'in')