'''
In dataR (as well as R), categorical variables are often represented as factors.

#################################

1. Create factor variable
   + dr.factor()
   + dr.ordered()

2. Convert to factor variable
   + dr.as_factor()
   + dr.as_ordered()

3. Inspect core properties:
   + dr.nlevels()
   + dr.levels()
   + dr.is_factor()
   + dr.is_ordered()
   + dr.fct_unique()
   + dr.fct_count()

4. Add and Remove levels:
   + Add: dr.fct_expand()
   + Remove: dr.fct_drop(), dr.droplevels()

5. Reorder levels:
   + Manual reordering: dr.fct_relevel()
   + Automatic reordering: dr.fct_inorder(), dr.fct_infreq(), dr.fct_inseq()
   + Reordering by another variable: dr.fct_reorder(), dr.fct_reorder2()
   + Shuffle: dr.fct_shuffle()
   + Reverse/shift: dr.fct_rev(), dr.fct_shift()

6. Rename levels:
   + Manual renaming: dr.fct_recode()
   + Combine multiple levels into one: dr.fct_collapse()
   + Lumping infrequent levels: dr.fct_lump(), dr.fct_lump_min(), dr.fct_lump_prop(), dr.fct_lump_n(), dr.fct_lump_lowfreq()
   + Replacing with "other": dr.fct_other()
   + Apply function to relabel: dr.fct_relabel()

7. Handle multiple factors:
   + Concatenate factors: dr.fct_c()
   + Cross factors: dr.fct_cross()
   + Unify levels: dr.fct_unify(), dr.lvls_union()

8. Special Operations:
   + Handle missing levels: dr.fct_explicit_na()
   + Anonymize levels: dr.fct_anon()

9. Low-level operations:
   + dr.lvls_reorder()
   + dr.lvls_revalue()
   + dr.lvls_expand()

10. Apply to processing pipelines with dr.mutate()
'''

import datar.all as dr
from datar import f
import pandas as pd
import numpy as np


#------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 1. Create factor variable -----------------------------------------#
#------------------------------------------------------------------------------------------------------------#

#################
## dr.factor() ##
#################
'''Create a factor (categorical variable) from a list-like object.'''

fct_gender = dr.factor(
    x=["M", "F", "F", "M", "Others", "F", "M", "M", "F", "Others"],
    ordered=False # non-ordered factor
)

print(fct_gender)
# ['M', 'F', 'F', 'M', 'Others', 'F', 'M', 'M', 'F', 'Others']
# Categories (3, object): ['F', 'M', 'Others']

##################
## dr.ordered() ##
##################
'''Create an ordered factor (ordered categorical variable) from a list-like object.'''

#----
## Example 1
#----

ord_degree = dr.ordered(
      x=["Bachelors", "Masters", "PhD", "Bachelors", "PhD", "Masters", "Bachelors", "AssociateProf"],
      levels=["Bachelors", "Masters", "PhD", "AssociateProf"]  # specify the order of levels
)

print(ord_degree)
# ['Bachelors', 'Masters', 'PhD', 'Bachelors', 'PhD', 'Masters', 'Bachelors', 'AssociateProf']
# Categories (4, object): ['Bachelors' < 'Masters' < 'PhD' < 'AssociateProf']

#----
## Example 2
#----

ord_size = dr.ordered(
    x=[39, 42, 36, 40, 38, 41, 39, 37, 42, 40],
    levels=[36, 37, 38, 39, 40, 41, 42]  # specify the order of levels
)

print(ord_size)
# [39, 42, 36, 40, 38, 41, 39, 37, 42, 40]
# Categories (7, int64): [36 < 37 < 38 < 39 < 40 < 41 < 42]


#------------------------------------------------------------------------------------------------------------#
#------------------------------------- 2. Convert to factor variable ----------------------------------------#
#------------------------------------------------------------------------------------------------------------#

####################
## dr.as_factor() ##
####################
'''Convert an existing variable to a factor (categorical variable).'''

lst_gender = ["M", "F", "F", "M", "Others", "F", "M", "M", "F", "Others"]

fct_gender2 = dr.as_factor(lst_gender)

print(fct_gender2)
# ['M', 'F', 'F', 'M', 'Others', 'F', 'M', 'M', 'F', 'Others']
# Categories (3, object): ['F', 'M', 'Others']

#####################
## dr.as_ordered() ##
#####################
'''Convert an existing variable to an ordered factor (ordered categorical variable).'''

#----
## Example 1
#----

lst_degree = ["Bachelors", "Masters", "PhD", "Bachelors", "PhD", "Masters", "Bachelors", "AssociateProf"]

