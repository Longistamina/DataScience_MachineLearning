'''

The pandas.Timedelta class represents a duration, the difference between two dates or times.

It's the pandas equivalent of Python's datetime.timedelta and is interchangeable 
with it in most cases.

Key Features: Nanosecond precision, flexible construction, arithmetic operations with timestamps

######################################################

0. Creating Timedelta objects:
   + pd.Timedelta(value, unit): Create from value and unit
   + pd.Timedelta(days=, hours=, ...): Create from keyword arguments
   + pd.Timedelta(string): Create from string representation
   + pd.to_timedelta(): Convert Series/array to timedelta

1. Basic Timedelta attributes:
   + .days: Number of days
   + .seconds: Number of seconds (0-86399 in one day)
   + .microseconds: Number of microseconds (0-999999 in one second)
   + .nanoseconds: Number of nanoseconds (0-999 in one microsecond)
   + .components: All components as named tuple

2. Time unit properties:
   + .total_seconds(): Total duration in seconds
   + ._value: Internal nanosecond representation
   + .resolution_string: String representation of resolution
   + .asm8: NumPy timedelta64 view

3. Conversion methods:
   + .to_pytimedelta(): Convert to Python timedelta
   + .to_timedelta64(): Convert to NumPy timedelta64
   + .to_numpy(): Convert to NumPy timedelta64
   + .as_unit(unit): Convert to different unit

4. Rounding methods:
   + .round(freq): Round to frequency
   + .floor(freq): Floor to frequency
   + .ceil(freq): Ceil to frequency

5. String representation:
   + .isoformat(): ISO 8601 duration format
   + str(): String representation
   + repr(): Official representation

6. Arithmetic operations:
   + Addition and subtraction with Timedelta
   + Multiplication and division by scalars
   + Using with Timestamps
   + Absolute value and negation

7. Comparison operations:
   + Comparing Timedeltas
   + Minimum and maximum
   + Sorting

8. Working with Series and arrays:
   + pd.to_timedelta(): Convert to timedelta
   + .dt accessor for Series
   + Vectorized operations

9. Special Timedelta values:
   + pd.NaT: Not a Time
   + Handling missing values

10. Practical examples and use cases:
    + Time differences
    + Time windows
    + Business logic with durations

'''

###################################

'''

COMMON UNIT CODES FOR TIMEDELTA CONSTRUCTION:

'W' or 'weeks' - Week
'D' or 'days' or 'day' - Day
'h' or 'hours' or 'hour' or 'hr' - Hour
'min' or 'minutes' or 'minute' - Minute (use 'min', not 'm')
's' or 'seconds' or 'second' or 'sec' - Second
'ms' or 'milliseconds' or 'millisecond' or 'millis' - Millisecond
'us' or 'microseconds' or 'microsecond' or 'micros' - Microsecond
'ns' or 'nanoseconds' or 'nanosecond' or 'nanos' - Nanosecond (default)

VALID FREQUENCIES FOR ROUNDING (FIXED FREQUENCIES ONLY):

'D' - Day
'h' - Hour
'min' - Minute
's' - Second
'ms' - Millisecond
'us' - Microsecond
'ns' - Nanosecond

'''

import pandas as pd
import numpy as np
from datetime import timedelta, datetime

#-------------------------------------------------------------------------------------------------------------#
#------------------------------------ 0. Creating Timedelta objects -----------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

'''
#--------------------------
## Creating from value and unit
#--------------------------
'''

#####################################
## pd.Timedelta(value, unit) ##
#####################################

# Create Timedelta with value and unit
td1 = pd.Timedelta(1, 'D')  # 1 day
print(td1)
# 1 days 00:00:00

td2 = pd.Timedelta(5, 'h')  # 5 hours
print(td2)
# 0 days 05:00:00

td3 = pd.Timedelta(30, 'min')  # 30 minutes
print(td3)
# 0 days 00:30:00

td4 = pd.Timedelta(1000, 'ms')  # 1000 milliseconds = 1 second
print(td4)
# 0 days 00:00:01

