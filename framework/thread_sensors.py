#!python
from __future__ import division
import psutil, time, logging

from framework import Stoppable_Thread

import Adafruit_DHT
import serial

import settings
import update_sensors

#
# This file handles actually reading and returning any sensor data to the other modules
# If you have any specific sensors that are different than my setup, this is where they
# Should be changed.  If you use DHTxx or AM2302 sensors, this should be very easy.
#

# Manages the various sensor threads
class thread_sensors(Stoppable_Thread.Stoppable_Thread):
    def run(self):
        #Create the threads
        sensor_threads = []
        sensor_threads.append( update_inside() )
        sensor_threads.append( update_attic() )
        sensor_threads.append( update_serial() )
        sensor_threads.append( update_system() )
        
        #Wait until this thread is told to stop...
        while self.RUN:
            time.sleep(1)
        
        #Then tell deamon threads to die, and reap their souls
        logging.getLogger("thread-thread_sensors").info(" Telling sensor threads to die...")
        for thread in sensor_threads:
            thread.stop()
        for thread in sensor_threads:
            thread.join(settings.how_long_to_wait_before_killing_deamons)
        logging.getLogger("thread-thread_sensors").debug(" Sensor threads have been killed!")

# Thread for updating all serial sensors
# This is the wind sensor and the rain sensor
class update_serial(Stoppable_Thread.Stoppable_Thread):
    def run(self):
        ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=10)
        if (ser.isOpen() == False):
            ser.open()
        
        while self.RUN:
            line = ser.readline(),
            if "RAIN" in line[0]:
                update_sensors.trigger_sensor_rain()
            elif "OUT" in line[0]:
                try:
                    list = line[0].split(":")
                    temp  = float(list[1])
                    humid = float(list[2])
                    update_sensors.save_outside_reading(temp, humid)
                    logging.getLogger("sensor").debug(" Updated outside sensor data.")
                except Exception:
                    logging.getLogger("serial").warning(" got malformed serial temperature info!")
            elif "bat" in line[0]:
                try:
                    list = line[0].split(":")
                    number = float(list[1]) / 1000
                    #print "handle battery here:", number, "V"
                except Exception:
                    pass
            else:
                try:
                    number = int(line[0])
                    update_sensors.save_wind_reading(number)
                    logging.getLogger("sensor").debug(" Updated wind data.")
                except Exception:
                    logging.getLogger("serial").warning(" got malformed serial info!")
            #No sleep, as this is handled by waiting on the serial connection

# Thread for updating the inside T/H sensor
class update_inside(Stoppable_Thread.Stoppable_Thread):
    def run(self):
        while self.RUN:
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 19, retries=3, delay_seconds=1)
            if temperature and settings.fahrenheit:
                temperature = temperature * 9/5.0 + 32
            
            update_sensors.save_inside_reading(temperature, humidity)
            time.sleep(settings.how_often_to_check_temp)

# Thread for updating the attic T/H sensor
class update_attic(Stoppable_Thread.Stoppable_Thread):
    def run(self):
        while self.RUN:
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 20, retries=3, delay_seconds=1)
            if temperature and settings.fahrenheit:
                temperature = temperature * 9/5.0 + 32 + 1
            
            update_sensors.save_attic_reading(temperature, humidity)
            time.sleep(settings.how_often_to_check_temp)

# Thread for updating the system statistics
class update_system(Stoppable_Thread.Stoppable_Thread):
    def run(self):
        while self.RUN:
            cpu = psutil.cpu_percent(interval=None)
            ram = (psutil.virtual_memory()[0] - psutil.virtual_memory()[1]) / psutil.virtual_memory()[0] * 100
            
            update_sensors.save_system_reading(cpu, ram)
            time.sleep(settings.how_often_to_check_system)