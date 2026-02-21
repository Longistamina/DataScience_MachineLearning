'''
1. Order statistics
   + np.ptp(): range of values (maximum - minimum) along an axis.
   + np.percentile(): compute the q-th percentile of the data along the specified axis.
   + np.nanpercentile(): compute the q-th percentile of the data along the specified axis, while ignoring nan values.
   + np.quantile(): compute the q-th quantile of the data along the specified axis.
   + np.nanquantile(): compute the q-th quantile of the data along the specified axis, while ignoring nan values.

2. Averages and variances
   + np.median(): compute the median along the specified axis.
   + np.average(): compute the weighted average along the specified axis.
   + np.mean(): compute the arithmetic mean along the specified axis.
   + np.std(): compute the standard deviation along the specified axis.
   + np.var(): compute the variance along the specified axis.
   + np.nanmedian(): compute the median along the specified axis, while ignoring NaNs.
   + np.nanmean(): compute the arithmetic mean along the specified axis, ignoring NaNs.
   + np.nanstd(): compute the standard deviation along the specified axis, while ignoring NaNs.
   + np.nanvar(): compute the variance along the specified axis, while ignoring NaNs.

3. Correlating
   + np.corrcoef(): return Pearson product-moment correlation coefficients.
   + np.correlate(): cross-correlation of two 1-dimensional sequences.
   + np.cov(): estimate a covariance matrix, given data and weights.

4. Histograms
   + np.histogram(): compute the histogram of a dataset.
   + np.histogram2d(): compute the bi-dimensional histogram of two data samples.
   + np.histogramdd(): compute the multidimensional histogram of some data.
   + np.bincount(): count number of occurrences of each value in array of non-negative ints.
   + np.histogram_bin_edges(): compute only the edges of the bins used by the histogram function.
   + np.digitize(): return the indices of the bins to which each value in input array belongs.

5. Application in data analysis
'''

import numpy as np

np.random.seed(10)
v1 = np.random.randint(1, 11, 5)
# array([10,  5,  1,  2, 10])

np.random.seed(11)
v2 = np.random.randint(1, 11, 5)
# array([10,  1,  2,  8,  2])

np.random.seed(12)
M1 = np.random.randint(1, 21, (3, 4))
# array([[12,  7, 18,  3],
#        [ 4,  4, 13, 17],
#        [18,  6, 14,  3]])

np.random.seed(13)
M2 = np.random.randint(1, 21, (3, 4))
# array([[19, 17, 11, 17],
#        [ 7,  3, 13,  4],
#        [ 3, 15,  6, 14]])

v_nan = np.array([1.0, 2.0, np.nan, 4.0, 5.0])
# array([ 1.,  2., nan,  4.,  5.])

M_nan = np.array([[1.0, np.nan, 3.0],
                  [4.0, 5.0,   6.0]])
# array([[ 1., nan,  3.],
#        [ 4.,  5.,  6.]])


#-------------------------------------------------------------------------------------------------#
#-------------------------------------- 1. Order statistics --------------------------------------#
#-------------------------------------------------------------------------------------------------#

##############
## np.ptp() ##
##############

'''
np.ptp() returns the range of values (maximum - minimum) along an axis.
"ptp" stands for "peak to peak".
'''

print(np.ptp(v1))
# 9  (10 - 1 = 9)

print(np.ptp(M1))
# 15 (18 - 3 = 15)

print(np.ptp(M1, axis=0))
# [14 3 5 14]  (range of horizontally, each column)

print(np.ptp(M1, axis=1))
# [15 13 15]  (range of vertically, each row)

#####################
## np.percentile() ##
#####################
'''
np.percentile() computes the q-th percentile of the data along the specified axis.

q: Percentile or sequence of percentiles to compute, in the range [0, 100].
axis: Axis along which the percentiles are computed.
'''

# Single percentile (50th percentile = median)
print(np.percentile(v1, 50))
# 5.0

# Multiple percentiles at once
print(np.percentile(v1, [25, 50, 75]))
# [ 2.  5. 10.]

# Along a specific axis
print(np.percentile(M1, 50, axis=0))
# [12.  6. 14.  3.]  (median of each column)

print(np.percentile(M1, 50, axis=1))
# [ 9.5  8.5 10. ]  (median of each row)

