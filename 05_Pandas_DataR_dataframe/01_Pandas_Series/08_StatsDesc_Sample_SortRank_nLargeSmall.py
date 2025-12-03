'''
Flow of contents:
1. Statistical methods
    + Reduction methods: .count(), .sum(), .product(), .mean(), .median(), .var(), .std(),
                         .min(), .max(), .quantile(), .skew(), .kurtosis(), .sem(), .describe()
    + Cumulative methods: .cumsum(), .cumprod(), .cummin(), .cummax(), .pct_change()
    + Covariance and Correlation methods: .cov(), .corr()

2. Sampling: .sample()
    
3. Ranking and Sorting methods
    + .rank() 
    + .sort_values(), .sort_index(), .argsort() 
    + .nlargest(), .nsmallest()
'''

import pandas as pd
import numpy as np


#----------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 1. Statistical methods ----------------------------------------------#
#----------------------------------------------------------------------------------------------------------------#

'''
#-------------------------------------
## Reduction methods
#-------------------------------------
'''

s_demo = pd.Series([2, 5.8, np.nan, 4.6, 14, 37, 25.2, np.nan, 9.3, 10.5])

##############
## .count() ##
##############
# .count() returns the number of non-NA/null observations in the Series.
print(s_demo.count())
# 8

print(s_demo.size)
# 10


############
## .sum() ##
############
# .sum() returns the sum of the values in the Series, excluding NA/null values.
print(s_demo.sum())
# 108.39999999999999

print(np.sum([2, 5.8, 4.6, 14, 37, 25.2, 9.3, 10.5]))
# 108.4


################
## .product() ##
################
# .product() returns the product of the values in the Series, excluding NA/null values.
print(s_demo.product())
# 68017140.37439999

print(2*5.8*4.6*14*37*25.2*9.3*10.5)
# 68017140.37439999


#############
## .mean() ##
#############
# .mean() returns the mean (average) of the values in the Series, excluding NA/null values.
print(s_demo.mean())
# 13.549999999999999


###############
## .median() ##
###############
# .median() returns the median (middle value) of the values in the Series, excluding NA/null values.
print(s_demo.median())
# 9.9


#################
## .variance() ##
#################
# .var() returns the variance of the values in the Series, excluding NA/null values.
print(s_demo.var())
# 140.9657142857143


############
## .std() ##
############
# .std() returns the standard deviation of the values in the Series, excluding NA/null values.
print(s_demo.std())
# 11.872898310257455


############
## .min() ##
############
# .min() returns the minimum value in the Series, excluding NA/null values.
print(s_demo.min())
# 2.0


############
## .max() ##
############
# .max() returns the maximum value in the Series, excluding NA/null values.
print(s_demo.max())
# 37.0


#################
## .quantile() ##
#################
# .quantile(q) returns the q-th quantile of the values in the Series, excluding NA/null values.

print(s_demo.quantile(q = 0.25))  # Q1 (25th percentile)
# 5.5

print(s_demo.quantile(q = [0.25, 0.5, 0.75]))   # Q1 - Q2 - Q3 (25th, 50th, and 75th percentiles)
# 0.25     5.5
# 0.50     9.9
# 0.75    16.8
# dtype: float64

'''
interpolation : {'linear', 'lower', 'higher', 'midpoint', 'nearest'}

This optional parameter specifies the interpolation method to use, 
when the desired quantile lies between two data points i and j:

linear: i + (j - i) * (x-i)/(j-i), where (x-i)/(j-i) is the fractional part of the index surrounded by i > j.
lower: i.
higher: j.
nearest: i or j whichever is nearest.
midpoint: (i + j) / 2.

For example, assumes Q1 is between 5.8 and 4.6, then:
+ linear: 5.8 + (4.6 - 5.8) * (0.25-0.2)/(0.3-0.2) = 5.8 + (-1.2) * 0.5 = 5.2
+ lower: 4.6
+ higher: 5.8
+ nearest: 5.8
+ midpoint: (5.8 + 4.6) / 2 = 5.2
'''

# By default, the interpolation method is 'linear', which is the most common method used for quantile calculations.

# Run with lower interpolation method
print(s_demo.quantile(q = [0.25, 0.5, 0.75], interpolation='lower'))
# 0.25     4.6
# 0.50     9.3
# 0.75    14.0
# dtype: float64


#############
## .skew() ##
#############
# .skew() returns the skewness of the distribution of values in the Series, excluding NA/null values.
print(s_demo.skew())
# 1.325643580258475


#################
## .kurtosis() ##
#################
# .kurtosis() returns the kurtosis of the distribution of values in the Series, excluding NA/null values.
print(s_demo.kurtosis())
# 1.122395658614919