ord_degree2 = dr.as_ordered(lst_degree)

print(ord_degree2)
# ['Bachelors', 'Masters', 'PhD', 'Bachelors', 'PhD', 'Masters', 'Bachelors', 'AssociateProf']
# Categories (4, object): ['AssociateProf' < 'Bachelors' < 'Masters' < 'PhD']

'''
NOTE: dr.as_ordered() DOES NOT allow specifying levels.
      it will set the order automatically like A-Z, 0-9 based on unique values.
'''

#----
## Example 2
#----

lst_size = [39, 42, 36, 40, 38, 41, 39, 37, 42, 40]

ord_size2 = dr.as_ordered(lst_size)

print(ord_size2)
# [39, 42, 36, 40, 38, 41, 39, 37, 42, 40]
# Categories (7, int64): [36 < 37 < 38 < 39 < 40 < 41 < 42]


#------------------------------------------------------------------------------------------------------------#
#-------------------------- 3. Inspect core properties of factor variable -----------------------------------#
#------------------------------------------------------------------------------------------------------------#

fct_gender = dr.factor(x=["M", "F", "F", "M", "Others", "F", "M", "M", "F", "Others"])

ord_size = dr.ordered(x=[39, 42, 36, 40, 38, 41, 39, 37, 42, 40])

ord_degree = dr.ordered(
      x=["Bachelors", "Masters", "PhD", "Bachelors", "PhD", "Masters", "Bachelors", "AscProf"],
      levels=["Bachelors", "Masters", "PhD", "AscProf"]
)

##################
## dr.nlevels() ##
##################
'''Return the number of levels in a factor variable.'''

print(dr.nlevels(fct_gender)) # 3
print(dr.nlevels(ord_size))   # 7
print(dr.nlevels(ord_degree)) # 4

#################
## dr.levels() ##
#################
'''Return the levels of a factor variable'''

print(dr.levels(fct_gender)) # ['F' 'M' 'Others']
print(dr.levels(ord_size))   # [36 37 38 39 40 41 42]
print(dr.levels(ord_degree)) # ['Bachelors' 'Masters' 'PhD' 'AscProf']

####################
## dr.is_factor() ##
####################
'''Check if a variable is a factor variable.'''

print(dr.is_factor(fct_gender)) # True
print(dr.is_factor(ord_size))   # True
print(dr.is_factor(ord_degree)) # True

#####################
## dr.is_ordered() ##
#####################
'''Check if a variable is an ordered factor variable.'''

print(dr.is_ordered(fct_gender)) # False
print(dr.is_ordered(ord_size))   # True
print(dr.is_ordered(ord_degree)) # True

#####################
## dr.fct_unique() ##
#####################
'''Return the unique values of a factor variable, preserving the levels order.'''

print(dr.fct_unique(fct_gender))
# ['F', 'M', 'Others']
# Categories (3, object): ['F', 'M', 'Others']

print(dr.fct_unique(ord_size))
# [36, 37, 38, 39, 40, 41, 42]
# Categories (7, int64): [36 < 37 < 38 < 39 < 40 < 41 < 42]

print(dr.fct_unique(ord_degree))
# ['Bachelors', 'Masters', 'PhD', 'AscProf']
# Categories (4, object): ['Bachelors' < 'Masters' < 'PhD' < 'AscProf']

####################
## dr.fct_count() ##
####################
'''Count the occurrences of each level in a factor variable.'''

print(dr.fct_count(fct_gender))
#            f       n
#   <category> <int64>
# 0          F       4
# 1          M       4
# 2     Others       2

print(dr.fct_count(ord_size))
#            f       n
#   <category> <int64>
# 0         36       1
# 1         37       1
# 2         38       1
# 3         39       2
# 4         40       2
# 5         41       1
# 6         42       2

print(dr.fct_count(ord_degree))
#            f       n
#   <category> <int64>
# 0  Bachelors       3
# 1    Masters       2
# 2        PhD       2
# 3    AscProf       1


#------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 4. Add and Remove levels -----------------------------------------#
#------------------------------------------------------------------------------------------------------------#

fct_gender = dr.factor(x=["M", "F", "F", "M", "Others", "F", "M", "M", "F", "Others"])

ord_size = dr.ordered(x=[39, 42, 36, 40, 38, 41, 39, 37, 42, 40])

ord_degree = dr.ordered(
      x=["Bachelors", "Masters", "PhD", "Bachelors", "PhD", "Masters", "Bachelors", "AscProf"],
      levels=["Bachelors", "Masters", "PhD", "AscProf", "PostDoc"]  # "PostDoc" level is unused
)

