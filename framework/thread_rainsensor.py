#!python
import logging, random, time, datetime
import stoppable_thread, database, settings

#
# This Handles saving the data when the rain guage tips.
# It saves a record to the rain table.  If you want to know
# How the rain sub-system works, have a look at README-ADVANCED.txt
class thread_sensor_rain(stoppable_thread.stoppable_thread):
	def run(self):
		while self.RUN:
			self.update_sensor_rain()
			time.sleep( random.randint(1, 240) )
	
	def update_sensor_rain(self):
		#Add this to the rain table
		now = database.Table_Rain(quantity=settings.rainTipAmount, time=datetime.datetime.now())
		
		#Now update the main sensor
		sensor_rain = database.Table_Sensors.selectBy(int_id="Rain_Since_Reset").getOne()
		sensor_rain.sync()
		sensor_rain.value = sensor_rain.value + settings.rainTipAmount
		logging.getLogger("thread-rain_fake").info(" Caused a fake rain pulse.")