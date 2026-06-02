'''
1. Statistical methods
+ Reduction methods: .count(), .len(), .sum(), .product(), .mean(), .median(), .var(), .std(),
.min(), .max(), .quantile(), .skew(), .kurtosis(), .describe()
+ Cumulative methods: .cum_sum(), .cum_prod(), .cum_min(), .cum_max(), .pct_change()
+ Covariance and Correlation methods: pl.cov(), pl.corr()

2. Sampling: .sample()
'''
import polars as pl

#----------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 1. Statistical methods ----------------------------------------------#
#----------------------------------------------------------------------------------------------------------------#

'''
#-------------------------------------
## Reduction methods
#-------------------------------------
'''

s_demo = pl.Series([2.0, 5.8, None, 4.6, 14.0, 37.0, 25.2, None, 9.3, 10.5])

##############
## .count() ##
##############
# .count() returns the number of non-null observations in the Series.

print(s_demo.count())
# 8

# .len() returns the total number of elements (including nulls).
print(s_demo.len())
# 10

############
## .sum() ##
############
# .sum() returns the sum of the values in the Series, excluding null values.

print(s_demo.sum())
# 108.4

################
## .product() ##
################
# .product() returns the product of the values in the Series, excluding null values.

print(s_demo.product())
# 68017140.37439999

#############
## .mean() ##
#############
# .mean() returns the mean (average) of the values in the Series, excluding null values.
print(s_demo.mean())
# 13.55

###############
## .median() ##
###############
# .median() returns the median (middle value) of the values in the Series, excluding null values.

print(s_demo.median())
# 9.9

#####################
## .var() / .std() ##
#####################
# .var() and .std() return the variance and standard deviation, excluding null values.
# By default, Polars uses ddof=1 (Delta Degrees of Freedom), just like pandas.

print(s_demo.var())
# 140.9657142857143

print(s_demo.std())
# 11.872898310257455

############
## .min() ##
############

print(s_demo.min())
# 2.0

############
## .max() ##
############

print(s_demo.max())
# 37.0

#################
## .quantile() ##
#################
# .quantile(quantile, interpolation="linear") returns the q-th quantile.
# Polars interpolation options: "nearest", "higher", "lower", "midpoint", "linear"

print(s_demo.quantile(0.25, interpolation="linear"))  # Q1 (25th percentile)
# 5.5

print(s_demo.quantile([0.25, 0.5, 0.75], interpolation="linear")) # Q1, Q2 and Q3
# [5.5, 9.9, 16.8]

# Run with lower interpolation method
print(s_demo.quantile([0.25, 0.5, 0.75], interpolation="lower"))
# [4.6, 9.3, 14.0]

#############
## .skew() ##
#############

print(s_demo.skew())
# 1.0628794487793372

print(s_demo.skew(bias=False)) # Like pandas default
# 1.325643580258475

#################
## .kurtosis() ##
#################

print(s_demo.kurtosis())
# -0.13219254351670662

print(s_demo.kurtosis(bias=False))
# 1.122395658614919

############
## .sem() ##
############
'''
Polars does NOT have a built-in .sem() (Standard Error of the Mean) method.
You must calculate it manually using the formula: std / sqrt(count)
'''

sem = s_demo.std() / (s_demo.count() ** 0.5)
print(sem)
# 4.197703453760673

#################
## .describe() ##
#################
'''
Unlike pandas (which returns a Series), Polars' Series.describe() returns a DataFrame!
It also includes a "null_count" row, which is very useful.
'''

print(s_demo.describe())
# shape: (9, 2)
# ┌────────────┬───────────┐
# │ statistic  ┆           │
# │ ---        ┆ ---       │
# │ str        ┆ f64       │
# ╞════════════╪═══════════╡
# │ count      ┆ 8.0       │
# │ null_count ┆ 2.0       │
# │ mean       ┆ 13.55     │
# │ std        ┆ 11.872898 │
# │ min        ┆ 2.0       │
# │ 25%        ┆ 5.5       │
# │ 50%        ┆ 9.9       │
# │ 75%        ┆ 16.8      │
# │ max        ┆ 37.0      │
# └────────────┴───────────┘

