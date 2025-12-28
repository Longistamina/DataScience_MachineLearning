'''

The pandas.Timestamp class is pandas' replacement for Python's datetime.datetime object.

It's the fundamental building block for time series data in pandas and is interchangeable 
with Python's datetime.datetime in most cases.

Key Features: Nanosecond precision, timezone awareness, extensive date/time manipulation methods

######################################################

0. Creating Timestamp objects:
   + pd.Timestamp(ts_input): Create from string, int, float, or datetime
   + pd.Timestamp(year, month, day, ...): Create from components
   + pd.Timestamp.now(): Current time
   + pd.Timestamp.today(): Today's date
   + pd.Timestamp.utcnow(): Current UTC time

1. Basic Timestamp attributes:
   + .year, .month, .day
   + .hour, .minute, .second
   + .microsecond, .nanosecond
   + .dayofweek, .dayofyear
   + .quarter, .week

2. Boolean properties:
   + .is_month_start, .is_month_end
   + .is_quarter_start, .is_quarter_end
   + .is_year_start, .is_year_end
   + .is_leap_year

3. Date/Time extraction methods:
   + .date(): Extract date object
   + .time(): Extract time object
   + .timetz(): Extract time with timezone
   + .to_datetime(): Convert to Python datetime
   + .to_datetime64(): Convert to numpy datetime64

4. String representation and formatting:
   + .isoformat(): ISO 8601 format
   + .strftime(format): Custom formatting
   + .day_name(): Day name
   + .month_name(): Month name
   + .ctime(): C-style string

5. Timezone operations:
   + .tz: Get timezone info
   + .tz_localize(tz): Assign timezone to naive timestamp
   + .tz_convert(tz): Convert between timezones
   + .tzname(): Timezone name
   + .utcoffset(): UTC offset
   + .dst(): Daylight saving time info

6. Time manipulation methods:
   + .replace(): Replace components
   + .round(freq): Round to frequency
   + .floor(freq): Floor to frequency
   + .ceil(freq): Ceil to frequency
   + .normalize(): Set time to midnight

7. Timestamp construction from special formats:
   + .fromtimestamp(ts): From POSIX timestamp
   + .fromisoformat(string): From ISO format string
   + .fromordinal(ordinal): From proleptic Gregorian ordinal

8. Conversions and transformations:
   + .to_period(freq): Convert to Period
   + .to_julian_date(): Convert to Julian date
   + .to_numpy(): Convert to numpy datetime64
   + .timestamp(): Get POSIX timestamp
   + .toordinal(): Get proleptic Gregorian ordinal

9. ISO calendar operations:
   + .isocalendar(): ISO year, week, weekday tuple
   + .isoweekday(): ISO weekday (1=Monday)
   + .weekday(): Weekday (0=Monday)

10. Arithmetic and comparisons:
    + Timestamps support +/- with timedeltas
    + Timestamps support comparison operators (<, >, ==, etc.)
    + Can calculate differences between timestamps

'''

###################################

'''

COMMON UNIT CODES FOR TIMESTAMP CONSTRUCTION:

'D' - Day
'h' - Hour
'm' - Minute (use 'min' for timedelta)
's' - Second
'ms' - Millisecond
'us' - Microsecond
'ns' - Nanosecond (default)

'''

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

#-------------------------------------------------------------------------------------------------------------#
#------------------------------------ 0. Creating Timestamp objects -----------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

'''
#--------------------------
## Creating from strings
#--------------------------
'''

#####################################
## pd.Timestamp() from string input ##
#####################################

# Basic string formats
ts1 = pd.Timestamp('2023-01-15')
print(ts1)
# 2023-01-15 00:00:00

ts2 = pd.Timestamp('2023-01-15 14:30:45')
print(ts2)
# 2023-01-15 14:30:45

ts3 = pd.Timestamp('2023-01-15T14:30:45')  # ISO format
print(ts3)
# 2023-01-15 14:30:45

