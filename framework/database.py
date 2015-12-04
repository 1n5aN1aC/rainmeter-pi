#!python
from settings import *
import time

def getDB():
	if Database_Type is "mySQL":
		#Import Libraries
		import MySQLdb
		from MySQLdb.constants import FIELD_TYPE
		
		#Type conversion dictionary
		my_conv = {FIELD_TYPE.FLOAT: float, FIELD_TYPE.LONG: int}
		
		# Connect to db
		return MySQLdb.connect(host = Database_Host, user = Database_User, passwd = Database_Password, db = Database_Name, conv=my_conv)

	elif Database_Type is "SQLite":
		#Import Libraries
		import sqlite3
		
		#Connect to db
		return sqlite3.connect(Database_Name)

	else:
		sys.exit(Database_Type + " is not a valid Database_Type option!")

# Fixes the DB query to be compatable with any DB paramstyle
def fixDBQuery(query):
	if Database_Type is "mySQL":
		return query
	elif Database_Type is "SQLite":
		return query.replace("%s", "?")
	else:
		sys.exit(Database_Type + " is not a valid Database_Type option!")

# Inserts the required tables into a new database.
def populate_database_tables():
	print "Creating database tables"
	db = getDB()
	cursor = db.cursor()
	
	make_table_rain = "CREATE TABLE `rain` (`count` int(11) NOT NULL, `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, `quantity` float NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;"
	alter_rain = "ALTER TABLE `rain` ADD PRIMARY KEY (`count`), ADD UNIQUE KEY `timestamp` (`time`);"
	alter_rain_2 = "ALTER TABLE `rain` MODIFY `count` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;"
	cursor.execute(make_table_rain)
	cursor.execute(alter_rain)
	cursor.execute(alter_rain_2)
	db.commit()
	
	make_table_now = "CREATE TABLE `now` (`ref` int(11) NOT NULL, `IN_Temp` float NOT NULL, `IN_Humid` float NOT NULL, `OUT_Temp` float NOT NULL, `OUT_Humid` float NOT NULL, `OUT_Wind_Avg` float NOT NULL, `OUT_Wind_Max` float NOT NULL, `OUT_Rain_Today` float NOT NULL, `OUT_Rain_Last_24h` float NOT NULL, `OUT_Rain_Since_Reset` float NOT NULL, `ATTIC_Temp` float NOT NULL, `ATTIC_Humid` float NOT NULL, `NOW_URL` varchar(100) COLLATE utf8_bin NOT NULL, `NOW_Feel` float NOT NULL, `SYSTEM_CPU` float NOT NULL, `SYSTEM_RAM` float NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;"
	alter_now = "ALTER TABLE `now` ADD PRIMARY KEY (`ref`);"
	alter_now_2 = "ALTER TABLE `now` MODIFY `ref` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;"
	cursor.execute(make_table_now)
	cursor.execute(alter_now)
	cursor.execute(alter_now_2)
	db.commit()
	
	make_table_archive = "CREATE TABLE `archive` (`count` int(11) NOT NULL, `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, `IN_Temp` float NOT NULL, `IN_Humid` float NOT NULL, `OUT_Temp` float NOT NULL, `OUT_Humid` float NOT NULL, `OUT_Wind_Avg` float NOT NULL, `OUT_Wind_Max` float NOT NULL, `OUT_Rain_Minute` float NOT NULL, `ATTIC_Temp` float NOT NULL, `ATTIC_Humid` float NOT NULL, `NOW_Feel` float NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;"
	alter_archive = "ALTER TABLE `archive` ADD PRIMARY KEY (`count`), ADD KEY `date` (`date`) USING BTREE;"
	alter_archive_2 = "ALTER TABLE `archive` MODIFY `count` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;"
	cursor.execute(make_table_archive)
	cursor.execute(alter_archive)
	cursor.execute(alter_archive_2)
	db.commit()
	print "Done creating database tables!"
	time.sleep(5)

# If someone runs this script directly, it inserts the tables into the database
if __name__ == '__main__':
	populate_database_tables()