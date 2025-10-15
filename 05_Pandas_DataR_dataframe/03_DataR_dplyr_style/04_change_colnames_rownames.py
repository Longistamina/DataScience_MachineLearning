'''
1. Change column names:
   + dr.rename()
   + dr.rename_with()
   + Apply pandas method with pipda.register_verb (dr.pipe = register_verb(func = pd.DataFrame.pipe)

2. Change row names (index):
   + dr.column_to_rownames()
   + combine dr.column_to_rownames() with dr.mutate()
   + dr.rownames_to_column() (dr.has_rownames() must be True)
   + Apply pandas method with pipda.register_verb (dr.pipe = register_verb(func = pd.DataFrame.pipe)
'''

import datar.all as dr
from datar import f
import pandas as pd

# Suppress all warnings
import warnings
warnings.filterwarnings("ignore")

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
#--------------------------------------------- 1. Change column names ------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#

#################
## dr.rename() ##
#################

tb_renamed = (
    tb_emp 
    >> dr.rename(emp_id=f.id, emp_name=f.name)
)

print(tb_renamed.head())
#    emp_id  emp_name    salary  start_date        dept
#   <int64>  <object> <float64>    <object>    <object>
# 0       1      Rick    623.30  2012-01-01          IT
# 1       2       Dan    515.20  2013-09-23  Operations
# 2       3  Michelle    611.00  2014-11-15          IT
# 3       4      Ryan    729.00  2014-05-11          HR
# 4       5      Gary    843.25  2015-03-27     Finance

######################
## dr.rename_with() ##
######################

tb_renamed2 = (
    tb_emp 
    >> dr.rename_with(str.upper, f[f.salary, f.dept])
)

print(tb_renamed2.tail())
#        id     name    SALARY  start_date        DEPT
#   <int64> <object> <float64>    <object>    <object>
# 3       4     Ryan    729.00  2014-05-11          HR
# 4       5     Gary    843.25  2015-03-27     Finance
# 5       6     Nina    578.00  2013-05-21          IT
# 6       7    Simon    632.80  2013-07-30  Operations
# 7       8     Guru    722.50  2014-06-17     Finance

###################
## pandas method ##
###################

from pipda import register_verb
dr.pipe = register_verb(func = pd.DataFrame.pipe)
dr.filter = register_verb(func = dr.filter_)

tb_renamed3 = (
    tb_emp 
    >> dr.pipe(lambda f: f.add_prefix('emp_'))
    >> dr.filter( f.emp_salary > 600)
)

print(tb_renamed3.head())
#    emp_id  emp_name  emp_salary emp_start_date    emp_dept
#   <int64>  <object>   <float64>       <object>    <object>
# 0       1      Rick      623.30     2012-01-01          IT
# 2       3  Michelle      611.00     2014-11-15          IT
# 3       4      Ryan      729.00     2014-05-11          HR
# 4       5      Gary      843.25     2015-03-27     Finance
# 6       7     Simon      632.80     2013-07-30  Operations

'''--- Example with f.set_axis() ---'''

print(
    tb_emp 
    >> dr.pipe(lambda f: f.set_axis(["ID", "Name", "Salary", "Start_Date", "Department"], axis=1))
)
#        ID      Name    Salary       Start_Date  Department
#   <int64>  <object> <float64> <datetime64[ns]>    <object>
# 0       1      Rick    623.30       2012-01-01          IT
# 1       2       Dan    515.20       2013-09-23  Operations
# 2       3  Michelle    611.00       2014-11-15          IT
# 3       4      Ryan    729.00       2014-05-11          HR
# 4       5      Gary    843.25       2015-03-27     Finance
# 5       6      Nina    578.00       2013-05-21          IT
# 6       7     Simon    632.80       2013-07-30  Operations
# 7       8      Guru    722.50       2014-06-17     Finance


#---------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 2. Change row names --------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#

#############################
## dr.column_to_rownames() ##
#############################

tb_to_rownames = (
    tb_emp 
    >> dr.column_to_rownames('id')
)

print(tb_to_rownames.head())
#        name    salary  start_date        dept
#    <object> <float64>    <object>    <object>
# 1      Rick    623.30  2012-01-01          IT
# 2       Dan    515.20  2013-09-23  Operations
# 3  Michelle    611.00  2014-11-15          IT
# 4      Ryan    729.00  2014-05-11          HR
# 5      Gary    843.25  2015-03-27     Finance

######################################################
## Combine dr.column_to_rownames() with dr.mutate() ##
######################################################

print(
    tb_emp
    >> dr.select(~f.id)
    >> dr.mutate(emp_id = [f"employee_{i}" for i in range(1, len(tb_emp) + 1)])
    >> dr.column_to_rownames('emp_id')
)
#                 name    salary  start_date        dept
#             <object> <float64>    <object>    <object>
# employee_1      Rick    623.30  2012-01-01          IT
# employee_2       Dan    515.20  2013-09-23  Operations
# employee_3  Michelle    611.00  2014-11-15          IT
# employee_4      Ryan    729.00  2014-05-11          HR
# employee_5      Gary    843.25  2015-03-27     Finance
# employee_6      Nina    578.00  2013-05-21          IT
# employee_7     Simon    632.80  2013-07-30  Operations
# employee_8      Guru    722.50  2014-06-17     Finance

#############################
## dr.rownames_to_column() ##
#############################

tb_from_rownames = (
    tb_to_rownames
    >> dr.rownames_to_column('emp_id')
)

print(tb_from_rownames.head())
#        name   emp_id    salary  start_date        dept
#    <object> <object> <float64>    <object>    <object>
# 0      Rick        1    623.30  2012-01-01          IT
# 1       Dan        2    515.20  2013-09-23  Operations
# 2  Michelle        3    611.00  2014-11-15          IT
# 3      Ryan        4    729.00  2014-05-11          HR
# 4      Gary        5    843.25  2015-03-27     Finance

###################
## pandas method ##
###################

from pipda import register_verb
dr.pipe = register_verb(func = pd.DataFrame.pipe)
dr.filter = register_verb(func = dr.filter_)


tb_set_index = (
    tb_emp 
    >> dr.pipe(lambda f: f.set_index('id'))
    >> dr.filter( f.salary > 600)
)

print(tb_set_index.head())
#         name    salary  start_date        dept
                                              
# id  <object> <float64>    <object>    <object>
# 1       Rick    623.30  2012-01-01          IT
# 3   Michelle    611.00  2014-11-15          IT
# 4       Ryan    729.00  2014-05-11          HR
# 5       Gary    843.25  2015-03-27     Finance
# 7      Simon    632.80  2013-07-30  Operations