td5 = pd.Timedelta(500, 'us')  # 500 microseconds
print(td5)
# 0 days 00:00:00.000500

# Using full unit names
td6 = pd.Timedelta(2, 'weeks')
print(td6)
# 14 days 00:00:00

td7 = pd.Timedelta(45, 'seconds')
print(td7)
# 0 days 00:00:45

'''
#--------------------------
## Creating from keyword arguments
#--------------------------
'''

#####################################
## pd.Timedelta(days=, hours=, ...) ##
#####################################

# Create with single keyword argument
td_days = pd.Timedelta(days=3)
print(td_days)
# 3 days 00:00:00

td_hours = pd.Timedelta(hours=12)
print(td_hours)
# 0 days 12:00:00

# Create with multiple keyword arguments
td_complex = pd.Timedelta(days=1, hours=2, minutes=30, seconds=45)
print(td_complex)
# 1 days 02:30:45

td_precise = pd.Timedelta(days=2, hours=5, minutes=30, seconds=15, 
                          milliseconds=500, microseconds=250)
print(td_precise)
# 2 days 05:30:15.500250

# Using weeks
td_weeks = pd.Timedelta(weeks=2, days=3)
print(td_weeks)
# 17 days 00:00:00

'''
#--------------------------
## Creating from strings
#--------------------------
'''

#####################################
## pd.Timedelta(string) ##
#####################################

# Various string formats
td_str1 = pd.Timedelta('1 days')
print(td_str1)
# 1 days 00:00:00

td_str2 = pd.Timedelta('2 days 03:00:00')
print(td_str2)
# 2 days 03:00:00

td_str3 = pd.Timedelta('5 days 12:30:45')
print(td_str3)
# 5 days 12:30:45

td_str4 = pd.Timedelta('1 day 2 hours 30 minutes')
print(td_str4)
# 1 days 02:30:00

# Short forms
td_short1 = pd.Timedelta('1D')
print(td_short1)
# 1 days 00:00:00

td_short2 = pd.Timedelta('2h30min')
print(td_short2)
# 0 days 02:30:00

td_short3 = pd.Timedelta('30s')
print(td_short3)
# 0 days 00:00:30

'''
#--------------------------
## Creating from Python timedelta
#--------------------------
'''

#####################################
## pd.Timedelta(timedelta) ##
#####################################

# Convert Python timedelta to pandas Timedelta
py_td = timedelta(days=3, hours=5, minutes=30)
pd_td = pd.Timedelta(py_td)
print(pd_td)
# 3 days 05:30:00

print(type(pd_td))
# <class 'pandas._libs.tslibs.timedeltas.Timedelta'>

'''
#--------------------------
## Converting Series to timedelta
#--------------------------
'''

#####################################
## pd.to_timedelta() ##
#####################################

# Convert string Series to timedelta
s_str = pd.Series(['1 days', '2 days 03:00:00', '4 days 05:30:00'])
s_td = pd.to_timedelta(s_str)
print(s_td)
# 0   1 days 00:00:00
# 1   2 days 03:00:00
# 2   4 days 05:30:00
# dtype: timedelta64[ns]

# Convert numeric Series with unit
s_numeric = pd.Series([1, 2.5, 4.25])
s_td_hours = pd.to_timedelta(s_numeric, unit='h')
print(s_td_hours)
# 0   0 days 01:00:00
# 1   0 days 02:30:00
# 2   0 days 04:15:00
# dtype: timedelta64[ns]

s_td_days = pd.to_timedelta(s_numeric, unit='D')
print(s_td_days)
# 0   1 days 00:00:00
# 1   2 days 12:00:00
# 2   4 days 06:00:00
# dtype: timedelta64[ns]

'''
#--------------------------
## From NumPy timedelta64
#--------------------------
'''

#####################################
## pd.Timedelta(np.timedelta64) ##
#####################################

# Convert NumPy timedelta64 to pandas Timedelta
np_td = np.timedelta64(5, 'D')
pd_td_from_np = pd.Timedelta(np_td)
print(pd_td_from_np)
# 5 days 00:00:00

