#!python
# -*- coding: UTF-8 -*-
from database import *
import time

#
# This file will reset the current rainfall to 0.
# We have it look executing 3 times, once per second, because there's
# A strange race condition that can cause it to not actually be reset.
#

# Print the Header
print "Content-Type: text/html;charset=utf-8"
print

# Reset rain_since_reset in the table
# (╯°□°）╯︵ ┻━┻
for x in range(0, 3):
	now = Table_Now.get(1)
	now.Out_Rain_Since_Reset = 0
	time.sleep(1)

# Print the Data
print "reset!"