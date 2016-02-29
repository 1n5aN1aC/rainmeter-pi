#!python
import collections, logging, time

import Stoppable_Thread
import Now

import settings
import sensors

#
# This File Handles reading the actual Temperature and Humidity Sensors.
# It handles relatively advanced dequeues, which are essentually a ring buffer
# This is used to provide a slight averaging to temperature and humidity sensors,
# as well as handeling gusts and averaging for the wind sensor.
#

# Create the dequeues
# These are dictionaries which contain the Q, consecutive fail count, and a debug name.
IN_Temp_Q = {"Q":collections.deque(maxlen=settings.Temp_Average_Length), "Fails":0, "Name":'IN_Temp'}
IN_Humid_Q = {"Q":collections.deque(maxlen=settings.Humid_Average_Length), "Fails":0, "Name":'IN_Humid'}
OUT_Temp_Q = {"Q":collections.deque(maxlen=settings.Temp_Average_Length), "Fails":0, "Name":'OUT_Temp'}
OUT_Humid_Q = {"Q":collections.deque(maxlen=settings.Humid_Average_Length), "Fails":0, "Name":'OUT_Humid'}
ATT_Temp_Q = {"Q":collections.deque(maxlen=settings.Temp_Average_Length), "Fails":0, "Name":'ATT_Temp'}
ATT_Humid_Q = {"Q":collections.deque(maxlen=settings.Humid_Average_Length), "Fails":0, "Name":'ATT_Humid'}
Wind_Avg_Q = {"Q":collections.deque(maxlen=settings.Wind_Average_Length), "Fails":0, "Name":'Wind_Avg'}
Wind_Max_Q = {"Q":collections.deque(maxlen=int(60) ), "Fails":0, "Name":'Wind_Max'}

# Manages the various sensor threads
class thread_sensors(Stoppable_Thread):
	def run(self):
		#Create the threads
		sensor_threads = []
		sensor_threads.append( update_outside() )
		sensor_threads.append( update_attic() )
		sensor_threads.append( update_inside() )
		sensor_threads.append( update_wind() )
		sensor_threads.append( update_system() )
		
		#Wait until this thread is told to stop...
		while self.RUN:
			time.sleep(1)
		
		#Then tell deamon threads to die, and reap their souls
		logging.getLogger("thread-sensors").info(" Telling sensor threads to die...")
		for thread in sensor_threads:
			thread.stop()
		for thread in sensor_threads:
			thread.join(settings.how_long_to_wait_before_killing_deamons)
		logging.getLogger("thread-sensors").debug(" Sensor threads have been killed!")

# Thread for updating the wind sensor
class update_wind(Stoppable_Thread):
	def run(self):
		while self.RUN:
			wind_speed = sensors.read_wind_outside()
			
			add_reading_to_dequeue(Wind_Avg_Q, wind_speed)
			add_reading_to_dequeue(Wind_Max_Q, wind_speed)
			
			now = Now.get(1)
			now.Out_Wind_Avg = sum(Wind_Avg_Q['Q']) / float(len(Wind_Avg_Q['Q']))
			now.Out_Wind_Max = max(Wind_Max_Q['Q'])
			
			logging.getLogger("sensor").debug(" Updated wind data.")
			time.sleep(settings.how_often_to_check_wind)

# Thread for updating the outside T/H sensor
class update_outside(Stoppable_Thread):
	def run(self):
		while self.RUN:
			temp_outside, humid_outside = sensors.read_outside_sensor()
			add_reading_to_dequeue(OUT_Temp_Q, temp_outside)
			add_reading_to_dequeue(OUT_Humid_Q, humid_outside)
			
			now = Now.get(1)
			now.Out_Temp = sum(OUT_Temp_Q['Q']) / float(len(OUT_Temp_Q['Q']))
			now.Out_Humid = sum(OUT_Humid_Q['Q']) / float(len(OUT_Humid_Q['Q']))
			
			logging.getLogger("sensor").debug(" Updated outside sensor data.")
			time.sleep(settings.how_often_to_check_temp)

# Thread for updating the attic T/H sensor
class update_attic(Stoppable_Thread):
	def run(self):
		while self.RUN:
			temp_attic, humid_attic = sensors.read_attic_sensor()
			add_reading_to_dequeue(ATT_Temp_Q, temp_attic)
			add_reading_to_dequeue(ATT_Humid_Q, humid_attic)
			
			now = Now.get(1)
			now.Attic_Temp = sum(ATT_Temp_Q['Q']) / float(len(ATT_Temp_Q['Q']))
			now.Attic_Humid = sum(ATT_Humid_Q['Q']) / float(len(ATT_Humid_Q['Q']))
			
			logging.getLogger("sensor").debug(" Updated attic sensor data.")
			time.sleep(settings.how_often_to_check_temp)

# Thread for updating the inside T/H sensor
class update_inside(Stoppable_Thread):
	def run(self):
		while self.RUN:
			temp_inside, humid_inside = sensors.read_inside_sensor()
			add_reading_to_dequeue(IN_Temp_Q, temp_inside)
			add_reading_to_dequeue(IN_Humid_Q, humid_inside)
			
			now = Now.get(1)
			now.In_Temp = sum(IN_Temp_Q['Q']) / float(len(IN_Temp_Q['Q']))
			now.In_Humid = sum(IN_Humid_Q['Q']) / float(len(IN_Humid_Q['Q']))
			
			logging.getLogger("sensor").debug(" Updated inside sensor data.")
			time.sleep(settings.how_often_to_check_temp)

# Thread for updating the system stats
class update_system(Stoppable_Thread):
	def run(self):
		while self.RUN:
			now = Now.get(1)
			now.System_CPU = sensors.read_cpu_usage()
			now.System_RAM = sensors.read_ram_usage()
			
			logging.getLogger("sensor").debug(" Updated SYSTEM data.")
			time.sleep(settings.how_often_to_check_system)

# This takes a dequeue, and a reading, and adds that reading to the dequeue.
# It also handles checking for update failures, and not including them when applicable.
def add_reading_to_dequeue(dequeue, new_reading):
	if new_reading is not None:
		dequeue['Q'].append(new_reading)
		(dequeue)['Fails'] = 0
	elif dequeue['Fails'] < settings.failed_readings_before_error:
		dequeue['Fails'] = dequeue['Fails'] + 1
		logging.getLogger("thread_sensors").warning(" Failed to update sensor " + dequeue['Name'] + ".")
	else:
		dequeue['Q'].append(0)
		logging.getLogger("thread_sensors").error(" Sensor has failed: " + dequeue['Name'] + "!!")