np_td_hours = np.timedelta64(12, 'h')
pd_td_hours = pd.Timedelta(np_td_hours)
print(pd_td_hours)
# 0 days 12:00:00

#-------------------------------------------------------------------------------------------------------------#
#------------------------------------ 1. Basic Timedelta attributes -----------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

td = pd.Timedelta(days=5, hours=12, minutes=30, seconds=45, 
                  milliseconds=123, microseconds=456, nanoseconds=789)
print(td)
# 5 days 12:30:45.123456789

'''
#--------------------------
## Basic component attributes
#--------------------------
'''

##############
## .days ##
##############

# Get days component
print(td.days)
# 5

################
## .seconds ##
################

# Get seconds component within the day (0-86399)
# This is NOT total seconds, just the time portion
print(td.seconds)
# 45045  (12*3600 + 30*60 + 45)

#####################
## .microseconds ##
#####################

# Get microseconds component (0-999999)
print(td.microseconds)
# 123456

#####################
## .nanoseconds ##
#####################

# Get nanoseconds component (0-999)
print(td.nanoseconds)
# 789

'''
#--------------------------
## Components named tuple
#--------------------------
'''

####################
## .components ##
####################

# Get all components as a named tuple
components = td.components
print(components)
# Components(days=5, hours=12, minutes=30, seconds=45, milliseconds=123, microseconds=456, nanoseconds=789)

print(components.days)
# 5

print(components.hours)
# 12

print(components.minutes)
# 30

print(components.seconds)
# 45

print(components.milliseconds)
# 123

print(components.microseconds)
# 456

print(components.nanoseconds)
# 789

# Access as attributes
print(f"Days: {components.days}, Hours: {components.hours}, Minutes: {components.minutes}")
# Days: 5, Hours: 12, Minutes: 30

#-------------------------------------------------------------------------------------------------------------#
#------------------------------------ 2. Time unit properties -----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

td = pd.Timedelta(days=2, hours=5, minutes=30, seconds=15)
print(td)
# 2 days 05:30:15

'''
#--------------------------
## Total duration
#--------------------------
'''

#######################
## .total_seconds() ##
#######################

# Get total duration in seconds
total_secs = td.total_seconds()
print(total_secs)
# 192615.0

print(type(total_secs))
# <class 'float'>

# Can use to convert to other units
total_minutes = td.total_seconds() / 60
print(total_minutes)
# 3210.25

total_hours = td.total_seconds() / 3600
print(total_hours)
# 53.504166666666666

total_days = td.total_seconds() / 86400
print(total_days)
# 2.2293402777777777

'''
#--------------------------
## Internal representation
#--------------------------
'''

##############
## ._value ##
##############

# Get internal nanosecond representation
print(td._value)
# 192615000000000

# This is the actual stored value in nanoseconds
print(f"{td._value:,} nanoseconds")
# 192,615,000,000,000 nanoseconds

'''
#--------------------------
## Resolution
#--------------------------
'''

##########################
## .resolution_string ##
##########################

# Get resolution as string
print(td.resolution_string)
# N (nanosecond resolution)

# For different timedeltas
td_sec = pd.Timedelta(30, 's')
print(td_sec.resolution_string)
# N

'''
#--------------------------
## NumPy view
#--------------------------
'''

#############
## .asm8 ##
#############

# Get NumPy timedelta64 scalar view
np_view = td.asm8
print(np_view)
# 192615000000000 nanoseconds

print(type(np_view))
# <class 'numpy.timedelta64'>

#-------------------------------------------------------------------------------------------------------------#
#------------------------------------ 3. Conversion methods -------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

td = pd.Timedelta(days=3, hours=12, minutes=30, seconds=45)
print(td)
# 3 days 12:30:45

'''
#--------------------------
## To Python timedelta
#--------------------------
'''

#########################
## .to_pytimedelta() ##
#########################

# Convert to Python timedelta object
py_td = td.to_pytimedelta()
print(py_td)
# 3 days, 12:30:45

print(type(py_td))
# <class 'datetime.timedelta'>

