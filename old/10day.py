import urllib2
import json
key = "e8b292334779aa96"
zip = "97338"

url = 'http://api.wunderground.com/api/' + key + '/geolookup/forecast10day/q/' + zip + '.json'
f = urllib2.urlopen(url)
json_string = f.read()
parsed_json = json.loads(json_string)


count = 0
for day in parsed_json['forecast']['simpleforecast']['forecastday']:
	print day['date']['weekday_short']
	print '  High:   ' + day['high']['fahrenheit'] + 'F'
	print '  Low:    ' + day['low']['fahrenheit'] + 'F'
	print '  Precip: ' + str(day['pop']) + "% (" + str(day['qpf_allday'][u'in']) + "in)"
	print '  ' + day['icon_url']
	count += 1
	if count >= 8:
		break
f.close()