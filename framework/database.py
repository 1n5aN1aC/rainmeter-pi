#!python
import sqlobject

import settings

# The database connection for all threads
connection = None

# Returns a reference to the db connection.
def getDB():
    global connection
    if connection is not None:
        return connection

    connection = sqlobject.connectionForURI(settings.Connection_String)
    return connection

# Connect!
getDB()
# Makes all classes use this connection by default
sqlobject.sqlhub.processConnection = connection

# This table stores every instance of a rain_tip_event
# From the last week, and the precise time.
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
    System_CPU = sqlobject.FloatCol()
    System_RAM = sqlobject.FloatCol()
    Now_Feel = sqlobject.FloatCol()
Table_Archive.createTable(ifNotExists = True)