# Python timedelta has limited precision (microseconds, not nanoseconds)
td_precise = pd.Timedelta(days=1, nanoseconds=500)
py_td_precise = td_precise.to_pytimedelta()
print(py_td_precise)
# 1 day, 0:00:00
# (nanoseconds are lost)

'''
#--------------------------
## To NumPy timedelta64
#--------------------------
'''

##########################
## .to_timedelta64() ##
##########################

# Convert to NumPy timedelta64
np_td = td.to_timedelta64()
print(np_td)
# 306645000000000 nanoseconds

print(type(np_td))
# <class 'numpy.timedelta64'>

###################
## .to_numpy() ##
###################

# Alternative method to convert to NumPy
np_td2 = td.to_numpy()
print(np_td2)
# 306645000000000 nanoseconds

print(type(np_td2))
# <class 'numpy.timedelta64'>

'''
#--------------------------
## Convert to different units
#--------------------------
'''

######################
## .as_unit(unit) ##
######################

# Convert to different time units
td = pd.Timedelta('1 days 12:00:00')

# Convert to seconds
td_seconds = td.as_unit('s')
print(td_seconds)
# 1 days 12:00:00

print(td_seconds._value)
# 129600 (in seconds now)

# Convert to milliseconds
td_ms = td.as_unit('ms')
print(td_ms)
# 1 days 12:00:00

print(td_ms._value)
# 129600000 (in milliseconds)

# Convert to microseconds
td_us = td.as_unit('us')
print(td_us._value)
# 129600000000 (in microseconds)

#-------------------------------------------------------------------------------------------------------------#
#------------------------------------ 4. Rounding methods ---------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

td = pd.Timedelta('2 days 14:45:23.123456789')
print(td)
# 2 days 14:45:23.123456789

'''
IMPORTANT: Rounding methods only work with FIXED frequencies!
Valid: 'D', 'h', 'min', 's', 'ms', 'us', 'ns'
'''

'''
#--------------------------
## Round to frequency
#--------------------------
'''

#################
## .round(freq) ##
#################

# Round to nearest hour
td_round_hour = td.round('h')
print(td_round_hour)
# 2 days 15:00:00

# Round to nearest minute
td_round_min = td.round('min')
print(td_round_min)
# 2 days 14:45:00

# Round to nearest second
td_round_sec = td.round('s')
print(td_round_sec)
# 2 days 14:45:23

# Round to nearest day
td_round_day = td.round('D')
print(td_round_day)
# 3 days 00:00:00

'''
#--------------------------
## Floor to frequency
#--------------------------
'''

#################
## .floor(freq) ##
#################

# Floor to hour
td_floor_hour = td.floor('h')
print(td_floor_hour)
# 2 days 14:00:00

# Floor to minute
td_floor_min = td.floor('min')
print(td_floor_min)
# 2 days 14:45:00

# Floor to second
td_floor_sec = td.floor('s')
print(td_floor_sec)
# 2 days 14:45:23

# Floor to day
td_floor_day = td.floor('D')
print(td_floor_day)
# 2 days 00:00:00

'''
#--------------------------
## Ceil to frequency
#--------------------------
'''

#################
## .ceil(freq) ##
#################

# Ceil to hour
td_ceil_hour = td.ceil('h')
print(td_ceil_hour)
# 2 days 15:00:00

# Ceil to minute
td_ceil_min = td.ceil('min')
print(td_ceil_min)
# 2 days 14:46:00

# Ceil to second
td_ceil_sec = td.ceil('s')
print(td_ceil_sec)
# 2 days 14:45:24

# Ceil to day
td_ceil_day = td.ceil('D')
print(td_ceil_day)
# 3 days 00:00:00

#-------------------------------------------------------------------------------------------------------------#
#------------------------------------ 5. String representation ----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

td = pd.Timedelta(days=3, hours=12, minutes=30, seconds=45)
print(td)
# 3 days 12:30:45

'''
#--------------------------
## ISO 8601 format
#--------------------------
'''

###################
## .isoformat() ##
###################

# Get ISO 8601 duration format
iso_str = td.isoformat()
print(iso_str)
# P3DT12H30M45S

