'''
1. Categorical Encoding: pd.factorize(), pd.get_dummies()
2. Binning and Discretization: pd.cut(), pd.qcut()
'''

import pandas as pd


#---------------------------------------------------------------------------------------------------#
#---------------------------------------- 1. Categorical Encoding ----------------------------------#
#---------------------------------------------------------------------------------------------------#

'''
Categorical Encoding is the process of converting categorical variables into numerical representations.
This is useful for machine learning algorithms that require numerical input.
'''

s_gender = pd.Series(["M", "M", "F", "M", "LGBTQ", "F", "M", "F", "LGBTQ", "M"])

##########################################
##            pd.factorize()            ##
##########################################

'''
pd.factorize() assigns a unique integer to each category in the Series.
It returns an array of integers and an Index of unique categories.

pd.factorize() returns a tuple containg two elements:
1. An array of integers representing the categories.
2. An Index of unique categories.

The integers are assigned in the order of appearance of the categories in the Series.
The first unique category gets 0, the second gets 1, and so on.
'''

print(pd.factorize(s_gender))
# (array([0, 0, 1, 0, 2, 1, 0, 1, 2, 0]), Index(['M', 'F', 'LGBTQ'], dtype='object'))

#-----------------
## Assign the result to separate variables
#-----------------

s_gender_factorized, codes = pd.factorize(s_gender)

print(s_gender_factorized)
# [0 0 1 0 2 1 0 1 2 0]
# <class 'numpy.ndarray'>

print(codes)
# Index(['M', 'F', 'LGBTQ'], dtype='object')


############################################
##            pd.get_dummies()            ##
############################################

'''
pd.get_dummies() creates a DataFrame with binary columns for each category in the Series.
Each column represents a category, and the values are 0 or 1 indicating the presence of that category.

It is useful for one-hot encoding categorical variables.
'''

#-----------------
## Without dropping the first category
#-----------------

s_gender_dummmies = pd.get_dummies(s_gender, prefix = "gender")
print(s_gender_dummmies)
#    gender_F  gender_LGBTQ  gender_M
# 0     False         False      True
# 1     False         False      True
# 2      True         False     False
# 3     False         False      True
# 4     False          True     False
# 5      True         False     False
# 6     False         False      True
# 7      True         False     False
# 8     False          True     False
# 9     False         False      True

s_gender_dummmies = pd.get_dummies(s_gender, prefix = "gender").astype("int64") # Convert to 0-1 binary integers
print(s_gender_dummmies)
#    gender_F  gender_LGBTQ  gender_M
# 0         0             0         1
# 1         0             0         1
# 2         1             0         0
# 3         0             0         1
# 4         0             1         0
# 5         1             0         0
# 6         0             0         1
# 7         1             0         0
# 8         0             1         0
# 9         0             0         1

#---------------------------------------
## With dropping the first category (to avoid multicollinearity)
#---------------------------------------

'''
In fact, if we have n categories, we just need n-1 columns to represent them.
The last n-th category can be inferred from the other n-1 columns.

=> Can drop the first category to avoid multicollinearity.
'''

s_gender_dummmies = pd.get_dummies(s_gender, drop_first = True, prefix = "gender").astype("int64")
print(s_gender_dummmies)
#    gender_LGBTQ  gender_M
# 0             0         1
# 1             0         1
# 2             0         0
# 3             0         1
# 4             1         0
# 5             0         0
# 6             0         1
# 7             0         0
# 8             1         0
# 9             0         1

'''
The 5-indexed person has LGBTQ = 0 and M = 0, which means they are F (the last category).

=> The F gender though is not included can still be inferred from the other 2 genders/columns.
'''


#----------------------------------------------------------------------------------------------------#
#---------------------------------------- 2. Binning and Discretization -----------------------------#
#----------------------------------------------------------------------------------------------------#

'''
Binning and Discretization are techniques to convert continuous data into discrete categories or bins.
This is useful for simplifying data analysis, especially when dealing with continuous variables.
'''

import numpy as np

