#!python
from settings import *

def getDB():
	if Database_Type is "mySQL":
		#Import Libraries
		import MySQLdb
		from MySQLdb.constants import FIELD_TYPE
		
		#Type conversion dictionary
		my_conv = {FIELD_TYPE.FLOAT: float, FIELD_TYPE.LONG: int}
		
		# Connect to db
		return MySQLdb.connect(host = Database_Host, user = Database_User, passwd = Database_Password, db = database_Name, conv=my_conv)
		return db.cursor()
	else if Database_Type is "SQLlite":
		print "lol"
	else:
		sys.exit(Database_Type + " is not a valid option!")