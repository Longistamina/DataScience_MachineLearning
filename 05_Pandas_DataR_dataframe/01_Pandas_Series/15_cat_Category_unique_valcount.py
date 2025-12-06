'''
pd.Series.cat is an accessor object for categorical properties of the Series values.

When converted to the 'category' dtype, the memory usage of the Series is reduced (upto 90% less memory), 
and operations on the Series can be performed more efficiently.

######################################################

0. Creat a Categorical Series: pd.Series(dtype='category'), .astype('category'), pd.Categorical()

1. Core attributes: .cat.categories, .cat.codes, .cat.ordered

2. Adding and Removing: .cat.add_categories(), 
                        .cat.remove_categories(), .cat.remove_unused_categories(), 
                        .cat.set_categories()

3. Renaming: .cat.rename_categories()

4. Reordering: .cat.reorder_categories()

5. Ordered categories: .cat.as_ordered() (Support meaningful min(), max(), and sorting operations)

6. Unordered categories: .cat.as_unordered() (Treat categories as nominal with no inherent order)

7. Exploring Categorical: .unique(), .value_counts()
'''

import pandas as pd
import numpy as np

#---------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 0. Create a Categorical Series -----------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

#############################################
## Using pd.Series() with dtype='category' ##
#############################################

s_gender = pd.Series(["M", "M", "F", "M", "LGBTQ", "F", "M", "F", "LGBTQ", "M"], dtype='category')

print(s_gender)
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


######################################
## Using .astype('category') method ##
######################################

s_gender = pd.Series(["M", "M", "F", "M", "LGBTQ", "F", "M", "F", "LGBTQ", "M"])

'''
How .astype('category') works:
- Converts the Series to a categorical type.
- Categories are stored as a separate array, which saves memory.
- Useful for columns with a limited number of unique values.
- Categories are ordered from A-Z or increasing order.
'''

s_gender = s_gender.astype('category')
print(s_gender)
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


####################################
## Using pd.Categorical() method  ##
####################################

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

#---------------------------
## string gender example
#---------------------------

lst_gender = ["M", "M", "F", "M", "LGBTQ", "F", "M", "F", "LGBTQ", "M"]

## With ordered = False
s_gender_categ = pd.Series(pd.Categorical(lst_gender, ordered=False))
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


## With ordered = True
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

#---------------------------
## numeric example with NaN
#---------------------------

lst_price_levels = [1, 1, 3, 2, 5, 2, None, 4, 4, np.nan, 3]

## With ordered = False
s_price_levels_categ = pd.Series(pd.Categorical(lst_price_levels, ordered=False))
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


## With ordered = True
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


#---------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 1. Core attributes -------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

s_gender = pd.Series(["M", "M", "F", "M", "LGBTQ", "F", "M", "F", "LGBTQ", "M"], dtype='category')

s_levels = pd.Series(
    pd.Categorical(
        values = [1, 1, 3, 2, 5, 2, None, 4, 4, np.nan, 3],
        categories = [1, 2, 3, 4, 5],
        ordered = True
    )
)

#####################
## .cat.categories ##
#####################
# Returns the categories of the categorical Series.

print(s_gender.cat.categories)
# Index(['F', 'LGBTQ', 'M'], dtype='object')

print(s_levels.cat.categories)
# Index([1, 2, 3, 4, 5], dtype='int64')


################
## .cat.codes ##
################
# Returns the category codes as a Series of integers.

print(s_gender.cat.codes)
# 0    2 ('M' is the 2nd index in .cat.categories)
# 1    2
# 2    0 ('F' is the 0th index in .cat.categories)
# 3    2
# 4    1 ('LGBTQ' is the 1st index in .cat.categories)
# 5    0
# 6    2
# 7    0
# 8    1
# 9    2
# dtype: int8

print(s_levels.cat.codes)
# 0     0
# 1     0
# 2     2 ('3' is the 2nd index in .cat.categories)
# 3     1
# 4     4
# 5     1
# 6    -1 (None is invalid => is represented as -1)
# 7     3
# 8     3
# 9    -1 (np.nan is invalid => is represented as -1)
# 10    2
# dtype: int8


