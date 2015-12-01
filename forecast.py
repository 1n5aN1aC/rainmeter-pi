#!python
from framework import weather

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
		<link rel="stylesheet" type="text/css" href="/css/forecast.css">
	</head>
	<body>'''

#Get the Forecast
parsed_json = weather.fetchWeather('forecast10day')

#Loop through the results, and print what is applicable
count = 0
for day in parsed_json['forecast']['simpleforecast']['forecastday']:
	count += 1
	
	print "<div class='box' id='box" + str(count) + "'>"
	print day['date']['weekday_short'] + "</br>"
	print "<img src=" + day['icon_url'] + " /></br>"
	print day['high']['fahrenheit'] + 'F / ' + day['low']['fahrenheit'] + 'F </br>'
	if day['pop'] > 0:
		print str(day['pop']) + "% (" + str(day['qpf_allday'][u'in']) + "in)"
	print "</div>"
	
	if count >= 8:
		break
weather.closeURL()

# Print the HTML Closing tags
print '''
		<div class='bottombar'>
			<a href="/radar.py"><div class='radar'>
				Radar
			</div></a>
			<a href="/hourly.py"><div class='hourly'>
				Hourly Forcast
			</div></a>
			<a href="/"><div class='back'>
				<img id='logo' src='/img/back-icon.png' />
			</div></a>
		</div>
	</body>
</html>'''