ts4 = pd.Timestamp('January 15, 2023')
print(ts4)
# 2023-01-15 00:00:00

# With timezone
ts5 = pd.Timestamp('2023-01-15 14:30:45', tz='US/Eastern')
print(ts5)
# 2023-01-15 14:30:45-05:00
# dtype: timestamp[ns, US/Eastern]

'''
#--------------------------
## Creating from numeric input
#--------------------------
'''

##############################################
## pd.Timestamp() from Unix epoch (seconds) ##
##############################################

# From integer (Unix timestamp in specified unit)
ts_epoch = pd.Timestamp(1513393355, unit='s')
print(ts_epoch)
# 2017-12-16 03:02:35

# From float (fractional seconds)
ts_epoch_float = pd.Timestamp(1513393355.5, unit='s')
print(ts_epoch_float)
# 2017-12-16 03:02:35.500000

# Different units
ts_ms = pd.Timestamp(1513393355000, unit='ms')
print(ts_ms)
# 2017-12-16 03:02:35

ts_ns = pd.Timestamp(1513393355000000000, unit='ns')
print(ts_ns)
# 2017-12-16 03:02:35

'''
#--------------------------
## Creating from components
#--------------------------
'''

########################################
## pd.Timestamp() with year, month, day ##
########################################

# Basic date components
ts_components = pd.Timestamp(year=2023, month=1, day=15)
print(ts_components)
# 2023-01-15 00:00:00

# With time components
ts_full = pd.Timestamp(year=2023, month=1, day=15, hour=14, minute=30, second=45)
print(ts_full)
# 2023-01-15 14:30:45

# With microseconds and nanoseconds
ts_precise = pd.Timestamp(year=2023, month=1, day=15, hour=14, minute=30, 
                          second=45, microsecond=123456, nanosecond=789)
print(ts_precise)
# 2023-01-15 14:30:45.123456789

# With timezone
ts_tz = pd.Timestamp(year=2023, month=1, day=15, hour=14, tz='Asia/Seoul')
print(ts_tz)
# 2023-01-15 14:00:00+09:00

'''
#--------------------------
## Current time methods
#--------------------------
'''

####################
## pd.Timestamp.now() ##
####################

# Get current local time
ts_now = pd.Timestamp.now()
print(ts_now)
# 2025-12-28 17:20:15.123456 (example output)

# Get current time in specific timezone
ts_now_utc = pd.Timestamp.now(tz='UTC')
print(ts_now_utc)
# 2025-12-28 08:20:15.123456+00:00 (example output)

ts_now_tokyo = pd.Timestamp.now(tz='Asia/Tokyo')
print(ts_now_tokyo)
# 2025-12-28 17:20:15.123456+09:00 (example output)

######################
## pd.Timestamp.today() ##
######################

# Get today's date (equivalent to now() without timezone)
ts_today = pd.Timestamp.today()
print(ts_today)
# 2025-12-28 17:20:15.123456 (example output)

#######################
## pd.Timestamp.utcnow() ##
#######################

# Get current UTC time
ts_utcnow = pd.Timestamp.utcnow()
print(ts_utcnow)
# 2025-12-28 08:20:15.123456 (example output, no timezone info)

'''
#--------------------------
## From Python datetime
#--------------------------
'''

#########################################
## pd.Timestamp() from datetime object ##
#########################################

# Convert Python datetime to Timestamp
dt = datetime(2023, 1, 15, 14, 30, 45)
ts_from_dt = pd.Timestamp(dt)
print(ts_from_dt)
# 2023-01-15 14:30:45

print(type(ts_from_dt))
# <class 'pandas._libs.tslibs.timestamps.Timestamp'>

#-------------------------------------------------------------------------------------------------------------#
#------------------------------------ 1. Basic Timestamp attributes -----------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

ts = pd.Timestamp('2023-03-15 14:30:45.123456789', tz='US/Pacific')
print(ts)
# 2023-03-15 14:30:45.123456789-07:00

