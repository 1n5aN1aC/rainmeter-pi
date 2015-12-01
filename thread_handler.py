#!python
import threading, time, signal, sys, random
from framework import database
from framework import update_sensor_temp
from framework import update_sensor_rain
from framework import update_rain_compile
from framework import update_feels_like
from framework import update_archive

#
# This File handles launching and running all the deamon threads 
# This includes:
#
# Thread to handle updating sensor readings
# Thread to handle simulating rain events
# Thread to compile rain into time averages
# Thread to update current conditions
# Thread to handle archiving
#

#We change this to False to kill all the threads 'gracefully'.
run = True
threads = []


# Thread to handle updating sensor readings
def thread_sensor_temp():
	db = database.getDB()
	while run:
		update_sensor_temp.update_sensor_temp(db)
		time.sleep(5)
	db.close()

# Thread to handle simulating rain events
def thread_sensor_rain():
	db = database.getDB()
	while run:
		update_sensor_rain.update_sensor_rain(db)
		time.sleep( random.randint(1, 240) )
	db.close()

# Thread to compile rain into time averages
def thread_rain_compile():
	db = database.getDB()
	while run:
		update_rain_compile.update_rain_compile(db)
		time.sleep(59)
	db.close()

# Thread to update current conditions
def thread_feels_like():
	db = database.getDB()
	while run:
		update_feels_like.update_feels_like(db)
		time.sleep(600)
	db.close()

# Thread to handle archiving
def thread_archive():
	db = database.getDB()
	while run:
		update_archive.update_archive(db)
		time.sleep(60)
	db.close()

# Signal handler to properly close all DB handles
def signal_handler(signal, frame):
	global run
	print('Closing...')
	run = False
	time.sleep(5)
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Create the threads
t = threading.Thread(target=thread_sensor_temp)
threads.append(t)
t = threading.Thread(target=thread_sensor_rain)
threads.append(t)
t = threading.Thread(target=thread_rain_compile)
threads.append(t)
t = threading.Thread(target=thread_feels_like)
threads.append(t)
t = threading.Thread(target=thread_archive)
threads.append(t)

# Start the threads
for thread in threads:
	thread.daemon = True
	thread.start()

# Loop to keep this thread alive
while 1:
	time.sleep(60)