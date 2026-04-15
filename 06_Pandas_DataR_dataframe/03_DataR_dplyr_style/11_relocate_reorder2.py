'''
dr.relocate(): Reorder columns in a DataFrame
dr.relocate(_after=)
dr.relocate(_before=)
dr.relocate(dr.where(dr.is_character)) # Move all character columns to the front
dr.relocate(dr.where(dr.is_numeric), _after=0) # Move all numeric columns to the back
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

#---------------------------------------------------------------------------------------------------------------------#
#-------------------------------------- Reorder columns using dr.relocate() ------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#

###################
## dr.relocate() ##
###################

tb_reordered = (
    tb_emp
    >> dr.relocate(f.dept, f.name, f.salary, f.id, f.start_date)
)

print(tb_reordered.head())
#          dept      name    salary      id  start_date
#      <object>  <object> <float64> <int64>    <object>
# 0          IT      Rick    623.30       1  2012-01-01
# 1  Operations       Dan    515.20       2  2013-09-23
# 2          IT  Michelle    611.00       3  2014-11-15
# 3          HR      Ryan    729.00       4  2014-05-11
# 4     Finance      Gary    843.25       5  2015-03-27

###################
## _after=f.col  ##
###################

tb_after = (
    tb_emp
    >> dr.relocate(f.dept, _after=f.name) # Move dept to right after name
)

print(tb_after.head())
#        id      name        dept    salary  start_date
#   <int64>  <object>    <object> <float64>    <object>
# 0       1      Rick          IT    623.30  2012-01-01
# 1       2       Dan  Operations    515.20  2013-09-23
# 2       3  Michelle          IT    611.00  2014-11-15
# 3       4      Ryan          HR    729.00  2014-05-11
# 4       5      Gary     Finance    843.25  2015-03-27

'''
_after = dr.last_col() # Move to the end
'''

tb_last = (
    tb_emp
    >> dr.relocate(f.id, _after=dr.last_col()) # Move id to the end
)

print(tb_last.head())
#        name    salary  start_date        dept      id
#    <object> <float64>    <object>    <object> <int64>
# 0      Rick    623.30  2012-01-01          IT       1
# 1       Dan    515.20  2013-09-23  Operations       2
# 2  Michelle    611.00  2014-11-15          IT       3
# 3      Ryan    729.00  2014-05-11          HR       4
# 4      Gary    843.25  2015-03-27     Finance       5

###################
## _before=f.col ##
###################

tb_before = (
    tb_emp
    >> dr.relocate(f.dept, _before=f.name) # Move dept to right before name
)

print(tb_before.head())
#        id        dept      name    salary  start_date
#   <int64>    <object>  <object> <float64>    <object>
# 0       1          IT      Rick    623.30  2012-01-01
# 1       2  Operations       Dan    515.20  2013-09-23
# 2       3          IT  Michelle    611.00  2014-11-15
# 3       4          HR      Ryan    729.00  2014-05-11
# 4       5     Finance      Gary    843.25  2015-03-27

#########################
## where(is_character) ##
#########################

tb_char_front = (
    tb_emp
    >> dr.relocate(dr.where(dr.is_character)) # Move all character columns to the front
)

print(tb_char_front.head())
#        name  start_date        dept      id    salary
#    <object>    <object>    <object> <int64> <float64>
# 0      Rick  2012-01-01          IT       1    623.30
# 1       Dan  2013-09-23  Operations       2    515.20
# 2  Michelle  2014-11-15          IT       3    611.00
# 3      Ryan  2014-05-11          HR       4    729.00
# 4      Gary  2015-03-27     Finance       5    843.25

#######################
## where(is_numeric) ##
####################### 

tb_num_back = (
    tb_emp
    >> dr.relocate(dr.where(dr.is_numeric), _after=0) # Move all numeric columns to the front
)

print(tb_num_back.head())
#        id    salary      name  start_date        dept
#   <int64> <float64>  <object>    <object>    <object>
# 0       1    623.30      Rick  2012-01-01          IT
# 1       2    515.20       Dan  2013-09-23  Operations
# 2       3    611.00  Michelle  2014-11-15          IT
# 3       4    729.00      Ryan  2014-05-11          HR
# 4       5    843.25      Gary  2015-03-27     Finance