##############################
## .year, .month, .day ##
##############################

print(ts.year)
# 2023

print(ts.month)
# 3

print(ts.day)
# 15

###################################
## .hour, .minute, .second ##
###################################

print(ts.hour)
# 14

print(ts.minute)
# 30

print(ts.second)
# 45

######################################
## .microsecond, .nanosecond ##
######################################

print(ts.microsecond)
# 123456

print(ts.nanosecond)
# 789

#######################################
## .dayofweek, .dayofyear, .week ##
#######################################

# Day of week (Monday=0, Sunday=6)
print(ts.dayofweek)
# 2  (Wednesday)

# Alternative: .weekday() (same as dayofweek)
print(ts.weekday())
# 2

# Day of year (1 to 365 or 366)
print(ts.dayofyear)
# 74

# Week number
print(ts.week)
# 11

##############
## .quarter ##
##############

# Quarter of the year (1 to 4)
print(ts.quarter)
# 1

##################
## .days_in_month ##
##################

# Number of days in the month
print(ts.days_in_month)
# 31

# Alternative: .daysinmonth
print(ts.daysinmonth)
# 31

#-------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 2. Boolean properties ----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

ts_month_start = pd.Timestamp('2023-03-01')
ts_month_end = pd.Timestamp('2023-03-31')
ts_quarter_start = pd.Timestamp('2023-01-01')
ts_quarter_end = pd.Timestamp('2023-03-31')
ts_year_start = pd.Timestamp('2023-01-01')
ts_year_end = pd.Timestamp('2023-12-31')
ts_leap = pd.Timestamp('2024-02-29')

##########################################
## .is_month_start, .is_month_end ##
##########################################

print(ts_month_start.is_month_start)
# True

print(ts_month_end.is_month_end)
# True

print(pd.Timestamp('2023-03-15').is_month_start)
# False

##############################################
## .is_quarter_start, .is_quarter_end ##
##############################################

print(ts_quarter_start.is_quarter_start)
# True

print(ts_quarter_end.is_quarter_end)
# True

print(pd.Timestamp('2023-02-15').is_quarter_start)
# False

##########################################
## .is_year_start, .is_year_end ##
##########################################

print(ts_year_start.is_year_start)
# True

print(ts_year_end.is_year_end)
# True

print(pd.Timestamp('2023-06-15').is_year_start)
# False

######################
## .is_leap_year ##
######################

print(ts_leap.is_leap_year)
# True (2024 is a leap year)

print(pd.Timestamp('2023-01-01').is_leap_year)
# False (2023 is not a leap year)

#-------------------------------------------------------------------------------------------------------------#
#------------------------------ 3. Date/Time extraction methods ----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

ts = pd.Timestamp('2023-03-15 14:30:45', tz='Asia/Seoul')
print(ts)
# 2023-03-15 14:30:45+09:00

##############
## .date() ##
##############

# Extract date object (loses time and timezone info)
date_obj = ts.date()
print(date_obj)
# 2023-03-15

print(type(date_obj))
# <class 'datetime.date'>

##############
## .time() ##
##############

# Extract time object (loses date and timezone info)
time_obj = ts.time()
print(time_obj)
# 14:30:45

print(type(time_obj))
# <class 'datetime.time'>

################
## .timetz() ##
################

# Extract time object with timezone info
timetz_obj = ts.timetz()
print(timetz_obj)
# 14:30:45+09:00

print(type(timetz_obj))
# <class 'datetime.time'>

######################
## .to_datetime() ##
######################

# Convert to Python datetime object
dt = ts.to_pydatetime()
print(dt)
# 2023-03-15 14:30:45+09:00

print(type(dt))
# <class 'datetime.datetime'>

########################
## .to_datetime64() ##
########################

# Convert to numpy datetime64
dt64 = ts.to_datetime64()
print(dt64)
# 2023-03-15T05:30:45.000000000

print(type(dt64))
# <class 'numpy.datetime64'>

