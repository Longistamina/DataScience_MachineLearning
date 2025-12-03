'''
The pandas.Series.str accessor provides vectorized string operations 
for Series and Index objects containing string data. 

It's one of pandas' most powerful features for text processing, 
offering over 50 methods that mirror Python's built-in string methods 
while handling missing values automatically and operating efficiently on entire Series at once.


Flow of contents:

0. pandas.Series.str accessor: "lazy" transform to string type

1. Slicing and Indexing:
   - .slice(start, stop, step)
   - .slice_replace(start, stop, repl)
   - .get(index)

2. Basic Transformations:
   - Case transformations: .lower(), .upper(), .title(), .capitalize(), .swapcase()
   - Information retrieval: .len(), .count(pattern)
   - Stripping: .strip(), .lstrip(), .rstrip()

3. Checking methods (Boolean returns):
   - Character type checks: .isalpha(), .isdigit(), .isnumeric(), .isdecimal(), .isalnum(), .isspace()
   - Case checks: .isupper(), .islower(), .istitle()
   - Pattern checks: .startswith(prefix), .endswith(suffix), .contains(pattern)

4. Split and Partion:
   - Spliting: .split(delimiter), .rsplit(delimiter)
   - SPLIT INDEXING:.str.split()[i], .str.split().str[i]
   - Partioning: .partition(separator), .rpartition(separator)
   
5. Joinning: .join(delimiter)

6. Replacement, Removal, Repeat, Wrap:
   - .replace(pat, repl)
   - .removeprefix(prefix)
   - .removesuffix(suffix)
   - .repeat(n)
   - .wrap(width)

7. RegEx, Matching, Finding, Extracting:
   - Matching: .match(pattern), .fullmatch(pattern), .contains(pattern, regex=True)
   - Finding: .find(pattern), .rfind(pattern), .findall(pattern), .index(pattern), .rindex(pattern)
   - Extracting: .extract(pattern), .extractall(pattern)

8. Concatenation: .cat(others=None, sep='', na_rep=None)

9. Padding and Alignment:
   - Padding: .pad(width, side='left', fillchar=' ')
   - Alignment: .ljust(), .rjust(), .center()
   - Zero-fill: .zfill(width)

10. Categorical Encoding: pd.factorize(), pd.get_dummies()

11. Unicode and Encoding:
    - .normalize(form='NFC')
    - .encode(encoding='utf-8', errors='strict')
    - .decode(encoding='utf-8', errors='strict')

12. Real applications:
    - Data cleaning
    - Email processing
'''

import pandas as pd
import numpy as np

#--------------------------------------------------------------------------------------------------------#
#----------------------------------- 0. pandas.Series.str accessor --------------------------------------#
#--------------------------------------------------------------------------------------------------------#

'''
The pandas.Series.str accessor provides a convenient way to apply string manipulation methods 
to each element of a Pandas Series containing string data.

 It acts as a specialized namespace, allowing you to use methods that are similar to Python's built-in string methods 
 (like lower(), upper(), contains(), split(), replace(), etc.) directly on the Series.
'''

#############################
## With string-type series ##
#############################

s = pd.Series(['hello', 'world'])

print(s.upper())
'''AttributeError: 'Series' object has no attribute 'upper'''

print(s.str.upper())
# 0    HELLO
# 1    WORLD
# dtype: object


#######################################################
## With numeric series, must convert to string first ##
#######################################################

s_nums = pd.Series([1, 2, 3, np.nan, 5])

print(s_nums.astype(str))
# 0    1.0
# 1    2.0
# 2    3.0
# 3    nan
# 4    5.0
# dtype: object

'''
NOTE: After using .astype(str), all the numeric values have the format with a decimal point (e.g., '1.0', '2.0', etc.),
      and the NaN value is represented as the string 'nan'.
'''

print(s_nums.astype(str).str.fullmatch(r"\d+\.\d+"))
# 0     True
# 1     True
# 2     True
# 3    False
# 4     True
# dtype: bool


#---------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. Slicing and Indexing -----------------------------------------#
#---------------------------------------------------------------------------------------------------------#

s_heroes = pd.Series(
    data = ["Tony_Stark", "Steve_Rogers", "Bruce_Banner", "Pietro_Maximoff"],
    index = ["Ironman", "CaptainAmerica", "Hulk", "Quicksilver"]
)

#####################
## .slice() method ##
#####################

'''
.str.slice(start=None, stop=None, step=None)
'''

print(s_heroes.str.slice(start = 0, stop = 4, step = 1))
# Ironman           Tony
# CaptainAmerica    Stev
# Hulk              Bruc
# Quicksilver       Piet
# dtype: object

print(s_heroes.str.slice(start = 5))
# Ironman                 Stark
# CaptainAmerica        _Rogers
# Hulk                  _Banner
# Quicksilver        o_Maximoff
# dtype: object