#####################
## dr.fct_expand() ##
#####################
'''Add new levels to a factor variable.'''

added_gender = dr.fct_expand(fct_gender, ["N/A", "Unknown"])
print(dr.levels(added_gender)) # ['F' 'M' 'Others' 'N/A' 'Unknown']

added_degree = dr.fct_expand(ord_degree, "PostDoc")
print(dr.levels(added_degree)) # ['Bachelors' 'Masters' 'PhD' 'AscProf' 'PostDoc']

###################
## dr.fct_drop() ##
###################
'''
Remove unused levels from a factor variable
Using condition to filter the target levels to be kept.
'''

dropped_degree = dr.fct_drop(ord_degree)
print(dr.levels(dropped_degree)) # ['Bachelors' 'Masters' 'PhD' 'AscProf']
                                 # "PostDoc" level is removed since it is unused.

dropped_degree = dr.fct_drop(ord_degree[ord_degree != "AscProf"], only=["AscProf"]) # Remove "AscProf" level, still keep "PostDoc"
print(dr.levels(dropped_degree)) # ['Bachelors' 'Masters' 'PhD' 'PostDoc']


#####################
## dr.droplevels() ##
#####################
'''
Remove unused levels from a factor variable.
Using condition to filter the target levels to be kept.
'''

dropped_size = dr.droplevels(ord_size[ord_size > 38]) # Keep only levels > 38
print(dr.levels(dropped_size)) # [39 40 41 42]

dropped_gender = dr.droplevels(fct_gender[~fct_gender.isin(["Others"])]) # Remove "Others" level
print(dr.levels(dropped_gender)) # ['F' 'M']


#------------------------------------------------------------------------------------------------------------#
#-------------------------------- 5. Reorder levels of factor variable --------------------------------------#
#------------------------------------------------------------------------------------------------------------#

fct_gender = dr.factor(x=["M", "F", "F", "M", "Others", "F", "M", "M", "F", "Others"])

ord_size = dr.ordered(x=[39, 42, 36, 40, 38, 41, 39, 37, 42, 40])

ord_degree = dr.ordered(
      x=["Bachelors", "Masters", "PhD", "Bachelors", "PhD", "Masters", "Bachelors", "AscProf"],
      levels=["Bachelors", "Masters", "PhD", "AscProf", "PostDoc"]  # "PostDoc" level is unused
)

############################
##    dr.fct_relevel()    ##
############################
''' Manually specify which levels to move and where to move them.'''

#------
## Original
#------

print(dr.levels(fct_gender)) # ['F' 'M' 'Others']
print(dr.levels(ord_size))   # [36 37 38 39 40 41 42]
print(dr.levels(ord_degree)) # ['Bachelors' 'Masters' 'PhD' 'AscProf' 'PostDoc']

#------
## dr.fct_relevel()
#------

relevel_gender = dr.fct_relevel(fct_gender, ["Others", "M", "F"])
print(dr.levels(relevel_gender)) # ['Others' 'M' 'F']

relevel_size = dr.fct_relevel(ord_size, [42, 41, 40]) # Move levels 42, 41, 40 to the front
print(dr.levels(relevel_size)) # [42 41 40 36 37 38 39]

relevel_degree = dr.fct_relevel(ord_degree, "PostDoc") # Move "PostDoc" level to the front
print(dr.levels(relevel_degree)) # ['PostDoc' 'Bachelors' 'Masters 'PhD' 'AscProf']

relevel_degree_after = dr.fct_relevel(ord_degree, "PostDoc", after=2) # Move "PostDoc" level after the 2-indexed position
print(dr.levels(relevel_degree_after)) # ['Bachelors' 'Masters' 'PhD' 'PostDoc' 'AscProf']

############################
##    dr.fct_inorder()    ##
############################
'''Reorder levels by the order they first appear in the data'''

#------
## Original
#------

print(fct_gender)
# ['M', 'F', 'F', 'M', 'Others', 'F', 'M', 'M', 'F', 'Others']
# Categories (3, object): ['F', 'M', 'Others']

print(ord_size)
# [39, 42, 36, 40, 38, 41, 39, 37, 42, 40]
# Categories (7, int64): [36 < 37 < 38 < 39 < 40 < 41 < 42]

#------
## dr.fct_inorder()
#------

inorder_gender = dr.fct_inorder(fct_gender)
print(dr.levels(inorder_gender)) # ['M' 'F' 'Others']
                                 # M appears first in the data, so it becomes the first level.

