'''
The pandas.Series.dt accessor is a powerful interface 
that provides access to datetime-like properties and methods for pandas Series.

Supported Types: datetime64[ns], datetime64[ns, tz], Period, timedelta[ns]

######################################################

0. Creating datetime data and index:
    + Datetime data: pd.to_datetime(), astype('datetime64[ns]'), pd.date_range(), pd.bdate_range()
    + Timedelta data: pd.to_timedelta(), astype('timedelta64[ns]'), pd.timedelta_range()
    + Period: pd.Period(), .Series.to_period(), pd.period_range(), 
    + pd.infer_freq(): Infers the frequency of a DatetimeIndex

1. Basic properties:
    + .dt.year, .dt.month, .dt.day
    + .dt.hour, .dt.minute, .dt.second
    + .dt.microsecond, .dt.nanosecond

2. ISO Calendar properties:
    + .dt.isocalendar(): Returns a DataFrame with ISO components = year + week + day
    + .dt.isocalendar().year: ISO year
    + .dt.isocalendar().week: ISO week number (1-53)
    + .dt.isocalendar().day: ISO day of the week (1=Monday, 7=Sunday)

3. Extended properties:
    + .dt.dayofyear
    + .dt.dayofweek, .dt.weekday
    + .dt.quarter
    + .dt.days_in_month

4. Extract Python datetime objects:
    + .dt.date: Returns datetime.date objects (date only)
    + .dt.time: Returns datetime.time objects (time only)
    + .dt.timetz: Returns datetime.time with timezone information

5. Boolean properties:
    + .dt.is_month_start, .dt.is_month_end
    + .dt.is_quarter_start, .dt.is_quarter_end
    + .dt.is_year_start, .dt.is_year_end
    + .dt.is_leap_year

6. String Representation Methods:
    + .dt.strftime(format): Custom string formatting using strftime codes
    + .dt.day_name(): Return day names ("Monday", "Tuesday", etc.)
    + .dt.month_name(): Return month names ("January", "February", etc.)

7. Time Rounding Methods:
    + .dt.round(freq): Round to nearest specified frequency
    + .dt.floor(freq): Round down to specified frequency
    + .dt.ceil(freq): Round up to specified frequency
    + .dt.normalize(): Convert times to midnight (00:00:00)

8. Timezone Handling:
    + pytz.all_timezones: List of all available timezones
    + .dt.tz: Get current timezone information
    + .dt.tz_localize(tz): Assign timezone to naive datetime
    + .dt.tz_convert(tz):  Convert between timezones

9. Timedelta Handling:
    + .dt.components: Returns DataFrame with timedelta components (days, hours, minutes, etc.)
    + .dt.days: Days component
    + .dt.seconds: Seconds component (0-86399)
    + .dt.total_seconds(): Total duration in seconds

10. Grouper with datetime-like data:
    + pd.Grouper(key=None, level=None, freq=None, axis=0, sort=False, closed=None, label=None, convention='start', base=0, origin='start', offset=None)
    + Used in groupby operations to group by specific time periods (e.g., month, year)
'''

###################################

'''
COMMON FREQUENCY CODES:

'ns' - Nanosecond
'us' - Microsecond
'ms' - Millisecond
's' - Second

'min' - Minute
'h' - Hour

'D' - Day
'B' - Business day
'W' - Weekly

'ME' - Month end
'MS' - Month start

'QE' - Quarter end
'QS' - Quarter start

'YE' - Year end
'YS' - Year start
'''

import pandas as pd
import numpy as np

#-------------------------------------------------------------------------------------------------------------#
#------------------------------------ 0. Creating datetime data and index ------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

'''
#--------------------------
## Datetime data
#--------------------------
'''

s_original = pd.Series(['2023-01-01', '2023-02-15', '2023-03-20'])
print(s_original.dtypes) # object

s_dayfirst = pd.Series(['31/12/2023', '15/11/2023', '20/10/2023'])
print(s_dayfirst.dtypes) # object

######################
## pd.to_datetime() ##
######################

# Basic use
s_datetime = pd.to_datetime(s_original)
print(s_datetime)
# 0   2023-01-01
# 1   2023-02-15
# 2   2023-03-20
# dtype: datetime64[ns]

