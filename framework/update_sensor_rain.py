#!python
import logging
from database import *

#
# This File Handles saving the data when the rain guage tips.
# This saves a record to the rain table.  If you want to know
# How the rain sub-system works, have a look at README-ADVANCED.txt
#

#####################################
rainTipAmount = "0.02"
#####################################

def update_sensor_rain(db):
	cursor = db.cursor()
	
	query = "INSERT INTO `rain`(`quantity`) VALUES (%s)"
	cursor.execute(query, [rainTipAmount] )
	db.commit()
	
	query = "UPDATE `now` SET `OUT_Rain_Since_Reset` = `OUT_Rain_Since_Reset` + %s"
	cursor.execute(query, [rainTipAmount] )
	db.commit()
	logging.getLogger("thread_rainSimulator").info(" Caused A Fake Rain Pulse.")