#!python
# -*- coding: UTF-8 -*-
import time, sys, os, datetime, logging
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

# This table contains each "grouping" of sensors
class Table_Groups(sqlobject.SQLObject):
	int_id = sqlobject.StringCol(length=32)
	name = sqlobject.StringCol(length=64)
	sensors = sqlobject.MultipleJoin("Table_Sensors", joinColumn="id")
	sort_order = sqlobject.IntCol()
	visable = sqlobject.BoolCol()

# This table stores the data for each sensor
class Table_Sensors(sqlobject.SQLObject):
	int_id = sqlobject.StringCol(length=32)
	name = sqlobject.StringCol(length=64)
	group = sqlobject.ForeignKey("Table_Groups")
	prefix = sqlobject.StringCol(length=32)
	postfix = sqlobject.UnicodeCol(length=32)
	sort_order = sqlobject.IntCol()
	visable = sqlobject.BoolCol()
	value = sqlobject.FloatCol()
	value_string = sqlobject.StringCol(length=255)

# This table stores every instance of a rain_tip_event
# Fromt he last week, and the precise time.
class Table_Rain(sqlobject.SQLObject):
	time = sqlobject.DateTimeCol()
	quantity = sqlobject.FloatCol()

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

Table_Groups.createTable(ifNotExists = True)
Table_Sensors.createTable(ifNotExists = True)
Table_Rain.createTable(ifNotExists = True)
Table_Archive.createTable(ifNotExists = True)

# Verifies that the group actually exists in the db.
def database_verify_group(the_int_id, the_name, is_visable=True):
	#If the group doesn't exist
	if Table_Groups.selectBy(int_id=the_int_id).count() == 0:
		logging.getLogger("database").warning(" db-group entry " + the_name + " does not exist, creating...")
		group = Table_Groups(int_id=the_int_id, name=the_name, sort_order=99, visable=is_visable)
	#If the group is messed up
	if Table_Groups.selectBy(int_id=the_int_id).count() != 1:
		logging.getLogger("database").error(" db-group " + the_name + " entry is invalid!")

# Verifies that the sensor actually exists in the db.
def database_verify_sensor(the_int_id, the_name, group_id, the_prefix, the_postfix, is_visable=True):
	#Get the parent group
	group = Table_Groups.selectBy(int_id=group_id).getOne()
	group_id = group.id
	
	#If the sensor doesn't exist
	if Table_Sensors.selectBy(int_id=the_int_id).count() == 0:
		logging.getLogger("database").warning(" db-sensor entry " + the_name + " does not exist, creating...")
		sensor = Table_Sensors(int_id=the_int_id, name=the_name, group=group_id, prefix=the_prefix, postfix=the_postfix, sort_order=99, visable=is_visable, value=0, value_string="")
	#If the sensor is messed up
	if Table_Sensors.selectBy(int_id=the_int_id).count() != 1:
		logging.getLogger("database").error(" db-sensor " + the_name +  " entry is invalid!")