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

5. Format and Parsing:
   + time.strftime(format, struct_time): struc_time -> string
   + time.strptime(string, format): string -> struct_time
   + time.ctime([secs]): Converts a timestamp to a string representation (Quick readable format)
   + time.asctime([struct_time]): Converts a struct_time to a string representation (Quick readable format)

6. Performance Timing and Benchmarking:
   + time.perf_counter(): highest resolution timer, includes sleep, monotonic, best for benchmarking.
   + time.perf_counter_ns(): same as perf_counter but in nanoseconds.
   + time.monotonic(): monotonic clock, cannot go backward, good for measuring elapsed time.
   + time.process_time(): CPU time used by the process, excludes sleep time.
   + time.thread_time(): CPU time used by the current thread.

7. Timezone Handling
   + Timezone Constants: time.timezone, time.altzone, time.daylight, time.tzname
   + Set timezone (Unix): time.tzset()
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

##########
## Demo ##
##########

print("Sleeping for 5 seconds...")

time.sleep(5)  # Pause execution for 5 seconds

print("Awake!")

#################
## Application ##
#################

start = time.time()

for i in range(10):
    print(i)
    time.sleep(0.3)  # Sleep for 0.3 second between prints

end = time.time()

duration = start - end

print(f"Total time taken: {duration} seconds")


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


#---------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 5. Format and Parsing ------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#

'''
%Y - Year with century (2025)
%m - Month as number (01-12)
%d - Day of month (01-31)
%H - Hour 24-hour (00-23)
%I - Hour 12-hour (01-12)
%M - Minute (00-59)
%S - Second (00-59)
%p - AM/PM
%A - Full weekday name
%B - Full month name
%a - Abbreviated weekday
%b - Abbreviated month
%j - Day of year (001-366)
%z - UTC offset (+HHMM or -HHMM)
'''

#####################
## time.strftime() ##
#####################
'''Format struct_time to string'''

french_revo = (1789, 7, 14, 12, 0, 0, 0, 195, 0) # July 14, 1789
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", french_revo)
print(formatted_time)  # 1789-07-14 12:00:00

print(time.strftime("%A, %B %d, %Y %I:%M:%S %p"))  # Tuesday, November 11, 2025 04:48:51 PM
                                                   # Automatically gets current time if struct_time not provided

#####################
## time.strptime() ##
#####################
'''Parse string to struct_time'''

time_string = "2025-11-11 16:50:00"
parsed_time = time.strptime(time_string, "%Y-%m-%d %H:%M:%S") # The format must match the string

print(parsed_time)
# time.struct_time(tm_year=2025, tm_mon=11, tm_mday=11, tm_hour=16, tm_min=50, tm_sec=0, tm_wday=1, tm_yday=315, tm_isdst=-1)

##################
## time.ctime() ##
##################
'''Convert timestamp to string (quick readable format)'''

print(time.ctime(1609459200))  # Fri Jan  1 09:00:00 2021

print(time.ctime())  # Tue Nov 11 16:55:45 2025
                     # Automatically gets current time if timestamp not provided

####################
## time.asctime() ##
####################
'''Convert struct_time to string (quick readable format)'''

usa_revo = (1776, 7, 4, 12, 0, 0, 0, 185, 0) # July 4, 1776
print(time.asctime(usa_revo))  # Mon Jul  4 12:00:00 1776

print(time.asctime())  # Tue Nov 11 16:57:30 2025
                       # Automatically gets current time if struct_time not provided


#--------------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 6. Performance Timing and Benchmarking -------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

#########################
## time.perf_counter() ##
#########################
'''
High-resolution timer for benchmarking
Includes time elapsed during sleep, monotonic (cannot go backward)
'''

start = time.perf_counter()

# Simulate work
result = sum(range(1000000))
time.sleep(2)

end = time.perf_counter()

duration = end - start

print(f"Execution time: {duration:.6f} seconds") # 2.013061 seconds

############################
## time.perf_counter_ns() ##
############################
'''Like perf_counter() but in nanoseconds'''

start_ns = time.perf_counter_ns()

# Simulate work
result_ns = sum(range(1000000))
time.sleep(2)

end_ns = time.perf_counter_ns()

duration_ns = end_ns - start_ns

print(f"Execution time: {duration_ns} nanoseconds") # 2014075259 nanoseconds

######################
## time.monotonic() ##
######################
'''
Monotonic clock, cannot go backward
Good for measuring elapsed time
'''

# Reliable elapsed time measurement
start = time.monotonic()
time.sleep(1.5)
end = time.monotonic()

elapsed = end - start
print(f"Elapsed time: {elapsed:.3f} seconds") # Elapsed time: 1.501 seconds

'''
time.monotonic() vs time.time():
# time.time(): System wall-clock time, can jump backwards if system clock is adjusted
# time.monotonic(): Guaranteed to never decrease, ideal for measuring elapsed time
'''

#########################
## time.process_time() ##
#########################
'''CPU time used by the process, excludes sleep time'''

start = time.process_time()

# Simulate CPU work
result = sum(range(1000000))
time.sleep(2)  # Sleep time is not counted

end = time.process_time()

cpu_time = end - start

print(f"CPU time used: {cpu_time:.6f} seconds") # 0.009294 seconds
                                                # 2 seconds of sleep not included

########################
## time.thread_time() ##
########################
'''CPU time used by the current thread'''

import threading

def worker():
    start = time.thread_time()
    # Thread work
    sum(range(100000))
    end = time.thread_time()
    print(f"Thread CPU time: {end - start:.6f}s")

thread = threading.Thread(target=worker)
thread.start()
thread.join()
# Thread CPU time: 0.001383s