print(s_heroes.str.slice(stop = 3))
# Ironman           Ton
# CaptainAmerica    Ste
# Hulk              Bru
# Quicksilver       Pie
# dtype: object

print(s_heroes.str.slice(step = 2))
# Ironman              Tn_tr
# CaptainAmerica      SeeRgr
# Hulk                BueBne
# Quicksilver       Per_aiof
# dtype: object


#############################
## .slice_replace() method ##
#############################

'''
.str.slice_replace(start=None, stop=None, repl=None)
'''

print(s_heroes.str.slice_replace(start = 0, stop = 4, repl = "Dr"))
# Ironman                Dr_Stark
# CaptainAmerica       Dre_Rogers
# Hulk                 Dre_Banner
# Quicksilver       Drro_Maximoff
# dtype: object


###################
## .get() method ##
###################

'''
.str.get(i) (works like .str[i] but handles out-of-bounds gracefully)
'''

print(s_heroes.str.get(0))
# Ironman           T
# CaptainAmerica    S
# Hulk              B
# Quicksilver       P
# dtype: object

print(s_heroes.str.get(-2))
# Ironman           r
# CaptainAmerica    r
# Hulk              e
# Quicksilver       f
# dtype: object

print(s_heroes.str.get(20))  # Out-of-bounds
# Ironman          NaN
# CaptainAmerica   NaN
# Hulk             NaN
# Quicksilver      NaN
# dtype: float64

#----------
## With dictionary-type series
#----------

s_ff4_dict = pd.Series(
    data = [
         {"name": "Reed_Richards", "code": "MrFantastic"},
         {"name": "Johnny_Storm", "code": "HumanTorch"},
         {"name": "Susan_Storm", "code": "InvisibleWoman"},
         {"name": "Ben_Grimm", "code": "TheThing"}
    ],
    name = "Fantastic Four"
)

print(s_ff4_dict)
# 0     {'name': 'Reed_Richards', 'code': 'MrFantastic'}
# 1       {'name': 'Johnny_Storm', 'code': 'HumanTorch'}
# 2    {'name': 'Susan_Storm', 'code': 'InvisibleWoman'}
# 3            {'name': 'Ben_Grimm', 'code': 'TheThing'}
# Name: Fantastic Four, dtype: object

print(s_ff4_dict.str.get("name"))
# 0    Reed_Richards
# 1     Johnny_Storm
# 2      Susan_Storm
# 3        Ben_Grimm
# Name: Fantastic Four, dtype: object

print(s_ff4_dict.str.get("code"))
# 0       MrFantastic
# 1        HumanTorch
# 2    InvisibleWoman
# 3          TheThing
# Name: Fantastic Four, dtype: object


#---------------------------------------------------------------------------------------------------------#
#------------------------------------- 2. Basic Transformations ------------------------------------------#
#---------------------------------------------------------------------------------------------------------#

##########################
## Case transformations ##
##########################

s_mixed = pd.Series(['Hello World', 'pandas is FUN', 'Data Science 101'])

#-----------
## .lower()
#-----------

print(s_mixed.str.lower())
# 0         hello world
# 1       pandas is fun
# 2    data science 101
# dtype: object

#-----------
## .upper()
#-----------

print(s_mixed.str.upper())
# 0         HELLO WORLD
# 1       PANDAS IS FUN
# 2    DATA SCIENCE 101
# dtype: object

#-----------
## .title()
#-----------

print(s_mixed.str.title())
# 0         Hello World
# 1       Pandas Is Fun
# 2    Data Science 101
# dtype: object

#--------------
## .capitalize()
#--------------

print(s_mixed.str.capitalize())
# 0         Hello world
# 1       Pandas is fun
# 2    Data science 101
# dtype: object

#--------------
## .swapcase()
#--------------

print(s_mixed.str.swapcase())
# 0         hELLO wORLD
# 1       PANDAS IS fun
# 2    dATA sCIENCE 101
# dtype: object

'''Swap case means converting uppercase letters to lowercase and vice versa.'''


###########################
## Information retrieval ##
###########################

#-----------
## .len()
#-----------

print(s_mixed.str.len())
# 0    11
# 1    13
# 2    16
# dtype: int64

#--------------
## .count(pattern)
#--------------

print(s_mixed.str.count('a'))
# 0    0
# 1    2
# 2    2
# dtype: int64

print(s_mixed.str.count(r'\d'))  # Count digits
# 0    0
# 1    0
# 2    3
# dtype: int64


######################
##     Stripping    ##
######################

s_spaced = pd.Series(['  hello  ', '  pandas  ', '  data science  '])

#-----------
## .strip()
#-----------
# Remove leading and trailing whitespace

print(s_spaced.str.strip())
# 0           hello
# 1          pandas
# 2    data science
# dtype: object

