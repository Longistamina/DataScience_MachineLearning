'''
1. datetime object's attributes

2. datetime.date() and datetime.datetime()

3. datetime.strptime() and datetime.strftime()

4. timedelta

5. pytz module (timezone)
'''

# https://www.programiz.com/python-programming/datetime

# 0: Monday
# 1: Tuesday
# 2: Wednesday
# 3: Thursday
# 4: Friday
# 5: Saturday
# 6: Sunday


#---------------------------------------------------------------------------------------------------------------#
#------------------------------------ 1. datetime object's attributes ------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

from datetime import datetime # from datetime: this datetime is a module, a .py file
                              # import datetime: this datetime is a class or a function inside the datetime module
from datetime import date

print()
print(datetime.now())   #Current moment
print(datetime.today()) #Current day

current_moment = datetime.now()

current_day = current_moment.day        #Get the .day attribute of the current_moment object
print(current_day)

current_month = current_moment.month    #Get the .month attribute of the current_moment object
print(current_month)

current_year = current_moment.year      #Get the .year attribute of the current_moment object
print(current_year)

'''
max: datetime.datetime(9999, 12, 31, 23, 59, 59, 999999) the maximum datetime value in python.
It means year 9999, December, day 31st, at 23h 59m 59s 999999ms

min: datetime.datetime(1, 1, 1, 0, 0) the miniimum datetime value in python.
It means year 1, January, day 1st, at 0h 0m
'''


#----------------------------------------------------------------------------------------------------------------#
#------------------------------ 2. datetime.date() and datetime.datetime() --------------------------------------#
#----------------------------------------------------------------------------------------------------------------#

# date() is a class inside the datetime module, used to create date objects
birthday1 = date(1890,5,19)             # Generate a datetime object, year 1890, May, day 29th
print(birthday1)

# datetime() is a class inside the datetime module, used to create datetime objects
birthday2 = datetime(1890,5,19,23,30)   # Like above, but add hour (23) and minute (30)
print(birthday2)

'''
Difference between date() and datetime():
- date() creates a date object, which only contains year, month, and day.
- datetime() creates a datetime object, which contains year, month, day, hour, minute, second, and microsecond.
'''


#----------------------------------------------------------------------------------------------------------------#
#------------------------------ 3. datetime.strptime() and datetime.strftime() ----------------------------------#
#----------------------------------------------------------------------------------------------------------------#

#############################################################
## datetime.strptime() convert string into datetime object ##
#############################################################

day1 = datetime.strptime('18/2/2024','%d/%m/%Y') # datetime.datetime(2024, 2, 18, 0, 0)
print(day1)

day2 = datetime.strptime('18-2-2024','%d-%m-%Y') # datetime.datetime(2024, 2, 18, 0, 0)
print(day2)

day3 = datetime.strptime('2/18/2024','%m/%d/%Y') # datetime.datetime(2024, 2, 18, 0, 0)
print(day3)

# day1 day2 day3 will share the same value as datetime.datetime(2024, 2, 18, 0, 0)


#############################################################
## datetime.strftime() convert datetime object into string ##
#############################################################

day4 = day1.strftime('%d-%m-%Y')    # '18-02-2024'
day5 = day2.strftime('%A %d/%m/%Y') # 'Sunday 18/02/2024' (return a string object)
day6 = day3.strftime('%a %m/%d/%Y') # 'Sun 02/18/2024'



week_day = day1.strftime('%A')  # Return the day of the week as string, 
print(week_day) # 'Sunday'

index_week_day = day1.weekday() # Return the day of the week as index, return  6 = Sunday
print(index_week_day) # 6

# (0: Monday, 1: Tuesday,....., 6: Sunday)


#-----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------ 4. timedelta ---------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------#

# timedelta is a class inside the datetime module, used to represent a duration, the difference between two dates or times

from datetime import date, datetime, timedelta

###################################
## timedelta object's attributes ##
###################################

# Calculate timedelta as day and second
day1 = datetime(2018,6,18,7,30,00)
day2 = datetime(2019,7,20,8,32,20)

