'''
1. Drop columns:
   + .drop(labels=..., axis=1, inplace=True/False)
   + .drop(columns=..., inplace=True/False)

2. Drop rows:
   + .drop(labels=..., axis=0, inplace=True/False)
    + .drop(index=..., inplace=True/False)
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


#------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 1. Drop columns ------------------------------------------------#
#------------------------------------------------------------------------------------------------------------#

###################################################
## .drop(labels=..., axis=1, inplace=True/False) ##
###################################################

df_dropped = df_emp.drop(labels=["start_date", "dept"], axis=1, inplace=False)
print(df_dropped)
#    id      name  salary
# 0   1      Rick  623.30
# 1   2       Dan  515.20
# 2   3  Michelle  611.00
# 3   4      Ryan  729.00
# 4   5      Gary  843.25
# 5   6      Nina  578.00
# 6   7     Simon  632.80
# 7   8      Guru  722.50

############################################
## .drop(columns=..., inplace=True/False) ##
############################################

df_dropped = df_emp.drop(columns=["id", "start_date"], inplace=False)
print(df_dropped)
#        name  salary        dept
# 0      Rick  623.30          IT
# 1       Dan  515.20  Operations
# 2  Michelle  611.00          IT
# 3      Ryan  729.00          HR
# 4      Gary  843.25     Finance
# 5      Nina  578.00          IT
# 6     Simon  632.80  Operations
# 7      Guru  722.50     Finance


#------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 2. Drop rows ---------------------------------------------------#
#------------------------------------------------------------------------------------------------------------#

###################################################
## .drop(labels=..., axis=0, inplace=True/False) ##
###################################################

df_dropped = df_emp.drop(labels=[0, 3, 5], axis=0, inplace=False) # Use default integer index
print(df_dropped)
#    id      name  salary  start_date        dept
# 1   2       Dan  515.20  2013-09-23  Operations
# 2   3  Michelle  611.00  2014-11-15          IT
# 4   5      Gary  843.25  2015-03-27     Finance
# 6   7     Simon  632.80  2013-07-30  Operations
# 7   8      Guru  722.50  2014-06-17     Finance

df_dropped = df_indexed.drop(labels=["row_2", "row_4"], axis=0, inplace=False) # Use custom label index
print(df_dropped)
#        id      name  salary  start_date        dept
# row_1   1      Rick  623.30  2012-01-01          IT
# row_3   3  Michelle  611.00  2014-11-15          IT
# row_5   5      Gary  843.25  2015-03-27     Finance
# row_6   6      Nina  578.00  2013-05-21          IT
# row_7   7     Simon  632.80  2013-07-30  Operations
# row_8   8      Guru  722.50  2014-06-17     Finance

###########################################
## .drop(index=..., inplace=True/False)  ##
###########################################

df_dropped = df_emp.drop(index=[1, 2, 3], inplace=False) # Use default integer index
print(df_dropped)
#    id   name  salary  start_date        dept
# 0   1   Rick  623.30  2012-01-01          IT
# 4   5   Gary  843.25  2015-03-27     Finance
# 5   6   Nina  578.00  2013-05-21          IT
# 6   7  Simon  632.80  2013-07-30  Operations
# 7   8   Guru  722.50  2014-06-17     Finance

df_dropped = df_indexed.drop(index=["row_5", "row_6"], inplace=False) # Use custom label index
print(df_dropped)
#        id      name  salary  start_date        dept
# row_1   1      Rick   623.3  2012-01-01          IT
# row_2   2       Dan   515.2  2013-09-23  Operations
# row_3   3  Michelle   611.0  2014-11-15          IT
# row_4   4      Ryan   729.0  2014-05-11          HR
# row_7   7     Simon   632.8  2013-07-30  Operations
# row_8   8      Guru   722.5  2014-06-17     Finance