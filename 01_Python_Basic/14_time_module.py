'''
1. Current Timestamp: 
   + time.time(): Returns the current timestamp in seconds since the epoch as a floating-point number.
   + time.time_ns(): Returns the current timestamp in nanoseconds as an integer.

2. time.sleep(secs): Suspends execution for the given number of seconds.

3. time.localtime([secs]):
   + time.localtime(): Returns the current local time as a struct_time object.
   + time.localtime([secs]): Converts a given timestamp (secs) to a struct_time object in local time.

4. struct_time object:
   + Attributes: tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst
   + time.gmtime([secs]): Similar to localtime() but returns UTC time.
   + time.mktime(struct_time): Converts a struct_time object in local time to a timestamp.

'''

import time

#---------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 1. Current Timestamp --------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#

############
## time() ##
############
'''Current timestamp in seconds since epoch'''

# Get the current timestamp (seconds since epoch)
current_timestamp = time.time()
print(current_timestamp) # 1762842898.081597

# Shorter version:
print(time.time()) # 1762842922.4453177

###############
## time_ns() ##
###############
'''Nanosecond precision timestamp'''

# Get the current timestamp in nanoseconds
current_timestamp_ns = time.time_ns()
print(current_timestamp_ns) # 1762842952081597696

# Shorter version:
print(time.time_ns()) # 1762842972445317760


#---------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 2. time.sleep(secs) -------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#

print("Sleeping for 5 seconds...")

time.sleep(5)  # Pause execution for 5 seconds

print("Awake!")


#---------------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 3. time.localtime([secs]) -----------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#
'''
Return a struct_time object representing local time.
If secs (timestamp) is not provided, the current time as returned by time() is used.
'''

#################
## localtime() ##
#################

local_time = time.localtime()

print(local_time)
# time.struct_time(tm_year=2025, tm_mon=11, tm_mday=11, tm_hour=16, tm_min=10, tm_sec=53, tm_wday=1, tm_yday=315, tm_isdst=0)

#######################
## localtime([secs]) ##
#######################

specific_time = time.localtime(1609459200)  # Timestamp for January 1, 2021

print(specific_time)
# time.struct_time(tm_year=2021, tm_mon=1, tm_mday=1, tm_hour=9, tm_min=0, tm_sec=0, tm_wday=4, tm_yday=1, tm_isdst=0)


#--------------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 4. struct_time object --------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

################
## Attributes ##
################

str_time_obj = time.localtime(1609459500)
print(str_time_obj)
# time.struct_time(tm_year=2021, tm_mon=1, tm_mday=1, tm_hour=9, tm_min=5, tm_sec=0, tm_wday=4, tm_yday=1, tm_isdst=0)

print(str_time_obj.tm_year)   # 2021
print(str_time_obj.tm_mon)    # 1
print(str_time_obj.tm_mday)   # 1
print(str_time_obj.tm_hour)   # 9
print(str_time_obj.tm_min)    # 5
print(str_time_obj.tm_sec)    # 0
print(str_time_obj.tm_wday)   # 4 (Friday)
print(str_time_obj.tm_yday)   # 1
print(str_time_obj.tm_isdst)  # 0 (Not in Daylight Saving Time)

'''Friday January 1, 2021 09:05:00 AM'''


###################
## time.gmtime() ##
###################
'''Convert to UTC time'''

utc_time = time.gmtime()
print(utc_time)
# time.struct_time(tm_year=2025, tm_mon=11, tm_mday=11, tm_hour=7, tm_min=26, tm_sec=37, tm_wday=1, tm_yday=315, tm_isdst=0)
'''tm_isdst is always 0 for UTC'''

#----

specific_time = time.gmtime(1627987508) # Convert specific timestamp
print(specific_time)
# time.struct_time(tm_year=2021, tm_mon=8, tm_mday=3, tm_hour=10, tm_min=45, tm_sec=8, tm_wday=1, tm_yday=215, tm_isdst=0)

###################
## time.mktime() ##
###################
'''Convert struct_time to timestamp'''

# Create a struct_time tuple (local time)
time_tuple = (2025, 11, 11, 14, 30, 0, 0, 315, 0)

# Convert struct_time to timestamp
timestamp = time.mktime(time_tuple)
print(timestamp)  # 1762839000.0



'''
| Function          | Purpose             | Returns         | Notes                           |
| ----------------- | ------------------- | --------------- | ------------------------------- |
| 1. time()         | Current timestamp   | float (seconds) | Wall-clock time, can jump       |
| 2. sleep(secs)    | Pause execution     | None            | May sleep longer than requested |
| 3. perf_counter() | High-res timing     | float           | Best for benchmarking           |
| 4. monotonic()    | Monotonic time      | float           | Never decreases                 |
| 5. process_time() | CPU time            | float           | Excludes sleep                  |
| 6. localtime()    | Convert to local    | struct_time     | Includes DST flag               |
| 7. gmtime()       | Convert to UTC      | struct_time     | DST always 0                    |
| 8. mktime()       | struct to timestamp | float           | Local time to epoch             |
| 9. strftime()     | Format time         | str             | Many format codes               |
| 10. strptime()    | Parse time          | struct_time     | Thread-safety issues on Windows |
'''