# Set the "dayfirst = True" for string format "DD/MM/YYYY" (or something similar like DD-MM-YYYY, DD.MM.YYYY)
s_datetime = pd.to_datetime(arg = s_dayfirst, dayfirst = True)
print(s_datetime)
# 0   2023-12-31
# 1   2023-11-15
# 2   2023-10-20
# dtype: datetime64[ns]

##############################
## astype('datetime64[ns]') ##
##############################

s_datetime = s_original.astype('datetime64[ns]')
print(s_datetime)
# 0   2023-01-01
# 1   2023-02-15
# 2   2023-03-20
# dtype: datetime64[ns]

s_datetime = s_dayfirst.astype('datetime64[ns]')
print(s_datetime)
# 0   2023-12-31
# 1   2023-11-15
# 2   2023-10-20
# dtype: datetime64[ns]

#####################
## pd.date_range() ##
#####################
# Create a DatetimeIndex with a specified frequency
# Can use this DatetimeIndex as index for a Series or DataFrame
'''Can wrap with pd.Series() to create a Series from this DatetimeIndex object'''
# https://pandas.pydata.org/docs/reference/api/pandas.date_range.html

# Create a date range from '2023-01-01' to '2023-01-10' with daily frequency
date_rng = pd.date_range(start = '2023-01-01', end = '2023-01-10', freq = 'D')
print(date_rng)
# DatetimeIndex(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04',
#                '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08',
#                '2023-01-09', '2023-01-10'],
#               dtype='datetime64[ns]', freq='D')

np.random.seed(0)
s_daterange = pd.Series(data = np.random.randint(0, 100, size = len(date_rng)), index = date_rng)
print(s_daterange)
# 2023-01-01    44
# 2023-01-02    47
# 2023-01-03    64
# 2023-01-04    67
# 2023-01-05    67
# 2023-01-06     9
# 2023-01-07    83
# 2023-01-08    21
# 2023-01-09    36
# 2023-01-10    87
# Freq: D, dtype: int64

######################
## pd.bdate_range() ##
######################
# Works like pd.date_range() but only includes business days (Monday to Friday)
'''Can wrap with pd.Series() to create a Series from this DatetimeIndex object'''
# https://pandas.pydata.org/docs/reference/api/pandas.bdate_range.html

bdate_range = pd.bdate_range(start = '2023-01-01', end = '2023-01-10', freq = 'B') # 'B' means business day frequency

print(bdate_range)
# DatetimeIndex(['2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05',
#                '2023-01-06', '2023-01-09', '2023-01-10'],
#               dtype='datetime64[ns]', freq='B')


# (Here, the weekends 2023-01-01, 2023-01-07, and 2023-01-08 are excluded 
# because they are not business days)


'''
#--------------------------
## Timedelta data
#--------------------------
'''

s_original = pd.Series(['1 days', '2 days 03:00:00', '4 days 05:30:00'])
s_original_nums = pd.Series([1, 2.5, 4.25])

#######################
## pd.to_timedelta() ##
#######################

# Basic use
s_timedelta = pd.to_timedelta(s_original)
print(s_timedelta)
# 0   1 days 00:00:00
# 1   2 days 03:00:00
# 2   4 days 05:30:00
# dtype: timedelta64[ns]

# Specify the unit of the numeric input
s_timedelta = pd.to_timedelta(s_original_nums, unit = 'h') # 'h' means hours
print(s_timedelta)
# 0   0 days 01:00:00 (1 -> 1 hour)
# 1   0 days 02:30:00 (2.5 -> 2 hours 30 minutes)
# 2   0 days 04:15:00 (4.25 -> 4 hours 15 minutes)
# dtype: timedelta64[ns]

'''
Only specify "unit=" when the input is NUMERIC (not string or object).
'''

###############################
## astype('timedelta64[ns]') ##
###############################

s_timedelta = s_original.astype('timedelta64[ns]')
print(s_timedelta)
# 0   1 days 00:00:00
# 1   2 days 03:00:00
# 2   4 days 05:30:00
# dtype: timedelta64[ns]

s_timedelta = s_original_nums.astype('timedelta64[ns]') # Interpreted as nanoseconds
print(s_timedelta)
# 0   0 days 00:00:00.000000001
# 1   0 days 00:00:00.000000002
# 2   0 days 00:00:00.000000004
# dtype: timedelta64[ns]

s_timedelta = s_original_nums.astype('timedelta64[h]') # Interpreted as hours
print(s_timedelta)
# 0   0 days 01:00:00
# 1   0 days 02:00:00
# 2   0 days 04:00:00
# dtype: timedelta64[s]

