#https://www.programiz.com/python-programming/datetime

# 0: Monday
# 1: Tuesday
# 2: Wednesday
# 3: Thursday
# 4: Friday
# 5: Saturday
# 6: Sunday

#---------------------------------------------------#
#-------------------- datetime ---------------------#
#---------------------------------------------------#

from datetime import datetime # from datetime: this datetime is a module, a .py file
                              # import datetime: this datetime is a class or a function inside the datetime module
from datetime import date

print()
print(datetime.now())   #Current moment
print(datetime.today()) #Current day

current_moment = datetime.now()
current_day = datetime.today()

current_day = current_moment.day        #Get the .day attribute of the current_moment object
print(current_day)

current_month = current_moment.month    #Get the .month attribute of the current_moment object
print(current_month)

current_year = current_moment.year      #Get the .year attribute of the current_moment object
print(current_year)

#max: datetime.datetime(9999, 12, 31, 23, 59, 59, 999999) the maximum datetime value in python.
#It means year 9999, December, day 31st, at 23h 59m 59s 999999ms

#min: datetime.datetime(1, 1, 1, 0, 0) the miniimum datetime value in python.
#It means year 1, January, day 1st, at 0h 0m

print()

#-------------------------------------------#
birthday1 = date(1890,5,19)             #Generate a datetime object, year 1890, May, day 29th
print(birthday1)

birthday2 = datetime(1890,5,19,23,30)   #Like above, but add hour (23) and minute (30)
print(birthday2)

#Attention: if using datetime.date() or datetime.datetime(), python will raise error since they are different functions
# datetime.date()     not equal   date()
# datetime.datetime() not equal   datetime()

#----- datetime.strptime() convert string into datetime object ------#
day1 = datetime.strptime('18/2/2024','%d/%m/%Y') # datetime.datetime(2024, 2, 18, 0, 0)
print(day1)

day2 = datetime.strptime('18-2-2024','%d-%m-%Y') # datetime.datetime(2024, 2, 18, 0, 0)
print(day2)

day3 = datetime.strptime('2/18/2024','%m/%d/%Y') # datetime.datetime(2024, 2, 18, 0, 0)
print(day3)

# day1 day2 day3 will share the same value as datetime.datetime(2024, 2, 18, 0, 0)

print()

#---- datetime.strftime() convert datetime object into string ---------------#
day4 = day1.strftime('%d-%m-%Y')    #  '18-02-2024'
day5 = day2.strftime('%A %d/%m/%Y') #  'Sunday 18/02/2024' (return a string object)
day6 = day3.strftime('%a %m/%d/%Y') #  'Sun 02/18/2024'
print()

#-------------------------------#
week_day = day1.strftime('%A')  #Return the day of the week as string, 'Sunday'
print(week_day)

index_week_day = day1.weekday() #Return the day of the week as index, return  6 = Sunday
print(index_week_day)
#(0: Monday, 1: Tuesday,....., 6: Sunday)


#---------------------------------------------------#
#-------------------- timedelta --------------------#
#---------------------------------------------------#

from datetime import date, datetime, timedelta
print()

#Calculate timedelta as day and second
day1 = datetime(2018,6,18,7,30,00)
day2 = datetime(2019,7,20,8,32,20)

t1 = day2-day1 #return t1 as a timedelta() object
print(t1)

delta_days = t1.days        #So ngay chenh lech
print(delta_days)

delta_seconds = t1.seconds  #So giay chenh lech
print(delta_seconds)

#Demo timedelta():
tomorrow = date.today() + timedelta(days=1)
print(tomorrow)

yesterday1 = date.today() + timedelta(days=-1)
print(yesterday1)

yesterday2 = date.today() - timedelta(days=1)
print(yesterday2)

# yesterday1 and yesterday2 will share the same value

#Create a timedelta() object
t = timedelta(days=5,hours=1,minutes=10,seconds=30)
total_delta_seconds = t.total_seconds() #Convert all the timedelta into seconds  = 436230 seconds
print(total_delta_seconds)

print()