############
## .sem() ##
############
# .sem() returns the standard error of the mean of the values in the Series, excluding NA/null values.
print(s_demo.sem())
# 4.197703453760673


#################
## .describe() ##
#################
# .describe() returns a summary of statistics for the Series, including count, mean, std, min, 25%, 50%, 75%, and max.
print(s_demo.describe())
# count     8.000000
# mean     13.550000
# std      11.872898
# min       2.000000
# 25%       5.500000
# 50%       9.900000
# 75%      16.800000
# max      37.000000
# dtype: float64


'''
#-------------------------------------
## Cumulative methods
#-------------------------------------
'''

s_demo = pd.Series([5.8, 4.6, 2, np.nan, 14, 37, 25.2, np.nan, 9.3, 10.5])

###############
## .cumsum() ##
###############
# .cumsum() returns the cumulative sum of the values in the Series.
print(s_demo.cumsum())
# 0      5.8 
# 1     10.4 (5.8 + 4.6)
# 2     12.4 (5.8 + 4.6 + 2)
# 3      NaN
# 4     26.4 (5.8 + 4.6 + 2 + 14)
# 5     63.4
# 6     88.6
# 7      NaN
# 8     97.9
# 9    108.4
# dtype: float64


################
## .cumprod() ##
################
# .cumprod() returns the cumulative product of the values in the Series.
print(s_demo.cumprod())
# 0    5.800000e+00
# 1    2.668000e+01 (5.8 * 4.6)
# 2    5.336000e+01 (5.8 * 4.6 * 2)
# 3             NaN
# 4    7.470400e+02 (5.8 * 4.6 * 2 * 14)
# 5    2.764048e+04
# 6    6.965401e+05
# 7             NaN
# 8    6.477823e+06
# 9    6.801714e+07
# dtype: float64

###############
## .cummin() ##
###############
# .cummin() returns the cumulative minimum of the values in the Series.
print(s_demo.cummin())
# 0    5.8 (min of [5.8])
# 1    4.6 (min of [5.8, 4.6])
# 2    2.0 (min of [5.8, 4.6, 2])
# 3    NaN 
# 4    2.0 (min of [5.8, 4.6, 2, 14])
# 5    2.0
# 6    2.0
# 7    NaN
# 8    2.0
# 9    2.0
# dtype: float64


###############
## .cummax() ##
###############
# .cummax() returns the cumulative maximum of the values in the Series.
print(s_demo.cummax())
# 0     5.8 (max of [5.8])
# 1     5.8 (max of [5.8, 4.6])
# 2     5.8 (max of [5.8, 4.6, 2])
# 3     NaN
# 4    14.0 (max of [5.8, 4.6, 2, 14])
# 5    37.0
# 6    37.0
# 7     NaN
# 8    37.0
# 9    37.0


###################
## .pct_change() ##
###################
s_demo_pctchange = pd.Series([100, 120, 150, 130, 160])

# .pct_change() returns the percentage change between the current and previous element in the Series.
print(s_demo_pctchange.pct_change())
# 0         NaN
# 1    0.200000
# 2    0.250000
# 3   -0.133333
# 4    0.230769


'''
#-------------------------------------
## Covariance and Correlation methods
#-------------------------------------
'''

s1 = pd.Series([10, 20, 30, 40, 50])
s2 = pd.Series([5, 25, 20, 44, 48])
s3 = pd.Series([5, 4, 3, 2, 1])

############
## .cov() ##
############
# .cov() returns the covariance between two Series.

print(s1.cov(s2))
# 262.5

print(s1.cov(s3))
# -62.5


#############
## .corr() ##
#############
# .corr() returns the correlation between two Series.
# Methods: 'pearson' (default), 'kendall', 'spearman'

print(s1.corr(s2, method = 'pearson'))  # Pearson correlation (default)
# 0.9364554314304976

print(s1.corr(s3, method = 'kendall'))  # Kendall correlation
# -0.9999999999999999


#----------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 2. Sampling -----------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------#

s_demo = pd.Series([5.8, 4.6, 2, np.nan, 14, 4.6, 25.2, np.nan, 9.3, 10.5])

#################
## .sample(n=) ##
#################
# .sample(n) returns a random sample of n items from the Series.

s_sampled_n = s_demo.sample(n = 3, random_state = 1)  # random_state for reproducibility
print(s_sampled_n)
# 2     2.0
# 9    10.5
# 6    25.2
# dtype: float64


####################
## .sample(frac=) ##
####################
# .sample(frac) returns a random sample of items from the Series, where frac is the fraction of items to return.

s_sampled_frac = s_demo.sample(frac = 0.5, random_state = 1, ignore_index = True)  # Targeting 50% of the data
print(s_sampled_frac)                                                              # ignore_index to reset the index
# 0     2.0
# 1    10.5
# 2    25.2
# 3    14.0
# 4     5.8
# dtype: float64


