#!python
import random, time
from database import *

#
# This File Handles reading the actual Temperature and Humidity Sensors.
# This happens Reletively often, and then the data is updated in the current table.
#

# For now, this makes up fake sensor data
# This helps with testing the GUI Design
def readSensor():
	return random.uniform(-20, 130)

# Same as above.
def readWind():
	return random.uniform(0, 40)

# Connect to the Database
db = getDB()
cursor = db.cursor()

# Keep updating the data on a loop
while 1:
	query = "UPDATE `now` SET `IN_Temp`=%s, `IN_Humid`=%s, `OUT_Temp`=%s, `OUT_Humid`=%s, `ATTIC_Temp`=%s, `ATTIC_Humid`=%s, `OUT_Wind_Avg`=%s, `OUT_Wind_Max`=%s"
	cursor.execute(query, [readSensor(), readSensor(), readSensor(), readSensor(), readSensor(), readSensor(), readWind(), readWind()] )
	db.commit()
	time.sleep(4)

# Close DB when done.
db.close()