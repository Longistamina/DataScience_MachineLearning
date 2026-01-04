'''
pandas has an options API configure and customize global behavior related to DataFrame display, 
data behavior and more.

#########################################

1. All available options: pd.describe_option()

2. Getting, Setting and Resetting options: 
   + Getting: pd.get_option() 
   + Setting: pd.set_option()
   + Resetting: pd.reset_option()

3. Setting startup options in Python/IPython environment

4. Frequently used options: max_rows, max_columns, display.width

5. Number formatting: pd.set_eng_float_format()

6. Unicode formatting

Detailed documentation: https://pandas.pydata.org/docs/user_guide/options.html#
'''

import pandas as pd

df_medals = pd.read_csv(
    filepath_or_buffer = "05_Pandas_DataR_dataframe/data/medals.csv",
    skiprows = 4
)

# Make all columns categorical
df_medals = df_medals.astype("category")

df_medals.head(3)
#    Year      City    Sport      Discipline  NOC       Event Event gender   Medal
# 0  1924  Chamonix  Skating  Figure skating  AUT  individual            M  Silver
# 1  1924  Chamonix  Skating  Figure skating  AUT  individual            W    Gold
# 2  1924  Chamonix  Skating  Figure skating  AUT       pairs            X    Gold

df_medals.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 2311 entries, 0 to 2310
# Data columns (total 8 columns):
#  #   Column        Non-Null Count  Dtype   
# ---  ------        --------------  -----   
#  0   Year          2311 non-null   category
#  1   City          2311 non-null   category
#  2   Sport         2311 non-null   category
#  3   Discipline    2311 non-null   category
#  4   NOC           2311 non-null   category
#  5   Event         2311 non-null   category
#  6   Event gender  2311 non-null   category
#  7   Medal         2311 non-null   category
# dtypes: category(8)
# memory usage: 24.8 KB


#-------------------------------------------------------------------------------------------------------#
#-------------------------------------- 1. All available options ---------------------------------------#
#-------------------------------------------------------------------------------------------------------#

'''
Use pd.describe_option() to see all available options in pandas.
'''

print(pd.describe_option())
# display.max_columns : int
#     If max_cols is exceeded, switch to truncate view. Depending on
#     `large_repr`, objects are either centrally truncated or printed as
#     a summary view. 'None' value means unlimited.

#     In case python/IPython is running in a terminal and `large_repr`
#     equals 'truncate' this can be set to 0 or None and pandas will auto-detect
#     the width of the terminal and print a truncated object which fits
#     the screen width. The IPython notebook, IPython qtconsole, or IDLE
#     do not run in a terminal and hence it is not possible to do
#     correct auto-detection and defaults to 20.
#     [default: 0] [currently: 0]
# display.max_colwidth : int or None
#     The maximum width in characters of a column in the repr of
#     a pandas data structure. When the column overflows, a "..."
#     placeholder is embedded in the output. A 'None' value means unlimited.
#     [default: 50] [currently: 50]
'''And more...'''


#-------------------------------------------------------------------------------------------------------#
#---------------------------- 2. Getting, Setting and Resetting options --------------------------------#
#-------------------------------------------------------------------------------------------------------#

#####################
## pd.get_option() ##
#####################
'''Use pd.get_option() to get the current value of a specific option.'''

print(pd.get_option("display.max_rows"))        # 60
print(pd.get_option("display.max_columns"))     # 0
print(pd.get_option("display.width"))           # 80
print(pd.get_option("display.precision"))       # 6
print(pd.get_option("mode.sim_interactive"))    # False

#####################
## pd.set_option() ##
#####################
'''Use pd.set_option() to set a specific option to a new value.'''

pd.get_option("display.max_rows") # 60

# Set new max_rows option
pd.set_option("display.max_rows", 30)

# Check the updated value
pd.get_option("display.max_rows") # 30

#######################
## pd.reset_option() ##
#######################
'''Use pd.reset_option() to reset a specific option to its default value.'''

print(pd.get_option("mode.sim_interactive"))    # False

pd.set_option("mode.sim_interactive", True)
print(pd.get_option("mode.sim_interactive"))    # True

# Reset to default value
pd.reset_option("mode.sim_interactive")

# Check the reset value
print(pd.get_option("mode.sim_interactive"))    # False


#-------------------------------------------------------------------------------------------------------#
#----------------------- 3. Setting startup options in Python/IPython environment ----------------------#
#-------------------------------------------------------------------------------------------------------#

'''
Pandas and Python support setting startup options via configuration files.
So that you don't have to set them manually every time you start a new session.

Check the tutorial here: 
https://pandas.pydata.org/docs/user_guide/options.html#setting-startup-options-in-python-ipython-environment
'''


#-------------------------------------------------------------------------------------------------------#
#------------------------------------- 4. Frequently used options --------------------------------------#
#-------------------------------------------------------------------------------------------------------#

###########################
##    max_rows option    ##
###########################

