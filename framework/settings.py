#!python

#
# This File contains all the easily-modifiable settings for the project
# You must fill out the 2 settings in the required section
# but everything after that is completely optional.
#


###################################
######## Required Settings ########
###################################

# This should be your API Key from weather underground.
# You can get one fro free from here:
# http://www.wunderground.com/weather/api
key = "e8b292334779aa96"

# The ZIP code you want to get weather forcasts and such from
zip = "97338"


###################################
##### Sensor Update Frequency #####
###################################
# All Values in seconds

# How often the Temp, Humidity, & Wind sensors are updated 
how_often_to_check_sensors = 5

# How often the current 'feel like' & picture are updated
# Feels_like update should not be < 180 (API Limits)
how_often_to_update_feels_like = 600

# How often the rain data is updated
how_often_to_compile_rain = 60

# How often the current data is archived to a backup table
# Archive time should be >= compile_rain time.
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
Temp_Average_Length = 10
Humid_Average_Length = 15
Wind_Average_Length = 10


###################################
######### Other Settings ##########
###################################

# Should we enable console logging for the deamon threads?
enable_deamon_logging = True

# How long we should wait for threads to finish before killing them
how_long_to_wait_before_killing_deamons = 5