# Breakdown of ISO format:
# P = Period
# 3D = 3 Days
# T = Time separator
# 12H = 12 Hours
# 30M = 30 Minutes
# 45S = 45 Seconds

# Different timedeltas
td_days = pd.Timedelta(days=5)
print(td_days.isoformat())
# P5D

td_time = pd.Timedelta(hours=2, minutes=30)
print(td_time.isoformat())
# PT2H30M

td_complex = pd.Timedelta(weeks=2, days=3, hours=4, minutes=30)
print(td_complex.isoformat())
# P17DT4H30M

'''
#--------------------------
## String representations
#--------------------------
'''

###############
## str() ##
###############

# Get string representation
str_repr = str(td)
print(str_repr)
# 3 days 12:30:45

################
## repr() ##
################

# Get official representation
repr_str = repr(td)
print(repr_str)
# Timedelta('3 days 12:30:45')

# This can be used to recreate the object
td_recreated = eval(repr_str)
print(td_recreated)
# 3 days 12:30:45

#-------------------------------------------------------------------------------------------------------------#
#------------------------------------ 6. Arithmetic operations ----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

'''
#--------------------------
## Addition and subtraction
#--------------------------
'''

td1 = pd.Timedelta(days=2, hours=5)
td2 = pd.Timedelta(days=1, hours=10, minutes=30)

# Add timedeltas
td_sum = td1 + td2
print(td_sum)
# 3 days 15:30:00

# Subtract timedeltas
td_diff = td1 - td2
print(td_diff)
# 0 days 18:30:00

# Can chain operations
td_result = td1 + td2 - pd.Timedelta(hours=5)
print(td_result)
# 3 days 10:30:00

'''
#--------------------------
## Multiplication and division
#--------------------------
'''

td = pd.Timedelta(days=2, hours=12)

# Multiply by scalar
td_double = td * 2
print(td_double)
# 5 days 00:00:00

td_triple = td * 3
print(td_triple)
# 7 days 12:00:00

# Multiply by float
td_half = td * 0.5
print(td_half)
# 1 days 06:00:00

td_oneandahalf = td * 1.5
print(td_oneandahalf)
# 3 days 18:00:00

# Divide by scalar
td_divided = td / 2
print(td_divided)
# 1 days 06:00:00

td_divided_float = td / 2.5
print(td_divided_float)
# 1 days 00:00:00

# Floor division
td_floor_div = td // 2
print(td_floor_div)
# 1 days 06:00:00

# Modulo
td_mod = td % pd.Timedelta(days=1)
print(td_mod)
# 0 days 12:00:00

# Divide two timedeltas (get ratio)
td1 = pd.Timedelta(days=10)
td2 = pd.Timedelta(days=2)
ratio = td1 / td2
print(ratio)
# 5.0

'''
#--------------------------
## Using with Timestamps
#--------------------------
'''

ts = pd.Timestamp('2023-03-15 14:30:00')
td = pd.Timedelta(days=5, hours=3, minutes=15)

# Add timedelta to timestamp
ts_future = ts + td
print(ts_future)
# 2023-03-20 17:45:00

# Subtract timedelta from timestamp
ts_past = ts - td
print(ts_past)
# 2023-03-10 11:15:00

# Get timedelta between two timestamps
ts1 = pd.Timestamp('2023-03-15 14:30:00')
ts2 = pd.Timestamp('2023-03-20 18:45:30')
td_diff = ts2 - ts1
print(td_diff)
# 5 days 04:15:30
print(type(td_diff))
# <class 'pandas._libs.tslibs.timedeltas.Timedelta'>

'''
#--------------------------
## Absolute value and negation
#--------------------------
'''

td = pd.Timedelta(days=-3, hours=5)
print(td)
# -3 days +05:00:00

# Absolute value
td_abs = abs(td)
print(td_abs)
# 2 days 19:00:00

# Negation
td_neg = -td
print(td_neg)
# 2 days 19:00:00

# Double negation
td_pos = pd.Timedelta(days=2, hours=5)
td_neg2 = -td_pos
print(td_neg2)
# -3 days +19:00:00

