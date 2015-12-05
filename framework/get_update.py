#!python
import json
from database import *

#
# This File His requested by the index page every time it needs to update the data.
# It Returns all the current weather data in a json-file, formated for web-display.
# That means this is called very often, and should be reletively effecient
#

# Execute SELECT query
now = Table_Now.get(1)

# Now we parse all the data out of the results!
data = {}
data["IN_Temp"] = now.In_Temp
data["IN_Humid"] = now.In_Humid
data["OUT_Temp"] = now.Out_Temp
data["OUT_Humid"] = now.Out_Humid
data["OUT_Wind_Avg"] = now.Out_Wind_Avg
data["OUT_Wind_Max"] = now.Out_Wind_Max
data["OUT_Rain_Today"] = now.Out_Rain_Today
data["OUT_Rain_Last_24h"] = now.Out_Rain_Last_24h
data["OUT_Rain_Since_Reset"] = now.Out_Rain_Since_Reset
data["ATTIC_Temp"] = now.Attic_Temp
data["ATTIC_Humid"] = now.Attic_Humid
data["NOW_URL"] = now.Now_URL
data["NOW_Feel"] = now.Now_Feel
data["SYSTEM_CPU"] = now.System_CPU
data["SYSTEM_RAM"] = now.System_RAM

# Print the Header
print "Content-Type: text/html;charset=utf-8"
print
# Print the Data
print json.dumps(data)