# keepdims=True preserves the reduced axis as a dimension of size 1
print(np.percentile(M1, 50, axis=1, keepdims=True))
# [[ 9.5]
#  [ 8.5]
#  [10. ]]

########################
## np.nanpercentile() ##
########################
'''
np.nanpercentile() computes the q-th percentile of the data along the specified axis,
while ignoring nan values.
'''

print(np.nanpercentile(v_nan, 50))
# 3.0  (NaN at index 2 is ignored; percentile of [1., 2., 4., 5.])

print(np.nanpercentile(v_nan, [25, 75]))
# [1.75 4.25]

# Compare with np.percentile — NaN propagates to the result
print(np.percentile(v_nan, 50))
# nan  (NaN propagates when using np.percentile)

###################
## np.quantile() ##
###################
'''
np.quantile() computes the q-th quantile of the data along the specified axis.

Equivalent to np.percentile(a, q * 100), but q must be in the range [0.0, 1.0].
'''

print(np.quantile(v1, 0.5))
# 5.0  (equivalent to 50th percentile)

print(np.quantile(v1, [0.25, 0.5, 0.75]))
# [ 2.  5. 10.]

print(np.quantile(M1, 0.5, axis=0))
# [12.  6. 14.  3.]

print(np.quantile(M1, 0.5, axis=1))
# [ 9.5  8.5 10. ]

######################
## np.nanquantile() ##
######################
'''
np.nanquantile() computes the q-th quantile of the data along the specified axis,
while ignoring nan values.
'''

print(np.nanquantile(v_nan, 0.5))
# 3.0  (NaN ignored)

print(np.nanquantile(v_nan, [0.25, 0.75]))
# [1.75 4.25]

print(np.quantile(v_nan, 0.5))
# nan  (NaN propagates when using np.quantile)


#-------------------------------------------------------------------------------------------------#
#---------------------------------- 2. Averages and variances ------------------------------------#
#-------------------------------------------------------------------------------------------------#

#################
## np.median() ##
#################
'''
np.median() computes the median along the specified axis.

For even-length arrays, the median is the average of the two middle values.
'''

print(np.median(v1))
# 5.0  (sorted: [1, 2, 5, 10, 10] → middle element)

print(np.median(M1))
# 9.5 (median of flattened array)

print(np.median(M1, axis=0))
# [12.  6. 14.  3.]  (median of each column)

print(np.median(M1, axis=1))
# [ 9.5  8.5 10. ]  (median of each row; rows have 4 elements so avg of middle two)

# keepdims=True to preserve the reduced axis
print(np.median(M1, axis=1, keepdims=True))
# [[ 9.5]
#  [ 8.5]
#  [10. ]]

##################
## np.average() ##
##################
'''
np.average() computes the weighted average along the specified axis.

Without weights, it is identical to np.mean().
With weights, each element is multiplied by its weight before averaging.
'''

print(np.average(v1))
# 5.6  (same as np.mean for uniform weights)

# Weighted average: elements with larger weights contribute more
weights = np.array([0.1, 0.2, 0.3, 0.2, 0.2])
print(np.average(v1, weights=weights))
# 4.7  (smaller elements 1 and 2 carry higher weights, pulling average down)

print(np.average(M1))
# 9.9167  (average of all elements in M1; same as np.mean(M1))

print(np.average(M1, axis=0))
# [11.3333  5.6667 15.      7.6667]  (column averages; same as np.mean here)

# returned=True also returns the sum of weights alongside the average
avg, wsum = np.average(v1, weights=weights, returned=True)
print(avg, wsum)
# 4.7  1.0  (weights sum to 1.0 since they were normalized)

###############
## np.mean() ##
###############
'''
np.mean() computes the arithmetic mean along the specified axis.

Equivalent to np.average() with uniform weights.
'''

print(np.mean(v1))
# 5.6  (= (10 + 5 + 1 + 2 + 10) / 5)

print(np.mean(M1))
# 9.9167  (average of all elements in M1)

print(np.mean(M1, axis=0))
# [11.3333  5.6667 15.      7.6667]  (mean of each column)

print(np.mean(M1, axis=1))
# [10.    9.5  10.25]  (mean of each row)