print(s_spaced.str.strip().to_list())
# ['hello', 'pandas', 'data science']

#------------
## .lstrip()
#------------
# Remove leading whitespace only

print(s_spaced.str.lstrip().to_list())
# ['hello  ', 'pandas  ', 'data science  ']

#------------
## .rstrip()
#------------
# Remove trailing whitespace only

print(s_spaced.str.rstrip().to_list())
# ['  hello', '  pandas', '  data science']


#---------------------------------------------------------------------------------------------------------#
#---------------------------------------- 3. Checking methods --------------------------------------------#
#---------------------------------------------------------------------------------------------------------#

###########################
## Character type checks ##
###########################

s_check = pd.Series(['Hello', 'WORLD', '123', '225.2', '⅕', '³', 'Hello123', '   ', ''])

#-----------
## .isalpha()
#-----------
# Check if all characters are alphabetic

print(s_check.str.isalpha())
# 0     True ('Hello')
# 1     True ('WORLD')
# 2    False
# 3    False
# 4     True
# 5    False
# 6    False
# 7    False
# 8    False
# dtype: bool

#-----------
## .isdigit()
#-----------
# Check if all characters are digits

print(s_check.str.isdigit())
# 0    False
# 1    False
# 2     True ('123')
# 3    False
# 4    False
# 5    True ('³')
# 6    False
# 7    False
# 8    False
# dtype: bool

#-----------
## .isnumeric()
#-----------
# Check if all characters are numeric (includes digits and numeric characters like fractions)

print(s_check.str.isnumeric())
# 0    False
# 1    False
# 2     True ('123')
# 3    False
# 4     True ('⅕')
# 5     True ('³')
# 6    False
# 7    False
# 8    False
# dtype: bool

#-----------
## .isdecimal()
#-----------
# Checks for characters used to form numbers in base 10

print(s_check.str.isdecimal())
# 0    False
# 1    False
# 2     True ('123')
# 3    False
# 4    False
# 5    False
# 6    False
# 7    False
# 8    False
# dtype: bool

#-----------
## .isalnum()
#-----------
# Check if all characters are alphanumeric (letters and numbers)

print(s_check.str.isalnum())
# 0     True ('Hello')
# 1     True ('WORLD')
# 2     True ('123')
# 3    False 
# 4     True ('⅕')
# 5     True ('³')
# 6     True ('Hello123')
# 7    False
# 8    False
# dtype: bool

#-----------
## .isspace()
#-----------
# Check if all characters are whitespace

print(s_check.str.isspace())
# 0    False
# 1    False
# 2    False
# 3    False
# 4    False
# 5    False
# 6    False
# 7     True ('   ')
# 8    False
# dtype: bool


#####################
##   Case checks   ##
#####################

s_check = pd.Series(['Hello', 'WORLD', 'Hello World', 'hello123', '   ', ''])

#-----------
## .isupper()
#-----------
# Check if all characters are uppercase

print(s_check.str.isupper())
# 0    False
# 1     True ('WORLD')
# 2    False
# 3    False
# 4    False
# 5    False
# dtype: bool

#-----------
## .islower()
#-----------
# Check if all characters are lowercase

print(s_check.str.islower())
# 0    False
# 1    False
# 2    False
# 3     True ('hello123')
# 4    False
# 5    False
# dtype: bool

#-----------
## .istitle()
#-----------
# Check if the string is titlecased (first letter of each word is uppercase)

print(s_check.str.istitle())
# 0     True ('Hello')
# 1    False
# 2     True  ('Hello World')
# 3    False
# 4    False
# 5    False
# dtype: bool


############################
##     Pattern checks     ##
############################

#-----------
## .startswith(prefix)
#-----------
# Check if strings start with the specified prefix

s_start = s = pd.Series(['bat', 'Bear', 'cat', np.nan])

print(s_start.str.startswith('b'))
# 0     True ('bat')
# 1    False
# 2    False
# 3      NaN
# dtype: object

print(s_start.str.startswith(pat = ('b', 'B'), na = False)) # Treat NaN as False
# 0     True
# 1     True
# 2    False
# 3    False
# dtype: bool

#-----------
## .endswith(suffix)
#-----------
# Check if strings end with the specified suffix

s_end = pd.Series(['bat', 'bear', 'caT', np.nan])

print(s_end.str.endswith('t'))
# 0     True ('bat')
# 1    False
# 2    False
# 3      NaN
# dtype: object

print(s_end.str.endswith(pat = ('t', 'T'), na = False)) # Treat NaN as False
# 0     True ('bat')
# 1    False 
# 2     True ('caT')
# 3    False
# dtype: bool

#-----------
## .contains(pattern)
#-----------
# Check if strings contain the specified pattern (can be a substring or regex)