##########################
## pd.timedelta_range() ##
##########################
# Create a TimedeltaIndex with a specified frequency
# Can use this TimedeltaIndex as index for a Series or DataFrame
'''Can wrap with pd.Series() to create a Series from this TimedeltaIndex object'''
# https://pandas.pydata.org/docs/reference/api/pandas.timedelta_range.html

td_range = pd.timedelta_range(start = '1 days', end = '10 days', freq = '2D') # '2D' means every 2 days
print(td_range)
# TimedeltaIndex(['1 days', '3 days', '5 days', '7 days', '9 days'], dtype='timedelta64[ns]', freq='2D')

td_range = pd.timedelta_range(start = '1 day', end = '2 days', freq = '6h') # '6h' means every 6 hours
print(td_range)
# TimedeltaIndex(['1 days 00:00:00', '1 days 06:00:00', '1 days 12:00:00',
#                 '1 days 18:00:00', '2 days 00:00:00'],
#                dtype='timedelta64[ns]', freq='6h')

np.random.seed(0)
s_timedelta_range = pd.Series(data = np.random.randint(0, 100, size = len(td_range)), index = td_range)
print(s_timedelta_range)
# 1 days 00:00:00    44
# 1 days 06:00:00    47
# 1 days 12:00:00    64
# 1 days 18:00:00    67
# 2 days 00:00:00    67
# Freq: 6h, dtype: int64


'''
#--------------------------
## Period data
#--------------------------
'''

#################
## pd.Period() ##
#################
# Represents a period of time.

period = pd.Period('2012-1-1', freq='D')

print(period) 
# 2012-01-01

print(type(period))
# <class 'pandas._libs.tslibs.period.Period'>

print(period.freq)
# <Day>

print(period.day)
# 1

#########################
## .Series.to_period() ##
#########################
# Convert Series from DatetimeIndex to PeriodIndex.

idx = pd.DatetimeIndex(['2023', '2024', '2025'])
s = pd.Series([1, 2, 3], index=idx)
s = s.to_period()

print(s)
# 2023    1
# 2024    2
# 2025    3
# Freq: Y-DEC, dtype: int64

print(s.index)
# PeriodIndex(['2023', '2024', '2025'], dtype='period[Y-DEC]')

#######################
## pd.period_range() ##
#######################
# Return a fixed frequency PeriodIndex (Can use this as Series or DataFrame index).
# The day (calendar) is the default frequency.
'''Can wrap with pd.Series() to create a Series from this PeriodIndex object'''
# https://pandas.pydata.org/docs/reference/api/pandas.period_range.html#pandas.period_range

period_index = pd.period_range(start = '2017-01-01', end = '2018-01-01', freq = 'Q')
print(period_index)
# PeriodIndex(['2017Q1', '2017Q2', '2017Q3', '2017Q4', '2018Q1'], dtype='period[Q-DEC]')

np.random.seed(0)
s_period_range = pd.Series(data = np.random.randint(0, 100, size = len(period_index)), index = period_index)
print(s_period_range)
# 2017Q1    44
# 2017Q2    47
# 2017Q3    64
# 2017Q4    67
# 2018Q1    67
# Freq: Q-DEC, dtype: int64


'''
#--------------------------
## Infer the most likely frequency given the input index.
#--------------------------
'''

#####################
## pd.infer_freq() ##
#####################

idx = pd.date_range(start = '2020/12/01', end = '2020/12/30', periods = 30)

infered_freq = pd.infer_freq(idx)
print(infered_freq) # D (daily frequency)


#-------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 1. Basic properties ---------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

s_datetime = pd.Series(pd.date_range(start = '2023-01-01 08:30:15', periods = 5, freq = 'D'))
print(s_datetime)
# 0   2023-01-01 08:30:15
# 1   2023-01-02 08:30:15
# 2   2023-01-03 08:30:15
# 3   2023-01-04 08:30:15
# 4   2023-01-05 08:30:15
# dtype: datetime64[ns]

##################################
## .dt.year, .dt.month, .dt.day ##
##################################

print(s_datetime.dt.year)
# 0    2023
# 1    2023
# 2    2023
# 3    2023
# 4    2023
# dtype: int32

print(s_datetime.dt.month)
# 0    1
# 1    1
# 2    1
# 3    1
# 4    1
# dtype: int32