##############
## np.std() ##
##############
'''
np.std() computes the standard deviation along the specified axis.

ddof: Delta Degrees of Freedom. Divisor used is N - ddof.
  ddof=0 (default): population std (divide by N)
  ddof=1           : sample std     (divide by N-1)
'''

print(np.std(v1))
# 3.8262  (population std, ddof=0)

print(np.std(v1, ddof=1))
# 4.2778  (sample std, ddof=1)

print(np.std(M1))
# 5.78011 (std of all elements in M1)

print(np.std(M1, axis=0))
# [5.7349 1.2472 2.1602 6.5997]  (std of each column)

print(np.std(M1, axis=1))
# [5.6125 5.6789 6.0156]  (std of each row)

##############
## np.var() ##
##############
'''
np.var() computes the variance along the specified axis.

Variance = std^2. ddof works the same as in np.std().
'''

print(np.var(v1))
# 14.64  (population variance, ddof=0)

print(np.var(v1, ddof=1))
# 18.3  (sample variance, ddof=1)

print(np.var(M1))
# 33.40972 (variance of all elements in M1)

print(np.var(M1, axis=0))
# [32.8889  1.5556  4.6667 43.5556]  (variance of each column)

print(np.var(M1, axis=1))
# [31.5    32.25   36.1875]  (variance of each row)

####################
## np.nanmedian() ##
####################
'''np.nanmedian() computes the median along the specified axis, while ignoring NaNs.'''

print(np.nanmedian(v_nan))
# 3.0  (NaN excluded; median of [1., 2., 4., 5.] = (2+4)/2 = 3.0)

print(np.nanmedian(M_nan))
# 4.0 (median of flattened array, NaN ignored)

print(np.nanmedian(M_nan, axis=0))
# [2.5 5.  4.5]  (NaN treated as missing in column 1)

print(np.nanmedian(M_nan, axis=1))
# [2. 5.]  (NaN excluded from row 0; median of [1., 3.] = 2.0)

print(np.median(M_nan, axis=1))
# [nan 5.]  (NaN propagates when using np.median instead of

##################
## np.nanmean() ##
##################
'''np.nanmean() computes the arithmetic mean along the specified axis, ignoring NaNs.'''

print(np.nanmean(v_nan))
# 3.0  (= (1 + 2 + 4 + 5) / 4, NaN excluded)

print(np.nanmean(M_nan))
# 3.8  (mean of all elements, NaN ignored)

print(np.nanmean(M_nan, axis=0))
# [2.5 5.  4.5]  (NaN treated as missing; column 1 mean = 5.0 from single value)

print(np.nanmean(M_nan, axis=1))
# [2. 5.]  (NaN excluded from row 0; mean of [1., 3.] = 2.0)

print(np.mean(M_nan, axis=1))
# [nan 5.]  (NaN propagates when using np.mean instead of np.nanmean)

#################
## np.nanstd() ##
#################
'''np.nanstd() computes the standard deviation along the specified axis, while ignoring NaNs.'''

print(np.nanstd(v_nan))
# 1.5811  (std of [1., 2., 4., 5.], NaN excluded)

print(np.nanstd(v_nan, ddof=1))
# 1.8257  (sample std, ddof=1)

print(np.nanstd(M_nan))
# 1.7205  (std of all elements, NaN ignored)

print(np.nanstd(M_nan, axis=0))
# [1.5 0.  1.5]  (std of each column; column 1 has only one value, so std=0)

print(np.std(M_nan, axis=1))
# [       nan 0.81649658] (NaN propagates in row 0; std of row 1 is std of [4., 5., 6.])

#################
## np.nanvar() ##
#################
'''np.nanvar() computes the variance along the specified axis, while ignoring NaNs.'''

print(np.nanvar(v_nan))
# 2.5  (var of [1., 2., 4., 5.], NaN excluded)

print(np.nanvar(v_nan, ddof=1))
# 3.3333  (sample variance, ddof=1)

print(np.nanvar(M_nan))
# 2.96  (var of all elements, NaN ignored)

print(np.nanvar(M_nan, axis=0))
# [2.25 0.   2.25]  (var of each column; column 1 has only one value, so var=0)

print(np.var(M_nan, axis=1))
# [       nan 0.66666667] (NaN propagates in row 0; var of row 1 is var of [4., 5., 6.])