t1 = day2-day1 # return t1 as a timedelta() object
print(t1)

delta_days = t1.days        # Timedelta in counted in days
print(delta_days)

delta_seconds = t1.seconds  # Timedelta in counted in seconds (excluding days)
print(delta_seconds)


##########################
## timedelta() function ##
##########################

tomorrow = date.today() + timedelta(days = 1)
print(tomorrow)

yesterday1 = date.today() + timedelta(days = -1)
print(yesterday1)

yesterday2 = date.today() - timedelta(days = 1)
print(yesterday2)

# yesterday1 and yesterday2 will share the same value


#################################
## Create a timedelta() object ##
#################################

t = timedelta(days = 5, hours = 1,minutes = 10, seconds = 30)

total_delta_seconds = t.total_seconds() # Convert all the timedelta into seconds  = 436230 seconds
print(total_delta_seconds)


#-----------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------- 5. pytz module ----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------#

import pytz
import datetime

###########################
## Get a timezone object ##
###########################

tz_UTC = pytz.timezone('UTC')  # Coordinated Universal Time
print(tz_UTC) # UTC

tz_HCM = pytz.timezone('Asia/Ho_Chi_Minh') # Ho Chi Minh City, Vietnam
print(tz_HCM) # Asia/Ho_Chi_Minh

tz_US_Eastern = pytz.timezone('US/Eastern') # Eastern Time (US & Canada)
print(tz_US_Eastern) # US/Eastern

tz_Seoul = pytz.timezone('Asia/Seoul') # Seoul, South Korea
print(tz_Seoul) # Asia/Seoul

##########################################
## Name of all timezones in pytz module ##
##########################################

print(pytz.all_timezones) # Return a list of all timezone names supported in pytz module
# ['Africa/Abidjan', 'Africa/Accra', 'Africa/Addis_Ababa', ....... 'UTC', 'US/Alaska', 'US/Aleutian', 'US/Arizona', ....... ]

#----
## Apply for loop
#----

for i, tz_name in enumerate(pytz.all_timezones):
    print(i, tz_name)
    if i >= 10:
        break
# 0 Africa/Abidjan
# 1 Africa/Accra
# 2 Africa/Addis_Ababa
# 3 Africa/Algiers
# 4 Africa/Asmara
# 5 Africa/Asmera
# 6 Africa/Bamako
# 7 Africa/Bangui
# 8 Africa/Banjul
# 9 Africa/Bissau
# 10 Africa/Blantyre

#----
## Print timezone names with conditions
#----

for i, tz_name in enumerate(pytz.all_timezones):
    if ('Asia' in tz_name) and (269 <= i <= 279):
        print(i, tz_name)
# 269 Asia/Ho_Chi_Minh
# 270 Asia/Hong_Kong
# 271 Asia/Hovd
# 272 Asia/Irkutsk
# 273 Asia/Istanbul
# 274 Asia/Jakarta
# 275 Asia/Jayapura
# 276 Asia/Jerusalem
# 277 Asia/Kabul
# 278 Asia/Kamchatka
# 279 Asia/Karachi

################################
## Localize a datetime object ##
################################
'''Use timezone_object.localize(datetime_object) to localize a datetime object to a specific timezone.'''

# Create a datetime object without timezone info
dt_obj = datetime.datetime(2024, 6, 18, 12, 0, 0)
print(dt_obj) # 2024-06-18 12:00:00

# Create a timezone object
tz_NY = pytz.timezone('America/New_York')

# Localize the datetime object to New York timezone
dt_NY = tz_NY.localize(dt_obj)
print(dt_NY) # 2024-06-18 12:00:00-04:00
'''
The -04:00 indicates that New York is 4 hours behind UTC during Daylight Saving Time.

So, at NY is 12:00 PM (noon) on June 18, 2024.
At UTC, it will be 16:00 PM (4 hours ahead).
'''

# One-liner version
dt_Seoul = pytz.timezone('Asia/Seoul').localize(datetime.datetime(2024, 6, 18, 12, 0, 0))
print(dt_Seoul) # 2024-06-18 12:00:00+09:00
'''
The +09:00 indicates that Seoul is 9 hours ahead of UTC.

So, at Seoul is 12:00 PM (noon) on June 18, 2024.
At UTC, it will be 03:00 AM (9 hours behind).
'''

