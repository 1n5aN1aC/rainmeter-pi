[![Supports](https://img.shields.io/badge/platform-raspberry%20pi-lightgrey.svg?style=plastic)](https://www.raspberrypi.org/) [![Supports](https://img.shields.io/badge/supports-mysql%20or%20sqlite-lightgrey.svg?style=plastic)](https://github.com/1n5aN1aC/rainmeter-pi/blob/master/framework/settings.py#L29) [![License](https://img.shields.io/badge/license-cc--by--sa-green.svg?style=plastic)](http://creativecommons.org/licenses/by-sa/4.0/)

# Rainmeter-pi
Raspberry-pi powered Weather Station

Better Description Coming Soon!

## Pictures!

Coming Soon!

## How it works

TODO

## Materials

EDIT:  Out of date, new list coming soon...

Raspbery Pi Zero [(<$10)](http://swag.raspberrypi.org/products/pi-zero-kit)

DHT11 Temp & Humidity Sensor [($5)](https://www.adafruit.com/products/386)

DHT22 Temp & Humidity Sensors [($10)](https://www.adafruit.com/products/385)

MCP3008 Analog Digital Converter Chip [($3.75)](https://www.adafruit.com/product/856)

'Hot-Wire' wind sensor [($17)](https://moderndevice.com/product/wind-sensor/)

## Setup Instructions

### Physical

TODO

### Raspbian

If you have Linux experience, I reccomend using the ['Lite' Version](https://www.raspberrypi.org/downloads/raspbian/) of Rasbian.  It has none of the default bloat installed, and does not even have a GUI unless you install one.

If you wish to go this route, there is [a tool](https://andrewvaughan.io/raspbian-i-love-you-but-youre-fat/) which can help you easily customize what to install.

After burning, make sure you do ```sudo apt-get update && sudo apt-get upgrade && sudo apt-get dist-upgrade``` if needed.  [(Detailed Instructions)](https://www.raspberrypi.org/documentation/raspbian/updating.md)

### Installing Dependencies
Make sure you have the latest version of raspbery pi firmware:

```sudo apt-get install rpi-update && sudo rpi-update``` [(Detailed Instructions)](https://github.com/Hexxeh/rpi-update)

Make sure you have all the python and webserver dependencies:

```sudo apt-get install build-essential python-dev python-mysqldb libapache2-mod-wsgi apache2 mysql-server htop```

```pip install sqlobject pytz psutil```

Install the DHTXX Sensor library:

TODO https://github.com/adafruit/Adafruit_Python_DHT

### Copy the Files over

TODO

### Webserver set up

I used apache, so if you want to use a different webserver, such as nginx, sorry, but your on your own.

There used to be two options available, but it was a mess, so I only support wsgi now, which runs very fast.

WSGIPythonPath "/var/www/html/"
WSGIScriptAlias /status "/var/www/html/framework/http_status.wsgi"
WSGIScriptAlias /reset_rain "/var/www/html/framework/http_reset_rain.wsgi"

TODO

### Configure

Open ```./framework/settings.py``` and fill out the required settings, such as your API key & ZIP code.

Make any other changes you wish to make.

Open ```./framework/sensors.py``` and make any changes needed to support your specific sensors.  This should be easy if using similar sensors t one sI used, or it may require more work, depending on the specific sensors you have.