###################
## .to_numpy() ##
###################

# Convert to numpy datetime64 (alternative method)
np_dt = ts.to_numpy()
print(np_dt)
# 2023-03-15T05:30:45.000000000

print(type(np_dt))
# <class 'numpy.datetime64'>

#-------------------------------------------------------------------------------------------------------------#
#---------------------------- 4. String representation and formatting ---------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

ts = pd.Timestamp('2023-03-15 14:30:45', tz='US/Pacific')
print(ts)
# 2023-03-15 14:30:45-07:00

###################
## .isoformat() ##
###################

# ISO 8601 format
iso_str = ts.isoformat()
print(iso_str)
# 2023-03-15T14:30:45-07:00

# With separator and timespec
iso_str2 = ts.isoformat(sep=' ', timespec='seconds')
print(iso_str2)
# 2023-03-15 14:30:45-07:00

##########################
## .strftime(format) ##
##########################

# Custom formatting using strftime codes
# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

formatted1 = ts.strftime('%Y-%m-%d')
print(formatted1)
# 2023-03-15

formatted2 = ts.strftime('%d/%m/%Y %H:%M:%S')
print(formatted2)
# 15/03/2023 14:30:45

formatted3 = ts.strftime('%A, %B %d, %Y')
print(formatted3)
# Wednesday, March 15, 2023

formatted4 = ts.strftime('%I:%M %p on %b %d, %Y')
print(formatted4)
# 02:30 PM on Mar 15, 2023

####################
## .day_name() ##
####################

# Get day name
day = ts.day_name()
print(day)
# Wednesday

# With locale (requires locale parameter)
day_locale = ts.day_name(locale='en_US')
print(day_locale)
# Wednesday

######################
## .month_name() ##
######################

# Get month name
month = ts.month_name()
print(month)
# March

# With locale
month_locale = ts.month_name(locale='en_US')
print(month_locale)
# March

###############
## .ctime() ##
###############

# C-style string representation
ctime_str = ts.ctime()
print(ctime_str)
# Wed Mar 15 14:30:45 2023

#################
## str() ##
#################

# String representation
str_repr = str(ts)
print(str_repr)
# 2023-03-15 14:30:45-07:00

#-------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 5. Timezone operations -----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

'''
#--------------------------
## Get timezone info
#--------------------------
'''

ts_naive = pd.Timestamp('2023-03-15 14:30:45')
ts_aware = pd.Timestamp('2023-03-15 14:30:45', tz='US/Pacific')

##########
## .tz ##
##########

# Get timezone info
print(ts_naive.tz)
# None

print(ts_aware.tz)
# US/Pacific

print(type(ts_aware.tz))
# <class 'pytz.tzfile.America/Los_Angeles'>

'''
#--------------------------
## Localizing timezone
#--------------------------
'''

#######################
## .tz_localize(tz) ##
#######################

# Assign timezone to naive timestamp
ts_localized = ts_naive.tz_localize('Asia/Tokyo')
print(ts_localized)
# 2023-03-15 14:30:45+09:00

# This assumes the time was in Tokyo timezone and adds the UTC offset

# Cannot localize already timezone-aware timestamp
# ts_aware.tz_localize('UTC')  # Raises TypeError

# To handle ambiguous times during DST transitions
ts_dst = pd.Timestamp('2023-11-05 01:30:00')
ts_dst_first = ts_dst.tz_localize('US/Eastern', ambiguous=True)  # First occurrence
print(ts_dst_first)
# 2023-11-05 01:30:00-04:00

ts_dst_second = ts_dst.tz_localize('US/Eastern', ambiguous=False)  # Second occurrence
print(ts_dst_second)
# 2023-11-05 01:30:00-05:00

'''
#--------------------------
## Converting between timezones
#--------------------------
'''

######################
## .tz_convert(tz) ##
######################

# Convert timezone-aware timestamp to another timezone
ts_tokyo = ts_aware.tz_convert('Asia/Tokyo')
print(ts_tokyo)
# 2023-03-16 06:30:45+09:00

