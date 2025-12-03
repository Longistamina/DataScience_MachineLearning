'''
Boolean Indexing Boolean Filtering is a powerful technique
that allows you to filter data based on specific conditions. 

###############################

1. Single Condition Examples:
   + Logic Operators: >, <, >=, <=, .between(), ==, !=
   + .isin()
   + String Boolean: .str.contains(), .str.startswith(), .str.endswith(), ....
   + DateTime Boolean: .dt.is_month_start, .dt.is_month_end, ...

2. Negation of Condition: ~ (tilde) operator

3. Combine Multiple Conditions:
   + & (and),
   + | (or)
   + Combine & and |
'''

import pandas as pd
import numpy as np

np.random.seed(42)
s1_nums = pd.Series(np.random.uniform(10, 20, 10)).round(2)

np.random.seed(24)
s2_nums = pd.Series(np.random.uniform(10, 20, 10)).round(2)

print(s1_nums)
# 0    13.75
# 1    19.51
# 2    17.32
# 3    15.99
# 4    11.56
# 5    11.56
# 6    10.58
# 7    18.66
# 8    16.01
# 9    17.08
# dtype: float64

print(s2_nums)
# 0    13.21
# 1    13.66
# 2    17.10
# 3    19.00
# 4    15.34
# 5    12.47
# 6    16.72
# 7    15.62
# 8    15.43
# 9    18.93
# dtype: float64


#----------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 1. Single Condition Examples -----------------------------------------#
#----------------------------------------------------------------------------------------------------------------#

#######################################################
## Logic Operators: >, <, >=, <=, .between(), ==, != ##
#######################################################

#-------------
## > (greater than)
#-------------

print(s1_nums > 15)
# 0    False
# 1     True
# 2     True
# 3     True
# 4    False
# 5    False
# 6    False
# 7     True
# 8     True
# 9     True
# dtype: bool

print(s1_nums[s1_nums > 15]) # Returns values greater than 15 (True)
# 1    19.51
# 2    17.32
# 3    15.99
# 7    18.66
# 8    16.01
# 9    17.08
# dtype: float64

print(s2_nums[s2_nums > s1_nums]) # Returns values greater than corresponding values (same index) in s1_nums
# 3    19.00 (> 15.99)
# 4    15.34 (> 11.56)
# 5    12.47 (> 11.56)
# 6    16.72 (> 10.58)
# 9    18.93 (> 17.08)
# dtype: float64

#-------------
## < (less than)
#-------------

print(s1_nums[s1_nums < 13]) # Returns values less than 13 (True)
# 4    11.56
# 5    11.56
# 6    10.58
# dtype: float64

print(s2_nums[s2_nums < s1_nums]) # Returns values less than corresponding values (same index) in s1_nums
# 0    13.21
# 1    13.66
# 2    17.10
# 7    15.62
# 8    15.43
# dtype: float64

#-------------
## >= (greater than or equal to)
#-------------

print(s1_nums[s1_nums >= 15.99]) # Returns values greater than or equal to 15.99 (True)
# 1    19.51
# 2    17.32
# 3    15.99
# 7    18.66
# 8    16.01
# 9    17.08
# dtype: float64

print(s2_nums[s2_nums >= s1_nums]) # Returns values greater than or equal to corresponding values (same index) in s1_nums
# 3    19.00
# 4    15.34
# 5    12.47
# 6    16.72
# 9    18.93
# dtype: float64

#-------------
## <= (less than or equal to)
#-------------

print(s1_nums[s1_nums <= 11.56]) # Returns values less than or equal to 13 (True)
# 4    11.56
# 5    11.56
# 6    10.58
# dtype: float64

print(s2_nums[s2_nums <= s1_nums]) # Returns values less than or equal to corresponding values (same index) in s1_nums
# 0    13.21
# 1    13.66
# 2    17.10
# 7    15.62
# 8    15.43
# dtype: float64

#-------------
## .between()
#-------------
'''
inclusive = "both" (default): [left, right] or left <= x <= right
inclusive = "neither": (left, right) or left < x < right
inclusive = "left": [left, right) or left <= x < right
inclusive = "right": (left, right] or left < x <= right
'''

print(s1_nums[s1_nums.between(10, 15.99)]) # Returns values between 10 and 15.99 (both inclusive)
# 0    13.75
# 3    15.99
# 4    11.56
# 5    11.56
# 6    10.58
# dtype: float64

print(s1_nums[s1_nums.between(10, 15.99, inclusive = "left")]) # Returns values between 15.99 (left inclusive)
# 0    13.75
# 4    11.56
# 5    11.56
# 6    10.58
# dtype: float64
'''The value 15.99 is excluded because the right endpoint is not inclusive.'''

