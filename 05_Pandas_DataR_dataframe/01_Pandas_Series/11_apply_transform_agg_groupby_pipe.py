'''
1. .apply(): Element-wise Function Application

2. .map(): Dictionary Mapping

3. .transform(): Preserving Shape and Multiple Functions application

4. .agg(): Aggregation Functions

5. .groupby(): Grouping Data

6. .pipe(): Method Chaining with Custom Functions
'''

import pandas as pd
import numpy as np

s_mixed = pd.Series(["apple", "banana", "cherry", 42, 3.14, None])

np.random.seed(42)

s_nums = pd.Series(np.random.normal(loc = 3, scale = 2, size = 5)).round(2)
print(s_nums)
# 0    3.99
# 1    2.72
# 2    4.30
# 3    6.05
# 4    2.53
# dtype: float64

#---------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 1. .apply() ---------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

'''
.apply()  method invokes a function on each element or the entire Series.

Key Features:
+ Can apply functions element-wise or to the entire Series
+ Supports both built-in and custom functions
+ Most versatile method for function application
'''

s_applied = s_nums.apply(np.log) # Applying natural logarithm to each element
print(s_applied)
# 0    1.383791
# 1    1.000632
# 2    1.458615
# 3    1.800058
# 4    0.928219
# dtype: float64

s_applied = s_nums.apply(lambda x: 1/(1 + np.exp(-x))) # Apply Sigmoid function
print(s_applied)
# 0    0.981836
# 1    0.938197
# 2    0.986613
# 3    0.997648
# 4    0.926218
# dtype: float64

s_applied = s_mixed.apply(lambda x: str(x).upper() if isinstance(x, str) else x) # Convert strings to uppercase
print(s_applied)
# 0     APPLE
# 1    BANANA
# 2    CHERRY
# 3        42
# 4      3.14
# 5      None
# dtype: object


#---------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 2. .map() -----------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

'''
The map() method transforms each element by mapping values using dictionaries, Series, or functions.

Key Features:
+ Optimized for simple transformations and mappings
+ Can use dictionaries, Series, or functions as mapping source
+ Returns NaN for unmapped values when using dict/Series
'''

s_mapped = s_nums.map(np.sin)  # Applying sine function to each element
# print(s_mapped)
# 0   -0.750228
# 1    0.409214
# 2   -0.916166
# 3   -0.231078
# 4    0.574172
# dtype: float64

s_mapped = s_nums.map(lambda x: x**2)  # Squaring each element
print(s_mapped)
# 0    15.9201
# 1     7.3984
# 2    18.4900
# 3    36.6025
# 4     6.4009
# dtype: float64


######################################
## Using a dictionary to map values ##
######################################

s_mapped = s_mixed.map({"apple": "A", "banana": "B", "cherry": "C"})
print(s_mapped)
# 0      A
# 1      B
# 2      C
# 3    NaN
# 4    NaN
# 5    NaN
# dtype: object

'''Unmapped values will be NaN if not found in the mapping dictionary.'''


#---------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 3. .transform() -------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

'''
The transform() method applies functions while maintaining the same shape as the input Series.

Key Features:
+ Always returns Series with same length as input
+ Can apply multiple functions simultaneously
+ Useful for normalization and standardization
'''

# Single function transformation
s_transformed = s_nums.transform(lambda x: x+ 1)
print(s_transformed)
# 0    4.99
# 1    3.72
# 2    5.30
# 3    7.05
# 4    3.53
# dtype: float64

# Multiple functions transformation
s_transformed = s_nums.transform(func = {'x+1':lambda x: x+1, 'x*2':lambda x: x*2})
print(s_transformed)
#     x+1    x*2
# 0  4.99   7.98
# 1  3.72   5.44
# 2  5.30   8.60
# 3  7.05  12.10
# 4  3.53   5.06


##################################
## .transform() with .groupby() ##
##################################

df_date_value = pd.DataFrame({
    "Date": [
        "1st", "2nd", "3rd", "4th",
        "1st", "2nd", "3rd", "4th"],
    "Data": [5, 8, 6, 1, 50, 100, 60, 120],
})

print(df_date_value)
#   Date  Data
# 0  1st     5
# 1  2nd     8
# 2  3rd     6
# 3  4th     1
# 4  1st    50
# 5  2nd   100
# 6  3rd    60
# 7  4th   120

# Apply transform with groupby
df_transformed = df_date_value.groupby("Date").transform("sum")
print(df_transformed)
#    Data
# 0    55
# 1   108
# 2    66
# 3   121
# 4    55
# 5   108
# 6    66
# 7   121

'''
The 0-indexed row and the 4-indexed row share the same value (55) because they belong to the same group "1st", and so on.
'''


#---------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 4. .agg() -----------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