s_contain = pd.Series(['Mouse', 'dog', 'house and parrot', '23', np.nan])

print(s_contain.str.contains(pat = 'og', regex = False))
# 0    False
# 1     True ('dog')
# 2    False
# 3    False
# 4      NaN
# dtype: object

print(s_contain.str.contains(pat = 'oG', regex = False))
# 0    False
# 1    False
# 2    False
# 3    False
# 4      NaN
# dtype: object

print(s_contain.str.contains(pat = 'oG', case = False, regex = False, na = False)) # Case insensitive, Treat NaN as False
# 0    False
# 1     True ('dog')
# 2    False
# 3    False
# 4    False
# dtype: bool

print(s_contain.str.contains(pat = r"\d|parrot|Mo", regex = True, na = False)) # Regex pattern, Treat NaN as False
# 0     True ('Mouse' contains 'Mo')
# 1    False
# 2     True ('house and parrot' contains 'parrot')
# 3     True ('23' contains digit '\d')
# 4    False
# dtype: bool


#---------------------------------------------------------------------------------------------------------#
#--------------------------------------- 4. Split and Partion --------------------------------------------#
#---------------------------------------------------------------------------------------------------------#

#######################
##     Splitting     ##
#######################

s_split = pd.Series(['apple_banana_cherry', 'dog_cat', 'one_two_three_four', np.nan])

#-----------
## .split(delimiter)
#-----------
# Split strings by the specified delimiter
# By default, pat='\s+' (whitespace) and n=-1 (all occurrences)

print(s_split.str.split('_'))
# 0    [apple, banana, cherry]
# 1                 [dog, cat]
# 2    [one, two, three, four]
# 3                        NaN
# dtype: object

print(s_split.str.split(pat = '_', n = 2))  # Split up to 2 delimiters only (results in at most 3 parts)
# 0    [apple, banana, cherry]
# 1                 [dog, cat]
# 2     [one, two, three_four]
# 3                        NaN
# dtype: object

print(s_split.str.split(pat = '_', expand= True))  # Expand into separate columns
#        0       1       2     3
# 0  apple  banana  cherry  None
# 1    dog     cat    None  None
# 2    one     two   three  four
# 3    NaN     NaN     NaN   NaN

#------------
## .rsplit(delimiter)
#------------
# Split strings by the specified delimiter from the right
# By default, pat='\s+' (whitespace) and n=-1 (all occurrences)

print(s_split.str.rsplit('_'))
# 0    [apple, banana, cherry]
# 1                 [dog, cat]
# 2    [one, two, three, four]
# 3                        NaN
# dtype: object

print(s_split.str.rsplit(pat = '_', n = 2))  # Split up to 2 delimiters only from the right (results in at most 3 parts)
# 0    [apple, banana, cherry]
# 1                 [dog, cat]
# 2     [one_two, three, four]
# 3                        NaN
# dtype: object

'''
.str.split() => [one, two, three_four]
.str.rsplit() => [one_two, three, four]
'''

print(s_split.str.rsplit(pat = '_', n = 2, expand= True))  # Expand into separate columns
#          0       1       2
# 0    apple  banana  cherry
# 1      dog     cat    None
# 2  one_two   three    four
# 3      NaN     NaN     NaN

############################
##     SPLIT INDEXING     ##
############################

s_split = pd.Series(['day1_sample1', 'day1_sample2', 'day1_sample3', 'day2_sample4', 'day2_sample5', np.nan])

print(s_split.str.split('_'))
# 0    [day1, sample1]
# 1    [day1, sample2]
# 2    [day1, sample3]
# 3    [day2, sample4]
# 4    [day2, sample5]
# 5                NaN
# dtype: object

print(s_split.str.split('_')[0]) # ['day1', 'sample1']
print(s_split.str.split('_')[3]) # ['day2', 'sample4']
print(s_split.str.split('_')[5]) # nan

'''------------------------'''

print(s_split.str.split(pat = '_', expand= True))  # Expand into separate columns
#       0        1
# 0  day1  sample1
# 1  day1  sample2
# 2  day1  sample3
# 3  day2  sample4
# 4  day2  sample5
# 5   NaN      NaN

print(s_split.str.split('_').str[1])
# 0    sample1
# 1    sample2
# 2    sample3
# 3    sample4
# 4    sample5
# 5        NaN
# dtype: object

print(s_split.str.split('_').str[0].unique())
# ['day1' 'day2' nan]

#########################
##     Partioning      ##
#########################

s_partition = pd.Series(['apple-banana-cherry', 'dog-cat', 'one-two-three-four', np.nan])

#--------------
## .partition(separator)
#--------------
# Split strings at the first occurrence of the specified separator
# By default, sep=' ' (whitespace)