np.random.seed(42)  # For reproducibility
s_quantitative = pd.Series(np.random.normal(loc = 5, scale = 2, size = 20))  # Generate random data

print(s_quantitative)
# 0     5.993428
# 1     4.723471
# 2     6.295377
# 3     8.046060
# 4     4.531693
# 5     4.531726
# 6     8.158426
# 7     6.534869
# 8     4.061051
# 9     6.085120
# 10    4.073165
# 11    4.068540
# 12    5.483925
# 13    1.173440
# 14    1.550164
# 15    3.875425
# 16    2.974338
# 17    5.628495
# 18    3.183952
# 19    2.175393
# dtype: float64


####################################
##            pd.cut()            ##
####################################

#-----------------
## bins = [0, 2, 4, 6, 8, 10]
#-----------------

s_bins = pd.cut(
    x = s_quantitative, 
    bins = [0, 2, 4, 6, 8, 10], 
    labels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
)

print(s_bins)
# 0        Medium
# 1        Medium
# 2          High
# 3     Very High
# 4        Medium
# 5        Medium
# 6     Very High
# 7          High
# 8        Medium
# 9          High
# 10       Medium
# 11       Medium
# 12       Medium
# 13     Very Low
# 14     Very Low
# 15          Low
# 16          Low
# 17       Medium
# 18          Low
# 19          Low
# dtype: category
# Categories (5, object): ['Very Low' < 'Low' < 'Medium' < 'High' < 'Very High']

'''The last value (10.5) is NaN because it falls outside the specified bins.'''

#-----------------
## bins = 3 (equal-width bins)
#-----------------

s_bins = pd.cut(
    x = s_quantitative, 
    bins = 3,  # Create 3 equal-width bins
    labels = ['Low', 'Medium', 'High']
)

print(s_bins)
# 0       High
# 1     Medium
# 2       High
# 3       High
# 4     Medium
# 5     Medium
# 6       High
# 7       High
# 8     Medium
# 9       High
# 10    Medium
# 11    Medium
# 12    Medium
# 13       Low
# 14       Low
# 15    Medium
# 16       Low
# 17    Medium
# 18       Low
# 19       Low
# dtype: category
# Categories (3, object): ['Low' < 'Medium' < 'High']


#####################################
##            pd.qcut()            ##
#####################################

# Quantile-based discretization function

#-----------------
## bins = 4 (quartiles)
#-----------------

s_bins = pd.qcut(
    x = s_quantitative, 
    q = 4,  # Create 4 quantile-based bins
    labels = ['Q1', 'Q2', 'Q3', 'Q4']
)

print(s_bins)
# 0     Q3
# 1     Q3
# 2     Q4
# 3     Q4
# 4     Q2
# 5     Q3
# 6     Q4
# 7     Q4
# 8     Q2
# 9     Q4
# 10    Q2
# 11    Q2
# 12    Q3
# 13    Q1
# 14    Q1
# 15    Q2
# 16    Q1
# 17    Q3
# 18    Q1
# 19    Q1
# dtype: category
# Categories (4, object): ['Q1' < 'Q2' < 'Q3' < 'Q4']

#-----------------
## bins = 10 (deciles)
#-----------------

s_bins = pd.qcut(
    x = s_quantitative, 
    q = 10,
    labels = [f'Decile {i+1}' for i in range(10)]
)

print(s_bins)
# 0      Decile 8
# 1      Decile 6
# 2      Decile 9
# 3     Decile 10
# 4      Decile 5
# 5      Decile 6
# 6     Decile 10
# 7      Decile 9
# 8      Decile 4
# 9      Decile 8
# 10     Decile 5
# 11     Decile 4
# 12     Decile 7
# 13     Decile 1
# 14     Decile 1
# 15     Decile 3
# 16     Decile 2
# 17     Decile 7
# 18     Decile 3
# 19     Decile 2
# dtype: category
# Categories (10, object): ['Decile 1' < 'Decile 2' < 'Decile 3' < 'Decile 4' ... 'Decile 7' <
#                           'Decile 8' < 'Decile 9' < 'Decile 10']

