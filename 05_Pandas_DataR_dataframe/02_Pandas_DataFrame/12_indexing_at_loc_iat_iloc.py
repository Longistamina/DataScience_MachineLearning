'''
1. Using df[] or df.col_row_name:
   + df["col_name"]: Access a group of rows and columns by labels or a boolean array.
   + df[["col1", "col2"]]: Access multiple columns.
   + df.col_name: Access a single column.
   + df[start_row:end_row]: Access rows by index positions (slicing).
   + df[start_row:end_row][["col1", "col2"]]: Access specific rows and columns.
   + df[start_row:end_row].col_name: Access a specific column for specific rows.

2. Indexing with df.at and df.loc:
   + df.at: Access a single value for a row/column label pair.
   + df.loc: Access a group of rows and columns by labels or a BOOLEAN array.

3. Indexing with df.iat and df.iloc:
   + df.iat: Access a single value for a row/column pair by integer position.
   + df.iloc: Access a group of rows and columns by integer position(s).
'''

import pandas as pd

df_emp = pd.read_csv("05_Pandas_DataR_dataframe/data/emp.csv")
print(df_emp)
#    id      name  salary  start_date        dept
# 0   1      Rick  623.30  2012-01-01          IT
# 1   2       Dan  515.20  2013-09-23  Operations
# 2   3  Michelle  611.00  2014-11-15          IT
# 3   4      Ryan  729.00  2014-05-11          HR
# 4   5      Gary  843.25  2015-03-27     Finance
# 5   6      Nina  578.00  2013-05-21          IT
# 6   7     Simon  632.80  2013-07-30  Operations
# 7   8      Guru  722.50  2014-06-17     Finance

########################################################

df_set_id = df_emp.set_index("id", drop = True, inplace = False)
print(df_set_id)
#         name  salary  start_date        dept
# id                                          
# 1       Rick  623.30  2012-01-01          IT
# 2        Dan  515.20  2013-09-23  Operations
# 3   Michelle  611.00  2014-11-15          IT
# 4       Ryan  729.00  2014-05-11          HR
# 5       Gary  843.25  2015-03-27     Finance
# 6       Nina  578.00  2013-05-21          IT
# 7      Simon  632.80  2013-07-30  Operations
# 8       Guru  722.50  2014-06-17     Finance

########################################################

df_indexed = df_emp.set_axis(
    labels = [f"row_{i}" for i in df_emp["id"]],
    axis = 0,
    copy = True
)
print(df_indexed)
#        id      name  salary  start_date        dept
# row_1   1      Rick  623.30  2012-01-01          IT
# row_2   2       Dan  515.20  2013-09-23  Operations
# row_3   3  Michelle  611.00  2014-11-15          IT
# row_4   4      Ryan  729.00  2014-05-11          HR
# row_5   5      Gary  843.25  2015-03-27     Finance
# row_6   6      Nina  578.00  2013-05-21          IT
# row_7   7     Simon  632.80  2013-07-30  Operations
# row_8   8      Guru  722.50  2014-06-17     Finance


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. Using df[] or df.column_name --------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

########################
##   df["col_name"]   ##
########################
'''Access single column'''

print(df_emp["name"])
# 0        Rick
# 1         Dan
# 2    Michelle
# 3        Ryan
# 4        Gary
# 5        Nina
# 6       Simon
# 7        Guru
# Name: name, dtype: object

############################
##  df[["col1", "col2"]]  ##
############################
'''Access multiple columns'''

print(df_emp[["name", "salary"]])
#        name  salary
# 0      Rick  623.30
# 1       Dan  515.20
# 2  Michelle  611.00
# 3      Ryan  729.00
# 4      Gary  843.25
# 5      Nina  578.00
# 6     Simon  632.80
# 7      Guru  722.50

#####################
##   df.col_name   ##
#####################
'''
Access single column using attribute style

NOTE: This style only works when the column name is a valid Python identifier 
      (e.g., no spaces, doesn't start with a number, etc.)
'''

print(df_emp.dept)
# 0            IT
# 1    Operations
# 2            IT
# 3            HR
# 4       Finance
# 5            IT
# 6    Operations
# 7       Finance
# Name: dept, dtype: object

#############################
##  df[start_row:end_row]  ##
#############################
'''
Access rows by index positions (slicing)
NOTE: Should use with default integer index only
'''

print(df_emp[2:5])
#    id      name  salary  start_date     dept
# 2   3  Michelle  611.00  2014-11-15       IT
# 3   4      Ryan  729.00  2014-05-11       HR
# 4   5      Gary  843.25  2015-03-27  Finance
'''Note: The end_row "5" is excluded'''

print(df_emp[:4])
#    id      name  salary  start_date        dept
# 0   1      Rick   623.3  2012-01-01          IT
# 1   2       Dan   515.2  2013-09-23  Operations
# 2   3  Michelle   611.0  2014-11-15          IT
# 3   4      Ryan   729.0  2014-05-11          HR

print(df_emp[5:])
# 5   6   Nina   578.0  2013-05-21          IT
# 6   7  Simon   632.8  2013-07-30  Operations
# 7   8   Guru   722.5  2014-06-17     Finance

print(df_emp[::2])
#    id      name  salary  start_date        dept
# 0   1      Rick  623.30  2012-01-01          IT
# 2   3  Michelle  611.00  2014-11-15          IT
# 4   5      Gary  843.25  2015-03-27     Finance
# 6   7     Simon  632.80  2013-07-30  Operations

#-----------------
## Try with non-default-integer index
#-----------------

