#!/usr/bin/env python
from framework import http_reset_rain

#
# This is requested by the index page every time it needs to update the data.
# It will Return all the current weather data in a json-file, formated for web-display.
# That means this is called very often, and should be reletively effecient
def application(environ, start_response):
    status = '200 OK'
    output = http_reset_rain.reset_rain()
	
    response_headers = [('Content-type', 'application/json;charset=utf-8'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]