#-------------------------------------------------------------------------------------------------------------#
#------------------------------------ 7. Comparison operations ----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

td1 = pd.Timedelta(days=2, hours=5)
td2 = pd.Timedelta(days=1, hours=10)
td3 = pd.Timedelta(days=2, hours=5)

'''
#--------------------------
## Comparison operators
#--------------------------
'''

# Less than
print(td2 < td1)
# True

# Greater than
print(td1 > td2)
# True

# Equal to
print(td1 == td3)
# True

# Not equal to
print(td1 != td2)
# True

# Less than or equal
print(td2 <= td1)
# True

print(td1 <= td3)
# True

# Greater than or equal
print(td1 >= td2)
# True

'''
#--------------------------
## Minimum and maximum
#--------------------------
'''

# Find minimum
td_min = min(td1, td2, td3)
print(td_min)
# 1 days 10:00:00

# Find maximum
td_max = max(td1, td2, td3)
print(td_max)
# 2 days 05:00:00

'''
#--------------------------
## Sorting
#--------------------------
'''

# Sort list of timedeltas
td_list = [
    pd.Timedelta(days=5),
    pd.Timedelta(days=2, hours=12),
    pd.Timedelta(hours=36),
    pd.Timedelta(weeks=1)
]

td_sorted = sorted(td_list)
for td in td_sorted:
    print(td)
# 1 days 12:00:00
# 2 days 12:00:00
# 5 days 00:00:00
# 7 days 00:00:00

#-------------------------------------------------------------------------------------------------------------#
#-------------------------------- 8. Working with Series and arrays -----------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

'''
#--------------------------
## Converting to timedelta Series
#--------------------------
'''

# From strings
s_str = pd.Series(['1 days', '2 days 03:00:00', '4 days 05:30:00'])
s_td = pd.to_timedelta(s_str)
print(s_td)
# 0   1 days 00:00:00
# 1   2 days 03:00:00
# 2   4 days 05:30:00
# dtype: timedelta64[ns]

# From numeric values with unit
s_numeric = pd.Series([1, 2, 3, 4, 5])
s_td_days = pd.to_timedelta(s_numeric, unit='D')
print(s_td_days)
# 0   1 days
# 1   2 days
# 2   3 days
# 3   4 days
# 4   5 days
# dtype: timedelta64[ns]

s_td_hours = pd.to_timedelta(s_numeric, unit='h')
print(s_td_hours)
# 0   0 days 01:00:00
# 1   0 days 02:00:00
# 2   0 days 03:00:00
# 3   0 days 04:00:00
# 4   0 days 05:00:00
# dtype: timedelta64[ns]

'''
#--------------------------
## Using .dt accessor
#--------------------------
'''

s_td = pd.Series(pd.to_timedelta(['1 days 08:30:15', '2 days 12:45:30', '3 days 05:15:45']))
print(s_td)
# 0   1 days 08:30:15
# 1   2 days 12:45:30
# 2   3 days 05:15:45
# dtype: timedelta64[ns]

# Access components
print(s_td.dt.days)
# 0    1
# 1    2
# 2    3
# dtype: int64

print(s_td.dt.seconds)
# 0    30615
# 1    45930
# 2    18945
# dtype: int32

print(s_td.dt.total_seconds())
# 0    117015.0
# 1    218730.0
# 2    278145.0
# dtype: float64

# Get components as DataFrame
print(s_td.dt.components)
#    days  hours  minutes  seconds  milliseconds  microseconds  nanoseconds
# 0     1      8       30       15             0             0            0
# 1     2     12       45       30             0             0            0
# 2     3      5       15       45             0             0            0

'''
#--------------------------
## Vectorized operations
#--------------------------
'''

# Arithmetic operations on Series
s1 = pd.Series(pd.to_timedelta(['1 days', '2 days', '3 days']))
s2 = pd.Series(pd.to_timedelta(['12 hours', '6 hours', '18 hours']))

# Add Series
s_sum = s1 + s2
print(s_sum)
# 0   1 days 12:00:00
# 1   2 days 06:00:00
# 2   3 days 18:00:00
# dtype: timedelta64[ns]

