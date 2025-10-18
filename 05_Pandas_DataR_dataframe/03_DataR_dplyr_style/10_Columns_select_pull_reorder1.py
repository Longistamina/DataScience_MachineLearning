'''
1. dr.select() - Select columns
   + Normal usage: dr.select(f.col1, f.col2), dr.select(f['col1'], f['col2']), dr.select(f[['col1', 'col2']])
   + Range selection: dr.select(f[f.col1:f.col4]) (the end column is excluded)
   + Using index numbers: dr.select(f[0, 2, 4]) or dr.select(f[0:4]) (the end index is excluded)
   + Using string function: dr.select(dr.starts_with("col")), dr.select(dr.ends_with("col")), dr.select(dr.contains("col"))
   + Exclusive selection: dr.select(~f.col1, ~f.col2), dr.select(~f[f.col2:f.col4]), dr.select(~f[1, 3]), dr.select(~f[0:3])

2. dr.pull() - Pull a single column as a Series
   + Demo: dr.pull(f.col)
   + Assign to a variable: var = dr.pull(f.col)

3. Reorder columns using dr.select(): dr.select(f.col3, f.col1, f.col2)
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


#----------------------------------------------------------------------------------------------------------#
#--------------------------------- 1. dr.select() - Select columns ----------------------------------------#
#----------------------------------------------------------------------------------------------------------#

##################
## Normal usage ##
##################

print(
    tb_emp
    >> dr.select(f.name, f.salary)
)
#        name    salary
#    <object> <float64>
# 0      Rick    623.30
# 1       Dan    515.20
# 2  Michelle    611.00
# 3      Ryan    729.00
# 4      Gary    843.25
# 5      Nina    578.00
# 6     Simon    632.80
# 7      Guru    722.50

print(
    tb_emp
    >> dr.select(f['name'], f['salary'])
)
#        name    salary
#    <object> <float64>
# 0      Rick    623.30
# 1       Dan    515.20
# 2  Michelle    611.00
# 3      Ryan    729.00
# 4      Gary    843.25
# 5      Nina    578.00
# 6     Simon    632.80
# 7      Guru    722.50

print(
    tb_emp
    >> dr.select(f[['name', 'salary']])
)
#        name    salary
#    <object> <float64>
# 0      Rick    623.30
# 1       Dan    515.20
# 2  Michelle    611.00
# 3      Ryan    729.00
# 4      Gary    843.25
# 5      Nina    578.00
# 6     Simon    632.80
# 7      Guru    722.50

#####################
## Range selection ##
#####################

print(
    tb_emp
    >> dr.select(f[f.id:f.start_date]) # The start_date column is excluded
)
#        id      name    salary
#   <int64>  <object> <float64>
# 0       1      Rick    623.30
# 1       2       Dan    515.20
# 2       3  Michelle    611.00
# 3       4      Ryan    729.00
# 4       5      Gary    843.25
# 5       6      Nina    578.00
# 6       7     Simon    632.80
# 7       8      Guru    722.50

#########################
## Using index numbers ##
#########################

print(
    tb_emp
    >> dr.select(f[0, 2, 4]) # Select the 1st, 3rd, and 5th columns
)
#        id    salary        dept
#   <int64> <float64>    <object>
# 0       1    623.30          IT
# 1       2    515.20  Operations
# 2       3    611.00          IT
# 3       4    729.00          HR
# 4       5    843.25     Finance
# 5       6    578.00          IT
# 6       7    632.80  Operations
# 7       8    722.50     Finance

print(
    tb_emp
    >> dr.select(f[0:4]) # Select the 1st to 5th columns (the 5th column is excluded)
)
#        id      name    salary  start_date
#   <int64>  <object> <float64>    <object>
# 0       1      Rick    623.30  2012-01-01
# 1       2       Dan    515.20  2013-09-23
# 2       3  Michelle    611.00  2014-11-15
# 3       4      Ryan    729.00  2014-05-11
# 4       5      Gary    843.25  2015-03-27
# 5       6      Nina    578.00  2013-05-21
# 6       7     Simon    632.80  2013-07-30
# 7       8      Guru    722.50  2014-06-17

###########################
## Using string function ##
###########################

print(
    tb_emp
    >> dr.select(dr.starts_with("s")) # Select columns starting with "s"
)
#      salary  start_date
#   <float64>    <object>
# 0    623.30  2012-01-01
# 1    515.20  2013-09-23
# 2    611.00  2014-11-15
# 3    729.00  2014-05-11
# 4    843.25  2015-03-27
# 5    578.00  2013-05-21
# 6    632.80  2013-07-30
# 7    722.50  2014-06-17

print(
    tb_emp
    >> dr.select(dr.ends_with("e")) # Select columns ending with "e"
)
#        name  start_date
#    <object>    <object>
# 0      Rick  2012-01-01
# 1       Dan  2013-09-23
# 2  Michelle  2014-11-15
# 3      Ryan  2014-05-11
# 4      Gary  2015-03-27
# 5      Nina  2013-05-21
# 6     Simon  2013-07-30
# 7      Guru  2014-06-17

print(
    tb_emp
    >> dr.select(dr.contains("ar")) # Select columns containing "ar"
)
#      salary  start_date
#   <float64>    <object>
# 0    623.30  2012-01-01
# 1    515.20  2013-09-23
# 2    611.00  2014-11-15
# 3    729.00  2014-05-11
# 4    843.25  2015-03-27
# 5    578.00  2013-05-21
# 6    632.80  2013-07-30
# 7    722.50  2014-06-17

print(
    tb_emp
    >> dr.select(dr.starts_with("s") & dr.ends_with("e")) # Select columns starting with "s" AND ending with "e"
)
#    start_date
#      <object>
# 0  2012-01-01
# 1  2013-09-23
# 2  2014-11-15
# 3  2014-05-11
# 4  2015-03-27
# 5  2013-05-21
# 6  2013-07-30
# 7  2014-06-17

print(
    tb_emp
    >> dr.select(dr.starts_with("n") | dr.starts_with("s")) # Select columns starting with "n" OR starting with "s"
)
#        name    salary  start_date
#    <object> <float64>    <object>
# 0      Rick    623.30  2012-01-01
# 1       Dan    515.20  2013-09-23
# 2  Michelle    611.00  2014-11-15
# 3      Ryan    729.00  2014-05-11
# 4      Gary    843.25  2015-03-27
# 5      Nina    578.00  2013-05-21
# 6     Simon    632.80  2013-07-30
# 7      Guru    722.50  2014-06-17

#########################
## Exclusive selection ##
#########################

print(
    tb_emp
    >> dr.select(~f.start_date, ~f.dept) # Exclude the start_date and dept columns
)
#        id      name    salary
#   <int64>  <object> <float64>
# 0       1      Rick    623.30
# 1       2       Dan    515.20
# 2       3  Michelle    611.00
# 3       4      Ryan    729.00
# 4       5      Gary    843.25
# 5       6      Nina    578.00
# 6       7     Simon    632.80
# 7       8      Guru    722.50

print(
    tb_emp
    >> dr.select(~f[f.salary:f.dept])
)
#        id      name        dept
#   <int64>  <object>    <object>
# 0       1      Rick          IT
# 1       2       Dan  Operations
# 2       3  Michelle          IT
# 3       4      Ryan          HR
# 4       5      Gary     Finance
# 5       6      Nina          IT
# 6       7     Simon  Operations
# 7       8      Guru     Finance

'''
the f.dept is not in f[f.salary:f.dept], so it is not excluded by ~f[f.salary:f.dept]
'''

print(
    tb_emp
    >> dr.select(~f[1, 3]) # Exclude the 2nd and 4th columns
)
#        id    salary        dept
#   <int64> <float64>    <object>
# 0       1    623.30          IT
# 1       2    515.20  Operations
# 2       3    611.00          IT
# 3       4    729.00          HR
# 4       5    843.25     Finance
# 5       6    578.00          IT
# 6       7    632.80  Operations
# 7       8    722.50     Finance

print(
    tb_emp
    >> dr.select(~f[0:3])
)
#    start_date        dept
#      <object>    <object>
# 0  2012-01-01          IT
# 1  2013-09-23  Operations
# 2  2014-11-15          IT
# 3  2014-05-11          HR
# 4  2015-03-27     Finance
# 5  2013-05-21          IT
# 6  2013-07-30  Operations
# 7  2014-06-17     Finance

print(
    tb_emp
    >> dr.select(~(dr.starts_with("s") | dr.starts_with("d"))) # Exclude columns starting with "s" OR starting with "d"
)
#        id      name
#   <int64>  <object>
# 0       1      Rick
# 1       2       Dan
# 2       3  Michelle
# 3       4      Ryan
# 4       5      Gary
# 5       6      Nina
# 6       7     Simon
# 7       8      Guru

#----------------------------------------------------------------------------------------------------------#
#---------------------------- 2. dr.pull() - Pull a single column as a Series -----------------------------#
#----------------------------------------------------------------------------------------------------------#

##########
## Demo ##
##########

print(
    tb_emp
    >> dr.pull(f.name)
)
# 0        Rick
# 1         Dan
# 2    Michelle
# 3        Ryan
# 4        Gary
# 5        Nina
# 6       Simon
# 7        Guru
# Name: name, dtype: object

##########################
## Assign to a variable ##
##########################

salary = (
    tb_emp
    >> dr.pull(f.salary)
)
print(salary)
# 0    623.30
# 1    515.20
# 2    611.00
# 3    729.00
# 4    843.25
# 5    578.00
# 6    632.80
# 7    722.50
# Name: salary, dtype: float64


#----------------------------------------------------------------------------------------------------------#
#------------------------------------ 3. Reorder columns using dr.select() --------------------------------#
#----------------------------------------------------------------------------------------------------------#

print(
    tb_emp
    >> dr.select(f.dept, f.name, f.salary)
)
#          dept      name    salary
#      <object>  <object> <float64>
# 0          IT      Rick    623.30
# 1  Operations       Dan    515.20
# 2          IT  Michelle    611.00
# 3          HR      Ryan    729.00
# 4     Finance      Gary    843.25
# 5          IT      Nina    578.00
# 6  Operations     Simon    632.80
# 7     Finance      Guru    722.50