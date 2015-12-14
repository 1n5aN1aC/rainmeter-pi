#!python
import json
from database import *

# Gets the actual data, and dumps it as a json string
def get_json():
	#Execute SELECT query
	now = Table_Now.get(1)
	#mod_wsgi does not ever terminate, and it isn't made aware of other changes to the db
	#So we have to sync() each time to get the latest data.
	now.sync()

	#Now we parse all the data out of the results!
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
	
	#Now return the json as a string
	return json.dumps(data)

# If file ran directly, print the json directly as well.
# We use this to be able to support wsgi OR straight python.
if __name__ == '__main__':
	# Print the Header
	print "Content-Type: application/json;charset=utf-8"
	print
	# Print the Data
	print get_json()