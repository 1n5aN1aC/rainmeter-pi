#!python
import time, sys, signal, logging
from framework import update_sensors
from framework import update_sensor_rain
from framework import update_rain_compile
from framework import update_feels_like
from framework import update_archive
from framework import settings

#
# This File handles launching and running all the daemon threads 
# This includes:
#
# Thread to handle updating sensor readings
# Thread to handle simulating rain events
# Thread to compile rain into time averages
# Thread to update current conditions
# Thread to handle archiving
# Thread that cleans out old rain entries
#

threads = []
# Enable logging if wanted
if settings.enable_deamon_logging:
	logging.basicConfig(level=logging.INFO)

# Signal handler to properly close all DB handles
def signal_handler(signal, frame):
	logging.getLogger("core").warning(" Shutting down...")
	for thread in threads:
		thread.stop()
	time.sleep(settings.how_long_to_wait_before_killing_threads)
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Create the threads
logging.getLogger("core").info(" Launching the threads...")
threads.append( update_sensors.thread_sensors() )
threads.append( update_sensor_rain.thread_sensor_rain() )
threads.append( update_rain_compile.thread_rain_compile() )
threads.append( update_feels_like.thread_feels_like() )
threads.append( update_archive.thread_archive() )
threads.append( update_archive.thread_clean() )

# Loop to keep this thread alive
while 1:
	time.sleep(60)