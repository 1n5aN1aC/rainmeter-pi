#!python
from __future__ import division
import random, psutil

import Adafruit_DHT
import serial

import settings

#
# This file handles actually reading and returning any sensor data to the other modules
# If you have any specific sensors that are different than my setup, this is where they
# Should be changed.  If you use DHTxx or AM2302 sensors, this should be very easy.
#

# Read the DHTxx sensor located inside the house
def read_inside_sensor():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 19, retries=3, delay_seconds=1)
    if temperature and settings.fahrenheit:
        temperature = temperature * 9/5.0 + 32
    return temperature, humidity

# Read the DHTxx sensor located Outside the house
def read_outside_sensor():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 21, retries=3, delay_seconds=1)
    if temperature and settings.fahrenheit:
        temperature = temperature * 9/5.0 + 32
    return temperature, humidity

# Read the DHTxx sensor located in the attic, or other auxiliary location.
def read_attic_sensor():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 20, retries=3, delay_seconds=1)
    if temperature and settings.fahrenheit:
        temperature = temperature * 9/5.0 + 32
    return temperature, humidity

# returns the serial object for wind & rain
def get_serial():
    ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=2)
    if (ser.isOpen() == False):
        ser.open()
    return ser

# Read the current wind speed.
def read_wind_rain(serial_point):
    wind = 0
    rain = 0
    line = serial_point.readline(),
    if "RAIN" in line[0]:
        rain = settings.rainTipAmount
    try:
        number = int(line[0])
        wind = number
    finally:
        return wind, rain

# Check CPU Usage
def read_cpu_usage():
    return psutil.cpu_percent(interval=None)

# Check RAM Usage
def read_ram_usage():
    return (psutil.virtual_memory()[0] - psutil.virtual_memory()[1]) / psutil.virtual_memory()[0] * 100

# You can use this to make up fake sensor data
# This helps with testing the GUI Design
def fakeSensor():
    return random.uniform(-20, 130)
def fakeWind():
    return random.uniform(0, 70)