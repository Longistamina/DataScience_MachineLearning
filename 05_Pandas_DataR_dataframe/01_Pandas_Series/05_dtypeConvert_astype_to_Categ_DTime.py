'''
Converting and casting data types is a fundamental operation in pandas data manipulation.

##########################################

1. .astype(): .astype("int64"), .astype("float64"), .astype("str"), .astype("category"), .astype("bool")

2. pd.to_numeric(): Safe Numeric Conversion

3. pd.Categorical(): Create Categorical Data

4. pd.to_datetime(): Convert to Datetime

5. pd.to_timedelta(): Convert to Timedelta

6. String conversion: .astype(str), .map(str), .apply(str), .apply(lambda x: str(x))
'''

import pandas as pd

#-------------------------------------------------------------------------------------------------#
#---------------------------------------- 1. .astype() -------------------------------------------#
#-------------------------------------------------------------------------------------------------#

s_nums = pd.Series([1, 2, 3, 4, 5])
s_str_int = pd.Series(['1', '2', '3', '4', '5'])
s_str_float = pd.Series(['1.5', '2.3', '3.6', '4.2', '5.0'])
s_mixed = pd.Series([1, 'a', 3.0, '4.5', False])

####################
## .astype(int64) ##
####################

s_convert = s_str_int.astype('int64')
print(s_convert)
# 0    1
# 1    2
# 2    3
# 3    4
# 4    5
# dtype: int64

s_convert = s_str_float.astype('int64') 
"""ValueError: invalid literal for int() with base 10: '1.5'"""


######################
## .astype(float64) ##
######################

s_convert = s_nums.astype('float64')
print(s_convert)
# 0    1.0
# 1    2.0
# 2    3.0
# 3    4.0
# 4    5.0
# dtype: float64

s_convert = s_str_int.astype('float64')
print(s_convert)
# 0    1.0
# 1    2.0
# 2    3.0
# 3    4.0
# 4    5.0
# dtype: float64

s_convert = s_str_float.astype('float64')
print(s_convert)
# 0    1.5
# 1    2.3
# 2    3.6
# 3    4.2
# 4    5.0
# dtype: float64

s_convert = s_mixed.astype('float64')  
"""ValueError: could not convert string to float: 'a'"""


##################
## .astype(str) ##
##################

s_convert = s_nums.astype('str')
print(s_convert)
# 0    1
# 1    2
# 2    3
# 3    4
# 4    5
# dtype: object

s_convert = s_mixed.astype('str')
print(s_convert)
# 0        1
# 1        a
# 2      3.0
# 3      4.5
# 4    False
# dtype: object

print(s_convert[4])
# 'False'


#########################
## .astype('category') ##
#########################

s_gender = pd.Series(["M", "M", "F", "M", "LGBTQ", "F", "M", "F", "LGBTQ", "M"])

'''
How .astype('category') works:
- Converts the Series to a categorical type.
- Categories are stored as a separate array, which saves memory.
- Useful for columns with a limited number of unique values.
- Categories are ordered from A-Z or increasing order.
'''

s_convert = s_gender.astype('category')
print(s_convert)
# 0        M
# 1        M
# 2        F
# 3        M
# 4    LGBTQ
# 5        F
# 6        M
# 7        F
# 8    LGBTQ
# 9        M
# dtype: category
# Categories (3, object): ['F', 'LGBTQ', 'M']


###################
## .astype(bool) ##
###################

s_bool_demo = pd.Series([0, -1.1, 2, '', 'text', None, True, False])

'''
How .astype(bool) works:
- Numeric values: 0 is False, all other numbers are True.
- Strings: Empty strings are False, non-empty strings are True.
- Booleans: True remains True, False remains False.
- None/NaN: Treated as False.
'''

s_convert = s_bool_demo.astype('bool')
print(s_convert)
# 0    False
# 1     True
# 2     True
# 3    False
# 4     True
# 5    False
# 6     True
# 7    False
# dtype: bool


#-------------------------------------------------------------------------------------------------#
#---------------------------------------- 2. pd.to_numeric() -------------------------------------#
#-------------------------------------------------------------------------------------------------#

'''
pd.to_numeric() works like .astype("int64") or .astype("float64"), but it is safer.
It can handle errors more gracefully, allowing you to specify how to deal with invalid parsing.

It has parameters like errors='coerce' to convert invalid parsing to NaN, 
or errors='ignore' to return the original data without conversion.
(By default, errors='raise', which raises an error for invalid parsing.)
'''