print(s_datetime.dt.day)
# 0    1
# 1    2
# 2    3
# 3    4
# 4    5
# dtype: int32

######################################
## .dt.hour, .dt.minute, .dt.second ##
######################################

print(s_datetime.dt.hour)
# 0    8
# 1    8
# 2    8
# 3    8
# 4    8
# dtype: int32

print(s_datetime.dt.minute)
# 0    30
# 1    30
# 2    30
# 3    30
# 4    30
# dtype: int32

print(s_datetime.dt.second)
# 0    15
# 1    15
# 2    15
# 3    15
# 4    15
# dtype: int32

#####################################
## .dt.microsecond, .dt.nanosecond ##
#####################################

print(s_datetime.dt.microsecond)
# 0    0
# 1    0
# 2    0
# 3    0
# 4    0
# dtype: int32

print(s_datetime.dt.nanosecond)
# 0    0
# 1    0
# 2    0
# 3    0
# 4    0
# dtype: int32


#-------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 2. ISO Calendar properties -------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

s_datetime = pd.Series(pd.date_range(start = '2023-01-01', periods = 5, freq = 'D'))
print(s_datetime)
# 0   2023-01-01
# 1   2023-01-02
# 2   2023-01-03
# 3   2023-01-04
# 4   2023-01-05
# dtype: datetime64[ns]

#######################
## .dt.isocalendar() ##
#######################
# Returns a DataFrame with ISO components = year + week + day

print(s_datetime.dt.isocalendar())
#       year     week      day
#   <UInt32> <UInt32> <UInt32>
# 0     2022       52        7
# 1     2023        1        1
# 2     2023        1        2
# 3     2023        1        3
# 4     2023        1        4

############################
## .dt.isocalendar().year ##
############################

print(s_datetime.dt.isocalendar().year)
# 0    2022
# 1    2023
# 2    2023
# 3    2023
# 4    2023
# Name: year, dtype: UInt32

############################
## .dt.isocalendar().week ##
############################

print(s_datetime.dt.isocalendar().week)
# 0    52
# 1     1
# 2     1
# 3     1
# 4     1
# Name: week, dtype: UInt32

###########################
## .dt.isocalendar().day ##
###########################

print(s_datetime.dt.isocalendar().day)
# 0    7
# 1    1
# 2    2
# 3    3
# 4    4
# Name: day, dtype: UInt32


#-------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 3. Extended properties ----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

s_datetime = pd.Series(pd.date_range(start = '2023-03-01', periods = 5, freq = 'D'))
print(s_datetime)
# 0   2023-03-01
# 1   2023-03-02
# 2   2023-03-03
# 3   2023-03-04
# 4   2023-03-05
# dtype: datetime64[ns]

###################
## .dt.dayofyear ##
###################
# The day of the year (1 to 365 or 366 in leap years)

print(s_datetime.dt.dayofyear)
# 0    60
# 1    61
# 2    62
# 3    63
# 4    64
# dtype: int32

################################
## .dt.dayofweek, .dt.weekday ##
################################
# The day of the week with Monday=0, Sunday=6

print(s_datetime.dt.dayofweek)
# 0    2
# 1    3
# 2    4
# 3    5
# 4    6
# dtype: int32

print(s_datetime.dt.weekday)
# 0    2
# 1    3
# 2    4
# 3    5
# 4    6
# dtype: int32

#################
## .dt.quarter ##
#################
# The quarter of the year (1 to 4)

print(s_datetime.dt.quarter)
# 0    1
# 1    1
# 2    1
# 3    1
# 4    1
# dtype: int32
'''March is in the 1st quarter'''

#######################
## .dt.days_in_month ##
#######################
# The number of days in the month

print(s_datetime.dt.days_in_month)
# 0    31
# 1    31
# 2    31
# 3    31
# 4    31
# dtype: int32
'''March has 31 days'''



#-------------------------------------------------------------------------------------------------------------#
#----------------------------------- 4. Extract Python datetime objects --------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

s_datetime = pd.Series(["1/1/2020 10:00:00+00:00", "2/1/2020 11:00:00+00:00"], dtype = 'datetime64[ns, UTC]')
print(s_datetime)
# 0   2020-01-01 10:00:00+00:00
# 1   2020-02-01 11:00:00+00:00
# dtype: datetime64[ns, UTC]

##############
## .dt.date ##
##############
# Returns datetime.date objects (date only)