#-------------------------------------------------------------------------------------------------#
#---------------------------------------- 3. Correlating -----------------------------------------#
#-------------------------------------------------------------------------------------------------#

###################
## np.corrcoef() ##
###################
'''
np.corrcoef() returns the Pearson product-moment correlation coefficients.

Result is a 2D array where element [i, j] is the correlation between row i and row j.
Values range from -1 to +1:
  +1 : perfect positive linear correlation
   0 : no linear correlation
  -1 : perfect negative linear correlation
'''

# Correlation between two 1D arrays
print(np.corrcoef(v1, v2))
# [[1.     0.2025]
#  [0.2025 1.    ]]
# Diagonal is always 1.0 (each array is perfectly correlated with itself)

# Correlation between rows of a matrix
print(np.corrcoef(M1))
# [[ 1.     -0.149   0.8071]
#  [-0.149   1.     -0.4427]
#  [ 0.8071 -0.4427  1.    ]]
# Row 0 and row 2 are strongly positively correlated (r = 0.8071)

# rowvar=False: treat each column as a variable instead of each row
print(np.corrcoef(M1, rowvar=False))
# [[ 1.          0.71457523  0.269061   -0.90419443]
#  [ 0.71457523  1.          0.8660254  -0.94491118]
#  [ 0.269061    0.8660254   1.         -0.65465367]
#  [-0.90419443 -0.94491118 -0.65465367  1.        ]]
# 4x4 correlation matrix for the 4 columns of M1

####################
## np.correlate() ##
####################
'''
np.correlate() computes the cross-correlation of two 1-dimensional sequences.

mode options:
  'valid'  : only fully overlapping part  (output length = max(M,N) - min(M,N) + 1)
  'full'   : all overlaps                 (output length = M + N - 1)
  'same'   : centered output              (output length = max(M, N))
'''

x = np.array([1, 2, 3])
y = np.array([0, 1, 0.5])

print(np.correlate(x, y, mode='full'))
# [0.5 2.  3.5 3.  0. ]

print(np.correlate(x, y, mode='valid'))
# [3.5]  (single point where arrays fully overlap: 1*0 + 2*1 + 3*0.5 = 3.5)

print(np.correlate(x, y, mode='same'))
# [2.  3.5 3. ]

'''
Position 0  (partial overlap, left edge)
  x:          [1,  2,  3]
  y: [0,  1, 0.5]
              ↑ only x[0] * y[2] = 1 * 0.5
  result → 0.5

Position 1  (partial overlap)
  x:       [1,  2,  3]
  y:   [0,  1, 0.5]
             ↑ x[0]*y[1] + x[1]*y[2] = 1*1 + 2*0.5
  result → 2.0

Position 2  (FULL overlap — this is the 'valid' zone)
  x:   [1,  2,  3]
  y:   [0,  1, 0.5]
       x[0]*y[0] + x[1]*y[1] + x[2]*y[2]
       = 1*0 + 2*1 + 3*0.5
  result → 3.5

Position 3  (partial overlap)
  x:   [1,  2,  3]
  y:        [0,  1, 0.5]
             x[1]*y[0] + x[2]*y[1] = 2*0 + 3*1
  result → 3.0

Position 4  (partial overlap, right edge)
  x:   [1,  2,  3]
  y:             [0,  1, 0.5]
                  x[2]*y[0] = 3*0
  result → 0.0
'''

##############
## np.cov() ##
##############
'''
np.cov() estimates a covariance matrix, given data and optional weights.

Covariance measures how much two variables change together.
  Positive : both variables tend to increase together.
  Negative : one increases while the other decreases.

By default, ddof=1 (sample covariance, divided by N-1).
'''

# Covariance between two 1D arrays
print(np.cov(v1, v2))
# [[18.3    3.55]
#  [ 3.55  16.8 ]]
# Diagonal = variance of each array; off-diagonal = covariance between the two

# Covariance between rows of a matrix (each row treated as a variable)
print(np.cov(M1))
# [[ 42.      -6.3333  36.3333]
#  [ -6.3333  43.     -20.1667]
#  [ 36.3333 -20.1667  48.25  ]]