#-------------
## == (equal to)
#-------------

print(s1_nums[s1_nums == 11.56]) # Returns values equal to 11.56 (True)
# 4    11.56
# 5    11.56
# dtype: float64

print(s2_nums[s2_nums == s1_nums]) # Returns values equal to corresponding values (same index) in s1_nums
# Series([], dtype: float64)

#-------------
## != (not equal to)
#-------------

print(s1_nums[s1_nums != 11.56]) # Returns values not equal to 11.56 (True)
# 0    13.75
# 1    19.51
# 2    17.32
# 3    15.99
# 6    10.58
# 7    18.66
# 8    16.01
# 9    17.08
# dtype: float64

print(s2_nums[s2_nums != s1_nums]) # Returns values not equal to corresponding values (same index) in s1_nums
# 0    13.21
# 1    13.66
# 2    17.10
# 3    19.00
# 4    15.34
# 5    12.47
# 6    16.72
# 7    15.62
# 8    15.43
# 9    18.93
# dtype: float64
'''All values are returned because none of the values in s2_nums are equal to the corresponding values in s1_nums.'''

###############################
##          .isin()          ##
###############################

s_mamals =  pd.Series(['llama', 'cow', 'llama', 'beetle', 'llama', 'hippo'])

print(s_mamals.isin(['cow', 'llama']))
# 0     True ('llama')
# 1     True ('cow')
# 2     True ('llama')
# 3    False
# 4     True ('llama')
# 5    False
# dtype: bool

print(s_mamals[s_mamals.isin(['cow', 'llama'])]) # Returns values that are either 'cow' or 'llama'
# 0    llama
# 1      cow
# 2    llama
# 4    llama
# dtype: object

print(s_mamals[s_mamals.isin(['llama'])]) # Returns values that are 'llama'
# 0    llama
# 2    llama
# 4    llama
# dtype: object


##################################
##        String Boolean        ##
##################################

import pytz

s_timezones = pd.Series(pytz.all_timezones)

print(s_timezones[s_timezones.str.contains("Seoul")]) # Returns values that contain the substring "Africa"
# 311    Asia/Seoul
# dtype: object

print(s_timezones[s_timezones.str.startswith("Australia")]) # Returns values that start with "Australia"
# 347            Australia/ACT
# 348       Australia/Adelaide
# 349       Australia/Brisbane
# 350    Australia/Broken_Hill
# 351       Australia/Canberra
# 352         Australia/Currie
# 353         Australia/Darwin
# 354          Australia/Eucla
# 355         Australia/Hobart
# 356            Australia/LHI
# 357       Australia/Lindeman
# 358      Australia/Lord_Howe
# 359      Australia/Melbourne
# 360            Australia/NSW
# 361          Australia/North
# 362          Australia/Perth
# 363     Australia/Queensland
# 364          Australia/South
# 365         Australia/Sydney
# 366       Australia/Tasmania
# 367       Australia/Victoria
# 368           Australia/West
# 369     Australia/Yancowinna
# dtype: object

print(s_timezones[s_timezones.str.endswith("lu")]) # Returns values that end with "lu"
# 426            Etc/Zulu
# 544    Pacific/Honolulu
# 596                Zulu
# dtype: object

print(s_timezones[s_timezones == "Zulu"]) # Returns values that are exactly equal to "Zulu"
# 596    Zulu
# dtype: object

#################################
##      DateTime Boolean       ##
#################################

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

print(s_datetime[s_datetime.dt.is_quarter_start]) # Returns values that are the start of a quarter
# 0   2023-01-01
# dtype: datetime64[ns]

print(s_datetime[s_datetime.dt.is_quarter_end]) # Returns values that are the end of a quarter
# 3   2023-03-31
# 6   2023-06-30
# dtype: datetime64[ns]


#----------------------------------------------------------------------------------------------------------------#
#--------------------------------- 2. Negation of Condition: ~ (tilde) operator ---------------------------------#
#----------------------------------------------------------------------------------------------------------------#

'''
The tilde (~) operator is used to negate a boolean condition in Pandas.
From True to False, and from False to True.
'''

print(s1_nums > 15)
# 0    False
# 1     True
# 2     True
# 3     True
# 4    False
# 5    False
# 6    False
# 7     True
# 8     True
# 9     True
# dtype: bool

# Apply the negation operator (~) to invert the boolean values
print(~(s1_nums > 15))
# 0     True
# 1    False
# 2    False
# 3    False
# 4     True
# 5     True
# 6     True
# 7    False
# 8    False
# 9    False
# dtype: bool