ts_utc = ts_aware.tz_convert('UTC')
print(ts_utc)
# 2023-03-15 21:30:45+00:00

ts_london = ts_aware.tz_convert('Europe/London')
print(ts_london)
# 2023-03-15 21:30:45+00:00

# Cannot convert naive timestamp
# ts_naive.tz_convert('UTC')  # Raises TypeError

'''
#--------------------------
## Other timezone methods
#--------------------------
'''

################
## .tzname() ##
################

# Get timezone name
print(ts_aware.tzname())
# PDT (Pacific Daylight Time)

###################
## .utcoffset() ##
###################

# Get UTC offset as timedelta
offset = ts_aware.utcoffset()
print(offset)
# -1 day, 17:00:00 (equivalent to -7:00:00)

print(type(offset))
# <class 'datetime.timedelta'>

############
## .dst() ##
############

# Get daylight saving time adjustment
dst_info = ts_aware.dst()
print(dst_info)
# 1:00:00 (1 hour DST adjustment)

#-------------------------------------------------------------------------------------------------------------#
#------------------------------------ 6. Time manipulation methods -------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

ts = pd.Timestamp('2023-03-15 14:45:23.123456789')
print(ts)
# 2023-03-15 14:45:23.123456789

'''
#--------------------------
## Replacing components
#--------------------------
'''

###############
## .replace() ##
###############

# Replace specific components
ts_new_year = ts.replace(year=2024)
print(ts_new_year)
# 2024-03-15 14:45:23.123456789

ts_new_month = ts.replace(month=12)
print(ts_new_month)
# 2023-12-15 14:45:23.123456789

ts_new_time = ts.replace(hour=0, minute=0, second=0, microsecond=0, nanosecond=0)
print(ts_new_time)
# 2023-03-15 00:00:00

# Replace multiple components at once
ts_replaced = ts.replace(year=2024, month=12, day=25, hour=0)
print(ts_replaced)
# 2024-12-25 00:45:23.123456789

'''
#--------------------------
## Rounding methods
#--------------------------
'''

#################
## .round(freq) ##
#################

# Round to nearest frequency
ts_round_hour = ts.round('h')
print(ts_round_hour)
# 2023-03-15 15:00:00 (45 minutes rounds up to next hour)

ts_round_min = ts.round('min')
print(ts_round_min)
# 2023-03-15 14:45:00 (23 seconds rounds down)

ts_round_day = ts.round('D')
print(ts_round_day)
# 2023-03-15 00:00:00

ts_round_month = ts.round('ME')  # Month end
print(ts_round_month)
# 2023-03-31 00:00:00

#################
## .floor(freq) ##
#################

# Round down to frequency
ts_floor_hour = ts.floor('h')
print(ts_floor_hour)
# 2023-03-15 14:00:00

ts_floor_min = ts.floor('min')
print(ts_floor_min)
# 2023-03-15 14:45:00

ts_floor_day = ts.floor('D')
print(ts_floor_day)
# 2023-03-15 00:00:00

#################
## .ceil(freq) ##
#################

# Round up to frequency
ts_ceil_hour = ts.ceil('h')
print(ts_ceil_hour)
# 2023-03-15 15:00:00

ts_ceil_min = ts.ceil('min')
print(ts_ceil_min)
# 2023-03-15 14:46:00

ts_ceil_day = ts.ceil('D')
print(ts_ceil_day)
# 2023-03-16 00:00:00

'''
#--------------------------
## Normalization
#--------------------------
'''

###################
## .normalize() ##
###################

# Set time to midnight (00:00:00)
ts_normalized = ts.normalize()
print(ts_normalized)
# 2023-03-15 00:00:00

# Useful for grouping by date without considering time
ts_with_tz = pd.Timestamp('2023-03-15 14:45:23', tz='US/Pacific')
ts_norm_tz = ts_with_tz.normalize()
print(ts_norm_tz)
# 2023-03-15 00:00:00-07:00