inorder_size = dr.fct_inorder(ord_size)
print(dr.levels(inorder_size))   # [39 42 36 40 38 41 37]
                                 # 39 appears first, then 42, and so on. So the levels are reordered accordingly.

###########################
##    dr.fct_infreq()    ##
###########################
'''Reorder levels from most frequent to least frequent'''

#------
## Original
#------

print(fct_gender)
# ['M', 'F', 'F', 'M', 'Others', 'F', 'M', 'M', 'F', 'Others']
# Categories (3, object): ['F', 'M', 'Others']

print(ord_size)
# [39, 42, 36, 40, 38, 41, 39, 37, 42, 40]
# Categories (7, int64): [36 < 37 < 38 < 39 < 40 < 41 < 42]

#------
## dr.fct_infreq()
#------

infreq_gender = dr.fct_infreq(fct_gender)
print(dr.levels(infreq_gender)) # ['M' 'F' 'Others']
                                # M and F both appear 4 times, but M comes first in the original levels, so it is placed first.
                                # Then "Others" appears 2 times, so it is last.

infreq_size = dr.fct_infreq(ord_size)
print(dr.levels(infreq_size))   # [42 40 39 41 38 37 36]
                                # 42 appears 2 times, then 40 appears 2 times, then 39 appears 2 times, and so on.

##########################
##    dr.fct_inseq()    ##
##########################
'''
Reorder numeric factor levels by their numeric values
NOTE: only works for NUMERIC factor variables.
'''

#------
## Original
#------

generation = dr.ordered(
    x=[3, 1, 4, 2, 5, 1, 2, 3, 4, 5],
    levels=[5, 2, 4, 1 , 3] # original unordered levels
)

print(generation)
# [3, 1, 4, 2, 5, 1, 2, 3, 4, 5]
# Categories (5, int64): [5 < 2 < 4 < 1 < 3]

#------
## dr.fct_inseq()
#------

inseq_generation = dr.fct_inseq(generation)
print(inseq_generation)
# [3, 1, 4, 2, 5, 1, 2, 3, 4, 5]
# Categories (5, int64): [1 < 2 < 3 < 4 < 5]

############################
##    dr.fct_reorder()    ##
############################
'''Reorder factor levels based on a summary function applied to another variable'''

df_color = dr.tribble(
    f.color,  f.a, f.b,
    "blue",   1,   2,
    "green",  6,   2,
    "purple", 3,   3,
    "red",    2,   3,
    "yellow", 5,   1
) >> dr.mutate(color=dr.as_factor(f.color))

# Reorder gender by median salary
color_by_a = dr.fct_reorder(
    df_color['color'],
    df_color['a'],
    _fun=dr.median,
    _desc=False # ascending order
)

print(color_by_a)
# ['blue', 'green', 'purple', 'red', 'yellow']
# Categories (5, object): ['blue', 'red', 'purple', 'yellow', 'green']


############################
##   dr.fct_reorder2()    ##
############################
'''Reorder based on two variables, useful for line plots where you want legend order to match line endpoints'''

color_by_a_b = dr.fct_reorder2(
    df_color['color'],
    df_color['a'],
    df_color['b'],
    _desc=True # descending order
)

print(color_by_a_b)
# ['blue', 'green', 'purple', 'red', 'yellow']
# Categories (5, object): ['red', 'purple', 'green', 'blue', 'yellow']

###########################
##    dr.fct_shuffle()   ##
###########################
'''Randomly shuffle the levels of a factor variable'''

#------
## Original
#------

print(ord_size)
# [39, 42, 36, 40, 38, 41, 39, 37, 42, 40]
# Categories (7, int64): [36 < 37 < 38 < 39 < 40 < 41 < 42]

#------
## dr.fct_shuffle()
#------

shuffled_size = dr.fct_shuffle(ord_size)

print(shuffled_size)
# [39, 42, 36, 40, 38, 41, 39, 37, 42, 40]
# Categories (7, int64): [40 < 39 < 42 < 36 < 38 < 41 < 37]

#########################
##     dr.fct_rev()    ##
#########################
'''Simply reverse the current level order'''

#------
## Original
#------

print(dr.levels(ord_degree)) # ['Bachelors' 'Masters' 'PhD' 'AscProf' 'PostDoc']

#------
## dr.fct_rev()
#------

reversed_degree = dr.fct_rev(ord_degree)
print(dr.levels(reversed_degree)) # ['PostDoc' 'AscProf' 'PhD' 'Masters' 'Bachelors']

#########################
##    dr.fct_shift()   ##
#########################
'''Rotate levels left or right, wrapping around'''

