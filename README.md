<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/80x15.png" /></a>

# rainmeter-pi
Raspberry-pi powered Weather Station
TODO

## Pictures!

TODO

## How it works

TODO

## Materials

TODO

## Setup Instructions

### Physical

TODO

### Installing Dependencies
Make sure you have the latest version of raspbery pi firmware:

```sudo apt-get install rpi-update && sudo rpi-update```

Next, enable SPI support on your pi:

```sudo raspi-config -> Advanced Options -> SPI``` [(Click Here for Detailed Instructions)](http://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/)

Make sure you have all the python dependencies:

```sudo apt-get install build-essential python-dev```

```pip install sqlobject pytz```

Install the DHTXX Sensor library:

TODO https://github.com/adafruit/Adafruit_Python_DHT

### Copy the Files over

TODO

### Configure

Open ```./framework/settings.py``` and fill out the required settings, such as your API key & ZIP code.

Make any other changes you wish to make.

Open ```./framework/sensors.py``` and make any changes needed to support your specific sensors.  This should be easy if using similar sensors t one sI used, or it may require more work, depending on the specific sensors you have.