##################
## .cat.ordered ##
##################
# Returns True if the categories have an order, False otherwise

print(s_gender.cat.ordered)
# False

print(s_levels.cat.ordered)
# True


#---------------------------------------------------------------------------------------------------------------#
#------------------------------------- 2. Adding and Removing Categories ---------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

s_fruits = pd.Series(["Apple", "Banana", "Orange", "Apple", "Banana", "Grapes"], dtype='category')
s_degrees = pd.Series(
    pd.Categorical(
        values = ["Bachelor", "Master", "Bachelor", "Master", "Bachelor"],
        categories = ["Bachelor", "Master"],
        ordered = True
    )
)

###########################
## .cat.add_categories() ##
###########################
# Adds new categories to the categorical Series.

s_fruits = s_fruits.cat.add_categories(["Mango", "Pineapple"])
print(s_fruits)
# 0     Apple
# 1    Banana
# 2    Orange
# 3     Apple
# 4    Banana
# 5    Grapes
# dtype: category
# Categories (6, object): ['Apple', 'Banana', 'Grapes', 'Orange', 'Mango', 'Pineapple']

s_degrees = s_degrees.cat.add_categories(["PhD", "PostDoc"])
print(s_degrees)
# 0    Bachelor
# 1      Master
# 2    Bachelor
# 3      Master
# 4    Bachelor
# dtype: category
# Categories (4, object): ['Bachelor' < 'Master' < 'PhD' < 'PostDoc']

'''
NOTE: Adding a category does not assign it to any existing entries in the Series.
      You need to explicitly set values to the new category if desired.
'''

s_added = pd.concat(
    objs = [s_degrees, pd.Series(["PhD"], dtype=s_degrees.dtype)], # Must use the same dtype
    ignore_index = True
)
print(s_added)
# 0    Bachelor
# 1      Master
# 2    Bachelor
# 3      Master
# 4    Bachelor
# 5         PhD
# dtype: category
# Categories (4, object): ['Bachelor' < 'Master' < 'PhD' < 'PostDoc']


##############################
## .cat.remove_categories() ##
##############################
# Removes specified categories from the categorical Series.

s_removed = s_fruits.cat.remove_categories(["Orange", "Grapes"])
print(s_removed)
# 0     Apple
# 1    Banana
# 2       NaN ('Orange' is removed, so it's set to NaN)
# 3     Apple
# 4    Banana
# 5       NaN ('Grapes' is removed, so it's set to NaN)
# dtype: category
# Categories (4, object): ['Apple', 'Banana', 'Mango', 'Pineapple']

s_removed = s_degrees.cat.remove_categories(["Master"])
print(s_removed)
# 0    Bachelor
# 1         NaN ('Master' is removed, so it's set to NaN)
# 2    Bachelor
# 3         NaN ('Master' is removed, so it's set to NaN)
# 4    Bachelor
# dtype: category
# Categories (3, object): ['Bachelor' < 'PhD' < 'PostDoc']


#####################################
## .cat.remove_unused_categories() ##
#####################################
# Removes categories that are not used in the categorical Series.

s_removed_unused = s_fruits.cat.remove_unused_categories()
print(s_removed_unused)
# 0     Apple
# 1    Banana
# 2    Orange
# 3     Apple
# 4    Banana
# 5    Grapes
# dtype: category
# Categories (4, object): ['Apple', 'Banana', 'Grapes', 'Orange']
'''Here, 'Mango' and 'Pineapple' were removed as they were not used in the Series.'''

s_removed_unused = s_degrees.cat.remove_unused_categories()
print(s_removed_unused)
# 0    Bachelor
# 1      Master
# 2    Bachelor
# 3      Master
# 4    Bachelor
# dtype: category
# Categories (2, object): ['Bachelor' < 'Master']
'''Here, 'PhD' and 'PostDoc' were removed as they were not used in the Series.'''


###########################
## .cat.set_categories() ##
###########################
# Sets the categories of the categorical Series to the specified list of categories.
# Can be used to reorder categories or add/remove categories.