# rowvar=False: each column is a variable (results in a 4x4 matrix)
print(np.cov(M1, rowvar=False))
# [[ 49.33   7.67   5.   -51.33]
#  [  7.67   2.33   3.5  -11.67]
#  [  5.     3.5    7.   -14.  ]
#  [-51.33 -11.67 -14.    65.33]]


#-------------------------------------------------------------------------------------------------#
#----------------------------------------- 4. Histograms -----------------------------------------#
#-------------------------------------------------------------------------------------------------#

####################
## np.histogram() ##
####################
'''
np.histogram() computes the histogram of a dataset.

Returns:
  hist      : array of counts (or density) for each bin.
  bin_edges : array of bin boundary values (length = len(hist) + 1).
'''

hist, bin_edges = np.histogram(v1, bins=5)

print(hist)
# [2 0 1 0 2]

print(bin_edges)
# [ 1.   2.8  4.6  6.4  8.2 10. ]

# Specifying custom bin boundaries as a sequence
hist_custom, edges_custom = np.histogram(v1, bins=[1, 3, 6, 10])
print(hist_custom)
# [2 1 2]  (2 values in [1,3), 1 value in [3,6), 2 values in [6,10])

# density=True normalizes so the integral of the histogram sums to 1
hist_density, _ = np.histogram(v1, bins=5, density=True)
print(hist_density)
# [0.2222 0.     0.1111 0.     0.2222]

######################
## np.histogram2d() ##
######################
'''
np.histogram2d() computes the bi-dimensional histogram of two 1D data samples.

Returns:
  H      : 2D array of counts.
  xedges : bin edges along the first dimension.
  yedges : bin edges along the second dimension.
'''

H, xedges, yedges = np.histogram2d(v1, v2, bins=3)

print(H)
# [[1. 0. 1.]
#  [1. 0. 0.]
#  [1. 0. 1.]]

print(xedges)
# [ 1.  4.  7. 10.]

print(yedges)
# [ 1.  4.  7. 10.]

# H[i, j] counts points where x falls in xedges[i:i+2] and y in yedges[j:j+2]

######################
## np.histogramdd() ##
######################
'''
np.histogramdd() computes the multidimensional histogram of some data.

Input: sample with shape (N, D) — N data points in D dimensions.
Returns:
  H     : D-dimensional array of counts.
  edges : list of D bin edge arrays (one per dimension).
'''

# 2D sample: stack v1 and v2 into (5, 2) shape
sample_2d = np.column_stack([v1, v2])

H_dd, edges_dd = np.histogramdd(sample_2d, bins=3)

print(H_dd)
# [[1. 0. 1.]
#  [1. 0. 0.]
#  [1. 0. 1.]]  (equivalent to histogram2d with same bins)

print(H_dd.shape)
# (3, 3)

# For higher dimensions: each row of the input is a D-dimensional data point
H_4d, _ = np.histogramdd(M1, bins=3)  # M1 has shape (3,4) → 4 dimensions

print(H_4d.shape)
# (3, 3, 3, 3)  (3 bins per dimension, 4 dimensions)

###################
## np.bincount() ##
###################
'''
np.bincount() counts the number of occurrences of each non-negative integer value.

Input must be a 1D array of non-negative integers.
The output array has length max(x) + 1.
'''

v_int = np.array([0, 1, 2, 1, 3, 2, 1, 0])

print(np.bincount(v_int))
# [2 3 2 1]  (0 appears 2x, 1 appears 3x, 2 appears 2x, 3 appears 1x)

# minlength: ensures minimum output length (pads with zeros)
print(np.bincount(v_int, minlength=7))
# [2 3 2 1 0 0 0]

# weights: sum the weights for each bin instead of counting
v_int = np.array([0, 1, 2, 1, 3, 2, 1, 0])
wts = np.array([1.0, 0.5, 1.0, 0.5, 2.0, 1.0, 0.5, 1.0])
print(np.bincount(v_int, weights=wts))
# [2.  1.5 2.  2. ]
'''
0 appears 2 times, with weights 1.0, 1.0       → total weight 2.0
1 appears 3 times, with weights 0.5, 0.5, 0.5  → total weight 1.5
2 appears 2 times, with weights 1.0, 1.0       → total weight 2.0
3 appears 1 time, with weight 2.0              → total weight 2.0
'''

