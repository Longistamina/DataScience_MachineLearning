'''
1. Rolling: .rolling_mean(), .rolling_sum(), etc. (Direct methods, no intermediate .rolling() object)
2. Expanding: Polars lacks a dedicated .expanding() object. Use cumulative methods (.cum_sum()) or rolling with a large window.
3. Exponentially Weighted: .ewm_mean() (Direct method, no intermediate .ewm() object)
'''

import polars as pl
import numpy as np

np.random.seed(42)
s_nums = pl.Series(np.random.normal(loc=3, scale=2, size=5)).round(2)
print(s_nums)
# shape: (5,)
# Series: '' [f64]
# [
# 	3.99
# 	2.72
# 	4.3
# 	6.05
# 	2.53
# ]


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 1. .rolling_...() --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
In Polars, rolling operations are called directly on the Series as methods like
.rolling_mean(), .rolling_sum(), .rolling_min(), .rolling_max(), etc.
There is NO intermediate .rolling() object like in pandas.

Key Parameters:
+ window_size: Size of the moving window (required). Can be integer or string (for temporal).
+ min_periods: Minimum observations needed for a value (defaults to window size).
+ center: If True, labels are set at the center of the window.
+ weights: List of weights for weighted calculations.
'''

###############
## Basic use ##
###############

print(s_nums)
# shape: (5,)
# Series: '' [f64]
# [
# 	3.99
# 	2.72
# 	4.3
# 	6.05
# 	2.53
# ]

# Calculate rolling mean with a window of 2
s_rolling = s_nums.rolling_mean(window_size=2)
print(s_rolling)
# shape: (5,)
# Series: '' [f64]
# [
# 	null
# 	3.355
# 	3.51
# 	5.175
# 	4.29
# ]

# Calculate rolling mean with a window of 3
s_rolling = s_nums.rolling_mean(window_size=3)
print(s_rolling)
# shape: (5,)
# Series: '' [f64]
# [
# 	null
# 	null
# 	3.67
# 	4.356667
# 	4.293333
# ]

###################################
## Rolling with time-based index ##
###################################
'''
Polars handles time-based rolling natively using strings like "2s", "3d" for the window_size.
However, unlike pandas (which relies on the DatetimeIndex), Polars requires the temporal
column to be explicitly specified. This is typically done in a DataFrame context
using the expression `.rolling_mean_by()`.
'''

times = pl.Series([
    '2013-01-01 09:00:00',
    '2013-01-01 09:00:02',
    '2013-01-01 09:00:03',
    '2013-01-01 09:00:05',
    '2013-01-01 09:00:06'
]).str.to_datetime()

df_time = pl.DataFrame({"time": times, "value": s_nums})

# Calculate rolling mean with a 2-second window
# By default, Polars groups by the 'time' column and looks backward (closed="right").
df_rolling_time = df_time.with_columns(
    rolling_mean = pl.col("value").rolling_mean_by(window_size="2s", by="time")
)
print(df_rolling_time)
# shape: (5, 3)
# ┌─────────────────────┬───────┬──────────────┐
# │ time                ┆ value ┆ rolling_mean │
# │ ---                 ┆ ---   ┆ ---          │
# │ datetime[μs]        ┆ f64   ┆ f64          │
# ╞═════════════════════╪═══════╪══════════════╡
# │ 2013-01-01 09:00:00 ┆ 3.99  ┆ 3.99         │
# │ 2013-01-01 09:00:02 ┆ 2.72  ┆ 2.72         │
# │ 2013-01-01 09:00:03 ┆ 4.3   ┆ 3.51         │
# │ 2013-01-01 09:00:05 ┆ 6.05  ┆ 6.05         │
# │ 2013-01-01 09:00:06 ┆ 2.53  ┆ 4.29         │
# └─────────────────────┴───────┴──────────────┘


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 2. Expanding -------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Polars DOES NOT have a dedicated .expanding() method like pandas.
Instead, expanding operations are handled by:
1. Cumulative methods (.cum_sum(), .cum_min(), .cum_max()) for sum/min/max.
2. Using .rolling_mean() with a window size equal to the length of the Series and min_periods=1.
'''

###############
## Basic use ##
###############

print(s_nums)

# Expanding sum (equivalent to pandas .expanding().sum())
s_expanding_sum = s_nums.cum_sum()
print(s_expanding_sum)
# shape: (5,)
# Series: '' [f64]
# [
# 	3.99
# 	6.71
# 	11.01
# 	17.06
# 	19.59
# ]