#-------------------------------------------------------------------------------------------------------------#
#----------------------- 7. Timestamp construction from special formats --------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

'''
#--------------------------
## From POSIX timestamp
#--------------------------
'''

############################
## .fromtimestamp(ts, tz) ##
############################

# Create Timestamp from POSIX timestamp (seconds since epoch)
ts_from_posix = pd.Timestamp.fromtimestamp(1678896323)
print(ts_from_posix)
# 2023-03-15 14:45:23 (actual output depends on local timezone)

# With timezone
ts_from_posix_utc = pd.Timestamp.fromtimestamp(1678896323, tz='UTC')
print(ts_from_posix_utc)
# 2023-03-15 14:45:23+00:00

ts_from_posix_tokyo = pd.Timestamp.fromtimestamp(1678896323, tz='Asia/Tokyo')
print(ts_from_posix_tokyo)
# 2023-03-15 23:45:23+09:00

'''
#--------------------------
## From ISO format
#--------------------------
'''

############################
## .fromisoformat(string) ##
############################

# Create Timestamp from ISO 8601 format string
ts_iso = pd.Timestamp.fromisoformat('2023-03-15T14:45:23')
print(ts_iso)
# 2023-03-15 14:45:23

ts_iso_tz = pd.Timestamp.fromisoformat('2023-03-15T14:45:23+09:00')
print(ts_iso_tz)
# 2023-03-15 14:45:23+09:00

'''
#--------------------------
## From ordinal
#--------------------------
'''

#############################
## .fromordinal(ordinal, tz) ##
#############################

# Create Timestamp from proleptic Gregorian ordinal
# Day 1 is January 1 of year 1
ts_ordinal = pd.Timestamp.fromordinal(738598)
print(ts_ordinal)
# 2023-03-15 00:00:00

# With timezone
ts_ordinal_tz = pd.Timestamp.fromordinal(738598, tz='Asia/Seoul')
print(ts_ordinal_tz)
# 2023-03-15 00:00:00+09:00

'''
#--------------------------
## From ISO calendar
#--------------------------
'''

###########################################
## .fromisocalendar(year, week, day) ##
###########################################

# Create Timestamp from ISO year, week number, and weekday
# Week 1 is the first week with a Thursday
# Day 1 = Monday, Day 7 = Sunday
ts_iso_cal = pd.Timestamp.fromisocalendar(2023, 11, 3)
print(ts_iso_cal)
# 2023-03-15 00:00:00

#-------------------------------------------------------------------------------------------------------------#
#------------------------------ 8. Conversions and transformations ------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

ts = pd.Timestamp('2023-03-15 14:45:23', tz='US/Pacific')
print(ts)
# 2023-03-15 14:45:23-07:00

'''
#--------------------------
## To Period
#--------------------------
'''

########################
## .to_period(freq) ##
########################

# Convert to Period object
period_day = ts.to_period('D')
print(period_day)
# 2023-03-15

print(type(period_day))
# <class 'pandas._libs.tslibs.period.Period'>

period_month = ts.to_period('M')
print(period_month)
# 2023-03

period_quarter = ts.to_period('Q')
print(period_quarter)
# 2023Q1

'''
#--------------------------
## To Julian date
#--------------------------
'''

#########################
## .to_julian_date() ##
#########################

# Convert to Julian date
julian_date = ts.to_julian_date()
print(julian_date)
# 2460018.398645833

print(type(julian_date))
# <class 'float'>

'''
#--------------------------
## To timestamps
#--------------------------
'''

##################
## .timestamp() ##
##################

# Get POSIX timestamp (seconds since epoch)
posix_ts = ts.timestamp()
print(posix_ts)
# 1678918523.0

print(type(posix_ts))
# <class 'float'>

'''
#--------------------------
## To ordinal
#--------------------------
'''

##################
## .toordinal() ##
##################

# Get proleptic Gregorian ordinal
ordinal = ts.toordinal()
print(ordinal)
# 738598

