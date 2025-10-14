'''
Un like .assign() and .agg(), reframe technique allows returning a new DataFrame with a totally different shape.

(.assign() requires the same number of rows as the original DataFrame,
 .groupby() returns a DataFrame the same number of columns as the original DataFrame.)

####################################

1. Using df.apply(axis=0) with .pipe(): Apply one reframing function to specific columns of the DataFrame.

2. Using df.pipe(lambda df: pd.DataFrame(...)): Apply multiple reframing functions to the DataFrame.
'''

import pandas as pd
from scipy import stats
import numpy as np

df_boston = (
    pd.read_csv("05_Pandas_DataR_dataframe/data/BostonHousing.csv")
    .drop(columns=["CHAS", "RAD", "CAT. MEDV"], axis = 1)
    .pipe(lambda df: df.set_axis(df.columns.str.lower(), axis=1))
)

print(df_boston.head())
#       crim    zn  indus    nox     rm   age     dis  tax  ptratio  lstat  medv
# 0  0.00632  18.0   2.31  0.538  6.575  65.2  4.0900  296     15.3   4.98  24.0
# 1  0.02731   0.0   7.07  0.469  6.421  78.9  4.9671  242     17.8   9.14  21.6
# 2  0.02729   0.0   7.07  0.469  7.185  61.1  4.9671  242     17.8   4.03  34.7
# 3  0.03237   0.0   2.18  0.458  6.998  45.8  6.0622  222     18.7   2.94  33.4
# 4  0.06905   0.0   2.18  0.458  7.147  54.2  6.0622  222     18.7   5.33  36.2

print(df_boston.shape)  # (506, 11)


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 1. Using df.apply(axis=0) with .pipe() -------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''Apply the same reframing function to multiple columns of the DataFrame.'''

print(df_boston[["rm", "lstat", "medv"]].apply(stats.shapiro, axis=0)) # axis=0 to apply function to each column
#              rm         lstat          medv
# 0  9.608723e-01  9.369061e-01  9.171759e-01
# 1  2.411977e-10  8.286632e-14  4.941386e-16

###############

print(
    df_boston[["rm", "lstat", "medv"]]
    .apply(stats.shapiro, axis=0)
    .set_axis(["W-statistic", "p-value"], axis=0) # rename the index
)
#                        rm         lstat          medv
# W-statistic  9.608723e-01  9.369061e-01  9.171759e-01
# p-value      2.411977e-10  8.286632e-14  4.941386e-16

###############

print(
    df_boston[["rm", "lstat", "medv"]]
    .apply(lambda col: np.percentile(col, q=[0.25, 0.5, 0.75, 1]), axis=0)
    .set_axis(["Q1", "Q2", "Q3", "Q4"], axis=0) # rename the index
)
#           rm    lstat     medv
# Q1  3.935188  1.93575  5.15750
# Q2  4.138000  2.23725  5.96750
# Q3  4.319125  2.78500  6.85125
# Q4  4.524450  2.88300  7.01000


#--------------------------------------------------------------------------------------------------------------#
#------------------------------ 2. Using df.pipe(lambda df: pd.DataFrame(...)) --------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''Apply multiple reframing functions to the DataFrame.'''

#######################

'''
The cumulative distribution function (CDF) takes a value and returns the probability 
that a random variable is less than or equal to that value; 

The percent-point function (PPF), also called the inverse CDF or quantile function, 
takes a probability and returns the corresponding value whose CDF equals that probability. 

In short: CDF input is a value and output is a probability in ; 
PPF input is a probability in and output is a value on the distribution's scale.

########################

In this example,  for the sake of reframing demonstration,
we will calculate the PPF values for the 25th, 50th, 75th, and 100th percentiles,
but for different distributions: normal, exponential and gamma.

rm ~ normal distribution
lstat ~ exponential distribution
medv ~ gamma distribution
'''

df_ppf = (
    df_boston[["rm", "lstat", "medv"]]
    .pipe(
        lambda df: pd.DataFrame(
            {
                "rm_norm": stats.norm.ppf(q=[0.25, 0.5, 0.75, 1], loc=df["rm"].mean(), scale=df["rm"].std()),
                "lstat_expon": stats.expon.ppf(q=[0.25, 0.5, 0.75, 1], scale=df["lstat"].mean()),
                "medv_gamma": stats.gamma.ppf(q=[0.25, 0.5, 0.75, 1], a=2, scale=df["medv"].mean() / 2),
            },
            index=["ppf_25th", "ppf_50th", "ppf_75th", "ppf_100th"],
        )
    )
)

print(df_ppf)
#             rm_norm  lstat_expon  medv_gamma
# ppf_25th   5.810726     3.640059   10.830154
# ppf_50th   6.284634     8.770435   18.908934
# ppf_75th   6.758542    17.540870   30.336306
# ppf_100th       inf          inf         inf

'''
rm_norm: the value 5.810 is the 25th percentile of a normal distribution, 
         meaning it higher than 25% of the data points.

lstat_expon: the value 3.640 is the 25th percentile of an exponential distribution,
             meaning it higher than 25% of the data points.

medv_gamma: the value 10.830 is the 25th percentile of a gamma distribution,
            meaning it higher than 25% of the data points.
'''