s_fruits_set = s_fruits.cat.set_categories(
    new_categories = ["A", "B", "G", "O"], # Should correspond to existing categories ['Apple', 'Banana', 'Grapes', 'Orange']
    rename = True  # If True, renames existing categories to new ones
)
print(s_fruits_set)
# 0    A ('Apple' renamed to 'A')
# 1    B ('Banana' renamed to 'B')
# 2    O ('Orange' renamed to 'O')
# 3    A
# 4    B
# 5    G
# dtype: category
# Categories (4, object): ['A', 'B', 'G', 'O']

s_degrees_set = s_degrees.cat.set_categories(
    new_categories = ["BSc", "MSc"], # Should correspond to existing categories ['Bachelor', 'Master']
    rename = True,  # If True, renames existing categories to new ones
    ordered = True # Set to True if you want to treat categories as ordered
)
print(s_degrees_set)
# 0    BSc
# 1    MSc
# 2    BSc
# 3    MSc
# 4    BSc
# dtype: category
# Categories (2, object): ['BSc' < 'MSc']


#---------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 3. Renaming Categories ----------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

s_gender = pd.Series(["M", "M", "F", "M", "LGBTQ", "F", "M", "F", "LGBTQ", "M"], dtype='category')

print(s_gender)
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


###########################
## new_categories = list ##
###########################

s_renamed_lst = s_gender.cat.rename_categories(
    new_categories = ["Female", "LGBTQ+", "Male"]
)
print(s_renamed_lst)
# 0      Male
# 1      Male
# 2    Female
# 3      Male
# 4    LGBTQ+
# 5    Female
# 6      Male
# 7    Female
# 8    LGBTQ+
# 9      Male
# dtype: category
# Categories (3, object): ['Female', 'LGBTQ+', 'Male']


###########################
## new_categories = dict ##
###########################

s_renamed_dict = s_gender.cat.rename_categories(
    new_categories = {"F": "Female", "M": "Male", "LGBTQ": "Other"}
)
print(s_renamed_dict)
# 0      Male
# 1      Male
# 2    Female
# 3      Male
# 4     Other
# 5    Female
# 6      Male
# 7    Female
# 8     Other
# 9      Male
# dtype: category
# Categories (3, object): ['Female', 'Other', 'Male']


#---------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 4. Reordering Categories ---------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

s_levels = pd.Series(
    pd.Categorical(
        values = [1, 1, 3, 2, 5, 2, 4, 4, 3],
        categories = [1, 2, 3, 4, 5],
        ordered = True
    )
)

print(s_levels)
# 0    1
# 1    1
# 2    3
# 3    2
# 4    5
# 5    2
# 6    4
# 7    4
# 8    3
# dtype: category
# Categories (5, int64): [1 < 2 < 3 < 4 < 5]

'''
Rename categories:
5 -> 5th
4 -> 4th
3 -> 3rd
2 -> 2nd
1 -> 1st
'''

s_renamed = s_levels.cat.rename_categories(
    new_categories = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th"}
)
print(s_renamed)
# 0    1st
# 1    1st
# 2    3rd
# 3    2nd
# 4    5th
# 5    2nd
# 6    4th
# 7    4th
# 8    3rd
# dtype: category
# Categories (5, object): ['1st' < '2nd' < '3rd' < '4th' < '5th']


###############################
## .cat.reorder_categories() ##
###############################

s_reordered = s_renamed.cat.reorder_categories(
    new_categories = ["5th", "4th", "3rd", "2nd", "1st"], # New order of categories
    ordered = True # Set to True if you want to treat categories as ordered
)
print(s_reordered)
# 0    1st
# 1    1st
# 2    3rd
# 3    2nd
# 4    5th
# 5    2nd
# 6    4th
# 7    4th
# 8    3rd
# dtype: category
# Categories (5, object): ['5th' < '4th' < '3rd' < '2nd' < '1st']


#---------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 5. Ordered Categories ------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

'''
Ordered categories have a meaningful order, allowing for comparisons and sorting.

Can use .cat.as_ordered() to convert unordered categories to ordered ones.
(then use .cat.reorder_categories() to set a specific order if needed)
'''

s_sizes = pd.Series(["Medium", "Small", "Large", "Medium", "Small", "Large"], dtype='category')

