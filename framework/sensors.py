#!python
from __future__ import division
import random, psutil
#import Adafruit_DHT, spidev

#
# This file handles actually reading and returning any sensor data to the other modules
# If you have any specific sensors that are different than my setup, this is where they
# Should be added or changed.  If you use DHTxx sensors, this should be very easy.
#

# Read the DHTxx sensor located inside the house
def read_inside_sensor():
	return fakeSensor(), fakeSensor()
	#humidity, temperature = Adafruit_DHT.read_retry(DHT_22, pin, retries=3, delay_seconds=1, platform=None)

# Read the DHTxx sensor located Outside the house
def read_outside_sensor():
	return fakeSensor(), fakeSensor()

# Read the DHTxx sensor located in the attic, or other auxiliary location.
def read_attic_sensor():
	return fakeSensor(), fakeSensor()

# Read the current wind speed.
def read_wind_outside():
	return fakeWind()
	#spi = spidev.SpiDev()
	#spi.open(0,0)
	#adc = spi.xfer2( [1,( 8+channel ) << 4,0] )
	#data = ( (adc[1] & 3) << 8) + adc[2]
	#return data * math

# Check CPU Usage
def read_cpu_usage():
	return psutil.cpu_percent(interval=None)

# Check RAM Usage
def read_ram_usage():
	return (psutil.virtual_memory()[0] - psutil.virtual_memory()[1]) / psutil.virtual_memory()[0] * 100

# For now, this makes up fake sensor data
# This helps with testing the GUI Design
def fakeSensor():
	return random.uniform(-20, 130)
def fakeWind():
	return random.uniform(0, 70)