print(s_partition.str.partition('-'))
#        0    1               2
# 0  apple    -   banana-cherry
# 1    dog    -             cat
# 2    one    -  two-three-four
# 3    NaN  NaN             NaN

print(s_partition.str.partition(sep = 'a'))  # Split at first 'a'
#                     0    1                   2
# 0                        a  pple-banana-cherry
# 1               dog-c    a                   t
# 2  one-two-three-four                         
# 3                 NaN  NaN                 NaN

print(s_partition.str.partition(sep = '-', expand = False)) # Return as tuples, not expanded DataFrame
# 0    (apple, -, banana-cherry)
# 1                (dog, -, cat)
# 2     (one, -, two-three-four)
# 3                          NaN
# dtype: object

#----------------
## .rpartition(separator)
#----------------
# Split strings at the last occurrence of the specified separator
# By default, sep=' ' (whitespace)

print(s_partition.str.rpartition('-'))
#                0    1       2
# 0   apple-banana    -  cherry
# 1            dog    -     cat
# 2  one-two-three    -    four
# 3            NaN  NaN     NaN

print(s_partition.str.rpartition(sep = 'a'))  # Split at last 'a'
#              0    1                   2
# 0  apple-banan    a             -cherry
# 1        dog-c    a                   t
# 2                    one-two-three-four
# 3          NaN  NaN                 NaN

print(s_partition.str.rpartition(sep = '-', expand = False)) # Return as tuples, not expanded DataFrame
# 0    (apple-banana, -, cherry)
# 1                (dog, -, cat)
# 2     (one-two-three, -, four)
# 3                          NaN
# dtype: object


#---------------------------------------------------------------------------------------------------------#
#------------------------------------------ 5. Joinning --------------------------------------------------#
#---------------------------------------------------------------------------------------------------------#

'''
join(separator) - Join list elements with separator
'''

s_join = pd.Series([['apple', 'banana', 'cherry'], ['dog', 'cat'], ['one', 'two', 'three', 'four'], np.nan])

print(s_join.str.join('-'))
# 0    apple-banana-cherry
# 1                dog-cat
# 2     one-two-three-four
# 3                    NaN
# dtype: object

print(s_join.str.join(sep = ' || '))
# 0      apple || banana || cherry
# 1                     dog || cat
# 2    one || two || three || four
# 3                            NaN
# dtype: object


#---------------------------------------------------------------------------------------------------------#
#-------------------------------- 6. Replacement, Removal, Repeat, Wrap ----------------------------------#
#---------------------------------------------------------------------------------------------------------#

#########################
## .replace(pat, repl) ##
#########################

s_replace = pd.Series(['apple_banana_cherry', 'dog_cat', 'one_two_three_four', '1234', np.nan])

print(s_replace.str.replace(pat = 'a', repl = 'A', regex = False))  # Replace all 'a' with 'A'
# 0    Apple_bAnAnA_cherry
# 1                dog_cAt
# 2     one_two_three_four
# 3                   1234
# 4                    NaN
# dtype: object

print(s_replace.str.replace("_", ' || ', regex = False))  # Replace all '_' with ' || '
# 0      apple || banana || cherry
# 1                     dog || cat
# 2    one || two || three || four
# 3                           1234
# 4                            NaN
# dtype: object

print(s_replace.str.replace(pat = r'\d', repl = '#', regex = True))  # Replace all digits with '#'
# 0    apple_banana_cherry
# 1                dog_cat
# 2     one_two_three_four
# 3                   ####
# 4                    NaN
# dtype: object

print(s_replace.str.replace(pat = r'\d+', repl = '#', regex = True))  # Replace all digit sequences with '#'
# 0    apple_banana_cherry
# 1                dog_cat
# 2     one_two_three_four
# 3                      #
# 4                    NaN
# dtype: object


###########################
## .removeprefix(prefix) ##
###########################

s_prefix = pd.Series(['pre_apple', 'pre_banana', 'cat', np.nan])

print(s_prefix.str.removeprefix('pre_'))  # Remove 'pre_' if it exists at the start
# 0     apple
# 1    banana
# 2       cat
# 3       NaN
# dtype: object


###########################
## .removesuffix(suffix) ##
###########################

s_suffix = pd.Series(['apple_suf', 'banana_suf', 'dog', np.nan])

print(s_suffix.str.removesuffix('_suf'))  # Remove '_suf' if it exists at the end
# 0     apple
# 1    banana
# 2       dog
# 3       NaN
# dtype: object


################
## .repeat(n) ##
################

s_repeat = pd.Series(['ha', 'ho', 'he', np.nan])

print(s_repeat.str.repeat(3))  # Repeat each string 3 times
# 0    hahaha
# 1    hohoho
# 2    hehehe
# 3       NaN
# dtype: object


##################
## .wrap(width) ##
##################

s_wrap = pd.Series(['This is a long string that needs to be wrapped.', 'Short string', np.nan])

