#!python
import urllib2, json
from database import *

#
# This File Handles compiling the raw rain data, which is tip-time based
# to the format which you see on the main screen (last day, last 24h, since reset.)
# If you want to know how the rain sub-system works, have a look at README-ADVANCED.txt
#

def update_rain_compile(db):
	# Connect to the Database
	cursor = db.cursor()
	
	# Get Last 24 Hours
	cursor.execute("SELECT sum(`quantity`) FROM `rain` WHERE (`time` >= now() - interval 1 day)")
	last24 = cursor.fetchone()

	#Get Since midnight
	cursor.execute("SELECT sum(`quantity`)FROM `rain` WHERE (`time` >= current_date)")
	sinceMidnight = cursor.fetchone()
	if not sinceMidnight:
		sinceMidnight = 0

	query = "UPDATE `now` SET `OUT_Rain_Today`=%s, `OUT_Rain_Last_24h`=%s"
	cursor.execute(query, [sinceMidnight[0], last24[0]] )
	db.commit()