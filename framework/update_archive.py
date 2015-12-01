#!python
import json
from database import *

#
# This File Handles archiving the current weather data
# to a long-term table to keep FOREVER!
# We run this once a minute so we can save minute-by-minute data.
#
# This works out to a little over 500,000 records a year,
# Which makes it little enough to not be an issue assuming
# A mediocre-sized SD Card.
#

def update_archive(db):
	cursor = db.cursor()

	# Now get all the Current Data
	query = "SELECT `ref`, `IN_Temp`, `IN_Humid`, `OUT_Temp`, `OUT_Humid`, `OUT_Wind_Avg`, `OUT_Wind_Max`, `OUT_Rain_Today`, `OUT_Rain_Last_24h`, `OUT_Rain_Since_Reset`, `ATTIC_Temp`, `ATTIC_Humid`, `NOW_URL`, `NOW_Feel` FROM `now` WHERE 1"
	cursor.execute(query)
	result = cursor.fetchone()

	# Parse the data out of the results...
	data = {}
	data["IN_Temp"] = result[1]
	data["IN_Humid"] = result[2]
	data["OUT_Temp"] = result[3]
	data["OUT_Humid"] = result[4]
	data["OUT_Wind_Avg"] = result[5]
	data["OUT_Wind_Max"] = result[6]
	data["OUT_Rain_Today"] = result[7]
	data["OUT_Rain_Last_24h"] = result[8]
	data["OUT_Rain_Since_Reset"] = result[9]
	data["ATTIC_Temp"] = result[10]
	data["ATTIC_Humid"] = result[11]
	data["NOW_Feel"] = result[13]

	# Insert all values besides the rain into the archive table.
	query = "INSERT INTO `archive` (`IN_Temp`, `IN_Humid`, `OUT_Temp`, `OUT_Humid`, `OUT_Wind_Avg`, `OUT_Wind_Max`, `OUT_Rain_Minute`, `ATTIC_Temp`, `ATTIC_Humid`, `NOW_Feel`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	cursor.execute(query, [data["IN_Temp"], data["IN_Humid"], data["OUT_Temp"], data["OUT_Humid"], data["OUT_Wind_Avg"], data["OUT_Wind_Max"], 0, data["ATTIC_Temp"], data["ATTIC_Humid"], data["NOW_Feel"]] )
	db.commit()

	# Now update the latest archive entry to the total rainfall over the last minute.
	# Bit of a hack, but meh, it works.  :)
	query = "UPDATE `archive` SET `OUT_Rain_Minute` = ( SELECT sum(`quantity`) as RainResult FROM `rain` WHERE (`time` >= now() - interval 1 minute) ) ORDER BY `count` DESC LIMIT 1"
	cursor.execute(query)
	db.commit()

def update_clean_old():
	print "lol"