#------
## Original
#------

print(dr.levels(ord_size))   # [36 37 38 39 40 41 42]

#------
## dr.fct_shift()
#------

shifted_size = dr.fct_shift(ord_size, n=1) # Shift right by 1
print(dr.levels(shifted_size))   # [37 38 39 40 41 42 36]
                                 # "36" is wrapped around to the end.

shifted_size_left = dr.fct_shift(ord_size, n=-2) # Shift left by 2
print(dr.levels(shifted_size_left))   # [41 42 36 37 38 39 40]
                                 

#------------------------------------------------------------------------------------------------------------#
#--------------------------------- 6. Rename levels of factor variable --------------------------------------#
#------------------------------------------------------------------------------------------------------------#

fct_product = dr.factor([
    "Apple", "Samsung", "Apple", "Xiaomi", "Apple", "Huawei", "Samsung",
    "OnePlus", "Apple", "Oppo", "Vivo", "Apple", "Samsung", "Realme"
])

ord_size = dr.ordered(x=[39, 42, 36, 40, 38, 41, 39, 37, 42, 40])

ord_degree = dr.ordered(
      x=["Bachelors", "Masters", "PhD", "Bachelors", "PhD", "Masters", "Bachelors", "AscProf"],
      levels=["Bachelors", "Masters", "PhD", "AscProf", "PostDoc"]  # "PostDoc" level is unused
)

#############################
##     dr.fct_recode()     ##
#############################
'''
Change level names one by one, combine levels, or remove levels
NOTE: automatically drops unused levels.
'''

#------
## Basic renaming
#------
# new_name="old_name"

renamed_gender = dr.fct_recode(
    fct_gender,
    Male="M",
    Female="F",
    LGBTQ="Others"
)

print(renamed_gender)
# ['Male', 'Female', 'Female', 'Male', 'LGBTQ', 'Female', 'Male', 'Male', 'Female', 'LGBTQ']
# Categories (3, object): ['Female', 'Male', 'LGBTQ']

#------
## Combine levels
#------
# new_name=["old_name1", "old_name2", ...]

renamed_degree = dr.fct_recode(
    ord_degree,
    **{"Undergraduate": "Bachelors", "Graduate": ["Masters", "PhD"]}
)

print(renamed_degree)
# ['Undergraduate', 'Graduate', 'Graduate', 'Undergraduate', 'Graduate', 'Graduate', 'Undergraduate', 'AscProf']
# Categories (3, object): ['Undergraduate', 'Graduate', 'AscProf']

#############################
##    dr.fct_collapse()    ##
#############################
'''Shortcut for combining many levels at once (cleaner than multiple fct_recode() calls)'''

collapsed_size = dr.fct_collapse(
    ord_size,
    Small=[36, 37, 38],
    Medium=[39, 40],
    Large=[41, 42]
)

print(collapsed_size)
# ['Medium', 'Large', 'Small', 'Medium', 'Small', 'Large', 'Medium', 'Small', 'Large', 'Medium']
# Categories (3, object): ['Small', 'Medium', 'Large']

##############################
##     dr.fct_lump_min()    ##
##############################
'''Lump levels appearing fewer than min times into "Other"'''

lumped_product = dr.fct_lump_min(
    fct_product,
    min=3,               # levels appearing less than 3 times will be lumped
    other_level="Rare"   # rename the rests to "Rare" (default is "Other")
)

print(lumped_product)
# ['Apple', 'Samsung', 'Apple', 'Rare', 'Apple', ..., 'Rare', 'Rare', 'Apple', 'Samsung', 'Rare']
# Length: 14
# Categories (3, object): ['Apple', 'Samsung', 'Rare']
'''Other products are lumped into "Rare" since they appear less than 3 times.'''

###############################
##      dr.fct_lump_n()      ##
###############################
'''Keep only the n most (or least) frequent levels, lump the rest into "Other"'''

lumped_product_n = dr.fct_lump_n(
    fct_product,
    n=1,                  # keep only top 1 most frequent level
    other_level="Others", # rename the rests to "Others" (default is "Other")
)

print(lumped_product_n)
# ['Apple', 'Others', 'Apple', 'Others', 'Apple', ..., 'Others', 'Others', 'Apple', 'Others', 'Others']
# Length: 14
# Categories (2, object): ['Apple', 'Others']

#################################
##      dr.fct_lump_prop()     ##
#################################
'''Lump levels appearing in less than prop proportion of data into "Other"'''

