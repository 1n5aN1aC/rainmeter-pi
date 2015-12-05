#!python
import time, sys, signal, random
import threading, logging
from framework import database
from framework import update_sensors
from framework import update_sensor_rain
from framework import update_rain_compile
from framework import update_feels_like
from framework import update_archive
from framework import settings

#
# This File handles launching and running all the deamon threads 
# This includes:
#
# Thread to handle updating sensor readings
# Thread to handle simulating rain events
# Thread to compile rain into time averages
# Thread to update current conditions
# Thread to handle archiving
# Thread that cleans out old rain entries
#

if settings.enable_deamon_logging:
	logging.basicConfig(level=logging.INFO)
# We change this to False to kill all the threads 'gracefully'.
run = True

# Thread to handle updating sensor readings
def thread_sensors():
	while run:
		update_sensors.update_sensors()
		time.sleep(settings.how_often_to_check_sensors)

# Thread to handle simulating rain events
def thread_sensor_rain():
	while run:
		update_sensor_rain.update_sensor_rain()
		time.sleep( random.randint(1, 240) )

# Thread to compile rain into time averages
def thread_rain_compile():
	while run:
		update_rain_compile.update_rain_compile()
		time.sleep(settings.how_often_to_compile_rain)

# Thread to update current conditions
def thread_feels_like():
	while run:
		update_feels_like.update_feels_like()
		time.sleep(settings.how_often_to_update_feels_like)

# Thread to handle archiving
def thread_archive():
	while run:
		update_archive.update_archive()
		time.sleep(settings.how_often_to_archive_data)

# Thread that cleans out old rain entries
def thread_clean():
	while run:
		update_archive.update_clean_old()
		time.sleep(settings.how_often_to_clean_rain_db)

# Signal handler to properly close all DB handles
def signal_handler(signal, frame):
	global run
	print('Closing...')
	run = False
	time.sleep(settings.how_long_to_wait_before_killing_deamons)
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Create the threads
threads = []
t = threading.Thread(target=thread_sensors)
threads.append(t)
t = threading.Thread(target=thread_sensor_rain)
threads.append(t)
t = threading.Thread(target=thread_rain_compile)
threads.append(t)
t = threading.Thread(target=thread_feels_like)
threads.append(t)
t = threading.Thread(target=thread_archive)
threads.append(t)
t = threading.Thread(target=thread_clean)
threads.append(t)

# Start the threads
for thread in threads:
	thread.daemon = True
	thread.start()

# Loop to keep this thread alive
while 1:
	time.sleep(60)