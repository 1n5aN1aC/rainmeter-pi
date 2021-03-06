#!python

#
# This File contains all the easily-modifiable settings for the project
# You must check the few settings in the required section
# but everything after that is completely optional.
#


###################################
######## Required Settings ########
###################################

# This should be your API Key from weather underground.
# You can get one for free from here:
# http://www.wunderground.com/weather/api
key = "e8b292334779aa96"

# The ZIP code you want to get weather forecasts and such for
zipcode = "97338"

# How many inches per rain meter tip
rainTipAmount = 0.02

# Your timezone code can be found from the link below:
# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
my_timezone = "US/Pacific"

# Should we convert the Celsius sensor readings to Fahrenheit?
fahrenheit = True

# Database Settings:
# Scheme is one of: mysql, sqlite, postgres, firebird, interbase, maxdb, sapdb, mssql, sybase
# Only 'mysql' and 'sqlite' are tested.
#Connection_String = "scheme://[user[:password]@]host[:port]/database[?parameters]"
Connection_String = "mysql://rainmeter:password@localhost/rainmeter"
#Connection_String = "sqlite:///full/path/to/database"
#Connection_String = "sqlite:/D:/XAMPP/htdocs/database.db"


###################################
##### Sensor Update Frequency #####
###################################
# All Values in seconds

# How often the various sensors are updated
how_often_to_check_temp = 6
how_often_to_check_system = 6

# How often the current 'feel like' & picture are updated
# Feels_like update should not be < 180 (API Limits)
how_often_to_update_feels_like = 600

# How often the rain data is updated
how_often_to_compile_rain = 60

# How often the current data is archived to a backup table
# Archive time should be >= compile_rain time, preferably equal.
how_often_to_archive_data = 60

# How often the rain database should be cleaned of old values
how_often_to_clean_rain_db = 3600

# How many days of full rain data should be kept in the rain db
how_many_days_of_rain_data_to_keep = 7


###################################
##### Sensor Jitter Settings ######
###################################

# These values control how many recent values are averaged together
# to get the 'current' value.  This prevents stutter and bad readings.
Temp_Average_Length = 5
Humid_Average_Length = 10

# The wind sensor is a bit different.
# How many reading do we consider for avg / max?
Wind_Average_Length = 60

# This defines how many consecutive readings of a sensor must fail
# before the sensor actually displays an error.
# Until that point, the sensor will continue to operate on old data.
failed_readings_before_error = 10


###################################
##### Miscellaneous Settings ######
###################################

# Should we enable console logging for the deamon threads?
enable_deamon_logging = True

# How long we should wait for the main threads to finish before killing them
# How long we should wait for each deamon thread to finish before killing it
how_long_to_wait_before_killing_threads = 5
how_long_to_wait_before_killing_deamons = 2