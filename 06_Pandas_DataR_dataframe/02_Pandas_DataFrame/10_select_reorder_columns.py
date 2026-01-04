'''
Two ways to select and reorder columns in a Pandas DataFrame.

1. df = df[["col3", "col1", "col2"]]
2. df = df.reindex(columns=["col3", "col1", "col2"])
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


#----------------------------------------------------------------------------------------------------#
#-------------------------------- 1. df = df[["col3", "col1", "col2"]] ------------------------------#
#----------------------------------------------------------------------------------------------------#

df_reordered = df_emp[["dept", "name", "salary", "id", "start_date"]]
print(df_reordered)
#          dept      name  salary  id  start_date
# 0          IT      Rick  623.30   1  2012-01-01
# 1  Operations       Dan  515.20   2  2013-09-23
# 2          IT  Michelle  611.00   3  2014-11-15
# 3          HR      Ryan  729.00   4  2014-05-11
# 4     Finance      Gary  843.25   5  2015-03-27
# 5          IT      Nina  578.00   6  2013-05-21
# 6  Operations     Simon  632.80   7  2013-07-30
# 7     Finance      Guru  722.50   8  2014-06-17

df_reordered = df_emp[["salary", "id", "dept"]]
print(df_reordered)
#    salary  id        dept
# 0  623.30   1          IT
# 1  515.20   2  Operations
# 2  611.00   3          IT
# 3  729.00   4          HR
# 4  843.25   5     Finance
# 5  578.00   6          IT
# 6  632.80   7  Operations
# 7  722.50   8     Finance


#----------------------------------------------------------------------------------------------------#
#----------------------- 2. df = df.reindex(columns=["col3", "col1", "col2"]) -----------------------#
#----------------------------------------------------------------------------------------------------#

df_reindexed = df_emp.reindex(columns=["dept", "name", "salary", "id", "start_date"])
print(df_reindexed)
#          dept      name  salary  id  start_date
# 0          IT      Rick  623.30   1  2012-01-01
# 1  Operations       Dan  515.20   2  2013-09-23
# 2          IT  Michelle  611.00   3  2014-11-15
# 3          HR      Ryan  729.00   4  2014-05-11
# 4     Finance      Gary  843.25   5  2015-03-27
# 5          IT      Nina  578.00   6  2013-05-21
# 6  Operations     Simon  632.80   7  2013-07-30
# 7     Finance      Guru  722.50   8  2014-06-17

df_reindexed = df_emp.reindex(columns=["salary", "id", "dept"])
print(df_reindexed)
#    salary  id        dept
# 0  623.30   1          IT
# 1  515.20   2  Operations
# 2  611.00   3          IT
# 3  729.00   4          HR
# 4  843.25   5     Finance
# 5  578.00   6          IT
# 6  632.80   7  Operations
# 7  722.50   8     Finance