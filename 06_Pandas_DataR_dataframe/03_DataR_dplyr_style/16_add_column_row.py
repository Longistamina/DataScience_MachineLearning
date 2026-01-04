'''
1. dr.add_column(): adds a new column to the DataFrame (the name must be UNIQUE)
   + Add a single column
   + Add multiple columns
   + Error if the column name already exists

2. dr.add_row(): adds a new row to the DataFrame (the column names must match)
   + Add a single row
   + Add a single row with _before= to specify the position
   + Add multiple rows
   + Add a row with missing values (not all columns specified)
   + Error if trying to add a new column that doesn't exist in the DataFrame
'''

import datar.all as dr
from datar import f
import pandas as pd

########################

tb_emp = dr.tibble(pd.read_csv("05_Pandas_DataR_dataframe/data/emp.csv"))
print(tb_emp)
#        id      name    salary  start_date        dept
#   <int64>  <object> <float64>    <object>    <object>
# 0       1      Rick    623.30  2012-01-01          IT
# 1       2       Dan    515.20  2013-09-23  Operations
# 2       3  Michelle    611.00  2014-11-15          IT
# 3       4      Ryan    729.00  2014-05-11          HR
# 4       5      Gary    843.25  2015-03-27     Finance
# 5       6      Nina    578.00  2013-05-21          IT
# 6       7     Simon    632.80  2013-07-30  Operations
# 7       8      Guru    722.50  2014-06-17     Finance


#-------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 1. dr.add_column() -----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

#########################
## Add a single column ##
#########################

tb_emp_AddCol = (
    tb_emp
    >> dr.add_column(bonus = f.salary * 0.10)
)

print(tb_emp_AddCol)
#        id      name    salary  start_date        dept     bonus
#   <int64>  <object> <float64>    <object>    <object> <float64>
# 0       1      Rick    623.30  2012-01-01          IT    62.330
# 1       2       Dan    515.20  2013-09-23  Operations    51.520
# 2       3  Michelle    611.00  2014-11-15          IT    61.100
# 3       4      Ryan    729.00  2014-05-11          HR    72.900
# 4       5      Gary    843.25  2015-03-27     Finance    84.325
# 5       6      Nina    578.00  2013-05-21          IT    57.800
# 6       7     Simon    632.80  2013-07-30  Operations    63.280
# 7       8      Guru    722.50  2014-06-17     Finance    72.250

##########################
## Add multiple columns ##
##########################

tb_emp_AddCols = (
    tb_emp
    >> dr.add_column(
        bonus = f.salary * 0.15,
        tax = f.salary * 0.03
    )
)

print(tb_emp_AddCols)
#        id      name    salary  start_date        dept     bonus       tax
#   <int64>  <object> <float64>    <object>    <object> <float64> <float64>
# 0       1      Rick    623.30  2012-01-01          IT   93.4950   18.6990
# 1       2       Dan    515.20  2013-09-23  Operations   77.2800   15.4560
# 2       3  Michelle    611.00  2014-11-15          IT   91.6500   18.3300
# 3       4      Ryan    729.00  2014-05-11          HR  109.3500   21.8700
# 4       5      Gary    843.25  2015-03-27     Finance  126.4875   25.2975
# 5       6      Nina    578.00  2013-05-21          IT   86.7000   17.3400
# 6       7     Simon    632.80  2013-07-30  Operations   94.9200   18.9840
# 7       8      Guru    722.50  2014-06-17     Finance  108.3750   21.6750

###################################
## Error: Non-unique column name ##
###################################

print(
    tb_emp
    >> dr.add_column(salary = f.salary * 0.10)  # Error: 'salary' already exists
)
'''datar.core.names.NameNonUniqueError: Names must be unique: salary'''


#-------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 2. dr.add_row() ------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

######################
## Add a single row ##
######################

tb_emp_AddRow = (
    tb_emp
    >> dr.add_row(
        id = 9,
        name = "Laura",
        salary = 680.00,
        start_date = "2015-08-01",
        dept = "HR"
    )
)

