'''
Flow of contents:
1. Rolling: .rolling()
2. Expanding: .expanding()
3. Exponentially Weighted: .ewm()
'''

import pandas as pd
import numpy as np

np.random.seed(42)

s_nums = pd.Series(np.random.normal(loc = 3, scale = 2, size = 5)).round(2)
print(s_nums)
# 0    3.99
# 1    2.72
# 2    4.30
# 3    6.05
# 4    2.53
# dtype: float64

#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 1. .rolling() ------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

'''
The .rolling() method creates a fixed-size moving window that slides through your data. 

It calculates statistics over a consistent number of observations

Key Parameters:
+ window: Size of the moving window (required)
+ min_periods: Minimum observations needed for a value (defaults to window size)
+ center: If True, labels are set at the center of the window
+ win_type: Specifies window type for weighted calculations
'''

###############
## Basic use ##
###############

print(s_nums)
# 0    3.99
# 1    2.72
# 2    4.30
# 3    6.05
# 4    2.53
# dtype: float64

s_rolling = s_nums.rolling(window = 2).mean()  # Calculate rolling mean with a window of 2
print(s_rolling)
# 0      NaN (mean of [NaN, 0-indexed])
# 1    3.355 (mean of [0-indexed, 1-indexed])
# 2    3.510 (mean of [1-indexed, 2-indexed])
# 3    5.175 
# 4    4.290
# dtype: float64

s_rolling = s_nums.rolling(window = 3).mean()  # Calculate rolling mean with a window of 3
print(s_rolling)
# 0         NaN (mean of [NaN, NaN, 1-indexed])
# 1         NaN (mean of [NaN, 0-indexed, 1-indexed])
# 2    3.670000 (mean of [0-indexed, 1-indexed, 2-indexed])
# 3    4.356667
# 4    4.293333
# dtype: float64


###################################
## Rolling with time-based index ##
###################################

s_nums_time = pd.Series(
    data = s_nums.values,
    index = [pd.Timestamp('20130101 09:00:00'),
             pd.Timestamp('20130101 09:00:02'),
             pd.Timestamp('20130101 09:00:03'),
             pd.Timestamp('20130101 09:00:05'),
             pd.Timestamp('20130101 09:00:06')]
)

s_rolling = s_nums_time.rolling(window = '2s').mean()  # Calculate rolling mean with a 2-second window
# for each timestamp t, 
# take all observations whose timestamps fall in the interval (t − 2 seconds, t], 
# then compute the mean.

print(s_rolling)                                       
# 2013-01-01 09:00:00    3.99
# 2013-01-01 09:00:02    2.72
# 2013-01-01 09:00:03    3.51
# 2013-01-01 09:00:05    6.05
# 2013-01-01 09:00:06    4.29
# dtype: float64

'''
3.99:
 + 2013-01-01 09:00:00 (window: (08:59:58, 09:00:00])
 + Included points: only 09:00:00 → 3.99
 + => Mean = 3.99

2.72:
 + 2013-01-01 09:00:02 (window: (09:00:00, 09:00:02])
 + Included points: only 09:00:02 → 2.72
 + => Mean = 2.72

3.51:
 + 2013-01-01 09:00:03 (window: (09:00:01, 09:00:03])
 + Included points: 09:00:02 (2.72) and 09:00:03 (4.30)
 + => Mean = (2.72 + 4.30) / 2 = 3.51
'''


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 2. .expanding() ----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

'''
The .expanding() method creates a growing window that starts from the first observation 
and includes all data up to the current point. 

This produces cumulative statistics ideal for long-term trend analysis.

Key Parameters:
+ min_periods: Minimum observations required (default is 1)
+ center: Sets window label positioning
'''

###############
## Basic use ##
###############

print(s_nums)
# 0    3.99
# 1    2.72
# 2    4.30
# 3    6.05
# 4    2.53
# dtype: float64

s_expanding = s_nums.expanding().mean()  # Calculate expanding mean
print(s_expanding)
# 0    3.990 (mean of [0-indexed])
# 1    3.355 (mean of [0-indexed, 1-indexed])
# 2    3.670 (mean of [0-indexed, 1-indexed, 2-indexed])
# 3    4.265
# 4    3.918
# dtype: float64

s_expanding = s_nums.expanding().sum()  # Calculate expanding sum (like cumulative sum)
print(s_expanding)
# 0     3.99 (sum of [0-indexed])
# 1     6.71 (sum of [0-indexed, 1-indexed])
# 2    11.01 (sum of [0-indexed, 1-indexed, 2-indexed])
# 3    17.06
# 4    19.59
# dtype: float64


#############################
## Using with min_periods= ##
#############################

s_expanding = s_nums.expanding(min_periods = 3).mean()  # Calculate expanding mean with minimum 3 observations
print(s_expanding)
# 0      NaN (not enough 3 observations)
# 1      NaN (not enough 3 observations)
# 2    3.670 (mean of [0-indexed, 1-indexed, 2-indexed])
# 3    4.265 (mean of [0-indexed, 1-indexed, 2-indexed, 3-indexed])
# 4    3.918
# dtype: float64


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 3. .ewm() ----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

'''
The .ewm() method applies exponentially decreasing weights to observations, 
giving more importance to recent data while still considering historical values. 

This method is particularly valuable in financial analysis and forecasting.

Weighting Parameters (exactly one required):
+ span: Decay in terms of span, α = 2/(span+1)
+ halflife: Decay in terms of half-life
+ alpha: Direct smoothing factor (0 < α ≤ 1)
+ com: Center of mass, α = 1/(1+com)

Additional Parameters:
+ adjust: Controls weighting calculation method
+ min_periods: Minimum observations needed
'''

s_ewm = s_nums.ewm(span = 2).mean()  # Calculate exponentially weighted moving average with span of 2
print(s_ewm)
# 0    3.990000
# 1    3.037500
# 2    3.911538
# 3    5.355000
# 4    3.463884
# dtype: float64

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

If adjust=False, pandas uses the recursive update exactly:
  EWMA_t = alpha * x_t + (1 - alpha) * EWMA_{t-1}

with EWMA_0 = x_0.
'''