lumped_product_prop = dr.fct_lump_prop(
    fct_product,
    prop=0.2,              # levels appearing in less than 20% of data will be lumped
    other_level="Misc"     # rename the rests to "Misc" (default is "Other")
)

print(lumped_product_prop)
# ['Apple', 'Samsung', 'Apple', 'Misc', 'Apple', ..., 'Misc', 'Misc', 'Apple', 'Samsung', 'Misc']
# Length: 14
# Categories (3, object): ['Apple', 'Samsung', 'Misc']

####################################
##      dr.fct_lump_lowfreq()     ##
####################################
'''Lump levels with low frequency into "Other" based on a statistical method'''

lumped_degree_lowfreq = dr.fct_lump_lowfreq(
    ord_degree,
    other_level="OtherDegrees"  # rename the rests to "OtherDegrees" (default is "Other")
)

print(lumped_degree_lowfreq)
# ['Bachelors', 'Masters', 'PhD', 'Bachelors', 'PhD', 'Masters', 'Bachelors', 'OtherDegrees']
# Categories (4, object): ['Bachelors', 'Masters', 'PhD', 'OtherDegrees']

##############################
##      dr.fct_other()      ##
##############################
'''Manually specify which levels to keep or drop, converting the rest to "Other"'''

#------
## Keep specific levels
#------

product_keep = dr.fct_other(
    fct_product,
    keep=["Apple", "Xiaomi"],  # keep only these levels
    other_level="OtherBrands" # rename the rests to "OtherBrands" (default is "Other")
)

print(product_keep)
# ['Apple', 'OtherBrands', 'Apple', 'Xiaomi', 'Apple', ..., 'OtherBrands', 'OtherBrands', 'Apple', 'OtherBrands', 'OtherBrands']
# Length: 14
# Categories (3, object): ['Apple', 'Xiaomi', 'OtherBrands']

#------
## Drop specific levels
#------

product_drop = dr.fct_other(
    fct_product,
    drop=["Samsung", "Huawei", "Apple"], # drop these levels into "Other"
    other_level="OtherBrands"   # rename the rests to "OtherBrands" (default is "Other")
)

print(product_drop)
# ['OtherBrands', 'OtherBrands', 'OtherBrands', 'Xiaomi', 'OtherBrands', ..., 'Oppo', 'Vivo', 'OtherBrands', 'OtherBrands', 'Realme']
# Length: 14
# Categories (6, object): ['OnePlus', 'Oppo', 'Realme', 'Vivo', 'Xiaomi', 'OtherBrands']

#############################
##     dr.fct_relabel()    ##
#############################
'''Apply a function to transform all level names at once'''

relabel_product = dr.fct_relabel(
    fct_product,
    dr.toupper  # convert all level names to uppercase
)

print(relabel_product)
# ['APPLE', 'SAMSUNG', 'APPLE', 'XIAOMI', 'APPLE', ..., 'OPPO', 'VIVO', 'APPLE', 'SAMSUNG', 'REALME']
# Length: 14
# Categories (8, object): ['APPLE', 'HUAWEI', 'ONEPLUS', 'OPPO', 'REALME', 'SAMSUNG', 'VIVO', 'XIAOMI']


#------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 7. Handle multiple factors ----------------------------------------#
#------------------------------------------------------------------------------------------------------------#

######################
##    dr.fct_c()    ##
######################
'''Combine multiple factors into one, unifying their levels (useful when combining data from different sources)'''

survey_region1 = dr.factor(["High", "Medium", "Low", "High"])
survey_region2 = dr.factor(["Medium", "Very High", "Very Low", "Medium", "Low"])

combined_survey = dr.fct_c(survey_region1, survey_region2)

print(combined_survey)
# ['High', 'Medium', 'Low', 'High', 'Medium', 'Very High', 'Very Low', 'Medium', 'Low']
# Categories (5, object): ['High', 'Low', 'Medium', 'Very High', 'Very Low']

########################
##   dr.fct_cross()   ##
########################
'''Create interaction factors - all combinations of levels from multiple factors (like interaction terms in ANOVA)'''

fct_A = dr.factor(["A1", "A2", "A1", "A3"])
fct_B = dr.factor(["B1", "B1", "B2", "B2"])

crossed_factors = dr.fct_cross(fct_A, fct_B, sep="-")

print(crossed_factors)
# ['A1-B1', 'A2-B1', 'A1-B2', 'A3-B2']
# Categories (4, object): ['A1-B1', 'A1-B2', 'A2-B1', 'A3-B2']

#######################
##   dr.fct_unify()  ##
#######################
'''Standardize levels across a list of factors (make them all have the same levels)'''

