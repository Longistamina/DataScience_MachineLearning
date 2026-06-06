'''
In Polars, filtering and conditional operations are handled differently than in pandas.
Pandas uses .where(), .mask(), and boolean indexing directly on Series.
Polars uses .filter() for subsetting, and pl.when().then().otherwise() for conditional replacement.

1. Boolean Filtering: .filter()
2. Multiple Value Filtering: .is_in()
3. Conditional Replacement (.where() equivalent): pl.when().then().otherwise()
4. Conditional Replacement (.mask() equivalent): pl.when().then().otherwise()
5. Null-Aware Filtering: .is_null(), .is_not_null(), .drop_nulls()
'''

import polars as pl


#---------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- Setup Data ----------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

s_nums = pl.Series("nums", [10, 20, 30, 40, 50])
s_with_nulls = pl.Series("vals", [10, None, 30, None, 50])
s_str = pl.Series("letters", ["a", "b", "c", "d", "e"])


#---------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 1. Boolean Filtering ------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#
'''
In pandas, you use s[s > 25].

In Polars, you CANNOT use that bracket notation, instead must use ``.filter()`` method.
-> Return a new Series containing only the elements where the condition is True.
'''

# .filter() method (Recommended, especially inside expressions)
print(s_nums.filter(s_nums > 25))
# shape: (3,)
# Series: 'nums' [i64]
# [
# 	30
# 	40
# 	50
# ]

# Combining multiple conditions (use & for AND, | for OR, ~ for NOT)
# NOTE: Parentheses are REQUIRED around each condition due to Python operator precedence.
print(s_nums.filter((s_nums > 15) & (s_nums < 45)))
# shape: (2,)
# Series: 'nums' [i64]
# [
# 	20
# 	30
# 	40
# ]


#---------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 2. Multiple Value Filtering -----------------------------------------#
#---------------------------------------------------------------------------------------------------------------#
'''
In pandas, you use s.isin([values]).
In Polars, the method is snake_case: .is_in([values]).
'''

print(s_nums.filter(s_nums.is_in([10, 30, 50])))
# shape: (3,)
# Series: 'nums' [i64]
# [
# 	10
# 	30
# 	50
# ]

# Negation: filter values NOT in the list
print(s_nums.filter(~s_nums.is_in([10, 30, 50])))
# shape: (2,)
# Series: 'nums' [i64]
# [
# 	20
# 	40
# ]


#---------------------------------------------------------------------------------------------------------------#
#---------------------------------- 3. Conditional Replacement (.where() eq.) ----------------------------------#
#---------------------------------------------------------------------------------------------------------------#
'''
Pandas: s.where(cond, other) -> KEEPS values where cond is True, REPLACES others with `other`.

Polars: Does NOT have a Series.where() method. Instead, use pl.when().then().otherwise().
Since pl.when() returns an Expression, we wrap it in pl.select() and convert back to a Series.
'''
# Keep values > 25, replace others with 0
s_when = pl.select(
    pl.when(s_nums > 25).then(s_nums).otherwise(0)
).to_series()

print(s_when)
# shape: (5,)
# Series: 'nums' [i64]
# [
# 	0
# 	0
# 	30
# 	40
# 	50
# ]

# You can also replace with another Series or a computed value
s_when_custom = pl.select(
    pl.when(s_nums > 25).then(s_nums).otherwise(s_nums * -1)
).to_series()

print(s_when_custom)
# shape: (5,)
# Series: 'nums' [i64]
# [
# 	-10
# 	-20
# 	30
# 	40
# 	50
# ]


#---------------------------------------------------------------------------------------------------------------#
#------------------------------------ 4. Conditional Replacement (.mask() eq.) ---------------------------------#
#---------------------------------------------------------------------------------------------------------------#
'''
Pandas: s.mask(cond, other) -> REPLACES values where cond is True, KEEPS others.

Polars: Simply swap the .then() and .otherwise() branches in pl.when().
'''
# Replace values > 25 with 999, keep others
s_mask_eq = pl.select(
    pl.when(s_nums > 25).then(999).otherwise(s_nums)
).to_series()

print(s_mask_eq)
# shape: (5,)
# Series: 'nums' [i64]
# [
# 	10
# 	20
# 	999
# 	999
# 	999
# ]


#---------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 5. Null-Aware Filtering ---------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#
'''
Polars handles nulls explicitly. You cannot use s == None or s != None.
Instead, use .is_null() and .is_not_null().
'''
# Filter out nulls (equivalent to pandas s.dropna() or s[s.notna()])
print(s_with_nulls.filter(s_with_nulls.is_not_null()))
# shape: (3,)
# Series: 'vals' [i64]
# [
# 	10
# 	30
# 	50
# ]

# Polars also has a direct .drop_nulls() method
print(s_with_nulls.drop_nulls())
# shape: (3,)
# Series: 'vals' [i64]
# [
# 	10
# 	30
# 	50
# ]

# Keep ONLY nulls
print(s_with_nulls.filter(s_with_nulls.is_null()))
# shape: (2,)
# Series: 'vals' [i64]
# [
# 	null
# 	null
# ]

# Conditional replacement with null handling
# Replace nulls with a default value (equivalent to pandas s.fillna(0))
s_filled = pl.select(
    pl.when(s_with_nulls.is_null()).then(0).otherwise(s_with_nulls)
).to_series()

print(s_filled)
# shape: (5,)
# Series: 'vals' [i64]
# [
# 	10
# 	0
# 	30
# 	0
# 	50
# ]