print(s_datetime.dt.date)
# 0    2020-01-01
# 1    2020-02-01
# dtype: object

print(type(s_datetime.dt.date[0]))
# <class 'datetime.date'>

##############
## .dt.time ##
##############
# Returns datetime.time objects (time only)

print(s_datetime.dt.time)
# 0    10:00:00
# 1    11:00:00
# dtype: object

print(type(s_datetime.dt.time[0]))
# <class 'datetime.time'>

################
## .dt.timetz ##
################
# Returns datetime.time with timezone information

print(s_datetime.dt.timetz)
# 0    10:00:00+00:00 (the +00:00 indicates UTC timezone)
# 1    11:00:00+00:00
# dtype: object

print(type(s_datetime.dt.timetz[0]))
# <class 'datetime.time'>


#-------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 5. Boolean properties ----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

##########################################
## .dt.is_month_start, .dt.is_month_end ##
##########################################

s_datetime = pd.Series(pd.date_range(start = '2023-05-01', periods = 7, freq = '5D'))
print(s_datetime)
# 0   2023-05-01
# 1   2023-05-06
# 2   2023-05-11
# 3   2023-05-16
# 4   2023-05-21
# 5   2023-05-26
# 6   2023-05-31
# dtype: datetime64[ns]
'''
periods = 7 means creating 7 dates
freq = '5D' means each date is 5 days apart
'''

print(s_datetime.dt.is_month_start) # Indicates whether the date is the first day of the month
# 0     True (2023-05-01 is the first day of May)
# 1    False
# 2    False
# 3    False
# 4    False
# 5    False
# 6    False
# dtype: bool

print(s_datetime.dt.is_month_end) # Indicates whether the date is the last day of the month
# 0    False
# 1    False
# 2    False
# 3    False
# 4    False
# 5    False
# 6     True (2023-05-31 is the last day of May)
# dtype: bool

##############################################
## .dt.is_quarter_start, .dt.is_quarter_end ##
##############################################

s_datetime = pd.Series(pd.date_range(start = '2023-01-31', end = '2023-06-30', freq = 'ME')) # 'ME' means month end frequency
first_january = pd.Series(['2023-01-01'], dtype='datetime64[ns]')
s_datetime = pd.concat([first_january, s_datetime], ignore_index=True)
print(s_datetime)
# 0   2023-01-01
# 1   2023-01-31
# 2   2023-02-28
# 3   2023-03-31
# 4   2023-04-30
# 5   2023-05-31
# 6   2023-06-30
# dtype: datetime64[ns]

print(s_datetime.dt.is_quarter_start) # Indicates whether the date is the first day of the quarter
# 0     True (2023-01-01 is the first day of the 1st quarter)
# 1    False
# 2    False
# 3    False
# 4    False
# 5    False
# 6    False
# dtype: bool

print(s_datetime.dt.is_quarter_end) # Indicates whether the date is the last day of the quarter
# 0    False
# 1    False
# 2    False
# 3     True (2023-03-31 is the last day of the 1st quarter)
# 4    False
# 5    False
# 6     True (2023-06-30 is the last day of the 2nd quarter)
# dtype: bool 

########################################
## .dt.is_year_start, .dt.is_year_end ##
########################################

s_datetime = pd.Series(pd.date_range(start = '2023-01-31', end = '2023-12-31', freq = 'QE'))
first_january = pd.Series(['2023-01-01'], dtype='datetime64[ns]')
s_datetime = pd.concat([first_january, s_datetime], ignore_index=True)
print(s_datetime)
# 0   2023-01-01
# 1   2023-03-31
# 2   2023-06-30
# 3   2023-09-30
# 4   2023-12-31
# dtype: datetime64[ns]

print(s_datetime.dt.is_year_start) # Indicates whether the date is the first day of the year
# 0     True (2023-01-01 is the first day of the year)
# 1    False
# 2    False
# 3    False
# 4    False
# dtype: bool

print(s_datetime.dt.is_year_end) # Indicates whether the date is the last day of the year
# 0    False
# 1    False
# 2    False
# 3    False
# 4     True (2023-12-31 is the last day of the year)
# dtype: bool

######################
## .dt.is_leap_year ##
######################

s_datetime = pd.Series(pd.date_range(start = '2020-01-01', end = '2024-01-01', freq = 'YS')) # 'YS' means year start frequency
print(s_datetime)
# 0   2020-01-01
# 1   2021-01-01
# 2   2022-01-01
# 3   2023-01-01
# 4   2024-01-01
# dtype: datetime64[ns]

