#!python
import logging, random, time

from Stoppable_Thread import *
import Now

from database import *

#
# This Handles saving the data when the rain guage tips.
# It saves a record to the rain table.  If you want to know
# How the rain sub-system works, have a look at README-ADVANCED.txt
class thread_sensor_rain(Stoppable_Thread):
	def run(self):
		while self.RUN:
			self.update_sensor_rain()
			time.sleep( random.randint(1, 240) )

	def update_sensor_rain(self):
		#Add this to the rain table
		now = Table_Rain(quantity=rainTipAmount, time=datetime.datetime.now())
		
		#Now update the now table
		now = Now.get(1)
		now.Out_Rain_Since_Reset = now.Out_Rain_Since_Reset + rainTipAmount
		logging.getLogger("thread-rain_fake").info(" Caused a fake rain pulse.")