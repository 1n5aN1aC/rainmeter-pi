#!python
import collections, logging
from database import *
import sensors

#
# This File Handles reading the actual Temperature and Humidity Sensors.
# It handles relatively advanced dequeues, which are essentually a ring buffer
# This is used to provide a slight averaging to temperature and humidity sensors,
# as well as handeling gusts and averaging for the wind sensor.
#

#####################################
Temp_Average_Length = 10
Humid_Average_Length = 15
Wind_Average_Length = 10
#####################################

# Create the dequeues
IN_Temp_Q = collections.deque(maxlen=Temp_Average_Length)
IN_Humid_Q = collections.deque(maxlen=Humid_Average_Length)
OUT_Temp_Q = collections.deque(maxlen=Temp_Average_Length)
OUT_Humid_Q = collections.deque(maxlen=Humid_Average_Length)
ATT_Temp_Q = collections.deque(maxlen=Temp_Average_Length)
ATT_Humid_Q = collections.deque(maxlen=Humid_Average_Length)
Wind_Q = collections.deque(maxlen=Wind_Average_Length)

# This reads and updates each sensor
def read_all_sensors():
	IN_Temp_Q.append( sensors.read_temp_inside() )
	OUT_Temp_Q.append( sensors.read_temp_outside() )
	ATT_Temp_Q.append( sensors.read_temp_attic() )
	IN_Humid_Q.append( sensors.read_humid_inside() )
	OUT_Humid_Q.append( sensors.read_humid_outside() )
	ATT_Humid_Q.append( sensors.read_humid_attic() )
	Wind_Q.append( sensors.read_wind_outside() )

def update_sensor_temp(db):
	cursor = db.cursor()

	#Read the sensors; store in dequeue
	read_all_sensors()
	
	#commit the averages of the dequeues to the db
	query = "UPDATE `now` SET `IN_Temp`=%s, `IN_Humid`=%s, `OUT_Temp`=%s, `OUT_Humid`=%s, `ATTIC_Temp`=%s, `ATTIC_Humid`=%s, `OUT_Wind_Avg`=%s, `OUT_Wind_Max`=%s"
	cursor.execute(query, [
			sum(IN_Temp_Q) / float(len(IN_Temp_Q)), 
			sum(IN_Humid_Q) / float(len(IN_Humid_Q)), 
			sum(OUT_Temp_Q) / float(len(OUT_Temp_Q)), 
			sum(OUT_Humid_Q) / float(len(OUT_Humid_Q)), 
			sum(ATT_Temp_Q) / float(len(ATT_Temp_Q)), 
			sum(ATT_Humid_Q) / float(len(ATT_Humid_Q)), 
			sum(Wind_Q) / float(len(Wind_Q)), 
			max(Wind_Q) ])
	db.commit()
	logging.getLogger("thread_sensors").info(" Updated Sensor Data.")