print(s_datetime.dt.is_leap_year) # Indicates whether the year is a leap year
# 0     True (2020 is a leap year)
# 1    False
# 2    False
# 3    False
# 4     True (2024 is a leap year)
# dtype: bool


#-------------------------------------------------------------------------------------------------------------#
#------------------------------------ 6. String Representation Methods ---------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

s_datetime = pd.Series(pd.date_range(start = '2023-01-01 08:30:15', periods = 5, freq = 'D'))
print(s_datetime)
# 0   2023-01-01 08:30:15
# 1   2023-01-02 08:30:15
# 2   2023-01-03 08:30:15
# 3   2023-01-04 08:30:15
# 4   2023-01-05 08:30:15
# dtype: datetime64[ns]

##########################
## .dt.strftime(format) ##
##########################
'''
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
'''


print(s_datetime.dt.strftime('%d-%M-%Y %H:%M'))
# 0    01-30-2023 08:30
# 1    02-30-2023 08:30
# 2    03-30-2023 08:30
# 3    04-30-2023 08:30
# 4    05-30-2023 08:30
# dtype: object

print(s_datetime.dt.strftime('%A, %B %d, %Y'))
# 0       Sunday, January 01, 2023
# 1       Monday, January 02, 2023
# 2      Tuesday, January 03, 2023
# 3    Wednesday, January 04, 2023
# 4     Thursday, January 05, 2023
# dtype: object

####################
## .dt.day_name() ##
####################

print(s_datetime.dt.day_name())
# 0       Sunday
# 1       Monday
# 2      Tuesday
# 3    Wednesday
# 4     Thursday
# dtype: object

######################
## .dt.month_name() ##
######################
# Return month names ("January", "February", etc.)

print(s_datetime.dt.month_name())
# 0    January
# 1    January
# 2    January
# 3    January
# 4    January
# dtype: object


#-------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 7. Time Rounding Methods ---------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

s_datetime = pd.Series(pd.date_range(start = '2023-01-01 08:45:23', periods = 5, freq = 'D'))
print(s_datetime)
# 0   2023-01-01 08:45:23
# 1   2023-01-02 08:45:23
# 2   2023-01-03 08:45:23
# 3   2023-01-04 08:45:23
# 4   2023-01-05 08:45:23
# dtype: datetime64[ns]

#################
## .dt.round() ##
#################
'''Round to nearest specified frequency'''

print(s_datetime.dt.round('h')) # Round to nearest hour
# 0   2023-01-01 09:00:00 (The nearest hour to 08:45:23 is 09:00:00)
# 1   2023-01-02 09:00:00
# 2   2023-01-03 09:00:00
# 3   2023-01-04 09:00:00
# 4   2023-01-05 09:00:00
# dtype: datetime64[ns]

print(s_datetime.dt.round('min')) # Round to nearest minute
# 0   2023-01-01 08:45:00 (The nearest minute to 08:45:23 is 08:45:00)
# 1   2023-01-02 08:45:00
# 2   2023-01-03 08:45:00
# 3   2023-01-04 08:45:00
# 4   2023-01-05 08:45:00
# dtype: datetime64[ns]

#################
## .dt.floor() ##
#################
'''Round down to specified frequency'''

print(s_datetime.dt.floor('h')) # Floor to hour
# 0   2023-01-01 08:00:00
# 1   2023-01-02 08:00:00
# 2   2023-01-03 08:00:00
# 3   2023-01-04 08:00:00
# 4   2023-01-05 08:00:00
# dtype: datetime64[ns]

print(s_datetime.dt.floor('min')) # Floor to minute
# 0   2023-01-01 08:45:00
# 1   2023-01-02 08:45:00
# 2   2023-01-03 08:45:00
# 3   2023-01-04 08:45:00
# 4   2023-01-05 08:45:00
# dtype: datetime64[ns]

################
## .dt.ceil() ##
################
'''Round up to specified frequency'''

print(s_datetime.dt.ceil('h')) # Ceil to hour
# 0   2023-01-01 09:00:00
# 1   2023-01-02 09:00:00
# 2   2023-01-03 09:00:00
# 3   2023-01-04 09:00:00
# 4   2023-01-05 09:00:00
# dtype: datetime64[ns]