'''
#-------------------------------------
## Cumulative methods
#-------------------------------------
'''

s_demo = pl.Series([5.8, 4.6, 2.0, None, 14.0, 37.0, 25.2, None, 9.3, 10.5])

################
## .cum_sum() ##
################
# Polars uses snake_case for cumulative methods.
# Nulls are preserved in their original positions, but do not break the running total.

print(s_demo.cum_sum())
# shape: (10,)
# Series: '' [f64]
# [
# 	5.8
# 	10.4
# 	12.4
# 	null
# 	26.4
# 	63.4
# 	88.6
# 	null
# 	97.9
# 	108.4
# ]

#################
## .cum_prod() ##
#################

print(s_demo.cum_prod())
# shape: (10,)
# Series: '' [f64]
# [
# 	5.8
# 	26.68
# 	53.36
# 	null
# 	747.04
# 	27640.48
# 	696540.096
# 	null
# 	6477822.8832
# 	6.801714e7
# ]

################
## .cum_min() ##
################

print(s_demo.cum_min())
# shape: (10,)
# Series: '' [f64]
# [
# 	5.8
# 	4.6
# 	2.0
# 	null
# 	2.0
# 	2.0
# 	2.0
# 	null
# 	2.0
# 	2.0
# ]

################
## .cum_max() ##
################

print(s_demo.cum_max())
# shape: (10,)
# Series: '' [f64]
# [
# 	5.8
# 	5.8
# 	5.8
# 	null
# 	14.0
# 	37.0
# 	37.0
# 	null
# 	37.0
# 	37.0
# ]

###################
## .pct_change() ##
###################

s_demo_pctchange = pl.Series([100.0, 120.0, 150.0, 130.0, 160.0])
# .pct_change() calculates the percentage change between the current and previous element.

print(s_demo_pctchange.pct_change())
# shape: (5,)
# Series: '' [f64]
# [
# 	null
# 	0.2
# 	0.25
# 	-0.133333
# 	0.230769
# ]

'''
#-------------------------------------
## Covariance and Correlation methods
#-------------------------------------
'''

s1 = pl.Series([10.0, 20.0, 30.0, 40.0, 50.0])
s2 = pl.Series([5.0, 25.0, 20.0, 44.0, 48.0])
s3 = pl.Series([5.0, 4.0, 3.0, 2.0, 1.0])

############
## .cov() ##
############
'''
Polars does NOT have a .cov() method directly on Series objects.
Instead, you use the top-level pl.cov() function inside a pl.select() context
and extract the scalar value using .item().
'''

print(pl.select(pl.cov(s1, s2)).item())
# 262.5

print(pl.select(pl.cov(s1, s3)).item())
# -62.5

#############
## .corr() ##
#############
'''
Similarly, correlation is computed using the top-level pl.corr() function.
Methods supported: "pearson" (default), "spearman".
NOTE: "kendall" is NOT supported in Polars.
'''

print(pl.select(pl.corr(s1, s2, method="pearson")).item())
# 0.9364554314304976

print(pl.select(pl.corr(s1, s3, method="spearman")).item())
# -1.0


#----------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 2. Sampling -----------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------#

s_demo = pl.Series([5.8, 4.6, 2.0, None, 14.0, 4.6, 25.2, None, 9.3, 10.5])

#################
## .sample(n=) ##
#################
# Polars uses `seed` instead of pandas' `random_state`.

s_sampled_n = s_demo.sample(n=3, seed=1)
print(s_sampled_n)
# shape: (3,)
# Series: '' [f64]
# [
# 	2.0
# 	10.5
# 	25.2
# ]

########################
## .sample(fraction=) ##
########################
# Polars uses `fraction` instead of pandas' `frac`.
# Because Polars Series do not have custom index labels, there is no need for `ignore_index=True`.

s_sampled_frac = s_demo.sample(fraction=0.5, seed=1)
print(s_sampled_frac)
# shape: (5,)
# Series: '' [f64]
# [
# 	2.0
# 	10.5
# 	25.2
# 	14.0
# 	5.8
# ]