print(type(ordinal))
# <class 'int'>

'''
#--------------------------
## To time tuple
#--------------------------
'''

##################
## .timetuple() ##
##################

# Get time tuple (like time.localtime())
time_tuple = ts.timetuple()
print(time_tuple)
# time.struct_time(tm_year=2023, tm_mon=3, tm_mday=15, tm_hour=14, tm_min=45, tm_sec=23, tm_wday=2, tm_yday=74, tm_isdst=-1)

####################
## .utctimetuple() ##
####################

# Get UTC time tuple
utc_time_tuple = ts.utctimetuple()
print(utc_time_tuple)
# time.struct_time(tm_year=2023, tm_mon=3, tm_mday=15, tm_hour=21, tm_min=45, tm_sec=23, tm_wday=2, tm_yday=74, tm_isdst=0)

#-------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 9. ISO calendar operations -------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

ts = pd.Timestamp('2023-03-15 14:45:23')
print(ts)
# 2023-03-15 14:45:23

#######################
## .isocalendar() ##
#######################

# Get ISO calendar components as named tuple
iso_cal = ts.isocalendar()
print(iso_cal)
# datetime.IsoCalendarDate(year=2023, week=11, weekday=3)

print(iso_cal.year)
# 2023

print(iso_cal.week)
# 11

print(iso_cal.weekday)
# 3 (Wednesday in ISO format: Monday=1, Sunday=7)

#####################
## .isoweekday() ##
#####################

# ISO weekday (Monday=1, Sunday=7)
iso_weekday = ts.isoweekday()
print(iso_weekday)
# 3 (Wednesday)

#################
## .weekday() ##
#################

# Python weekday (Monday=0, Sunday=6)
weekday = ts.weekday()
print(weekday)
# 2 (Wednesday)

#-------------------------------------------------------------------------------------------------------------#
#------------------------------ 10. Arithmetic and comparisons ----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

ts1 = pd.Timestamp('2023-03-15 14:30:00')
ts2 = pd.Timestamp('2023-03-20 18:45:30')

'''
#--------------------------
## Arithmetic with timedeltas
#--------------------------
'''

######################################
## Adding and subtracting timedeltas ##
######################################

# Add timedelta
td = pd.Timedelta(days=5)
ts_future = ts1 + td
print(ts_future)
# 2023-03-20 14:30:00

# Add multiple components
td_complex = pd.Timedelta(days=5, hours=3, minutes=15)
ts_future2 = ts1 + td_complex
print(ts_future2)
# 2023-03-20 17:45:00

# Subtract timedelta
ts_past = ts1 - pd.Timedelta(days=10)
print(ts_past)
# 2023-03-05 14:30:00

# Using Python timedelta
from datetime import timedelta
ts_future3 = ts1 + timedelta(weeks=2)
print(ts_future3)
# 2023-03-29 14:30:00

'''
#--------------------------
## Difference between timestamps
#--------------------------
'''

####################################
## Subtracting timestamps ##
####################################

# Calculate difference
diff = ts2 - ts1
print(diff)
# 5 days 04:15:30

print(type(diff))
# <class 'pandas._libs.tslibs.timedeltas.Timedelta'>

# Extract components
print(diff.days)
# 5

print(diff.seconds)
# 15330 (4 hours * 3600 + 15 minutes * 60 + 30 seconds)

print(diff.total_seconds())
# 447330.0

'''
#--------------------------
## Comparisons
#--------------------------
'''

####################################
## Comparing timestamps ##
####################################

print(ts1 < ts2)
# True

print(ts1 > ts2)
# False

print(ts1 == ts1)
# True

print(ts1 != ts2)
# True

print(ts1 <= pd.Timestamp('2023-03-15 14:30:00'))
# True

print(ts1 >= pd.Timestamp('2023-03-15'))
# True

# Can compare with strings (they get converted)
print(ts1 > '2023-01-01')
# True