'''
The agg() method applies aggregation functions to Series or DataFrame, returning a single value or a Series of values.

Key Features:
+ Can apply single or multiple aggregation functions
+ Returns scalar, Series, or DataFrame depending on input
+ Supports both string function names and custom functions
'''

s_agg = s_nums.agg(['mean', 'std', 'min', 'max'])  # Applying multiple aggregation functions
print(s_agg)
# mean    3.918000
# std     1.419355
# min     2.530000
# max     6.050000
# dtype: float64


#########################################
## .agg() with dictionary of functions ##
#########################################

s_agg = s_nums.agg(
    {
        "custom_mean": "mean", 
        "custom_sum": "sum", 
        "custom_range": lambda x: x.max() - x.min()
    }
)

print(s_agg)
# custom_mean      3.918
# custom_sum      19.590
# custom_range     3.520
# dtype: float64


############################
## .agg() with .groupby() ##
############################

df_date_value = pd.DataFrame({
    "Date": [
        "1st", "2nd", "3rd", "4th",
        "1st", "2nd", "3rd", "4th"],
    "Data": [5, 8, 6, 1, 50, 100, 60, 120],
})

print(df_date_value)
#   Date  Data
# 0  1st     5
# 1  2nd     8
# 2  3rd     6
# 3  4th     1
# 4  1st    50
# 5  2nd   100
# 6  3rd    60
# 7  4th   120

'''Apply agg with groupby'''
df_agg = df_date_value.groupby("Date").agg({"Date": "count", "Data": ["mean", "sum"]})
print(df_agg)
#       Date  Data     
#      count  mean  sum
# Date                 
# 1st      2  27.5   55
# 2nd      2  54.0  108
# 3rd      2  33.0   66
# 4th      2  60.5  121

# join the column names for better readability
df_agg.columns = ['_'.join(col).strip() for col in df_agg.columns]
print(df_agg)
#       Date_count  Data_mean  Data_sum
# Date                                 
# 1st            2       27.5        55
# 2nd            2       54.0       108
# 3rd            2       33.0        66
# 4th            2       60.5       121


#---------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 5. .groupby() -------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

'''
The groupby() method splits data into groups for separate analysis.

Key Features:
+ Follows split-apply-combine methodology
+ Can group by index levels or external groupers
+ Enables group-wise operations
'''

s_birds_flight = pd.Series(
    data = [390., 350., 30., 20.],
    index = ['Falcon', 'Falcon', 'Parrot', 'Parrot']
)

print(s_birds_flight)
# Falcon    390.0
# Falcon    350.0
# Parrot     30.0
# Parrot     20.0
# dtype: float64


###############################
## Groupping by using level= ##
###############################

s_grouped = s_birds_flight.groupby(level = 0).mean()  # Grouping by the first index level (bird type)
print(s_grouped)
# Falcon    370.0
# Parrot     25.0
# dtype: float64


############################
## Groupping by using by= ##
############################

s_grouped = s_birds_flight.groupby(by = ["a", "b", "a", "b"]).agg(["mean", "max"])
print(s_grouped)
#     mean    max
# a  210.0  390.0
# b  185.0  350.0
# dtype: float64

'''
In this case:
+ Group "a" contains Falcon-390 and Parrot-30, resulting in a mean of 210 and a max of 390.
+ Group "b" contains Falcon-350 and Parrot-20, resulting in a mean of 185 and a max of 350.
'''


#----------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 6. .pipe() -----------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------#

'''
The pipe() method enables method chaining by applying functions that expect Series or DataFrames.

Key Features:
+ Facilitates readable method chaining
+ Can pass additional arguments to functions
+ Supports tuple syntax for functions expecting data as non-first argument
'''

import scipy as sp

################################
## Handle quantitative series ##
################################

np.random.seed(42)

query = (
    pd.Series(np.random.normal(loc = 3, scale = 2, size = 30))
    .round(2)
    .pipe(lambda ser: ser[ser < 2.9])
    .pipe(lambda ser: sp.stats.shapiro(ser))
)

print(query)
# ShapiroResult(statistic=np.float64(0.8865328120075993), pvalue=np.float64(0.033671906069434675))


###############################
## Handle categorical series ##
###############################

s_gender = pd.Series(["F", "LGBTQ", "M", "F", "M", "LGBTQ", "F", "M", "F", "M", "M", "LGBTQ"])

query = (
    s_gender.copy()
    .value_counts()
    .pipe(lambda ser: ser/ser.sum() * 100)  # Calculate percentage
    .round(2) # Round to 2 decimal places
    .pipe(lambda ser: ser.astype(str) + "%")   # Convert to string with percentage sign
)

print(query)
# M        41.67%
# F        33.33%
# LGBTQ     25.0%
# Name: count, dtype: object