##############################
## np.histogram_bin_edges() ##
##############################
'''
np.histogram_bin_edges() computes only the bin edges for a histogram, without counting.

Useful when you want to inspect or reuse bin boundaries without computing counts.
Accepts the same bin and range arguments as np.histogram().
'''

edges = np.histogram_bin_edges(v1, bins=5)
print(edges)
# [ 1.   2.8  4.6  6.4  8.2 10. ]

# Custom number of bins with an explicit range
edges_custom = np.histogram_bin_edges(v1, bins=4, range=(0, 12))
print(edges_custom)
# [ 0.  3.  6.  9. 12.]

# Using a string method for automatic bin width selection
edges_auto = np.histogram_bin_edges(v1, bins='auto')
print(edges_auto)
# [ 1.    3.25  5.5   7.75 10.  ]
# Automatically determined bin edges based on the data distribution (e.g., Sturges rule)

###################
## np.digitize() ##
###################
'''
np.digitize() returns the index of the bin to which each value in the input belongs.

bins must be monotonically increasing or decreasing.
  right=False (default): bins[i-1] <= x < bins[i]  (left-closed intervals)
  right=True           : bins[i-1] <  x <= bins[i]  (right-closed intervals)
'''

bins_arr = np.array([2, 4, 6, 8, 10])
print(np.digitize(v1, bins_arr))
# [5 2 0 1 5]
# v1 = [10, 5, 1, 2, 10]
# bins = [2, 4, 6, 8, 10]
# 10 -> index 5 (beyond last bin), 5 -> index 2 ([4,6)), 1 -> index 0 (<2), 2 -> index 1 ([2,4))

print(np.digitize(v1, bins_arr, right=True))
# [4 2 0 0 4]
# With right=True: 10 -> index 4 ((8,10] is the last closed interval), 2 -> index 0 (2 is not > 2)

# Practical use: map continuous values to categorical labels
labels = ['very low', 'low', 'medium', 'high', 'very high', 'extreme']
indices = np.digitize(v1, bins_arr)
categories = [labels[i] for i in indices]

print(categories)
# ['extreme', 'low', 'very low', 'very low', 'extreme']


#--------------------------------------------------------------------------------------------------#
#--------------------------------- 5. Application in data analysis --------------------------------#
#--------------------------------------------------------------------------------------------------#

np.random.seed(42)
data = np.random.normal(loc=50, scale=10, size=100)  # 100 samples, mean=50, std=10

# Descriptive statistics summary
print("Mean     :", np.mean(data).round(2))               # 48.96
print("Median   :", np.median(data).round(2))             # 48.73
print("Std      :", np.std(data, ddof=1).round(2))        # 9.08  (sample std)
print("Var      :", np.var(data, ddof=1).round(2))        # 82.48 (sample var)
print("Q1, Q3   :", np.quantile(data, [0.25, 0.75]).round(2))  # [43.99 54.06]
print("IQR      :", (np.quantile(data, 0.75) - np.quantile(data, 0.25)).round(2))  # 10.07
print("Range    :", (np.max(data) - np.min(data)).round(2))    # 44.72

########################

# Detect outliers using the IQR method (Tukey's fences)
Q1, Q3 = np.quantile(data, [0.25, 0.75])
IQR = Q3 - Q1
outliers = data[(data < Q1 - 1.5 * IQR) | (data > Q3 + 1.5 * IQR)]

print("Outliers :", outliers.round(2))
# [23.8]  (one value more than 1.5*IQR below Q1)

########################

# Correlation between two simulated measurement series
np.random.seed(1)
measurement_A = np.random.normal(0, 1, 50)
measurement_B = measurement_A * 0.8 + np.random.normal(0, 0.5, 50)

corr_matrix = np.corrcoef(measurement_A, measurement_B)

print("Pearson r:", corr_matrix[0, 1].round(4))
# ~0.93  (strong positive correlation, as expected by construction)

# Covariance and variance decomposition
cov_AB = np.cov(measurement_A, measurement_B)

print("Cov(A,B) :", cov_AB[0, 1].round(4)) # 0.7587
print("Var(A)   :", cov_AB[0, 0].round(4)) # 0.9593
print("Var(B)   :", cov_AB[1, 1].round(4)) # 0.7561
