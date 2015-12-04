#!python
import json
from database import *

#
# This File His requested by the index page every time it needs to update the data.
# It Returns all the current weather data in a json-file, formated for web-display.
# That means this is called very often, and should be reletively effecient
#

# Connect to the Database
db = getDB()
cursor = db.cursor()

# Execute SELECT query
query = fixDBQuery("SELECT `ref`, `IN_Temp`, `IN_Humid`, `OUT_Temp`, `OUT_Humid`, `OUT_Wind_Avg`, `OUT_Wind_Max`, `OUT_Rain_Today`, `OUT_Rain_Last_24h`, `OUT_Rain_Since_Reset`, `ATTIC_Temp`, `ATTIC_Humid`, `NOW_URL`, `NOW_Feel`, `SYSTEM_CPU`, `SYSTEM_RAM` FROM `now` WHERE 1")
cursor.execute(query)
result = cursor.fetchone()
db.close()

# Now we parse all the data out of the results!
data = {}
data["ref"] = result[0]
data["IN_Temp"] = result[1]
data["IN_Humid"] = result[2]
data["OUT_Temp"] = result[3]
data["OUT_Humid"] = result[4]
data["OUT_Wind_Avg"] = result[5]
data["OUT_Wind_Max"] = result[6]
data["OUT_Rain_Today"] = result[7]
data["OUT_Rain_Last_24h"] = result[8]
data["OUT_Rain_Since_Reset"] = result[9]
data["ATTIC_Temp"] = result[10]
data["ATTIC_Humid"] = result[11]
data["NOW_URL"] = result[12]
data["NOW_Feel"] = result[13]
data["SYSTEM_CPU"] = result[14]
data["SYSTEM_RAM"] = result[15]

# Print the Header
print "Content-Type: text/html;charset=utf-8"
print
# Print the Data
print json.dumps(data)