# Find min/max
print(min(ts1, ts2))
# 2023-03-15 14:30:00

print(max(ts1, ts2))
# 2023-03-20 18:45:30

'''
#--------------------------
## Using in ranges
#--------------------------
'''

####################################
## Checking if timestamp in range ##
####################################

start = pd.Timestamp('2023-03-01')
end = pd.Timestamp('2023-03-31')

print(start <= ts1 <= end)
# True

# Using between (for series operations)
dates = pd.Series([ts1, ts2, pd.Timestamp('2023-04-01')])
in_range = dates.between(start, end)
print(in_range)
# 0     True
# 1     True
# 2    False
# dtype: bool

#-------------------------------------------------------------------------------------------------------------#
#--------------------------------- Additional Useful Examples -----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

'''
#--------------------------
## Parsing different formats
#--------------------------
'''

# Various string formats that work
examples = [
    '2023-03-15',
    '2023/03/15',
    '03-15-2023',
    '03/15/2023',
    'March 15, 2023',
    '15-Mar-2023',
    '2023-03-15 14:30:45',
    '2023-03-15T14:30:45',
    '2023-03-15 14:30:45.123456',
    '2023-03-15 14:30:45+00:00',
]

for fmt in examples:
    ts = pd.Timestamp(fmt)
    print(f"{fmt:30s} -> {ts}")

# 2023-03-15                     -> 2023-03-15 00:00:00
# 2023/03/15                     -> 2023-03-15 00:00:00
# 03-15-2023                     -> 2023-03-15 00:00:00
# 03/15/2023                     -> 2023-03-15 00:00:00
# March 15, 2023                 -> 2023-03-15 00:00:00
# 15-Mar-2023                    -> 2023-03-15 00:00:00
# 2023-03-15 14:30:45            -> 2023-03-15 14:30:45
# 2023-03-15T14:30:45            -> 2023-03-15 14:30:45
# 2023-03-15 14:30:45.123456     -> 2023-03-15 14:30:45.123456
# 2023-03-15 14:30:45+00:00      -> 2023-03-15 14:30:45+00:00

'''
#--------------------------
## Working with resolution
#--------------------------
'''

# Timestamps have nanosecond resolution
ts_ns = pd.Timestamp('2023-03-15 14:30:45.123456789')
print(ts_ns)
# 2023-03-15 14:30:45.123456789

# Get resolution
print(ts_ns._value)  # Internal nanosecond representation
# 1678896645123456789 (example)

'''
#--------------------------
## DST handling examples
#--------------------------
'''

# Create timestamp during DST transition
# In US, DST starts on second Sunday of March at 2 AM
ts_before_dst = pd.Timestamp('2023-03-12 01:00:00', tz='US/Eastern')
print(ts_before_dst)
# 2023-03-12 01:00:00-05:00 (EST)

ts_after_dst = pd.Timestamp('2023-03-12 03:00:00', tz='US/Eastern')
print(ts_after_dst)
# 2023-03-12 03:00:00-04:00 (EDT)

# 2 AM doesn't exist on this day (nonexistent time)
# By default, pandas handles this automatically
ts_nonexistent = pd.Timestamp('2023-03-12 02:30:00', tz='US/Eastern')
print(ts_nonexistent)
# 2023-03-12 03:30:00-04:00 (shifts forward)

'''
#--------------------------
## Frequency and business days
#--------------------------
'''

# Timestamps work with business day calendars
from pandas.tseries.offsets import BDay

ts = pd.Timestamp('2023-03-17')  # Friday
ts_next_bday = ts + BDay(1)
print(ts_next_bday)
# 2023-03-20 00:00:00 (Monday, skipping weekend)

ts_prev_bday = ts - BDay(1)
print(ts_prev_bday)
# 2023-03-16 00:00:00 (Thursday)

# Multiple business days
ts_5_bdays = ts + BDay(5)
print(ts_5_bdays)
# 2023-03-24 00:00:00 (Next Friday)
