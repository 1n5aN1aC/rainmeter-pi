#!python
# -*- coding: UTF-8 -*-
from database import *

#
# This file will reset the current rainfall to 0.
def reset_rain():
	# Reset rain_since_reset in the table
	# (╯°□°）╯︵ ┻━┻
	now = Table_Now.get(1)
	now.sync()
	now.Out_Rain_Since_Reset = 0
	
	return "reset!"

# If file ran directly, reset the rain as well.
# We use this to be able to support wsgi OR straight python.
if __name__ == '__main__':
	# Print the Header
	print "Content-Type: text/html;charset=utf-8"
	print
	
	# Print the Data
	print reset_rain()