print(s_datetime.dt.ceil('min')) # Ceil to minute
# 0   2023-01-01 08:46:00
# 1   2023-01-02 08:46:00
# 2   2023-01-03 08:46:00
# 3   2023-01-04 08:46:00
# 4   2023-01-05 08:46:00
# dtype: datetime64[ns]

#####################
## .dt.normalize() ##
#####################
'''Convert times to midnight (00:00:00), useful when time does not matter'''

print(s_datetime.dt.normalize())
# 0   2023-01-01
# 1   2023-01-02
# 2   2023-01-03
# 3   2023-01-04
# 4   2023-01-05
# dtype: datetime64[ns]


#-------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 8. Timezone Handling -----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

s_datetime = pd.Series(pd.date_range(start = '2023-01-01 08:30:15', periods = 5, freq = 'D'))
print(s_datetime)
# 0   2023-01-01 08:30:15
# 1   2023-01-02 08:30:15
# 2   2023-01-03 08:30:15
# 3   2023-01-04 08:30:15
# 4   2023-01-05 08:30:15
# dtype: datetime64[ns]

s_datetime_UTC = pd.Series(pd.date_range(start = '2023-01-01 08:30:15', periods = 5, freq = 'D', tz = 'UTC'))
print(s_datetime_UTC)
# 0   2023-01-01 08:30:15+00:00
# 1   2023-01-02 08:30:15+00:00
# 2   2023-01-03 08:30:15+00:00
# 3   2023-01-04 08:30:15+00:00
# 4   2023-01-05 08:30:15+00:00
# dtype: datetime64[ns, UTC]
'''(The +00:00 indicates UTC timezone)'''

s_datetime_HCM = pd.Series(pd.date_range(start = '2023-01-01 08:30:15', periods = 5, freq = 'D', tz = 'Asia/Ho_Chi_Minh'))
print(s_datetime_HCM)
# 0   2023-01-01 08:30:15+07:00
# 1   2023-01-02 08:30:15+07:00
# 2   2023-01-03 08:30:15+07:00
# 3   2023-01-04 08:30:15+07:00
# 4   2023-01-05 08:30:15+07:00
# dtype: datetime64[ns, Asia/Ho_Chi_Minh]
'''(The +07:00 indicates Asia/Ho_Chi_Minh timezone)'''

########################
## pytz.all_timezones ##
########################
'''List all available timezones'''

import pytz

print(pytz.all_timezones)
# ['Africa/Abidjan', 'Africa/Accra', 'Africa/Addis_Ababa', ... 'US/Samoa', 'UTC', 'Universal', 'W-SU', 'WET', 'Zulu']

for tz in pytz.all_timezones: # Print all timezones line by line
    print(tz)
# Africa/Abidjan
# Africa/Accra
# Africa/Addis_Ababa
# ...
# WET
# Zulu

for tz in pytz.all_timezones: # Print timezones containing 'Asia' line by line
    if 'Asia' in tz:
        print(tz)
# Asia/Aden
# Asia/Almaty
# Asia/Amman

############
## .dt.tz ##
############
'''Get current timezone information'''

print(s_datetime.dt.tz)
# None

print(s_datetime_UTC.dt.tz)
# UTC

print(s_datetime_HCM.dt.tz)
# Asia/Ho_Chi_Minh

#######################
## .dt.tz_localize() ##
#######################
'''Set timezone for timezone-naive datetime (i.e., datetime without timezone info)'''

s_localized = s_datetime.dt.tz_localize('US/Samoa')
print(s_localized)
# 0   2023-01-01 08:30:15-11:00
# 1   2023-01-02 08:30:15-11:00
# 2   2023-01-03 08:30:15-11:00
# 3   2023-01-04 08:30:15-11:00
# 4   2023-01-05 08:30:15-11:00
# dtype: datetime64[ns, US/Samoa]
'''(The -11:00 indicates US/Samoa timezone)'''

s_localized = s_datetime_HCM.dt.tz_localize('Zulu')
# This will raise an error because s_datetime_HCM already has timezone info
'''TypeError: Already tz-aware, use tz_convert to convert.'''

######################
## .dt.tz_convert() ##
######################
'''Convert timezone for timezone-aware datetime (i.e., datetime with timezone info)'''