factor1 = dr.factor(["a", "b", "a"])
factor2 = dr.factor(["b", "c", "b"])
factor3 = dr.factor(["a", "b", "c", "a"])

unified_factors = dr.fct_unify([factor1, factor2, factor3]) # Must put them in a list

print(unified_factors)
# [['a', 'b', 'a']
# Categories (3, object): ['a', 'b', 'c'], ['b', 'c', 'b']
# Categories (3, object): ['a', 'b', 'c'], ['a', 'b', 'c', 'a']
# Categories (3, object): ['a', 'b', 'c']]

for i, f in enumerate(unified_factors, start=1):
    print(f"Factor: {dr.unique(f)} ___ Levels: {dr.levels(f)}")
# Factor: ['a' 'b'] ___ Levels: ['a' 'b' 'c']
# Factor: ['b' 'c'] ___ Levels: ['a' 'b' 'c']
# Factor: ['a' 'b' 'c'] ___ Levels: ['a' 'b' 'c']

'''
Before unification, your three factors had different levels:
+ factor1: values ["a", "b", "a"] with levels ['a', 'b'] (only 2 levels)
+ factor2: values ["b", "c", "b"] with levels ['b', 'c'] (only 2 levels)
+ factor3: values ["a", "b", "c", "a"] with levels ['a', 'b', 'c'] (3 levels)

After unification, all three factors now share the same complete set of levels: ['a', 'b', 'c']
'''


#------------------------------------------------------------------------------------------------------------#
#------------------------------- 8. Special operations on factor variable -----------------------------------#
#------------------------------------------------------------------------------------------------------------#

##############################
##   dr.fct_explicit_na()   ##
##############################
'''Convert NA (missing) values into an explicit factor level, making them visible in summaries, tables, and plots'''

#------
## Before
#------
survey_response = dr.factor([
    "Satisfied", "Very Satisfied", None, "Satisfied", 
    "Dissatisfied", None, "Very Satisfied", np.nan, 
    "Satisfied", None, "Very Satisfied"
])

print(survey_response)
# ['Satisfied', 'Very Satisfied', NaN, 'Satisfied', 'Dissatisfied', ..., 'Very Satisfied', NaN, 'Satisfied', NaN, 'Very Satisfied']
# Length: 11
# Categories (3, object): ['Dissatisfied', 'Satisfied', 'Very Satisfied']
'''None/NaN values are not shown as a level.'''

print(dr.table(survey_response))
#        Dissatisfied  Satisfied  Very Satisfied
#             <int64>    <int64>         <int64>
# count             1          3               3

#------
## After
#------

explicit_na_response = dr.fct_explicit_na(survey_response, na_level="No Response")

print(explicit_na_response)
# ['Satisfied', 'Very Satisfied', 'No Response', 'Satisfied', 'Dissatisfied', ..., 'Very Satisfied', 'No Response', 'Satisfied', 'No Response', 'Very Satisfied']
# Length: 11
# Categories (4, object): ['Dissatisfied', 'Satisfied', 'Very Satisfied', 'No Response']
'''Now None/NaN values are converted to "No Response" level and shown in the levels.'''

print(dr.table(explicit_na_response))
#        Dissatisfied  Satisfied  Very Satisfied  No Response
#             <int64>    <int64>         <int64>      <int64>
# count             1          3               3            4

#########################
##    dr.fct_anon()    ##
#########################
'''
Replace factor levels with anonymized values (typically random letters or numbers) 
for privacy protection while preserving factor structure.
'''

patient_nationality = dr.factor([
    "USA", "Canada", "Mexico", "USA", "Canada",
    "USA", "Mexico", "Canada", "USA", "Mexico"
])

anon_nationality = dr.fct_anon(patient_nationality, prefix="Nat_")

print(anon_nationality)
# ['Nat_1', 'Nat_0', 'Nat_2', 'Nat_1', 'Nat_0', 'Nat_1', 'Nat_2', 'Nat_0', 'Nat_1', 'Nat_2']
# Categories (3, object): ['Nat_0', 'Nat_1', 'Nat_2']


#------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 9. Low-level operations ---------------------------------------------#
#------------------------------------------------------------------------------------------------------------#

ord_degree = dr.ordered(
      x=["Bachelors", "Masters", "PhD", "Bachelors", "PhD", "Masters", "Bachelors", "AscProf"],
      levels=["Bachelors", "Masters", "PhD", "AscProf", "PostDoc"]  # "PostDoc" level is unused
)