#----------------------------------------------------------------------------------------------------------------#
#------------------------------------- 3. Ranking and Sorting methods -------------------------------------------#
#----------------------------------------------------------------------------------------------------------------#

s_demo = pd.Series([5.8, 4.6, 2, np.nan, 14, 4.6, 25.2, np.nan, 9.3, 10.5])

#############
## .rank() ##
#############
# .rank() returns the ranks of the values in the Series, with ties getting the average rank.
print(s_demo.rank())
# 0    4.0
# 1    2.5
# 2    1.0
# 3    NaN
# 4    7.0
# 5    2.5
# 6    8.0
# 7    NaN
# 8    5.0
# 9    6.0

'''
method{"average", "min", "max", "first", "dense"}, default "average"

How to rank the group of records that have the same value (i.e. ties):
+ average: average rank of the group
+ min: lowest rank in the group
+ max: highest rank in the group
+ first: ranks assigned in order they appear in the array
+ dense: like 'min', but rank always increases by 1 between groups.

Default is "average", which is the most common method used for ranking.
'''

print(s_demo.rank(method = 'min'))
# 0    4.0
# 1    2.0
# 2    1.0
# 3    NaN
# 4    7.0
# 5    2.0
# 6    8.0
# 7    NaN
# 8    5.0
# 9    6.0

print(s_demo.rank(method = 'max'))
# 0    4.0
# 1    3.0
# 2    1.0
# 3    NaN
# 4    7.0
# 5    3.0
# 6    8.0
# 7    NaN
# 8    5.0
# 9    6.0
# dtype: float64


####################
## .sort_values() ##
####################
# .sort_values() sorts the values in the Series in ascending order by default.
print(s_demo.sort_values())
# 2     2.0
# 1     4.6
# 5     4.6
# 0     5.8
# 8     9.3
# 9    10.5
# 4    14.0
# 6    25.2
# 3     NaN
# 7     NaN
# dtype: float64

print(s_demo.sort_values(ascending=False))
# 6    25.2
# 4    14.0
# 9    10.5
# 8     9.3
# 0     5.8
# 1     4.6
# 5     4.6
# 2     2.0
# 3     NaN
# 7     NaN
# dtype: float64


###################
## .sort_index() ##
###################
# .sort_index() sorts the Series by its index in ascending order by default.
s_demo_indexed = pd.Series([5.8, 4.6, 2, 14, 4.6, 25.2],
                           index = [3, 1, 0, 4, 5, 2])

print(s_demo_indexed)
# 3     5.8
# 1     4.6
# 0     2.0
# 4    14.0
# 5     4.6
# 2    25.2
# dtype: float64

# .sort_index() sorts the Series by its index in ascending order by default.
print(s_demo_indexed.sort_index())
# 0     2.0
# 1     4.6
# 2    25.2
# 3     5.8
# 4    14.0
# 5     4.6
# dtype: float64

# .sort_index() sorts the Series by its index in descending order.
print(s_demo_indexed.sort_index(ascending=False))
# 5     4.6
# 4    14.0
# 3     5.8
# 2    25.2
# 1     4.6
# 0     2.0
# dtype: float64


################
## .argsort() ##
################
s_demo_default_index = pd.Series([5.8, 4.6, 2, 14, 4.6, 25.2]) 

# .argsort() returns the indices that would sort the Series in ascending order.
print(s_demo_default_index.argsort())
# 0    2 (index of value 2)
# 1    1 (index of value 4.6)
# 2    4 (index of value 4.6 duplicate)
# 3    0 (index of value 5.8)
# 4    3 (index of value 14)
# 5    5 (index of value 25.2)


#################
## .nlargest() ##
#################
# .nlargest(n) returns the n largest values in the Series.
print(s_demo_default_index.nlargest(3))
# 5    25.2
# 3    14.0
# 0     5.8
# dtype: float64


##################
## .nsmallest() ##
##################
# .nsmallest(n) returns the n smallest values in the Series.
print(s_demo_default_index.nsmallest(3))
# 2    2.0
# 1    4.6
# 4    4.6
# dtype: float64


'''
For all the sorting and ranking methods, if the data is string or object type,
=> the sorting is done lexicographically based on Unicode code points.
=> The sorting is case-sensitive, meaning uppercase letters come before lowercase letters.
For example, 'A' < 'a', 'B' < 'b', etc.
This means that 'A' will be sorted before 'a', and 'B' will be sorted before 'b'.
This behavior is consistent with the default sorting behavior in Python.
This is important to keep in mind when working with string data, as it can affect the order of the sorted values.
'''