print(pd.get_option("display.max_rows"))    # 30

print(df_medals)
#       Year      City       Sport      Discipline  NOC            Event Event gender   Medal
# 0     1924  Chamonix     Skating  Figure skating  AUT       individual            M  Silver
# 1     1924  Chamonix     Skating  Figure skating  AUT       individual            W    Gold
# 2     1924  Chamonix     Skating  Figure skating  AUT            pairs            X    Gold
# 3     1924  Chamonix   Bobsleigh       Bobsleigh  BEL         four-man            M  Bronze
# 4     1924  Chamonix  Ice Hockey      Ice Hockey  CAN       ice hockey            M    Gold
# ...    ...       ...         ...             ...  ...              ...          ...     ...
# 2306  2006     Turin      Skiing       Snowboard  USA        Half-pipe            M  Silver
# 2307  2006     Turin      Skiing       Snowboard  USA        Half-pipe            W    Gold
# 2308  2006     Turin      Skiing       Snowboard  USA        Half-pipe            W  Silver
# 2309  2006     Turin      Skiing       Snowboard  USA  Snowboard Cross            M    Gold
# 2310  2006     Turin      Skiing       Snowboard  USA  Snowboard Cross            W  Silver

# [2311 rows x 8 columns]

#--------------------
## Change max_rows
#--------------------

pd.set_option("display.max_rows", 5)

print(df_medals)
#       Year      City    Sport      Discipline  NOC            Event Event gender   Medal
# 0     1924  Chamonix  Skating  Figure skating  AUT       individual            M  Silver
# 1     1924  Chamonix  Skating  Figure skating  AUT       individual            W    Gold
# ...    ...       ...      ...             ...  ...              ...          ...     ...
# 2309  2006     Turin   Skiing       Snowboard  USA  Snowboard Cross            M    Gold
# 2310  2006     Turin   Skiing       Snowboard  USA  Snowboard Cross            W  Silver

# [2311 rows x 8 columns]

pd.reset_option("display.max_rows") # Reset to default value

############################
##   max_columns option   ##
############################

print(pd.get_option("display.max_columns"))    # 0

pd.set_option("display.max_columns", 5)
print(df_medals)
#       Year      City  ... Event gender   Medal
# 0     1924  Chamonix  ...            M  Silver
# 1     1924  Chamonix  ...            W    Gold
# ...    ...       ...  ...          ...     ...
# 2309  2006     Turin  ...            M    Gold
# 2310  2006     Turin  ...            W  Silver

# [2311 rows x 8 columns]

pd.reset_option("display.max_columns") # Reset to default value

#############################
##   display.width option  ##
#############################

pd.set_option("display.width", 100)
print(df_medals)
#       Year      City    Sport      Discipline  NOC            Event Event gender   Medal
# 0     1924  Chamonix  Skating  Figure skating  AUT       individual            M  Silver
# 1     1924  Chamonix  Skating  Figure skating  AUT       individual            W    Gold
# ...    ...       ...      ...             ...  ...              ...          ...     ...
# 2309  2006     Turin   Skiing       Snowboard  USA  Snowboard Cross            M    Gold
# 2310  2006     Turin   Skiing       Snowboard  USA  Snowboard Cross            W  Silver

# [2311 rows x 8 columns]


#-------------------------------------------------------------------------------------------------------#
#--------------------------------------- 5. Number formatting ------------------------------------------#
#-------------------------------------------------------------------------------------------------------#

'''
pandas also allows you to set how numbers are displayed in the console. 
This option is not set through the set_options API.

Use the pd.set_eng_float_format() function to alter the floating-point formatting of pandas objects 
to produce a particular format.
'''

import numpy as np

pd.set_eng_float_format(accuracy=3, use_eng_prefix=True)

s = pd.Series(np.random.randn(5), index=["a", "b", "c", "d", "e"])

print(s / 1.0e3)
# a     -1.209m
# b    147.928u
# c    783.731u
# d    766.854u
# e     -1.071m
# dtype: float64

print(s / 1.0e6)
# a     -1.209u
# b    147.928n
# c    783.731n
# d    766.854n
# e     -1.071u
# dtype: float64


#-------------------------------------------------------------------------------------------------------#
#--------------------------------------- 6. Unicode formatting -----------------------------------------#
#-------------------------------------------------------------------------------------------------------#

'''
Some East Asian countries use Unicode characters whose width corresponds to two Latin characters. 

If a DataFrame or Series contains these characters, 
the default output mode may not align them properly.
'''

df = pd.DataFrame({"国籍": ["UK", "日本"], "名前": ["Alice", "しのぶ"]})
print(df)
#    国籍     名前
# 0  UK  Alice
# 1  日本    しのぶ

#----------
## Enable Unicode formatting
#----------

pd.set_option("display.unicode.east_asian_width", True)

print(df)
#    国籍    名前
# 0    UK   Alice
# 1  日本  しのぶ