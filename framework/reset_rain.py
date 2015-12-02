#!python
from database import *

#
# This file will reset the current rainfall to 0.
#

# Connect to the Database
db = getDB()
cursor = db.cursor()

# Execute UPDATE query
query = "UPDATE `now` SET `OUT_Rain_Since_Reset`=%s WHERE 1"
cursor.execute(query, [0])
db.commit()
db.close()

# Print the Header
print "Content-Type: text/html;charset=utf-8"
print
# Print the Data
print "reset!"