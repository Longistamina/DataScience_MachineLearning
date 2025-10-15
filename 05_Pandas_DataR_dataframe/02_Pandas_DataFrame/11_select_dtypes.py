'''
df.select_dtypes(include=..., exclude=...) allows you to select columns in a DataFrame based on their data types.

include, exclude: scalar or list-like
=> A selection of dtypes or strings (column names) to be included/excluded. 
   At least one of these parameters must be supplied.
'''

########################

'''
To select all numeric types, use: 'np.number' or 'number'

To select strings you must use: object, 
but note that this will return all object dtype columns. 

To select datetimes, use: np.datetime64, 'datetime' or 'datetime64'

To select timedeltas, use: np.timedelta64, 'timedelta' or 'timedelta64'

To select Pandas categorical dtypes, use: 'category'

To select Pandas datetimetz dtypes, use: 'datetimetz' or 'datetime64[ns, tz]'
'''

import pandas as pd

df_emp = (
    pd.read_csv(
        filepath_or_buffer = "05_Pandas_DataR_dataframe/data/emp.csv",
        parse_dates = ["start_date"],
        dtype = {"dept": "category"}
    )
    .assign(
        **{
            "raise": [True, False, True, False, True, False, True, False],
            "comments": ["Good", "Bad", "Average", "Excellent", "Poor", "Good", "Bad", "Average"]
        }
    )
)

print(df_emp.dtypes)
# id                     int64
# name                  object
# salary               float64
# start_date    datetime64[ns]
# dept                category
# raise                   bool
# comments              object
# dtype: object


#-------------------------------------------------------------------------------------------------#
#----------------------------------- Apply df.select_dtypes() ------------------------------------#
#-------------------------------------------------------------------------------------------------#

####################################
## df.select_dtypes(include=...)  ##
####################################

# Select all "number" columns
df_num = df_emp.select_dtypes(include="number")
print(df_num.head())
#    id  salary
# 0   1  623.30
# 1   2  515.20
# 2   3  611.00
# 3   4  729.00
# 4   5  843.25

print(df_num.columns) # Index(['id', 'salary'], dtype='object')

# Select all "object" columns
df_obj = df_emp.select_dtypes(include="object")
print(df_obj.head())
#        name   comments
# 0      Rick       Good
# 1       Dan        Bad
# 2  Michelle    Average
# 3      Ryan  Excellent
# 4      Gary       Poor

# Select all "category" columns
df_cat = df_emp.select_dtypes(include="category")
print(df_cat.head())
#          dept
# 0          IT
# 1  Operations
# 2          IT
# 3          HR
# 4     Finance

# Select all "bool" columns
df_bool = df_emp.select_dtypes(include="bool")
print(df_bool.head())
#    raise
# 0   True
# 1  False
# 2   True
# 3  False
# 4   True

# Select all "datetime" columns
df_dt = df_emp.select_dtypes(include="datetime")
print(df_dt.head())
#   start_date
# 0 2012-01-01
# 1 2013-09-23
# 2 2014-11-15
# 3 2014-05-11
# 4 2015-03-27

# Select multiple dtypes: "number" and "datetime"
df_num_dt = df_emp.select_dtypes(include=["number", "datetime"])
print(df_num_dt.head())
#    id  salary start_date
# 0   1  623.30 2012-01-01
# 1   2  515.20 2013-09-23
# 2   3  611.00 2014-11-15
# 3   4  729.00 2014-05-11
# 4   5  843.25 2015-03-27

# Combine with .drop()
df_combined = df_emp.select_dtypes(include=["number", "object"]).drop(columns="id")
print(df_combined.head())
#        name  salary   comments
# 0      Rick  623.30       Good
# 1       Dan  515.20        Bad
# 2  Michelle  611.00    Average
# 3      Ryan  729.00  Excellent
# 4      Gary  843.25       Poor

####################################
## df.select_dtypes(exclude=...)  ##
####################################

# Select all columns except "object" columns
df_excl_obj = df_emp.select_dtypes(exclude="object")
print(df_excl_obj.head())
#    id  salary start_date        dept  raise
# 0   1  623.30 2012-01-01          IT   True
# 1   2  515.20 2013-09-23  Operations  False
# 2   3  611.00 2014-11-15          IT   True
# 3   4  729.00 2014-05-11          HR  False
# 4   5  843.25 2015-03-27     Finance   True

# Select all columns except "object" and "category" columns
df_excl_obj_cat = df_emp.select_dtypes(exclude=["object", "category"])
print(df_excl_obj_cat.head())
#    id  salary start_date  raise
# 0   1  623.30 2012-01-01   True
# 1   2  515.20 2013-09-23  False
# 2   3  611.00 2014-11-15   True
# 3   4  729.00 2014-05-11  False
# 4   5  843.25 2015-03-27   True

# Combine with .drop()
df_combined = df_emp.select_dtypes(exclude=["object", "category"]).drop(columns="id")
print(df_combined.head())
#    salary start_date  raise
# 0  623.30 2012-01-01   True
# 1  515.20 2013-09-23  False
# 2  611.00 2014-11-15   True
# 3  729.00 2014-05-11  False
# 4  843.25 2015-03-27   True

##############################################
## df.select_dtypes(include=, exclude=...)  ##
##############################################

# Select "number" columns but exclude "int64" columns
df_num_excl_int = df_emp.select_dtypes(include="number", exclude="int64")
print(df_num_excl_int.head())
#    salary
# 0  623.30
# 1  515.20
# 2  611.00
# 3  729.00
# 4  843.25