# Expanding mean (Workaround: rolling_mean with window_size = len(Series) and min_samples=1)
s_expanding_mean = s_nums.rolling_mean(window_size=s_nums.len(), min_samples=1)
print(s_expanding_mean)
# shape: (5,)
# Series: '' [f64]
# [
# 	3.99
# 	3.355
# 	3.67
# 	4.265
# 	3.918
# ]


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 3. .ewm_mean() -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Polars provides .ewm_mean(), .ewm_std(), and .ewm_var() directly on Series.
Unlike pandas which uses an intermediate .ewm() object, Polars calls these directly.

Weighting Parameters (exactly one required):
+ span: Decay in terms of span, α = 2/(span+1)
+ half_life: Decay in terms of half-life
+ alpha: Direct smoothing factor (0 < α ≤ 1)
+ com: Center of mass, α = 1/(1+com)

Additional Parameters:
+ adjust: Controls weighting calculation method (default True)
+ min_periods: Minimum observations needed
+ ignore_nulls: How to handle nulls in calculation
'''

# Calculate exponentially weighted moving average with span of 2
# Note: alpha = 2 / (2 + 1) = 0.666...
s_ewm = s_nums.ewm_mean(span=2, adjust=True)
print(s_ewm)
# shape: (5,)
# Series: '' [f64]
# [
# 	3.99
# 	3.0375
# 	3.911538
# 	5.355
# 	3.463884
# ]

'''
EXPLANATION:
-------------
1) Smoothing factor from span
alpha = 2 / (span + 1)
= 2 / (2 + 1)
= 2 / 3
≈ 0.6666667
one_minus_alpha = 1 - 2/3 = 1/3
-------------
2) Meaning of adjust=True (the default)
EWMA_t is a normalized weighted average over all observations up to t,
with geometrically decaying weights proportional to:
[1, (1-alpha), (1-alpha)^2, ..., (1-alpha)^t]
So:
EWMA_t = sum( (1-alpha)^k * x_{t-k} for k=0..t ) / sum( (1-alpha)^k for k=0..t )
-------------
3) Step-by-step verification on the given data
x0, x1, x2, x3, x4 = 3.99, 2.72, 4.30, 6.05, 2.53
t = 0
# weights: [1]
# EWMA_0 = 3.99
# ewma_0 = 3.99  # -> 3.990000
t = 1
# weights: [1 (for x1), 1/3 (for x0)]
# weighted sum = 1*2.72 + (1/3)*3.99 = 2.72 + 1.33 = 4.05
# sum weights = 1 + 1/3 = 4/3
# ewma_1 = 4.05 / (4/3) = 3.0375
t = 2
# weights: [1, 1/3, 1/9]
# weighted sum = 1*4.30 + (1/3)*2.72 + (1/9)*3.99
#              = 4.30 + 0.906666... + 0.443333... = 5.65
# sum weights = 1 + 1/3 + 1/9 = 13/9 ≈ 1.444444...
# ewma_2 = 5.65 / (13/9) = 3.911538...
t = 3
# weights: [1, 1/3, 1/9, 1/27]
# weighted sum = 6.05 + 1.433333... + 0.302222... + 0.147777... = 7.933333...
# sum weights = 1 + 1/3 + 1/9 + 1/27 = 40/27 ≈ 1.481481...
# ewma_3 = 7.933333... / (40/27) = 5.355000
t = 4
# weights: [1, 1/3, 1/9, 1/27, 1/81]
# weighted sum = 2.53 + 2.016666... + 0.477777... + 0.100740... + 0.049259... = 5.174444...
# sum weights = 1 + 1/3 + 1/9 + 1/27 + 1/81 = 121/81 ≈ 1.493827...
# ewma_4 = 5.174444... / (121/81) = 3.463884...
-----------------
4) Key takeaways
- span=2 implies alpha=2/3, putting strong weight on the newest observation.
- adjust=True computes a normalized weighted mean across all past points.
- Weights decay by a factor of 1/3 for each step further into the past.
-----------------
5) Recursive form (for intuition)
If adjust=False, Polars uses the recursive update exactly:
EWMA_t = alpha * x_t + (1 - alpha) * EWMA_{t-1}
with EWMA_0 = x_0.
'''

s_ewm_no_adjust = s_nums.ewm_mean(span=2, adjust=False)
print(s_ewm_no_adjust)
# shape: (5,)
# Series: '' [f64]
# [
# 	3.99
# 	3.143333
# 	3.914444
# 	5.338148
# 	3.466049
# ]
