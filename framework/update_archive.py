#!python
import json, logging, time
from database import *
from settings import *

#
# This File Handles archiving tasks to copy current weather data to a long-term table to keep FOREVER!
#
# 1/Minute works out to a little over 500,000 records a year,
# Which makes it little enough to not be an issue assuming a mediocre-sized SD Card.
#

# This archives the current 'now' data to an archive table for long-term storage.
def update_archive():
	#Now get all the Current Data
	now = Table_Now.get(1)
	
	#Get the amount of rain in the last period
	rain_amount = 0.0
	rains = Table_Rain.select()
	for rain in rains:
		if (datetime.datetime.now() - rain.time) > datetime.timedelta(seconds = how_often_to_archive_data):
			rain_amount = rain_amount + rain.quantity
	
	#Insert all values into the archive table.
	new_archive = Table_Archive(date=datetime.datetime.now(),
								In_Temp=now.In_Temp,
								Out_Temp=now.Out_Temp,
								Attic_Temp=now.Attic_Temp,
								In_Humid=now.In_Humid,
								Out_Humid=now.Out_Humid,
								Attic_Humid=now.Attic_Humid,
								Out_Wind_Avg=now.Out_Wind_Avg,
								Out_Wind_Max=now.Out_Wind_Max,
								Out_Rain_Minute=rain_amount,
								Now_Feel=now.Now_Feel)
	logging.getLogger("thread_archive").info(" Sensor Data Archived.")

# This deletes old rain data from the 'rain' table. This data is no longer needed,
# as it has already been logged to the archive table, and is too old to be used for display.
def update_clean_old():
	rains = Table_Rain.select()
	number_cleaned = 0
	start = time.time()
	for rain in rains:
		if (datetime.datetime.now() - rain.time) > datetime.timedelta(days = how_many_days_of_rain_data_to_keep):
			rain.destroySelf()
			number_cleaned = number_cleaned + 1
	logging.getLogger("thread_clean").info(" Rain Table Cleaned.  (" + str(number_cleaned) + " entries purged in " + str((time.time() - start)*1000) + "ms)")