###########################
##   dr.lvls_reorder()   ##
###########################
'''
Directly reorder the sequence of levels without changing the underlying data values
Requires you to specify complete new level order
'''

#------
## Original
#------

print(ord_degree)
# ['Bachelors', 'Masters', 'PhD', 'Bachelors', 'PhD', 'Masters', 'Bachelors', 'AscProf']
# Categories (5, object): ['Bachelors' < 'Masters' < 'PhD' < 'AscProf' < 'PostDoc']

#------
## dr.lvls_reorder()
#------

reordered_degree = dr.lvls_reorder(
    ord_degree,
    idx=[4, 0, 2, 1, 3]  # New order of levels by their original indices
)

print(reordered_degree)
# ['Bachelors', 'Masters', 'PhD', 'Bachelors', 'PhD', 'Masters', 'Bachelors', 'AscProf']
# Categories (5, object): ['PostDoc' < 'Bachelors' < 'PhD' < 'Masters' < 'AscProf']

#############################
##    dr.lvls_revalue()    ##
#############################
'''
Directly rename/recode factor levels by providing a mapping (Dictionary)
Low-level, straightforward 1-to-1 renaming
'''

#------
## Original
#------

print(ord_degree)
# ['Bachelors', 'Masters', 'PhD', 'Bachelors', 'PhD', 'Masters', 'Bachelors', 'AscProf']
# Categories (5, object): ['Bachelors' < 'Masters' < 'PhD' < 'AscProf' < 'PostDoc']

#------
## dr.lvls_revalue()
#------

revalued_degree = dr.lvls_revalue(
    ord_degree,
    new_levels=["BSc", "MSc", "PhD", "AscProf", "PostDoc"]
    #            ↑      ↑      ↑      ↑         ↑
    #         Level1  Level2  Level3 Level4   Level5
    # Must match the order and count of original levels!
)

print(revalued_degree)
# ['BSc', 'MSc', 'PhD', 'BSc', 'PhD', 'MSc', 'BSc', 'AscProf']
# Categories (4, object): ['BSc', 'MSc', 'PhD', 'AscProf']
'''Lose the ordinal property since levels are renamed arbitrarily, and "PostDoc" level is unused and dropped.'''

############################
##    dr.lvls_expand()    ##
############################
'''Add additional levels to a factor without them appearing in the data'''

#------
## Original
#------

print(ord_degree)
# ['Bachelors', 'Masters', 'PhD', 'Bachelors', 'PhD', 'Masters', 'Bachelors', 'AscProf']
# Categories (5, object): ['Bachelors' < 'Masters' < 'PhD' < 'AscProf' < 'PostDoc']

#------
## dr.lvls_expand()
#------

expanded_degree = dr.lvls_expand(
    ord_degree,
    new_levels=["Bachelors", "Masters", "PhD", "AscProf", "PostDoc", "Professor"]
)

print(expanded_degree)
# ['Bachelors', 'Masters', 'PhD', 'Bachelors', 'PhD', 'Masters', 'Bachelors', 'AscProf']
# Categories (6, object): ['Bachelors' < 'Masters' < 'PhD' < 'AscProf' < 'PostDoc' < 'Professor']


#------------------------------------------------------------------------------------------------------------#
#--------------------------- 10. Apply to processing pipelines with dr.mutate() -----------------------------#
#------------------------------------------------------------------------------------------------------------#

tb_pokemon = dr.tibble(
    pd.read_csv("05_Pandas_DataR_dataframe/data/pokemon.csv")
    >> dr.rename_with(lambda col: col.strip().replace(" ", "_").replace(".", "")) # Clean column names
    >> dr.select(f.Name, f.Type_1, f.Type_2, f.Speed, f.Generation, f.Legendary)
    >> dr.mutate(
        Type_1 = f.Type_1.astype("category"),      # convert to category (pandas style)
        Type_2 = dr.as_factor(f.Type_2),           # convert to category (datar style)
        Generation = dr.as_ordered(f.Generation),  # convert to ordered category (datar style)
        Legendary = dr.as_logical(f.Legendary)     # convert to boolean (datar style)
    )
)

print(
    tb_pokemon
    >> dr.slice_head(n=5)
)
#                     Name     Type_1     Type_2   Speed Generation  Legendary
#                 <object> <category> <category> <int64> <category>     <bool>
# 0              Bulbasaur      Grass     Poison      45          1      False
# 1                Ivysaur      Grass     Poison      60          1      False
# 2               Venusaur      Grass     Poison      80          1      False
# 3  VenusaurMega Venusaur      Grass     Poison      80          1      False
# 4             Charmander       Fire        NaN      65          1      False