print(s_sizes)
# 0    Medium
# 1     Small
# 2     Large
# 3    Medium
# 4     Small
# 5     Large
# dtype: category
# Categories (3, object): ['Large', 'Medium', 'Small']

print(s_sizes.cat.ordered)
# False


############################################################
## Use .cat.as_ordered() to convert to ordered categories ##
############################################################

s_sizes_ordered = s_sizes.cat.as_ordered()

print(s_sizes_ordered.cat.ordered)
# True

print(s_sizes_ordered)
# 0    Medium
# 1     Small
# 2     Large
# 3    Medium
# 4     Small
# 5     Large
# dtype: category
# Categories (3, object): ['Large' < 'Medium' < 'Small']

'''Use .cat.reorder_categories() to set a specific order'''

s_sizes_ordered = s_sizes_ordered.cat.reorder_categories(
    new_categories = ["Small", "Medium", "Large"], # New order of categories
    ordered = True # Set to True if you want to treat categories as ordered
)

print(s_sizes_ordered)
# 0    Medium
# 1     Small
# 2     Large
# 3    Medium
# 4     Small
# 5     Large
# dtype: category
# Categories (3, object): ['Small' < 'Medium' < 'Large']

'''Combine both steps with method chaining'''

s_sizes_ordered = (
    s_sizes
    .cat.as_ordered()
    .cat.reorder_categories(
        new_categories = ["Small", "Medium", "Large"],
        ordered = True
    )
)
print(s_sizes_ordered)
# 0    Medium
# 1     Small
# 2     Large
# 3    Medium
# 4     Small
# 5     Large
# dtype: category
# Categories (3, object): ['Small' < 'Medium' < 'Large']


#########################################
## Meaningful min(), max() and sorting ##
#########################################

print(s_sizes_ordered.min()) # Small
print(s_sizes_ordered.max()) # Large

print(s_sizes_ordered.sort_values())
# 1     Small
# 4     Small
# 0    Medium
# 3    Medium
# 2     Large
# 5     Large
# dtype: category
# Categories (3, object): ['Small' < 'Medium' < 'Large']

print(s_sizes_ordered.sort_values(ascending=False))
# 2     Large
# 5     Large
# 0    Medium
# 3    Medium
# 1     Small
# 4     Small
# dtype: category
# Categories (3, object): ['Small' < 'Medium' < 'Large']


#---------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 6. Unordered Categories -----------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

'''
Unordered categories do not have a meaningful order, treating categories as nominal.

Can use .cat.as_unordered() to convert ordered categories to unordered ones.
'''

s_gender = pd.Series(
    pd.Categorical(
        values = ["M", "M", "F", "M", "LGBTQ", "F", "M", "F", "LGBTQ", "M"],
        categories = ["LGBTQ", "F", "M"],
        ordered = True
    )
)

print(s_gender)
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

print(s_gender.cat.ordered)
# True


################################################################
## Use .cat.as_unordered() to convert to unordered categories ##
################################################################

s_gender_unordered = s_gender.cat.as_unordered()

print(s_gender_unordered.cat.ordered)
# False

print(s_gender_unordered)
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
# Categories (3, object): ['LGBTQ', 'F', 'M']


print(s_gender_unordered.min())
'''
TypeError: Categorical is not ordered for operation min
you can use .as_ordered() to change the Categorical to an ordered one
'''


#---------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 7. Exploring Categorical ----------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

s_gender = pd.Series(["M", "M", "F", "M", "LGBTQ", "F", "M", "F", "LGBTQ", "M"], dtype='category')

###############
## .unique() ##
###############
# Returns the unique categories in the categorical/object Series.

uniques = s_gender.unique()
print(uniques)
# ['M', 'F', 'LGBTQ']
# Categories (3, object): ['F', 'LGBTQ', 'M']

lst_uniques = s_gender.unique().tolist()
print(lst_uniques)
# ['M', 'F', 'LGBTQ']


#####################
## .value_counts() ##
#####################
# Returns a Series containing counts of unique categories

print(s_gender.value_counts())
# M        5
# F        3
# LGBTQ    2
# Name: count, dtype: int64

print(s_gender.value_counts().get("M")) # Get the count of category "M"
# 5