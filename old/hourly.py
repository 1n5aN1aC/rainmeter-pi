import urllib2
import json
key = "e8b292334779aa96"
zip = "97338"

url = 'http://api.wunderground.com/api/' + key + '/geolookup/hourly10day/q/' + zip + '.json'
f = urllib2.urlopen(url)
json_string = f.read()
parsed_json = json.loads(json_string)
hours = parsed_json['hourly_forecast']

count = 0
for hour in hours:
	print hour['FCTTIME']['civil']
	print '  Temp:  ' + hour['temp']['english'] + 'F'
	print '  Precip:' + hour['pop'] + '%'
	print '  Humid: ' + hour['humidity'] + '%'
	print hour['icon_url']
	count += 1
	if count >= 24:
		break
f.close()