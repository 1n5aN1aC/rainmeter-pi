#!python

# The now object for all threads
now = None

# Returns a reference to the now object.
def get(lol=1):
    global now
    if now is not None:
        return now

    now = Table_Now()
    return now

# This object stores the current weather data.
class Table_Now():
    In_Temp = 0
    Out_Temp = 0
    Attic_Temp = 0
    In_Humid = 0
    Out_Humid = 0
    Attic_Humid = 0
    Out_Wind_Avg = 0
    Out_Wind_Max = 0
    Out_Rain_Today = 0
    Out_Rain_Last_24h = 0
    Out_Rain_Since_Reset = 0
    System_CPU = 0
    System_RAM = 0
    Now_URL = "error"
    Now_Feel = 0