#!python
import site
site.addsitedir('/usr/local/pythonenv/PYLONS-1/lib/python2.5/site-packages')

import json
from database import *

#
# This is requested by the index page every time it needs to update the data.
# It will Return all the current weather data in a json-file, formated for web-display.
# That means this is called very often, and should be reletively effecient
def application(environ, start_response):
    status = '200 OK'
    output = get_json()
	
    response_headers = [('Content-type', 'application/json;charset=utf-8'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]

# Gets the actual data, and dumps it as a json string
def get_json():
	#Execute SELECT query
	now = Table_Now.get(1)

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