print(tb_emp_AddRow)
#        id      name    salary  start_date        dept
#   <int64>  <object> <float64>    <object>    <object>
# 0       1      Rick    623.30  2012-01-01          IT
# 1       2       Dan    515.20  2013-09-23  Operations
# 2       3  Michelle    611.00  2014-11-15          IT
# 3       4      Ryan    729.00  2014-05-11          HR
# 4       5      Gary    843.25  2015-03-27     Finance
# 5       6      Nina    578.00  2013-05-21          IT
# 6       7     Simon    632.80  2013-07-30  Operations
# 7       8      Guru    722.50  2014-06-17     Finance
# 8       9     Laura    680.00  2015-08-01          HR (New Row)

###########################
## Add row with _before= ##
###########################

tb_emp_AddRow_before = (
    tb_emp
    >> dr.add_row(
        id = 9,
        name = "Laura",
        salary = 680.00,
        start_date = "2015-08-01",
        dept = "HR",
        _before=3  # Insert before the 3rd index (4th row)
    )
)

print(tb_emp_AddRow_before)
#        id      name    salary  start_date        dept
#   <int64>  <object> <float64>    <object>    <object>
# 0       1      Rick    623.30  2012-01-01          IT
# 1       2       Dan    515.20  2013-09-23  Operations
# 2       3  Michelle    611.00  2014-11-15          IT
# 3       9     Laura    680.00  2015-08-01          HR   (New Row)
# 4       4      Ryan    729.00  2014-05-11          HR
# 5       5      Gary    843.25  2015-03-27     Finance
# 6       6      Nina    578.00  2013-05-21          IT
# 7       7     Simon    632.80  2013-07-30  Operations
# 8       8      Guru    722.50  2014-06-17     Finance

#######################
## Add multiple rows ##
#######################

tb_emp_AddRows = (
    tb_emp
    >> dr.add_row(
        id = [11, 12],
        name = ["Laura", "Bob"],
        salary = [680.00, 590.00],
        start_date = ["2015-08-01", "2016-09-15"],
        dept = ["HR", "IT"]
    )
)

print(tb_emp_AddRows)
#        id      name    salary  start_date        dept
#   <int64>  <object> <float64>    <object>    <object>
# 0       1      Rick    623.30  2012-01-01          IT
# 1       2       Dan    515.20  2013-09-23  Operations
# 2       3  Michelle    611.00  2014-11-15          IT
# 3       4      Ryan    729.00  2014-05-11          HR
# 4       5      Gary    843.25  2015-03-27     Finance
# 5       6      Nina    578.00  2013-05-21          IT
# 6       7     Simon    632.80  2013-07-30  Operations
# 7       8      Guru    722.50  2014-06-17     Finance
# 8      11     Laura    680.00  2015-08-01          HR (New Row)
# 9      12       Bob    590.00  2016-09-15          IT (New Row)

#################################################
## Not specify enough columns (Missing Values) ##
#################################################

tb_emp_AddRow_Missing = (
    tb_emp
    >> dr.add_row(
        id = 10,
        name = "Sam"
        # Missing salary, start_date, dept
    )
)

print(tb_emp_AddRow_Missing)
#        id      name    salary  start_date        dept
#   <int64>  <object> <float64>    <object>    <object>
# 0       1      Rick    623.30  2012-01-01          IT
# 1       2       Dan    515.20  2013-09-23  Operations
# 2       3  Michelle    611.00  2014-11-15          IT
# 3       4      Ryan    729.00  2014-05-11          HR
# 4       5      Gary    843.25  2015-03-27     Finance
# 5       6      Nina    578.00  2013-05-21          IT
# 6       7     Simon    632.80  2013-07-30  Operations
# 7       8      Guru    722.50  2014-06-17     Finance
# 8      10       Sam       NaN         NaN         NaN (New Row with Missing Values)

##################################
## Error: Can't add new columns ##
##################################

print(
    tb_emp
    >> dr.add_row(
        id = 10,
        fullname = "Sam",  # Error: 'fullname' does not match any existing column
        salary = 600.00,
        start_date = "2016-10-01",
        dept = "IT"
    )
)
'''ValueError: New rows can't add columns: ['fullname']'''