s_str_float = pd.Series(['1.5', '2.3', '3.6', '4.2', '5.0'])
s_mixed = pd.Series([1, 'a', 3.0, '4.5', False])

#------------------
## Try with valid numeric strings
#------------------

s_convert = pd.to_numeric(s_str_float)
print(s_convert)
# 0    1.5
# 1    2.3
# 2    3.6
# 3    4.2
# 4    5.0
# dtype: float64

#------------------
## Try with invalid mixed data (will raise an error)
#------------------

s_convert = pd.to_numeric(s_mixed) 
"""ValueError: Unable to parse string "a" at position 1"""

#------------------
## Try with mixed data, but coerce errors to NaN
#------------------

s_convert = pd.to_numeric(s_mixed, errors = 'coerce')
print(s_convert)
# 0    1.0
# 1    NaN
# 2    3.0
# 3    4.5
# 4    0.0 (The False is converted to 0.0)
# dtype: float64


#-------------------------------------------------------------------------------------------------#
#---------------------------------------- 3. pd.Categorical() ------------------------------------#
#-------------------------------------------------------------------------------------------------#

'''
pd.Categorical() is used to create categorical data from a Series.

It allows you to specify categories and their order, 
which can be useful for memory efficiency and performance 
when dealing with columns that have a limited number of unique values.

It's an improved version of .astype('category') that provides more control over the categories.

Note: missing values like NaN or None are not included in the categories by default.
'''

'''
By default, the ordered=False, meaning categories are unordered.
'''

'''
NOTE: THIS WILL NOT CREATE A pd.Series OBJECT, IT CREATES A pd.Categorical OBJECT.
=> MUST WRAP IT IN A pd.Series() TO GET A CATEGORICAL SERIES.
'''

#################################################
##            string gender example            ##
#################################################

lst_gender = ["M", "M", "F", "M", "LGBTQ", "F", "M", "F", "LGBTQ", "M"]

#---------------
## With ordered = False
#---------------

s_gender_categ = pd.Series(pd.Categorical(lst_gender, ordered = False))
print(s_gender_categ)
# 0        M
# 1        M
# 2        F
# 3        M
# 4    LGBTQ
# 5        F
# 6        M
# 7        F
# 8    LGBTQ
# 9        M
# dtype: category
# Categories (3, object): ['F', 'LGBTQ', 'M']

#---------------
## With ordered = True
#---------------

s_gender_categ = pd.Series(pd.Categorical(
    values = lst_gender,
    categories = ["LGBTQ", "F", "M"],  # Specify the order of categories
    ordered = True  # Set to True if you want to treat categories as ordered
))
print(s_gender_categ)
# 0        M
# 1        M
# 2        F
# 3        M
# 4    LGBTQ
# 5        F
# 6        M
# 7        F
# 8    LGBTQ
# 9        M
# dtype: category
# Categories (3, object): ['LGBTQ' < 'F' < 'M']


####################################################
##            numeric example with NaN            ##
####################################################

import numpy as np
lst_price_levels = [1, 1, 3, 2, 5, 2, None, 4, 4, np.nan, 3]

#---------------
## With ordered = False
#---------------

s_price_levels_categ = pd.Series(pd.Categorical(lst_price_levels, ordered = False))
print(s_price_levels_categ)
# 0       1
# 1       1
# 2       3
# 3       2
# 4       5
# 5       2
# 6     NaN
# 7       4
# 8       4
# 9     NaN
# 10      3
# dtype: category
# Categories (5, int64): [1, 2, 3, 4, 5]
'''Here, the NaN and None values are not included in the categories.'''

#---------------
## With ordered = True
#---------------

s_price_levels_categ = pd.Series(pd.Categorical(
    values = lst_price_levels,
    categories = [1, 2, 3, 4, 5], # Define the level
    ordered = True  # Set to True if you want to treat categories as ordered
))
print(s_price_levels_categ)
# 0       1
# 1       1
# 2       3
# 3       2
# 4       5
# 5       2
# 6     NaN
# 7       4
# 8       4
# 9     NaN
# 10      3
# dtype: category
# Categories (5, int64): [1 < 2 < 3 < 4 < 5]


#--------------------------------------------------------------------------------------------------#
#---------------------------------------- 4. pd.to_datetime() -------------------------------------#
#--------------------------------------------------------------------------------------------------#