s_converted = s_datetime_HCM.dt.tz_convert('Asia/Amman')
print(s_converted)
# 0   2023-01-01 04:30:15+03:00
# 1   2023-01-02 04:30:15+03:00
# 2   2023-01-03 04:30:15+03:00
# 3   2023-01-04 04:30:15+03:00
# 4   2023-01-05 04:30:15+03:00
# dtype: datetime64[ns, Asia/Amman]
'''(The +03:00 indicates Asia/Amman timezone)'''

s_converted = s_datetime.dt.tz_convert('Zulu')
# This will raise an error because s_datetime is timezone-naive
'''TypeError: Cannot convert tz-naive timestamps, use tz_localize to localize'''


#-------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 9. Timedelta handling ----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

s_timedelta = pd.Series(pd.to_timedelta(['1 days 08:30:15', '2 days 12:45:30', '3 days 05:15:45']))
print(s_timedelta)
# 0   1 days 08:30:15
# 1   2 days 12:45:30
# 2   3 days 05:15:45
# dtype: timedelta64[ns]

####################
## .dt.components ##
####################
'''Returns DataFrame with timedelta components'''

print(s_timedelta.dt.components)
#    days  hours  minutes  seconds  milliseconds  microseconds  nanoseconds
# 0     1      8       30       15             0             0            0
# 1     2     12       45       30             0             0            0
# 2     3      5       15       45             0             0            0

##############
## .dt.days ##
##############
'''Days component'''

print(s_timedelta.dt.days)
# 0    1
# 1    2
# 2    3
# dtype: int64

#################
## .dt.seconds ##
#################
'''Seconds component (0-86399) of ONE DAY'''

print(s_timedelta.dt.seconds)
# 0    30615
# 1    45930 (12*3600 + 45*60 + 30)
# 2    18945
# dtype: int32

#########################
## .dt.total_seconds() ##
#########################
'''Total duration in seconds (across ALL DAYS)'''

print(s_timedelta.dt.total_seconds())
# 0    117015.0
# 1    218730.0 (2*86400 + 12*3600 + 45*60 + 30)
# 2    278145.0
# dtype: float64

'''
NOTE: since these are all numeric values (int or float), you can perform numeric operations on them directly.
'''


#-------------------------------------------------------------------------------------------------------------#
#----------------------------------- 10. Grouper with datetime-like data -------------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
A Grouper allows the user to specify a groupby instruction for an object.
https://pandas.pydata.org/docs/reference/api/pandas.Grouper.html#pandas.Grouper
'''

day_range = pd.date_range(start = '2023-01-01', end = '2023-01-07', freq = 'D')
s_price = pd.Series([100, 150, 200, 250, 300, 350, 400], index = day_range)
print(s_price)
# 2023-01-01    100
# 2023-01-02    150
# 2023-01-03    200
# 2023-01-04    250
# 2023-01-05    300
# 2023-01-06    350
# 2023-01-07    400
# Freq: D, dtype: int64

###############################################
## using pandas methods like pd.Series.sum() ##
###############################################

# Calculate sum for every 3 days
sum_3_days = s_price.groupby(pd.Grouper(freq = '3D')).sum()

print(sum_3_days)
# 2023-01-01    450 (100 + 150 + 200)
# 2023-01-04    900 (250 + 300 + 350)
# 2023-01-07    400 (400)
# Freq: 3D, dtype: int64

##################
## using .agg() ##
##################

# Calculate mean for every 2 days
mean_2_days = s_price.groupby(pd.Grouper(freq = '2D')).agg('mean')

print(mean_2_days)
# 2023-01-01    125.0 ( (100 + 150) / 2 )
# 2023-01-03    225.0 ( (200 + 250) / 2 )
# 2023-01-05    325.0
# 2023-01-07    400.0
# Freq: 2D, dtype: float64

##########################################
##  using external funciton with .agg() ##
##########################################

# Calculate standard deviation for every 3 days
std_3_days = s_price.groupby(pd.Grouper(freq = '3D')).agg(np.std)

print(std_3_days)
# 2023-01-01    50.0 ( std of 100, 150, 200 )
# 2023-01-04    50.0
# 2023-01-07     NaN
# Freq: 3D, dtype: float64

########################################
##  using lambda funciton with .agg() ##
########################################

# Calculate max for every 4 days
max_4_days = s_price.groupby(pd.Grouper(freq = '4D')).agg(lambda x: x.max())

print(max_4_days)
# 2023-01-01    250 ( max of 100, 150, 200, 250 )
# 2023-01-05    400 ( max of 300, 350, 400 )
# Freq: 4D, dtype: int64