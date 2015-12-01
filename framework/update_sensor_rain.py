#!python
import random, time
from database import *

#
# This File Handles saving the data when the rain guage tips.
# This saves a record to the rain table.  If you want to know
# How the rain sub-system works, have a look at README-ADVANCED.txt
#

#####################################
rainTipAmount = "0.02"
#####################################

def simulateRain():
	return random.randint(1, 240)

# Connect to the Database
db = getDB()
cursor = db.cursor()

# Keep faking it on a loop
while 1:
	query = "INSERT INTO `rain`(`quantity`) VALUES (%s)"
	cursor.execute(query, [rainTipAmount] )
	db.commit()
	
	query = "UPDATE `now` SET `OUT_Rain_Since_Reset` = `OUT_Rain_Since_Reset` + %s"
	cursor.execute(query, [rainTipAmount] )
	db.commit()
	
	#We sleep for a random amount of time to simulate rain for testing
	time.sleep(simulateRain() )

# Close DB when done.
db.close()