# Apply in filtering
print(s1_nums[~(s1_nums > 15)]) # Returns values NOT greater than 15
# 0    13.75
# 4    11.56
# 5    11.56
# 6    10.58
# dtype: float64

s_mamals =  pd.Series(['llama', 'cow', 'llama', 'beetle', 'llama', 'hippo'])
print(s_mamals[~s_mamals.isin(['cow', 'llama'])]) # Returns values that are neither 'cow' nor 'llama'
# 3    beetle
# 5     hippo
# dtype: object

print(s_datetime[~s_datetime.dt.is_quarter_end]) # Returns values that are NOT the end of a quarter
# 0   2023-01-01
# 1   2023-01-31
# 2   2023-02-28
# 4   2023-04-30
# 5   2023-05-31
# dtype: datetime64[ns]


#----------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 3. Combine Multiple Conditions ------------------------------------------#
#----------------------------------------------------------------------------------------------------------------#

###########################
##       & (and)         ##
###########################
'''True if only all the conditions (clauses) are True.'''

print(s1_nums[(s1_nums > 12) & (s1_nums.round(0) % 2 == 0)]) # Returns values greater than 12 AND rounded value is even number
# 0    13.75 (13.75 > 12 and rounded is 14, which is even)
# 1    19.51 (19.51 > 12 and rounded is 20, which is even)
# 3    15.99
# 8    16.01
# dtype: float64

print(s1_nums[~((s1_nums > 12) & (s1_nums.round(0) % 2 == 0))]) # Returns the NEGATION of above condition
# 2    17.32 (17.32 > 12 but rounded is 17, which is odd)
# 4    11.56 (11.56 < 12)
# 5    11.56
# 6    10.58
# 7    18.66
# 9    17.08
# dtype: float64

import pytz
s_timezones = pd.Series(pytz.all_timezones)
print(s_timezones[s_timezones.str.contains("Asia") & s_timezones.str.endswith(pat = ("e", "u"))])
# 240        Asia/Aqtau
# 241       Asia/Aqtobe
# 244       Asia/Atyrau
# 247         Asia/Baku
# 264     Asia/Dushanbe
# 281    Asia/Kathmandu
# 282     Asia/Katmandu
# 290        Asia/Macau
# 313    Asia/Singapore
# 320       Asia/Thimbu
# 321      Asia/Thimphu
# 329    Asia/Vientiane
# dtype: object

###########################
##       | (or)          ##
###########################
'''False if only all the conditions (clauses) are False.'''

print(s1_nums[(s1_nums < 12) | (s1_nums > 18)]) # Returns values less than 12 OR greater than 18
# 1    19.51
# 4    11.56
# 5    11.56
# 6    10.58
# 7    18.66
# dtype: float64

print(s1_nums[~((s1_nums < 12) | (s1_nums > 18))]) # Returns the NEGATION of above condition
# 0    13.75
# 2    17.32
# 3    15.99
# 8    16.01
# 9    17.08
# dtype: float64

import pytz
s_tzs = pd.Series(pytz.all_timezones)
print(s_tzs[s_tzs.str.contains("Kyoto") | s_tzs.str.contains("Tokyo") | s_tzs.str.contains("Seoul")])
# 311    Asia/Seoul
# 322    Asia/Tokyo
# dtype: object

###############################
##      Combine & and |      ##
###############################

print(s1_nums[((s1_nums < 12) | (s1_nums > 18)) & (s1_nums.round(0) % 2 == 0)])
# 1    19.51
# 4    11.56
# 5    11.56
# dtype: float64

print(s1_nums[~(((s1_nums < 12) | (s1_nums > 18)) & (s1_nums.round(0) % 2 == 0))])
# 0    13.75
# 2    17.32
# 3    15.99
# 6    10.58
# 7    18.66
# 8    16.01
# 9    17.08
# dtype: float64

import pytz
s_tzs = pd.Series(pytz.all_timezones)
print(s_tzs[(s_tzs.str.contains("Asia") & s_tzs.str.endswith(pat = ("e", "u"))) | s_tzs.str.contains("Tokyo")])
# 240        Asia/Aqtau
# 241       Asia/Aqtobe
# 244       Asia/Atyrau
# 247         Asia/Baku
# 264     Asia/Dushanbe
# 281    Asia/Kathmandu
# 282     Asia/Katmandu
# 290        Asia/Macau
# 313    Asia/Singapore
# 320       Asia/Thimbu
# 321      Asia/Thimphu
# 322        Asia/Tokyo
# 329    Asia/Vientiane
# dtype: object
'''
Though "Tokyo" does not end with "e" or "u" (first condition),
but it satisfies the second condition (s_tzs.str.contains("Tokyo")),
=> Still returned in the final result.
'''