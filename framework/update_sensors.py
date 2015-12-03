#!python
import collections, logging
from database import *
from settings import *
import sensors

#
# This File Handles reading the actual Temperature and Humidity Sensors.
# It handles relatively advanced dequeues, which are essentually a ring buffer
# This is used to provide a slight averaging to temperature and humidity sensors,
# as well as handeling gusts and averaging for the wind sensor.
#

# Create the dequeues
IN_Temp_Q = ["Q" = collections.deque(maxlen=Temp_Average_Length), "Fails" = 0]
IN_Humid_Q = ["Q" = collections.deque(maxlen=Humid_Average_Length), "Fails" = 0]
OUT_Temp_Q = ["Q" = collections.deque(maxlen=Temp_Average_Length), "Fails" = 0]
OUT_Humid_Q = ["Q" = collections.deque(maxlen=Humid_Average_Length), "Fails" = 0]
ATT_Temp_Q = ["Q" = collections.deque(maxlen=Temp_Average_Length), "Fails" = 0]
ATT_Humid_Q = ["Q" = collections.deque(maxlen=Humid_Average_Length), "Fails" = 0]
Wind_Q = ["Q" = collections.deque(maxlen=Wind_Average_Length), "Fails" = 0]

# This reads and updates each sensor
def read_all_sensors():
	temp_inside, humid_inside = sensors.read_inside_sensor()
	temp_outside, humid_outside = sensors.read_outside_sensor()
	temp_attic, humid_attic = sensors.read_attic_sensor()

	add_reading_to_dequeue(IN_Temp_Q, temp_inside)
	add_reading_to_dequeue(OUT_Temp_Q, temp_outside)
	add_reading_to_dequeue(ATT_Temp_Q, temp_attic)
	add_reading_to_dequeue(IN_Humid_Q, humid_inside)
	add_reading_to_dequeue(OUT_Humid_Q, humid_outside)
	add_reading_to_dequeue(ATT_Humid_Q, humid_attic)
	add_reading_to_dequeue(Wind_Q, sensors.read_wind_outside() )

# Updates all non-special sensors
def update_sensors(db):
	cursor = db.cursor()

	#Read the sensors; store in dequeue
	read_all_sensors()
	
	#commit the averages of the dequeues to the db
	query = "UPDATE `now` SET `IN_Temp`=%s, `IN_Humid`=%s, `OUT_Temp`=%s, `OUT_Humid`=%s, `ATTIC_Temp`=%s, `ATTIC_Humid`=%s, `OUT_Wind_Avg`=%s, `OUT_Wind_Max`=%s, `SYSTEM_CPU`=%s, `SYSTEM_RAM`=%s"
	cursor.execute(query, [
			sum(IN_Temp_Q)['Q'] / float(len(IN_Temp_Q)['Q'] ), 
			sum(IN_Humid_Q)['Q'] / float(len(IN_Humid_Q)['Q'] ), 
			sum(OUT_Temp_Q)['Q'] / float(len(OUT_Temp_Q)['Q'] ), 
			sum(OUT_Humid_Q)['Q'] / float(len(OUT_Humid_Q)['Q'] ), 
			sum(ATT_Temp_Q)['Q'] / float(len(ATT_Temp_Q)['Q'] ), 
			sum(ATT_Humid_Q)['Q'] / float(len(ATT_Humid_Q)['Q'] ), 
			sum(Wind_Q)['Q'] / float(len(Wind_Q)['Q']), 
			max(Wind_Q)['Q'],
			sensors.read_cpu_usage(),
			sensors.read_ram_usage() ])
	db.commit()
	logging.getLogger("thread_sensors").info(" Updated Sensor Data.")

def add_reading_to_dequeue(dequeue, new_reading) {
	if new_reading is not None:
		dequeue['Q'].append(new_reading)
		(dequeue)['Fails'] = 0
	else if dequeue['Fails'] < failed_readings_before_error:
		dequeue['Fails'] = dequeue['Fails'] + 1
		logging.getLogger("thread_sensors").warning(" Failed to update Sensor." + )
	else:
		dequeue['Q'].append(0)
		logging.getLogger("thread_sensors").error(" Sensor has Failed!!" + )
}