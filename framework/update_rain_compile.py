#!python
import logging, pytz, time
from database import *
from settings import *
from stoppable_thread import *

#
# This Handles compiling the raw rain data, (which is time-of-tip based)
# to the format seen on the main screen (last day, last 24h, since reset.)
# If you want to know how the rain sub-system works, have a look at README-ADVANCED.txt
class thread_rain_compile(stoppable_thread):
	def run(self):
		while self.RUN:
			self.update_rain_compile()
			time.sleep(how_often_to_compile_rain)

	def update_rain_compile(self):
		rain_24h = 0.0
		rain_today = 0.0
		
		now = datetime.datetime.now()
		midnight = now.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone(my_timezone)).replace(hour=0,minute=0,second=0,microsecond=0).astimezone(pytz.UTC).replace(tzinfo=None)
		
		rains = Table_Rain.select()
		for rain in rains:
			if (now - rain.time) < datetime.timedelta(hours = 24):
				rain_24h = rain_24h + rain.quantity
			if (rain.time > midnight):
				rain_today = rain_today + rain.quantity
				
		now = Table_Now.get(1)
		now.Out_Rain_Last_24h = rain_24h
		now.Out_Rain_Today = rain_today
		
		logging.getLogger("thread_rainCompile").info(" Compiled Rain Data.")