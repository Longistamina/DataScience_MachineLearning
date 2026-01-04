'''
1. Shape and Size attributes:
   + df.shape: Returns a tuple (rows, columns)
   + df.size: Returns total number of elements (rows * columns)
   + df.ndim: Returns number of dimensions (always 2 for DataFrame)

2. Data types and Structure attributes:
   + df.dtypes: Returns data types of each column
   + df.columns: Returns column labels
   + df.index: Returns row labels
   + df.axes: Returns a list of both row and column labels

3. Data Access attributes:
   + df.values: Returns the underlying numpy array of the DataFrame
   + df.T: Returns the transpose of the DataFrame
   + df.empty: Returns True if DataFrame is empty, else False

4. Advanced attributes:
   + df.attrs: Dictionary for storing custom metadata
   + df.style: Returns a Styler object for HTML/CSS formatting
   + df.flags: Configuration object controlling DataFrame behavior. 
'''

import pandas as pd

df_baseball = pd.read_csv(
    filepath_or_buffer = "05_Pandas_DataR_dataframe/data/baseball.csv",
    dtype = {"Team": "category", "Position": "category", "PosCategory": "category"}
)

df_baseball.head()
#               Name Team       Position  Height  Weight    Age PosCategory
# 0    Adam_Donachie  BAL        Catcher      74     180  22.99     Catcher
# 1        Paul_Bako  BAL        Catcher      74     215  34.69     Catcher
# 2  Ramon_Hernandez  BAL        Catcher      72     210  30.78     Catcher
# 3     Kevin_Millar  BAL  First_Baseman      72     210  35.43   Infielder
# 4      Chris_Gomez  BAL  First_Baseman      73     188  35.71   Infielder

df_baseball.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 1015 entries, 0 to 1014
# Data columns (total 7 columns):
#  #   Column       Non-Null Count  Dtype   
# ---  ------       --------------  -----   
#  0   Name         1015 non-null   object  
#  1   Team         1015 non-null   category
#  2   Position     1015 non-null   category
#  3   Height       1015 non-null   int64   
#  4   Weight       1015 non-null   int64   
#  5   Age          1015 non-null   float64 
#  6   PosCategory  1015 non-null   category
# dtypes: category(3), float64(1), int64(2), object(1)
# memory usage: 36.5+ KB

'''
Here, if leave the "Team", "Position", "PosCategory" columns as "object" type, 
the memory usage will be 55.6+ KB.
'''


#------------------------------------------------------------------------------------------------------#
#------------------------------------ 1. Shape and Size attributes ------------------------------------#
#------------------------------------------------------------------------------------------------------#

##############
## df.shape ##
##############
'''df.shape returns a tuple representing the dimensionality of the DataFrame.'''

print(df_baseball.shape)  # (1015, 7)
                          # There are 1015 rows and 7 columns in the DataFrame.

#############
## df.size ##
#############
'''df.size returns the total number of elements (nrows x ncols) in the DataFrame.'''

print(df_baseball.size)   # 7105
                          # Total number of elements = 1015 rows * 7 columns = 7105

#############
## df.ndim ##
#############
'''df.ndim returns the number of dimensions of the DataFrame (always = 2 for DataFrame).'''

print(df_baseball.ndim)   # 2
                          # DataFrames are always 2-dimensional.


#------------------------------------------------------------------------------------------------------#
#---------------------------- 2. Data types and Structure attributes ----------------------------------#
#------------------------------------------------------------------------------------------------------#

###############
## df.dtypes ##
###############
'''df.dtypes returns the data types of each column in the DataFrame.'''

print(df_baseball.dtypes)
# Name             object
# Team           category
# Position       category
# Height            int64
# Weight            int64
# Age             float64
# PosCategory    category
# dtype: object

################
## df.columns ##
################
'''df.columns returns the column labels of the DataFrame.'''

print(df_baseball.columns)
# Index(['Name', 'Team', 'Position', 'Height', 'Weight', 'Age', 'PosCategory'], dtype='object')

