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

from pathlib import Path

import datar.all as dr
import pandas as pd
from datar import f
from loguru import logger

pd.set_option("display.width", 200)

data_dir = Path("/home").rglob("*/DataScience_MachineLearning/data")
data_dir = next(data_dir)

##--------------------##

tb_emp = dr.tibble(pd.read_csv(data_dir/"emp.csv"))
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

##------------------##
## Add a single row ##
##------------------##

tb_emp_AddRow = (
    tb_emp
    >> dr.add_row(
        id=9,
        name="Laura",
        salary=680.00,
        start_date="2015-08-01",
        dept="HR"
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

##-----------------------##
## Add row with _before= ##
##-----------------------##

tb_emp_AddRow_before = (
    tb_emp
    >> dr.add_row(
        id=9,
        name="Laura",
        salary=680.00,
        start_date="2015-08-01",
        dept="HR",
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

##-------------------##
## Add multiple rows ##
##-------------------##

tb_emp_AddRows = (
    tb_emp
    >> dr.add_row(
        id=[11, 12],
        name=["Laura", "Bob"],
        salary=[680.00, 590.00],
        start_date=["2015-08-01", "2016-09-15"],
        dept=["HR", "IT"]
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

##---------------------------------------------##
## Not specify enough columns (Missing Values) ##
##---------------------------------------------##

tb_emp_AddRow_Missing = (
    tb_emp
    >> dr.add_row(
        id=10,
        name="Sam"
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

##------------------------------##
## Error: Can't add new columns ##
##------------------------------##

try:
    print(
        tb_emp
        >> dr.add_row(
            id=10,
            fullname="Sam",  # Error: 'fullname' does not match any existing column
            salary=600.00,
            start_date="2016-10-01",
            dept="IT"
        )
    )
except Exception as e:
    logger.error(e)

'''ValueError: New rows can't add columns: ['fullname']'''
