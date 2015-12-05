#!python
import logging
from database import *

#
# This File Handles saving the data when the rain guage tips.
# This saves a record to the rain table.  If you want to know
# How the rain sub-system works, have a look at README-ADVANCED.txt
#

def update_sensor_rain():
	#Add this to the rain table
	now = Table_Rain(quantity=rainTipAmount, time=datetime.datetime.now())
	
	#Now update the now table
	now = Table_Now.get(1)
	now.Out_Rain_Since_Reset = now.Out_Rain_Since_Reset + rainTipAmount
	logging.getLogger("thread_rainSimulator").info(" Caused A Fake Rain Pulse.")