print(df_set_id[2:5])
#         name  salary  start_date     dept
# id                                       
# 3   Michelle  611.00  2014-11-15       IT
# 4       Ryan  729.00  2014-05-11       HR
# 5       Gary  843.25  2015-03-27  Finance

print(df_indexed[2:5])
#        id      name  salary  start_date     dept
# row_3   3  Michelle  611.00  2014-11-15       IT
# row_4   4      Ryan  729.00  2014-05-11       HR
# row_5   5      Gary  843.25  2015-03-27  Finance

'''
Ase we can see, slicing with non-default-integer index still works,
but the rows are selected based on their integer position, NOT their index labels.
'''

###############################################
##  df[start_row:end_row][["col1", "col2"]]  ##
###############################################
'''Access specific rows and columns'''

print(df_emp[2:5]["name"])
# 2    Michelle
# 3        Ryan
# 4        Gary
# Name: name, dtype: object

print(df_emp[:4][["name", "dept"]])
#        name        dept
# 0      Rick          IT
# 1       Dan  Operations
# 2  Michelle          IT
# 3      Ryan          HR

print(df_emp[5:][["name", "salary"]])
#     name  salary
# 5   Nina   578.0
# 6  Simon   632.8
# 7   Guru   722.5

print(df_emp[::2][["id", "dept"]])
#    id        dept
# 0   1          IT
# 2   3          IT
# 4   5     Finance
# 6   7  Operations

######################################
##  df[start_row:end_row].col_name  ##
######################################
'''Access a specific column for specific rows (attribute style)'''

print(df_emp[2:5].name)
# 2    Michelle
# 3        Ryan
# 4        Gary
# Name: name, dtype: object

print(df_emp[::2].salary)
# 0    623.30
# 2    611.00
# 4    843.25
# 6    632.80
# Name: salary, dtype: float64


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 2. Indexing with df.at and df.loc -------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

#################
##    df.at    ##
#################
'''Access a SINGLE value for a row/column label pair'''

print(df_set_id.at[3, "name"])
# Michelle

print(df_indexed.at["row_5", "dept"])
# Finance

#########################################
##   df.loc (allow BOOLEAN indexing)   ##
#########################################
'''
Access a MULTIPLE rows and columns by labels or a BOOLEAN array.
NOTE: The end_row is INCLUDED when using df.loc
'''

print(df_emp.loc[2:5])
#    id      name  salary  start_date     dept
# 2   3  Michelle  611.00  2014-11-15       IT
# 3   4      Ryan  729.00  2014-05-11       HR
# 4   5      Gary  843.25  2015-03-27  Finance
# 5   6      Nina  578.00  2013-05-21       IT

print(df_emp.loc[:, ["name", "dept"]]) # All rows and specific columns
#        name        dept
# 0      Rick          IT
# 1       Dan  Operations
# 2  Michelle          IT
# 3      Ryan          HR
# 4      Gary     Finance
# 5      Nina          IT
# 6     Simon  Operations
# 7      Guru     Finance

print(df_set_id.loc[3:5, ["name", "salary"]])
#         name  salary
# id                  
# 3   Michelle  611.00
# 4       Ryan  729.00
# 5       Gary  843.25

print(df_indexed.loc["row_3":"row_5", ["name", "dept"]])
#            name     dept
# row_3  Michelle       IT
# row_4      Ryan       HR
# row_5      Gary  Finance

#-----------------
## Try BOOLEAN indexing
#-----------------
'''
The CONDITION is on the side of the ROW selection

df.loc[condition, ["columns"]]
'''

print(df_emp.loc[df_emp["salary"] > 700])
#    id  name  salary  start_date     dept
# 3   4  Ryan  729.00  2014-05-11       HR
# 4   5  Gary  843.25  2015-03-27  Finance
# 7   8  Guru  722.50  2014-06-17  Finance

print(df_emp.loc[df_emp["dept"] == "IT", ["name", "salary"]])
#        name  salary
# 0      Rick   623.3
# 2  Michelle   611.0
# 5      Nina   578.0

print(df_set_id.loc[df_set_id["name"].str.startswith("R"), ["name", "salary", "dept"]])
#     name  salary dept
# id                   
# 1   Rick   623.3   IT
# 4   Ryan   729.0   HR


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------- 3. Indexing with df.iat and df.iloc ------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

##################
##    df.iat    ##
##################
'''Access a SINGLE value for a row/column pair by INTEGER position'''

print(df_emp.iat[2, 1])
# Michelle

print(df_indexed.iat[4, 4])
# Finance

#################
##   df.iloc   ##
#################
'''Access a MULTIPLE rows and columns by INTEGER position(s).
NOTE: The end_row is EXCLUDED when using df.iloc
'''

print(df_emp.iloc[2:5])
#    id      name  salary  start_date     dept
# 2   3  Michelle  611.00  2014-11-15       IT
# 3   4      Ryan  729.00  2014-05-11       HR
# 4   5      Gary  843.25  2015-03-27  Finance

print(df_emp.iloc[:, [1, 4]]) # All rows and specific columns
#        name        dept
# 0      Rick          IT
# 1       Dan  Operations
# 2  Michelle          IT
# 3      Ryan          HR
# 4      Gary     Finance
# 5      Nina          IT
# 6     Simon  Operations
# 7      Guru     Finance

print(df_set_id.iloc[2:5, 2]) # Single column
# id
# 3    2014-11-15
# 4    2014-05-11
# 5    2015-03-27
# Name: start_date, dtype: object