##############
## df.index ##
##############
'''df.index returns the row labels of the DataFrame.'''

print(df_baseball.index)
# RangeIndex(start=0, stop=1015, step=1)

'''
This means the true index ranges from 0 to 1014 (total 1015 rows).
The 1015 is excluded
'''

#############
## df.axes ##
#############
'''df.axes returns a list containing the row and column labels of the DataFrame.'''

print(df_baseball.axes)
# [
#     RangeIndex(start=0, stop=1015, step=1), 
#     Index(['Name', 'Team', 'Position', 'Height', 'Weight', 'Age', 'PosCategory'], dtype='object')
# ]


#------------------------------------------------------------------------------------------------------#
#-------------------------------------- 3. Data Access attributes -------------------------------------#
#------------------------------------------------------------------------------------------------------#

###############
## df.values ##
###############
'''df.values returns the underlying numpy array of the DataFrame.'''

print(df_baseball.values)
# [['Adam_Donachie' 'BAL' 'Catcher' ... 180 22.99 'Catcher']
#  ['Paul_Bako' 'BAL' 'Catcher' ... 215 34.69 'Catcher']
#  ['Ramon_Hernandez' 'BAL' 'Catcher' ... 210 30.78 'Catcher']
#  ...
#  ['Chris_Narveson' 'STL' 'Relief_Pitcher' ... 205 25.19 'Pitcher']
#  ['Randy_Keisler' 'STL' 'Relief_Pitcher' ... 190 31.01 'Pitcher']
#  ['Josh_Kinney' 'STL' 'Relief_Pitcher' ... 195 27.92 'Pitcher']]

print(type(df_baseball.values))  # <class 'numpy.ndarray'>

##########
## df.T ##
##########
'''df.T returns the transpose of the DataFrame (swaps rows and columns).'''

print(df_baseball.T)
#                       0          1                2     ...            1012            1013            1014
# Name         Adam_Donachie  Paul_Bako  Ramon_Hernandez  ...  Chris_Narveson   Randy_Keisler     Josh_Kinney
# Team                   BAL        BAL              BAL  ...             STL             STL             STL
# Position           Catcher    Catcher          Catcher  ...  Relief_Pitcher  Relief_Pitcher  Relief_Pitcher
# Height                  74         74               72  ...              75              75              73
# Weight                 180        215              210  ...             205             190             195
# Age                  22.99      34.69            30.78  ...           25.19           31.01           27.92
# PosCategory        Catcher    Catcher          Catcher  ...         Pitcher         Pitcher         Pitcher
'''[7 rows x 1015 columns]'''

##############
## df.empty ##
##############
'''df.empty returns True if the DataFrame is empty (has no elements), else False.'''

print(df_baseball.empty)  
# False

df_void = pd.DataFrame()
print(df_void.empty)
# True


#------------------------------------------------------------------------------------------------------#
#------------------------------------- 4. Advanced attributes -----------------------------------------#
#------------------------------------------------------------------------------------------------------#

##############
## df.attrs ##
##############
'''df.attrs is a dictionary for storing custom metadata about the DataFrame.'''

print(df_baseball.attrs)  
# {}
# Initially empty dictionary.

df_baseball.attrs['source'] = 'Baseball Dataset 2023'
df_baseball.attrs['description'] = 'Player statistics including height, weight, age, and position.'
print(df_baseball.attrs)
# {
#     'source': 'Baseball Dataset 2023', 
#     'description': 'Player statistics including height, weight, age, and position.'
# }

##############
## df.style ##
##############
'''df.style returns a Styler object for HTML/CSS formatting of the DataFrame.'''

print(df_baseball.style)
# <pandas.io.formats.style.Styler object at 0x7f9a405a7a70>

##############
## df.flags ##
##############
'''df.flags is a configuration object controlling various DataFrame behaviors.'''

print(df_baseball.flags)
# <Flags(allows_duplicate_labels=True)>
