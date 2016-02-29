#!python
import logging, datetime

import Now

import database
import settings

#
# This Handles saving the data when the rain gauge tips.
# It saves a record to the rain table.  If you want to know
# How the rain sub-system works, have a look at README-ADVANCED.txt
def update_sensor_rain():
	#Add this to the rain table
	now = database.Table_Rain(quantity=settings.rainTipAmount, time=datetime.datetime.now())
	
	#Now update the now table
	now = Now.get(1)
	now.Out_Rain_Since_Reset = now.Out_Rain_Since_Reset + settings.rainTipAmount
	logging.getLogger("thread-rain").info(" rain bucket tipped.")