#!python
import random, time
from database import *
from weather import *

#
# This File Handles updating the 'feels-like' display.
# This is the small window in the top-right of the index page
# that show what the weather currently 'feels like.'
#

# Gets the Weather data from the internet.
def readNow():
	parsed_json = fetchWeather('conditions')
	closeURL()
	return parsed_json

# Connect to the Database
db = getDB()
cursor = db.cursor()

# Keep checking on a delayed loop
while 1:
	parsed_json = readNow()
	
	NOW_URL = parsed_json['current_observation']['icon_url']
	NOW_Feel = parsed_json['current_observation']['feelslike_f']
	
	query = "UPDATE `now` SET `NOW_URL`=%s, `NOW_Feel`=%s"
	cursor.execute(query, [NOW_URL, NOW_Feel] )
	db.commit()
	time.sleep(600)

# Close DB when done.
db.close()