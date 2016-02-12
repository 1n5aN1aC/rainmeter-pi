[![Supports](https://img.shields.io/badge/platform-raspberry%20pi-lightgrey.svg?style=plastic)](https://www.raspberrypi.org/) [![Supports](https://img.shields.io/badge/supports-mysql%20or%20sqlite-lightgrey.svg?style=plastic)](https://github.com/1n5aN1aC/rainmeter-pi/blob/master/framework/settings.py#L29) [![License](https://img.shields.io/badge/license-cc--by--sa-green.svg?style=plastic)](http://creativecommons.org/licenses/by-sa/4.0/)

# Rainmeter-pi
Raspberry-pi powered Weather Station

Better Description Coming Soon!

## Pictures!

Coming Soon!

## How it works

TODO

## Materials

Raspbery Pi Zero [(<$10)](http://swag.raspberrypi.org/products/pi-zero-kit)

DHT11 Temp & Humidity Sensor [($5)](https://www.adafruit.com/products/386)

DHT22 Temp & Humidity Sensors [($10)](https://www.adafruit.com/products/385)

MCP3008 Analog Digital Converter Chip [($3.75)](https://www.adafruit.com/product/856)

'Hot-Wire' wind sensor [($17)](https://moderndevice.com/product/wind-sensor/)

## Setup Instructions

### Physical

TODO

### Installing Dependencies
Make sure you have the latest version of raspbery pi firmware:

```sudo apt-get update && sudo apt-get upgrade``` [(Detailed Instructions)](https://www.raspberrypi.org/documentation/raspbian/updating.md)

Next, enable SPI support on your pi:

```sudo raspi-config -> Advanced Options -> SPI``` [(Detailed Instructions)](http://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/)

Make sure you have all the python dependencies:

```sudo apt-get install build-essential python-dev```

```pip install sqlobject pytz```

Install the DHTXX Sensor library:

TODO https://github.com/adafruit/Adafruit_Python_DHT

### Copy the Files over

TODO

### Webserver set up

I used apache, so if you want to use a different webserver, such as nginx, sorry, but your on your own.

There are two options available:  the 'simple' way, which is much slower, or wsgi, which runs very fast.

WSGIPythonPath "/var/www/html/"
WSGIScriptAlias /status "/var/www/html/framework/http_status.wsgi"
WSGIScriptAlias /reset_rain "/var/www/html/framework/http_reset_rain.wsgi"

TODO

### Configure

Open ```./framework/settings.py``` and fill out the required settings, such as your API key & ZIP code.

Make any other changes you wish to make.

Open ```./framework/sensors.py``` and make any changes needed to support your specific sensors.  This should be easy if using similar sensors t one sI used, or it may require more work, depending on the specific sensors you have.