##################################################
## Convert between timezones of datetime object ##
##################################################
'''Use datetime_object.astimezone(timezone_object) to convert a datetime object to another timezone.'''

# Create a datetime object in UTC timezone
dt_UTC = pytz.timezone('UTC').localize(datetime.datetime(2024, 6, 18, 8, 35, 12))
print(dt_UTC) # 2024-06-18 08:35:12+00:00

# Convert to NY timezone
dt_NY = dt_UTC.astimezone(pytz.timezone('America/New_York'))
print(dt_NY) # 2024-06-18 04:35:12-04:00

# Convert to Seoul timezone
print(dt_UTC.astimezone(pytz.timezone('Asia/Seoul'))) # 2024-06-18 17:35:12+09:00

# Convert to Ho Chi Minh City timezone
print(dt_UTC.astimezone(pytz.timezone('Asia/Ho_Chi_Minh'))) # 2024-06-18 15:35:12+07:00

#################################
## Normalize a datetime object ##
#################################
'''
------------------------------

Daylight Saving Time (DST) Transitions are when clocks change between Standard Time and Daylight Saving Time, 
happening twice per year:

Spring Forward
# Clocks jump ahead 1 hour (2:00 AM → 3:00 AM
# The 2:00 AM hour is skipped (doesn't exist)
# Day is only 23 hours long

Fall (Autumn) Back
# Clocks jump backward 1 hour (2:00 AM → 1:00 AM)
# The 1:00 AM hour happens twice (ambiguous)
# Day is 25 hours long

Why It Matters for Code
When datetime arithmetic crosses these boundaries, you can get non-existent times (spring) or ambiguous times (fall), 
and the UTC offset changes (e.g., -05:00 → -04:00). This is why normalize() is needed to fix the resulting datetime.

------------------------------

When you do datetime arithmetic (like adding hours) with pytz timezone-aware datetimes, 
the offset might not automatically update if you've crossed a daylight saving time (DST) boundary. 
This can leave you with a datetime that shows the wrong local time or offset, 
even though it represents the correct instant in absolute time.

normalize() fixes this by recalculating which UTC offset should apply at the new moment in local time. 
It ensures that your datetime matches real-world clocks after any addition or subtraction that might span a DST change.

------------------------------

Bottom line:
Call normalize() after any arithmetic on pytz-aware datetimes to get the correct wall clock time, 
especially when crossing DST transitions.

------------------------------

Use: 
# timezone_object.normalize(datetime_object)
# pytz.timezone('Your/Timezone').normalize(your_datetime_object)
'''

dt_Eastern = pytz.timezone('US/Eastern').localize(datetime.datetime(2024, 3, 10, 1, 30)) # Before DST starts
print(dt_Eastern) # 2024-03-10 01:30:00-05:00

dt_plus_3h = dt_Eastern + datetime.timedelta(hours=3) # Add 3 hours, crossing DST start
print(dt_plus_3h) # 2024-03-10 04:30:00-05:00

dt_normalized = pytz.timezone('US/Eastern').normalize(dt_plus_3h) # Normalize to adjust for DST
print(dt_normalized) # 2024-03-10 05:30:00-04:00

'''
After normalization, the time is adjusted to 05:30 AM, reflecting the start of Daylight Saving Time (UTC-4).

Why from -05:00 to -04:00?
- Before DST starts, Eastern Time is UTC-5.
- After DST starts, Eastern Time shifts to UTC-4.
'''

############################################
## Check timezone info of datetime object ##
############################################
'''Use datetime_object.tzinfo to check the timezone info of a datetime object.'''

naive_dt = datetime.datetime(2024,6,18,12,0,0) # Naive datetime object (no timezone info)
print(naive_dt.tzinfo) # None

localized_dt = pytz.timezone('Asia/Seoul').localize(naive_dt) # Localized datetime object
print(localized_dt.tzinfo) # Asia/Seoul