# Multiply by scalar
s_double = s1 * 2
print(s_double)
# 0   2 days
# 1   4 days
# 2   6 days
# dtype: timedelta64[ns]

# Add to Timestamp Series
dates = pd.Series(pd.date_range('2023-01-01', periods=3))
print(dates)
# 0   2023-01-01
# 1   2023-01-02
# 2   2023-01-03
# dtype: datetime64[ns]

dates_shifted = dates + s1
print(dates_shifted)
# 0   2023-01-02
# 1   2023-01-04
# 2   2023-01-06
# dtype: datetime64[ns]

#-------------------------------------------------------------------------------------------------------------#
#------------------------------------ 9. Special Timedelta values -------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

'''
#--------------------------
## NaT (Not a Time)
#--------------------------
'''

# Create NaT
nat = pd.NaT
print(nat)
# NaT

print(type(nat))
# <class 'pandas._libs.tslibs.nattype.NaTType'>

# NaT in operations
td = pd.Timedelta(days=5)
result = td + pd.NaT
print(result)
# NaT

# Create Series with NaT
s_with_nat = pd.Series([pd.Timedelta('1 days'), pd.NaT, pd.Timedelta('3 days')])
print(s_with_nat)
# 0   1 days
# 1      NaT
# 2   3 days
# dtype: timedelta64[ns]

# Check for NaT
print(s_with_nat.isna())
# 0    False
# 1     True
# 2    False
# dtype: bool

print(s_with_nat.notna())
# 0     True
# 1    False
# 2     True
# dtype: bool

'''
#--------------------------
## Handling missing values
#--------------------------
'''

# Fill NaT values
s_filled = s_with_nat.fillna(pd.Timedelta('0 days'))
print(s_filled)
# 0   1 days
# 1   0 days
# 2   3 days
# dtype: timedelta64[ns]

# Drop NaT values
s_dropped = s_with_nat.dropna()
print(s_dropped)
# 0   1 days
# 2   3 days
# dtype: timedelta64[ns]

# Forward fill
s_ffill = s_with_nat.ffill()
print(s_ffill)
# 0   1 days
# 1   1 days
# 2   3 days
# dtype: timedelta64[ns]

#-------------------------------------------------------------------------------------------------------------#
#-------------------------- 10. Practical examples and use cases --------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

'''
#--------------------------
## Time differences
#--------------------------
'''

# Calculate age from birthdate
birth_date = pd.Timestamp('1990-05-15')
today = pd.Timestamp('2023-03-15')
age_td = today - birth_date
print(f"Age in days: {age_td.days}")
# Age in days: 12022

print(f"Age in years: {age_td.days / 365.25:.1f}")
# Age in years: 32.9

# Calculate time until deadline
deadline = pd.Timestamp('2023-12-31 23:59:59')
now = pd.Timestamp('2023-03-15 10:30:00')
time_left = deadline - now
print(f"Time until deadline: {time_left}")
# Time until deadline: 291 days 13:29:59

print(f"Hours left: {time_left.total_seconds() / 3600:.0f}")
# Hours left: 6997

'''
#--------------------------
## Time windows
#--------------------------
'''

# Create rolling time window
dates = pd.date_range('2023-01-01', periods=10, freq='D')
values = pd.Series(range(10), index=dates)

# Define window size
window = pd.Timedelta(days=3)

# Calculate rolling operations (using groupby with Grouper)
# Here's a simple example of working with time windows
for date in dates[:5]:
    start = date - window
    mask = (values.index >= start) & (values.index <= date)
    window_values = values[mask]
    print(f"Date: {date.date()}, Window sum: {window_values.sum()}")

# Date: 2023-01-01, Window sum: 0
# Date: 2023-01-02, Window sum: 1
# Date: 2023-01-03, Window sum: 3
# Date: 2023-01-04, Window sum: 6
# Date: 2023-01-05, Window sum: 10

'''
#--------------------------
## Business logic with durations
#--------------------------
'''

