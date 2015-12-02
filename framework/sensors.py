#!python
import random

#####################################

#####################################

def read_temp_inside():
	return fakeSensor()

def read_temp_outside():
	return fakeSensor()

def read_temp_attic():
	return fakeSensor()

def read_humid_inside():
	return fakeSensor()

def read_humid_outside():
	return fakeSensor()

def read_humid_attic():
	return fakeSensor()

def read_wind_outside():
	return fakeWind()

# For now, this makes up fake sensor data
# This helps with testing the GUI Design
def fakeSensor():
	return random.uniform(-20, 130)
def fakeWind():
	return random.uniform(0, 70)