print(s_wrap.str.wrap(10))  # Wrap text to a width of 10 characters
# 0    This is a\nlong\nstring\nthat needs\nto be\nwr...
# 1                                        Short\nstring
# 2                                                  NaN
# dtype: object

print(s_wrap.str.wrap(width = 10).get(0))
# This is a
# long
# string
# that needs
# to be
# wrapped.


#---------------------------------------------------------------------------------------------------------#
#------------------------------- 7. RegEx, Matching, Finding, Extracting ---------------------------------#
#---------------------------------------------------------------------------------------------------------#

##########################################
##               Matching               ##
##########################################

s_match = pd.Series(['abc123', 'def456', 'ghi789', '123abc', np.nan])

#-----------
## .match(pattern)
#-----------
# Check if the BEGINNING of each string matches the regex pattern

print(s_match.str.match(r'^[a-z]{3}'))  # Starts with exactly 3 lowercase letters
# 0     True
# 1     True
# 2     True
# 3    False ('123abc' starts with digits)
# 4      NaN
# dtype: object

print(s_match.str.match(r'^[a-z]{3}', na = False))  # Treat NaN as False
# 0     True
# 1     True
# 2     True
# 3    False ('123abc' starts with digits)
# 4    False (NaN treated as False)
# dtype: bool

#-------------------
## .fullmatch(pattern)
#-------------------
# Check if the ENTIRE string matches the regex pattern

print(s_match.str.fullmatch(r'[a-z]{3}\d{3}'))  # Exactly 3 lowercase letters followed by exactly 3 digits
# 0     True
# 1     True
# 2     True
# 3    False ('123abc' does not match the pattern)
# 4      NaN
# dtype: object

print(s_match.str.fullmatch(r"\d{3}.*", na = False))  # Treat NaN as False, check if string starts with exactly 3 digits
# 0    False
# 1    False
# 2    False
# 3     True (only '123abc' starts with 3 digits hence matches the pattern)
# 4    False (NaN treated as False)
# dtype: bool

#-------------------
## .contains(pattern, regex=True)
#-------------------
# Check if each string contains the regex pattern

print(s_match.str.contains(r'\d{3}', regex = True, na = False))  # Contains a sequence of exactly 3 digits
# 0    True ('abc123' contains digits '123')
# 1    True ('def456' contains digits '456')
# 2    True ('ghi789' contains digits '789')
# 3    True ('123abc' contains digits '123')
# 4   False (NaN treated as False)
# dtype: object


#########################################
##               Finding               ##
#########################################

s_find = pd.Series(["cow_", "duck_", "do_v_e", "abcxyz", np.nan])
s_index = pd.Series(["cow_", "duck_", "do_v_e"])

#-----------
## .find(pattern)
#-----------
# Find the first occurrence of the substring pattern and return its LOWEST index

print(s_find.str.find('_'))  # Find the first occurrence of '_'
# 0    3.0 ('cow_' has '_' at index 3 as the lowest)
# 1    4.0 
# 2    2.0 ('do_v_e' has '_' at index 2 as the lowest)
# 3   -1.0 ('abcxyz' does not contain '_', returns -1)
# 4    NaN
# dtype: float64

#-----------
## .rfind(pattern)
#-----------
# Find the last occurrence of the substring pattern and return its HIGHEST index

print(s_find.str.rfind('_'))  # Find the last occurrence of '_'
# 0    3.0
# 1    4.0
# 2    4.0 ('do_v_e' has '_' at index 4 as the highest)
# 3   -1.0
# 4    NaN
# dtype: float64

#-----------
## .findall(pattern)
#-----------
# Find all occurrences of the regex pattern and return them as a list

print(s_find.str.findall(r'[a-z]{2}'))  # Find all occurrences of exactly 2 lowercase letters
# 0            [co]
# 1        [du, ck]
# 2            [do]
# 3    [ab, cx, yz]
# 4             NaN
# dtype: object

#-----------
## .index(pattern)
#-----------
# Find the first occurrence of the substring pattern and return its LOWEST index
# Raises ValueError if the pattern is not found (or encounters NaN)

print(s_find.str.index(sub = '_'))
"""Raise  ValueError because s_find contains NaN and 'abcxyz' which does not contain '_' """

print(s_index.str.index(sub = '_'))  # Find the first occurrence of '_' in s_index
# 0    3 
# 1    4
# 2    2 ('do_v_e' has '_' at index 2 as the lowest)
# dtype: int64

#-----------
## .rindex(pattern)
#-----------
# Find the last occurrence of the substring pattern and return its HIGHEST index
# Raises ValueError if the pattern is not found (or encounters NaN)

print(s_index.str.rindex(sub = '_'))  # Find the last occurrence of '_' in s_index
# 0    3
# 1    4
# 2    4 ('do_v_e' has '_' at index 4 as the highest)
# dtype: int64