'''
pd.to_datetime() is used to convert a Series or DataFrame column to datetime format.
It can handle various date formats and is very flexible in parsing dates.

It can also handle errors gracefully with parameters like 
errors='coerce' to convert invalid parsing to NaT (Not a Time),
errors='ignore' to return the original data without conversion,
or errors='raise' to raise an error for invalid parsing (default).
'''

s_dates = pd.Series(['2023-01-01', '2023-02-15', '2023-03-10', '2023-04-20'])
s_dates_invalid = pd.Series(['2023-01-01', '2023-02-15', '2023-03-10', 'invalid_date'])

#------------------
## Convert valid date strings to datetime
#------------------

s_dates_converted = pd.to_datetime(s_dates)
print(s_dates_converted)
# 0   2023-01-01
# 1   2023-02-15
# 2   2023-03-10
# 3   2023-04-20
# dtype: datetime64[ns]

#------------------
## Convert invalid date strings to datetime (will raise an error)
#------------------

s_dates_converted = pd.to_datetime(s_dates_invalid)  
"""ValueError: time data "invalid_date" doesn't match format "%Y-%m-%d", at position 3"""

#------------------
## Convert invalid date strings to datetime, but coerce errors to NaT
#------------------

s_dates_converted = pd.to_datetime(
    arg = s_dates_invalid, 
    errors='coerce'
)
print(s_dates_converted)
# 0   2023-01-01
# 1   2023-02-15
# 2   2023-03-10
# 3          NaT
# dtype: datetime64[ns]


#--------------------------------------------------------------------------------------------------#
#---------------------------------------- 5. pd.to_timedelta() ------------------------------------#
#--------------------------------------------------------------------------------------------------#

'''
pd.to_timedelta() is used to convert a Series or DataFrame column to timedelta format.
It can handle various time formats and is useful for representing durations or differences between dates.

It can also handle errors gracefully with parameters like
errors='coerce' to convert invalid parsing to NaT (Not a Time),
errors='ignore' to return the original data without conversion,
or errors='raise' to raise an error for invalid parsing (default).
'''

s_timedeltas = pd.Series(['2 days', '4 days 3 hours', '6 days 1 hours 15 minutes'])
s_timedeltas_invalid = pd.Series(['1 days', '2 days 3 hours', '3 days 4 hours 5 minutes', 'invalid_time'])

#------------------
## Convert valid timedelta strings to timedelta
#------------------

s_timedeltas_converted = pd.to_timedelta(s_timedeltas)
print(s_timedeltas_converted)
# 0   2 days 00:00:00
# 1   4 days 03:00:00
# 2   6 days 01:15:00
# dtype: timedelta64[ns]

#------------------
## Convert invalid timedelta strings to timedelta (will raise an error)
#------------------

s_timedeltas_converted = pd.to_timedelta(s_timedeltas_invalid) 
"""ValueError: Could not convert 'invalid_time' to NumPy timedelta"""

#------------------
## Convert invalid timedelta strings to timedelta, but coerce errors to NaT
#------------------

s_timedeltas_converted = pd.to_timedelta(
    arg = s_timedeltas_invalid, 
    errors='coerce'
)
print(s_timedeltas_converted)
# 0   1 days 00:00:00
# 1   2 days 03:00:00
# 2   3 days 04:05:00
# 3               NaT
# dtype: timedelta64[ns]


#---------------------------------------------------------------------------------------------------#
#---------------------------------------- 6. String conversion -------------------------------------#
#---------------------------------------------------------------------------------------------------#

s_nums = pd.Series([1.3, 5.4, 2.7, 8.6, 10])

print(s_nums.dtype)
# float64

##################
## .astype(str) ##
##################

s_str = s_nums.astype(str)
print(s_str)
# 0     1.3
# 1     5.4
# 2     2.7
# 3     8.6
# 4    10.0
# dtype: object


###############
## .map(str) ##
###############

s_str_map = s_nums.map(str)
print(s_str_map)
# 0     1.3
# 1     5.4
# 2     2.7
# 3     8.6
# 4    10.0
# dtype: object


#################
## .apply(str) ##
#################

s_str_apply = s_nums.apply(str)
print(s_str_apply)
# 0     1.3
# 1     5.4
# 2     2.7
# 3     8.6
# 4    10.0
# dtype: object


##############################
## .apply(lambda x: str(x)) ##
##############################

s_str_lambda = s_nums.apply(lambda x: str(x))
print(s_str_lambda)
# 0     1.3
# 1     5.4
# 2     2.7
# 3     8.6
# 4    10.0
# dtype: object

