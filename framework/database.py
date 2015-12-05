#!python
import time, sys, os, datetime
import sqlobject 
from settings import *

# The database connection for all threads
connection = None

# Returns a reference to the db connection.
def getDB():
	global connection
	if connection is not None:
		return connection

	connection = sqlobject.connectionForURI(Connection_String)
	return connection

# Connect!
getDB()
# Makes all classes use this connection by default
sqlobject.sqlhub.processConnection = connection

# This table stores the current weather data.
# It should have ONLY ONE entry in it.
class Table_Now(sqlobject.SQLObject):
	In_Temp = sqlobject.FloatCol()
	Out_Temp = sqlobject.FloatCol()
	Attic_Temp = sqlobject.FloatCol()
	In_Humid = sqlobject.FloatCol()
	Out_Humid = sqlobject.FloatCol()
	Attic_Humid = sqlobject.FloatCol()
	Out_Wind_Avg = sqlobject.FloatCol()
	Out_Wind_Max = sqlobject.FloatCol()
	Out_Rain_Today = sqlobject.FloatCol()
	Out_Rain_Last_24h = sqlobject.FloatCol()
	Out_Rain_Since_Reset = sqlobject.FloatCol()
	System_CPU = sqlobject.FloatCol()
	System_RAM = sqlobject.FloatCol()
	Now_URL = sqlobject.StringCol(length=255)
	Now_Feel = sqlobject.FloatCol()
Table_Now.createTable(ifNotExists = True)

# This table stores every instance of a rain_tip_event
# Fromt he last week, and the precise time.
class Table_Rain(sqlobject.SQLObject):
	time = sqlobject.DateTimeCol()
	quantity = sqlobject.FloatCol()
Table_Rain.createTable(ifNotExists = True)

# This table stores the up-to-the minute sensor data
# Every minute to an archive database for long-term logging.
class Table_Archive(sqlobject.SQLObject):
	date = sqlobject.DateTimeCol()
	In_Temp = sqlobject.FloatCol()
	Out_Temp = sqlobject.FloatCol()
	Attic_Temp = sqlobject.FloatCol()
	In_Humid = sqlobject.FloatCol()
	Out_Humid = sqlobject.FloatCol()
	Attic_Humid = sqlobject.FloatCol()
	Out_Wind_Avg = sqlobject.FloatCol()
	Out_Wind_Max = sqlobject.FloatCol()
	Out_Rain_Minute = sqlobject.FloatCol()
	Now_Feel = sqlobject.FloatCol()
Table_Archive.createTable(ifNotExists = True)

# This checks if there are any rows in the 'now' table.
# If there are none, it inserts one.
# If there is more than one, it crashes.
nows_found = 0;
nows = Table_Now.select()
for now in nows:
	nows_found = nows_found + 1
if nows_found is 0:
	now = Table_Now(In_Temp=0,
	Out_Temp=0,
	Attic_Temp=0,
	In_Humid=0,
	Out_Humid=0,
	Attic_Humid=0,
	Out_Wind_Avg=0,
	Out_Wind_Max=0,
	Out_Rain_Today=0,
	Out_Rain_Last_24h=0,
	Out_Rain_Since_Reset=0,
	System_CPU=0,
	System_RAM=0,
	Now_URL="/",
	Now_Feel=0)
elif nows_found > 1:
	sys.exit("Too many entries in the 'now' table!")