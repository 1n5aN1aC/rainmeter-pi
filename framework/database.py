#!python
import MySQLdb
from MySQLdb.constants import FIELD_TYPE

#####################################
DBhost = "127.0.0.1"
DBuser = "rainmeter"
DBpasswd = "password"
DBdb = "rainmeter"
#####################################

def getDB():
	#Type conversion dictionary
	my_conv = {FIELD_TYPE.FLOAT: float, FIELD_TYPE.LONG: int}
	# Connect to db
	return MySQLdb.connect(host = DBhost, user = DBuser, passwd = DBpasswd, db = DBdb, conv=my_conv)
	return db.cursor()