##########################################
##              Extracting              ##
##########################################

#-----------
## .extract(pattern)
#-----------
# Extract capture groups from the first match of the regex pattern
# By default, expand=True (returns DataFrame)

s_extract = pd.Series(['a1', 'b2', 'c3'])


print(s_extract.str.extract(r'[ab](\d)')) # Returns only one group (the digit after 'a' or 'b')
#      0                                  # This is a DATAFRAME since expand=True by default
# 0    1
# 1    2
# 2  NaN ('c3' does not starts with 'a' or 'b', hence no match)
'''A pattern with one group will return a DataFrame with one column if expand=True (default).'''

print(s_extract.str.extract(r'[ab](\d)', expand = False)) # Returns only one group (the digit after 'a' or 'b')
# 0      1                                                # This is a SERIES since expand=False
# 1      2
# 2    NaN
# dtype: object
'''A pattern with one group will return a Series if expand=False.'''

print(s_extract.str.extract(r'([ab])(\d)'))  # Returns two groups (the letter and the digit)
#      0    1
# 0    a    1
# 1    b    2
# 2  NaN  NaN

print(s_extract.str.extract(r'([ab])?(\d)'))  # Make the first group optional
#      0  1
# 0    a  1
# 1    b  2
# 2  NaN  3 (the digit '3' is extracted, but no letter before it)

#-----------
## .extractall(pattern)
#-----------
# Extract all capture groups from all matches of the regex pattern
# By default, expand=True (returns DataFrame)

s_extall = pd.Series(["a2a4", "b63", "ccc"], index=["A", "B", "C"])

print(s_extall.str.extractall(r'[ab](\d)'))  # Extract all occurrences of letter-digit pairs with one group
#          0
#   match   
# A 0      2 (match 0: 'a2')
#   1      4 (match 1: 'a4')
# B 0      6 (match 0: 'b6')
'''
The "3" in "b63" is not extracted because it is not preceded by 'a' or 'b'.
The "ccc" in index "C" does not contain 'a' or 'b' or any digits '\d', so no matches are found there.
'''

print(s_extall.str.extractall(r'([ab])(\d)'))  # Extract all occurrences of letter-digit pairs with two groups
#          0  1
#   match      
# A 0      a  2 (match 0: 'a2')
#   1      a  4 (match 1: 'a4')
# B 0      b  6 (match 0: 'b6')


#---------------------------------------------------------------------------------------------------------#
#----------------------------------------- 8. Concatenation ----------------------------------------------#
#---------------------------------------------------------------------------------------------------------#

'''
.str.cat(others=None, sep='', na_rep=None)

Without others: concatenates all values in Series
With others: element-wise concatenation
Supports multiple Series and alignment

=> Returns a single concatenated string if others is None
=> Returns a Series of concatenated strings if others is provided
'''

s1 = pd.Series(['a', 'b', 'c'])
s2 = pd.Series(['1', '2', '3'])

# Without others, concatenates s1 with itself with no separator
print(s1.str.cat()) # 'abc'

# Without others, concatenates s1 with '-' as separator
print(s1.str.cat(sep='-')) # 'a-b-c'

# With others=s2, concatenates s1 and s2 element-wise with no separator
print(s1.str.cat(s2))
# 0    a1
# 1    b2
# 2    c3
# dtype: object

# With others=s2, concatenates s1 and s2 element-wise with '_' as separator
print(s1.str.cat(s2, sep='_'))
# 0    a_1
# 1    b_2
# 2    c_3
# dtype: object


#---------------------------------------------------------------------------------------------------------#
#-------------------------------------- 9. Padding and Alignment -----------------------------------------#
#---------------------------------------------------------------------------------------------------------#

#################################
## .pad(width, side, fillchar) ##
#################################

s_pad = pd.Series(['cat', 'elephant', 'dog'])

print(s_pad.str.pad(width = 10)) # Default side='left', fillchar=' ' (space)
# 0           cat
# 1      elephant
# 2           dog
# dtype: object

print(s_pad.str.pad(width = 10, side = 'right', fillchar = '*'))
# 0    cat******* (added 7 '*' to the right to make length 10)
# 1    elephant**
# 2    dog*******
# dtype: object

print(s_pad.str.pad(width = 10, side = 'both', fillchar = '-'))
# 0    ---cat----
# 1    -elephant- (added 1 '-' to the left and 1 '-' to the right to make length 10)
# 2    ---dog----
# dtype: object

print(s_pad.str.pad(width = 5, side = 'left', fillchar = '_'))
# 0       __cat  (added 2 '_' to the left to make length 5)
# 1    elephant (no padding needed)
# 2       __dog
# dtype: object


#######################################
##             Alignment             ##
#######################################

