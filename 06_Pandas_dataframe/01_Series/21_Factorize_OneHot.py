'''
Categorical Encoding is the process of converting categorical variables into numerical representations.
This is useful for machine learning algorithms that require numerical input.

Categorical Encoding with:
    1. pd.factorize()
    2. pd.get_dummies(): One-Hot encoding
'''

import pandas as pd

s_gender = pd.Series(["M", "M", "F", "M", "LGBTQ", "F", "M", "F", "LGBTQ", "M"])

# =========================================================================================
# 1. pd.factorize()
# =========================================================================================
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

### Assign the result to separate variables ###

s_gender_factorized, codes = pd.factorize(s_gender)

print(s_gender_factorized)
# [0 0 1 0 2 1 0 1 2 0]
# <class 'numpy.ndarray'>

print(codes)
# Index(['M', 'F', 'LGBTQ'], dtype='object')

# =========================================================================================
#  2. pd.get_dummies(): One-Hot encoding
# =========================================================================================
'''
pd.get_dummies() creates a DataFrame with binary columns for each category in the Series.
Each column represents a category, and the values are 0 or 1 indicating the presence of that category.

It is useful for one-hot encoding categorical variables.
'''

### Without dropping the first category ###

s_gender_dummmies = pd.get_dummies(s_gender, prefix="gender")
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

s_gender_dummmies = pd.get_dummies(s_gender, prefix="gender").astype("int64") # Convert to 0-1 binary integers
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

### With dropping the first category (to avoid multicollinearity) ###
'''
In fact, if we have n categories, we just need n-1 columns to represent them.
The last n-th category can be inferred from the other n-1 columns.

=> Can drop the first category to avoid multicollinearity.
'''

s_gender_dummmies = pd.get_dummies(s_gender, drop_first=True, prefix="gender").astype("int64")
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