# Service level agreement (SLA) tracking
ticket_created = pd.Timestamp('2023-03-15 09:00:00')
sla_duration = pd.Timedelta(hours=24)
sla_deadline = ticket_created + sla_duration
print(f"Ticket created: {ticket_created}")
print(f"SLA deadline: {sla_deadline}")
# Ticket created: 2023-03-15 09:00:00
# SLA deadline: 2023-03-16 09:00:00

ticket_resolved = pd.Timestamp('2023-03-15 18:30:00')
resolution_time = ticket_resolved - ticket_created
print(f"Resolution time: {resolution_time}")
# Resolution time: 0 days 09:30:00

sla_met = resolution_time <= sla_duration
print(f"SLA met: {sla_met}")
# SLA met: True

'''
#--------------------------
## Working with time ranges
#--------------------------
'''

# Create timedelta range
td_range = pd.timedelta_range(start='1 day', end='10 days', freq='2D')
print(td_range)
# TimedeltaIndex(['1 days', '3 days', '5 days', '7 days', '9 days'], dtype='timedelta64[ns]', freq='2D')

# Or specify periods instead of end
td_range2 = pd.timedelta_range(start='1 hour', periods=10, freq='30min')
print(td_range2)
# TimedeltaIndex(['0 days 01:00:00', '0 days 01:30:00', '0 days 02:00:00',
#                 '0 days 02:30:00', '0 days 03:00:00', '0 days 03:30:00',
#                 '0 days 04:00:00', '0 days 04:30:00', '0 days 05:00:00',
#                 '0 days 05:30:00'],
#                dtype='timedelta64[ns]', freq='30min')

'''
#--------------------------
## Duration statistics
#--------------------------
'''

# Analyze durations
durations = pd.Series([
    pd.Timedelta('2 days 03:00:00'),
    pd.Timedelta('1 days 12:30:00'),
    pd.Timedelta('3 days 08:15:00'),
    pd.Timedelta('0 days 18:45:00'),
    pd.Timedelta('2 days 21:00:00')
])

print("Mean duration:")
print(durations.mean())
# 2 days 00:42:00

print("\nMedian duration:")
print(durations.median())
# 2 days 03:00:00

print("\nStandard deviation:")
print(durations.std())
# 1 days 01:01:54.335539

print("\nMin and Max:")
print(f"Min: {durations.min()}")
print(f"Max: {durations.max()}")
# Min: 0 days 18:45:00
# Max: 3 days 08:15:00

'''
#--------------------------
## Frequency conversion
#--------------------------
'''

# Convert between different frequencies
td = pd.Timedelta('5 days 12:30:45')

# Express in different units
print(f"Total seconds: {td.total_seconds()}")
# Total seconds: 477045.0

print(f"Total minutes: {td.total_seconds() / 60}")
# Total minutes: 7950.75

print(f"Total hours: {td.total_seconds() / 3600}")
# Total hours: 132.5125

print(f"Total days (exact): {td.total_seconds() / 86400}")
# Total days (exact): 5.5209375

# Using components for precise breakdown
c = td.components
print(f"{c.days} days, {c.hours} hours, {c.minutes} minutes, {c.seconds} seconds")
# 5 days, 12 hours, 30 minutes, 45 seconds

'''
#--------------------------
## Time-based filtering
#--------------------------
'''

# Create sample data
dates = pd.date_range('2023-01-01', periods=100, freq='h')
df = pd.DataFrame({
    'timestamp': dates,
    'value': range(100)
})

# Add elapsed time column
df['elapsed'] = df['timestamp'] - df['timestamp'].min()

# Filter by duration
mask = df['elapsed'] <= pd.Timedelta(days=2)
df_filtered = df[mask]
print(f"Records within 2 days: {len(df_filtered)}")
# Records within 2 days: 49

# Group by time buckets
df['time_bucket'] = (df['elapsed'] // pd.Timedelta(days=1))
grouped = df.groupby('time_bucket')['value'].mean()
print(grouped.head())
# time_bucket
# 0    11.5
# 1    35.5
# 2    59.5
# 3    83.5
# Name: value, dtype: float64
