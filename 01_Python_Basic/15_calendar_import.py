# 0: Monday
# 1: Tuesday
# 2: Wednesday
# 3: Thursday
# 4: Friday
# 5: Saturday
# 6: Sunday

import calendar


############################################
## .isleap(): Check leap year (nam nhuan) ##
############################################

check_leap_year_1 = calendar.isleap(2000) 
print(check_leap_year_1) # True

check_leap_year_2 = calendar.isleap(1999) 
print(check_leap_year_2) # False


#########################################
##            .monthrange()            ##
#########################################

tuple_MR = calendar.monthrange(2019,11)
print(tuple_MR) # (4,30)

'''
# Return a tuple (4,30)
# 4 is the weekday index of the first day of the month, 4 ~ Friday, means 1/11/2019 is Friday
# 30 means November has 30 days
'''

#--------------
## Get the number of days from monthrange()
#--------------

month_days_1 = calendar.monthrange(2019,11)[1] # Get the 2nd element in tuple MR, the number of days = 30
print(month_days_1) # 30

tuple_MR = calendar.monthrange(2019,11)
month_days_2 = tuple_MR[1] 
print(month_days_2) # 30


#--------------
## Get the weekday index of the month's first day
#--------------

index_weekday_1 = calendar.monthrange(2019,11)[0]
print(index_weekday_1) # 4

tuple_MR = calendar.monthrange(2019,11)
index_weekday_2 = tuple_MR[0] 
print(index_weekday_1) #4


#--------------
## Get both information
#--------------

index_weekday, month_days = calendar.monthrange(2020,8)
print(index_weekday, month_days)


#####################################################
##                 .monthcalendar()                ##
#####################################################

november_2019 = calendar.monthcalendar(2019,11)
print(november_2019)
# [[0, 0, 0, 0, 1, 2, 3], [4, 5, 6, 7, 8, 9, 10], [11, 12, 13, 14, 15, 16, 17], [18, 19, 20, 21, 22, 23, 24], [25, 26, 27, 28, 29, 30, 0]]

# [[0, 0, 0, 0, 1, 2, 3], week 1, the 1st day of november_2019 is Friday (index = 4, means Friday)
# [4, 5, 6, 7, 8, 9, 10], week 2
# [11, 12, 13, 14, 15, 16, 17], week 3
# [18, 19, 20, 21, 22, 23, 24], week 4
# [25, 26, 27, 28, 29, 30, 0]]  week 5
