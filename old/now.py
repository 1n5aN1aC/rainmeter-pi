#
# Check Every 5 Minutes is safe.
#

import urllib2
import json
key = "e8b292334779aa96"
zip = "97338"

url = 'http://api.wunderground.com/api/' + key + '/geolookup/conditions/q/' + zip + '.json'
f = urllib2.urlopen(url)
json_string = f.read()
parsed_json = json.loads(json_string)

print 'Feels Like: ' + str(parsed_json['current_observation']['feelslike_f']) + 'F'
print parsed_json['current_observation']['icon_url']

f.close()