s_align = pd.Series(['dog', 'bird', 'mouse'])

#-----------
## .ljust(width, fillchar)
#-----------
# Left-align strings, padding on the right

print(s_align.str.ljust(width = 8, fillchar = '.')) # Default fillchar=' ' (space)
# 0    dog.....
# 1    bird....
# 2    mouse...
# dtype: object

#-----------
## .rjust(width, fillchar)
#-----------
# Right-align strings, padding on the left

print(s_align.str.rjust(width = 8, fillchar = '.')) # Default fillchar=' ' (space)
# 0    .....dog
# 1    ....bird
# 2    ...mouse
# dtype: object

#-----------
## .center(width, fillchar)
#-----------
# Center-align strings, padding on both sides

print(s_align.str.center(width = 8, fillchar = '.')) # Default fillchar=' ' (space)
# 0    ..dog...
# 1    ..bird..
# 2    .mouse..
# dtype: object


#---------------------------------------------------------------------------------------------------------#
#-------------------------------------- 10. Categorical Encoding -----------------------------------------#
#---------------------------------------------------------------------------------------------------------#

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


#---------------------------------------------------------------------------------------------------------#
#-------------------------------------- 11. Unicode and Decoding -----------------------------------------#
#---------------------------------------------------------------------------------------------------------#

s_raw = pd.Series(['café', 'naïve', 'résumé', 'coöperate', np.nan])

######################
## .normalize(form) ##
######################
# .normalize() standardizes Unicode strings to a consistent form.
# Common forms are 'NFC' (Normalization Form C) and 'NFD' (Normalization Form D).
# All the forms: {‘NFC’, ‘NFKC’, ‘NFD’, ‘NFKD’}

s_normalized = s_raw.str.normalize(form = 'NFC')  # Default form='NFC'
print(s_normalized)
# 0         café
# 1        naïve
# 2       résumé
# 3    coöperate
# 4          NaN
# dtype: object

s_normalized = s_raw.str.normalize(form = 'NFD')  # Decomposed form
print(s_normalized)
# 0         café
# 1        naïve
# 2      résumé
# 3    coöperate
# 4           NaN
# dtype: object


###############################
## .encode(encoding, errors) ##
###############################
# .encode() encodes strings to bytes using the specified encoding.
# Common encodings include 'utf-8', 'latin1', 'ascii', etc.
# The errors parameter specifies how to handle encoding errors: 'strict', 'ignore', 'replace', etc.

s_encoded = s_raw.str.encode(encoding = 'utf-8', errors = 'strict')  # Default errors='strict'
print(s_encoded)
# 0             b'caf\xc3\xa9'
# 1            b'na\xc3\xafve'
# 2    b'r\xc3\xa9sum\xc3\xa9'
# 3        b'co\xc3\xb6perate'
# 4                        NaN
# dtype: object

s_encoded = s_raw.str.encode(encoding = 'ascii', errors = 'ignore')  # Ignore non-ASCII characters
print(s_encoded)
# 0         b'caf'
# 1        b'nave'
# 2        b'rsum'
# 3    b'coperate'
# 4            NaN
# dtype: object


###############################
## .decode(encoding, errors) ##
###############################
# .decode() decodes bytes back to strings using the specified encoding.
# Common encodings include 'utf-8', 'latin1', 'ascii', etc.
# The errors parameter specifies how to handle decoding errors: 'strict', 'ignore', 'replace', etc.

s_coded = pd.Series([b'cow', b'123', b'()'])

s_decoded = s_coded.str.decode(encoding = 'ascii', errors = 'strict')  # Default errors='strict'
print(s_decoded)
# 0    cow
# 1    123
# 2     ()
# dtype: object


#---------------------------------------------------------------------------------------------------------#
#--------------------------------------- 12. Real applications -------------------------------------------#
#---------------------------------------------------------------------------------------------------------#

###################
## Data cleaning ##
###################

# Clean messy name data
messy_names = pd.Series(['  john doe  ', 'JANE SMITH', 'bob-johnson'])
clean_names = (messy_names
               .str.strip()
               .str.replace('-', ' ')
               .str.title()
               .str.replace(r'\s+', ' ', regex=True))

print(clean_names)
# 0       John Doe
# 1     Jane Smith
# 2    Bob Johnson
# dtype: object

######################
## Email processing ##
######################

emails = pd.Series(['user@example.com', 'ADMIN@SITE.ORG', 'invalid.email'])
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Validate and extract components
is_valid = emails.str.match(email_pattern)
domains = emails.str.extract(r'@([^.]+\..*)')
usernames = emails.str.extract(r'^([^@]+)@')

print(domains)
#              0
# 0  example.com
# 1     SITE.ORG
# 2          NaN

print(usernames)
#       0
# 0   user
# 1  ADMIN
# 2    NaN