#!python
import collections, logging, datetime

import Now

import database
import settings

#
# This File Handles saving reading read elsewhere (mostly thread_sensors.py)
# It handles relatively advanced dequeues, which are essentially a ring buffer
# This is used to provide a slight averaging to temperature and humidity thread_sensors,
# as well as handling gusts and averaging for the wind sensor.
#

# Create the dequeues
# These are dictionaries which contain the Q, consecutive fail count, and a debug name.
IN_Temp_Q =   {"Q":collections.deque(maxlen=settings.Temp_Average_Length),  "Fails":0, "Name":'IN_Temp'}
IN_Humid_Q =  {"Q":collections.deque(maxlen=settings.Humid_Average_Length), "Fails":0, "Name":'IN_Humid'}
OUT_Temp_Q =  {"Q":collections.deque(maxlen=settings.Temp_Average_Length),  "Fails":0, "Name":'OUT_Temp'}
OUT_Humid_Q = {"Q":collections.deque(maxlen=settings.Humid_Average_Length), "Fails":0, "Name":'OUT_Humid'}
ATT_Temp_Q =  {"Q":collections.deque(maxlen=settings.Temp_Average_Length),  "Fails":0, "Name":'ATT_Temp'}
ATT_Humid_Q = {"Q":collections.deque(maxlen=settings.Humid_Average_Length), "Fails":0, "Name":'ATT_Humid'}
Wind_Avg_Q =  {"Q":collections.deque(maxlen=settings.Wind_Average_Length),  "Fails":0, "Name":'Wind_Avg'}
Wind_Max_Q =  {"Q":collections.deque(maxlen=settings.Wind_Max_Length),      "Fails":0, "Name":'Wind_Max'}

#
# This Handles saving the data when the rain gauge tips.
# If you want to know more, have a look at README-ADVANCED.txt
def trigger_sensor_rain():
    #Add this to the rain table
    now = database.Table_Rain(quantity=settings.rainTipAmount, time=datetime.datetime.now())
    
    #Now update the now table
    now = Now.get(1)
    now.Out_Rain_Since_Reset = now.Out_Rain_Since_Reset + settings.rainTipAmount
    logging.getLogger("thread-rain").info(" rain bucket tipped.")

#
def save_wind_reading(wind_speed):
    add_reading_to_dequeue(Wind_Avg_Q, wind_speed)
    add_reading_to_dequeue(Wind_Max_Q, wind_speed)
    
    now = Now.get(1)
    now.Out_Wind_Avg = sum(Wind_Avg_Q['Q']) / float(len(Wind_Avg_Q['Q']))
    now.Out_Wind_Max = max(Wind_Max_Q['Q'])

# 
def save_inside_reading(temp, humid):
    add_reading_to_dequeue(IN_Temp_Q, temp)
    add_reading_to_dequeue(IN_Humid_Q, humid)
    
    now = Now.get(1)
    now.In_Temp = sum(IN_Temp_Q['Q']) / float(len(IN_Temp_Q['Q']))
    now.In_Humid = sum(IN_Humid_Q['Q']) / float(len(IN_Humid_Q['Q']))
    
    logging.getLogger("sensor").debug(" Updated inside sensor data.")

# 
def save_attic_reading(temp, humid):
    add_reading_to_dequeue(ATT_Temp_Q, temp)
    add_reading_to_dequeue(ATT_Humid_Q, humid)
    
    now = Now.get(1)
    now.Attic_Temp = sum(ATT_Temp_Q['Q']) / float(len(ATT_Temp_Q['Q']))
    now.Attic_Humid = sum(ATT_Humid_Q['Q']) / float(len(ATT_Humid_Q['Q']))
    
    logging.getLogger("sensor").debug(" Updated attic sensor data.")

# 
def save_outside_reading(temp, humid):
    add_reading_to_dequeue(OUT_Temp_Q, temp)
    add_reading_to_dequeue(OUT_Humid_Q, humid)
    
    now = Now.get()
    
    now.Out_Temp = sum(OUT_Temp_Q['Q']) / float(len(OUT_Temp_Q['Q']))
    now.Out_Humid = sum(OUT_Humid_Q['Q']) / float(len(OUT_Humid_Q['Q']))
    
    logging.getLogger("sensor").debug(" Updated outside sensor data.")

# 
def save_system_reading(cpu, ram):
    now = Now.get(1)
    now.System_CPU = cpu
    now.System_RAM = ram
    
    logging.getLogger("sensor").debug(" Updated SYSTEM data.")

# This takes a dequeue & reading, then adds that reading to the dequeue.
# It also handles checking for update failures, and not including them when applicable.
def add_reading_to_dequeue(dequeue, new_reading):
    if new_reading is not None:
        dequeue['Q'].append(new_reading)
        (dequeue)['Fails'] = 0
    elif dequeue['Fails'] < settings.failed_readings_before_error:
        if len(dequeue['Q']) is 0:
            dequeue['Q'].append(1)
        dequeue['Fails'] = dequeue['Fails'] + 1
        logging.getLogger("thread_sensors").warning(" Failed to update sensor " + dequeue['Name'] + ".")
    else:
        dequeue['Q'].append(0)
        logging.getLogger("thread_sensors").error(" Sensor has failed: " + dequeue['Name'] + "!!")