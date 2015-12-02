#!python
# -*- coding: UTF-8 -*-
from framework import weather

#
# This File Handles displaying the hourly forcast.
# It fetches the forecast from weather underground,
# then displays it in a table-based format.
#
# It also redirects back to the home page after 2 minutes,
# in case someone left it on this screen by accident.
#
# If you are looking for how to change it to your own location,
# You can find that option in weather.py
#

#####################################
Max_Hours_To_Show = 36
#####################################

# Print the Header
print "Content-Type: text/html;charset=utf-8"
print

# Print HTML Header
print '''<!DOCTYPE HTML>
<html>
	<head>
		<meta charset="UTF-8">
		<meta http-equiv="refresh" content="120;URL=/">
		<link rel="stylesheet" type="text/css" href="/css/common.css">
		<link rel="stylesheet" type="text/css" href="/css/hourly.css">
	</head>
	<body>
		<div class="scrollpanel">
			<table class="hourly">
				<tr>
					<th></th>
					<th></th>
					<th>Temp (°F)</th>
					<th>% Hum</th>
					<th>Precip</th>
					<th>dewpoint</th>
					<th>wind</th>
				</tr>'''

#Get the hourly Forecast
parsed_json = weather.fetchWeather('hourly10day')

#Loop through the results, and print what is applicable
count = 0
for hour in parsed_json['hourly_forecast']:
	count += 1
	
	print "<tr>"
	print "<td>" + hour['FCTTIME']['weekday_name'] + "</br>" + hour['FCTTIME']['civil'] + "</td>"
	print "<td><img class='small' src=" + hour['icon_url'] + " /></td>"
	print "<td><span class='larger'>" + str(hour['temp']['english']) + u'° </span></td>'.encode('utf-8')
	print "<td>" + hour['humidity'] + '% </td>'
	if hour['pop'] > 0 and float(hour['qpf']['english']) > 0:
		print "<td>" + str(hour['pop']) + "% (" + str(hour['qpf']['english']) + "in) </td>"
	else:
		print "<td>" + hour['pop'] + '% </td>'
	print "<td>" + str(hour['dewpoint']['english']) + u'° </td>'.encode('utf-8')
	print "<td>" + hour['wspd']['english'] + ' mph </td>'
	print "</tr>"
	
	if count >= Max_Hours_To_Show:
		break
weather.closeURL()

# Print the HTML Closing tags
print '''
			</table>
		</div>
		<div class='rightbar'>
			<a href="/forecast.py"><div class='back'>
				<img id='logo' src='/img/back-icon.png' />
			</div></a>
		</div>
	</body>
</html>'''