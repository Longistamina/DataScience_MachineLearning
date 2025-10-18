'''
1. Sorting
   + dr.arrange()
   + dr.arrange(dr.desc())
   + combine ascending and descending order

2. Ranking
   + dr.row_number()
   + dr.min_rank()
   + dr.dense_rank()
   + dr.percent_rank()
'''

import datar.all as dr
from datar import f

# Suppress all warnings
import warnings
warnings.filterwarnings("ignore")

########################

tb_raw = dr.tibble(
        name = ["Alice", "Alice", "Alice", "Bob", "Bob", "Charlie"],
        subject = ["Math", "English", "Science", "Math", "English", "Math"],
        score = [85, 90, 78, 92, 88, 95],
        age = [20, 20, 20, 22, 22, 23],
)

print(tb_raw)
#       name  subject   score     age
#   <object> <object> <int64> <int64>
# 0    Alice     Math      85      20
# 1    Alice  English      90      20
# 2    Alice  Science      78      20
# 3      Bob     Math      92      22
# 4      Bob  English      88      22
# 5  Charlie     Math      95      23


#-------------------------------------------------------------------------------------------------------#
#------------------------------------------ 1. Sorting -------------------------------------------------#
#-------------------------------------------------------------------------------------------------------#

##################################
## Ascending order dr.arrange() ##
##################################

# Sort by one column
print(
    tb_raw 
    >> dr.arrange(f.score)
)
#       name  subject   score     age
#   <object> <object> <int64> <int64>
# 2    Alice  Science      78      20
# 0    Alice     Math      85      20
# 4      Bob  English      88      22
# 1    Alice  English      90      20
# 3      Bob     Math      92      22
# 5  Charlie     Math      95      23

# Sort by multiple columns
print(tb_raw >> dr.arrange(f.name, f.score))
#       name  subject   score     age
#   <object> <object> <int64> <int64>
# 2    Alice  Science      78      20
# 0    Alice     Math      85      20
# 1    Alice  English      90      20
# 4      Bob  English      88      22
# 3      Bob     Math      92      22
# 5  Charlie     Math      95      23

############################################
## Descending order dr.arrange(dr.desc()) ##
############################################

# Sort by one column
print(
    tb_raw 
    >> dr.arrange(dr.desc(f.score))
)
#       name  subject   score     age
#   <object> <object> <int64> <int64>
# 5  Charlie     Math      95      23
# 3      Bob     Math      92      22
# 1    Alice  English      90      20
# 4      Bob  English      88      22
# 0    Alice     Math      85      20
# 2    Alice  Science      78      20

# Sort by multiple columns
print(
    tb_raw 
    >> dr.arrange(dr.desc(f.age), dr.desc(f.score))
)
#       name  subject   score     age
#   <object> <object> <int64> <int64>
# 5  Charlie     Math      95      23
# 3      Bob     Math      92      22
# 4      Bob  English      88      22
# 1    Alice  English      90      20
# 0    Alice     Math      85      20
# 2    Alice  Science      78      20

############################################
## Combine ascending and descending order ##
############################################

print(
    tb_raw 
    >> dr.arrange(f.name, dr.desc(f.score))
)
#       name  subject   score     age
#   <object> <object> <int64> <int64>
# 1    Alice  English      90      20
# 0    Alice     Math      85      20
# 2    Alice  Science      78      20
# 3      Bob     Math      92      22
# 4      Bob  English      88      22
# 5  Charlie     Math      95      23


#-------------------------------------------------------------------------------------------------------#
#------------------------------------------- 2. Ranking ------------------------------------------------#
#-------------------------------------------------------------------------------------------------------#

#####################
## dr.row_number() ##
#####################
'''
BASIC RANKING

Assigns a unique sequential integer to rows within a partition of a result set, 
starting at 1 for the first row in each partition.

NOTE: dr.row_number() breaks ties, 
meaning even if two rows have the same ordering key value, they still get distinct consecutive numbers
'''

print(
    tb_raw 
    >> dr.mutate(row_num = dr.row_number(f.score))
)
#       name  subject   score     age   row_num
#   <object> <object> <int64> <int64> <float64>
# 0    Alice     Math      85      20       2.0
# 1    Alice  English      90      20       4.0
# 2    Alice  Science      78      20       1.0 (lowest score)
# 3      Bob     Math      92      22       5.0
# 4      Bob  English      88      22       3.0
# 5  Charlie     Math      95      23       6.0

print(
    tb_raw 
    >> dr.mutate(row_num = dr.row_number(f.age))
)
#       name  subject   score     age   row_num
#   <object> <object> <int64> <int64> <float64>
# 0    Alice     Math      85      20       1.0 (lowest age)
# 1    Alice  English      90      20       2.0 (lowest age, break tie by order of appearance)
# 2    Alice  Science      78      20       3.0
# 3      Bob     Math      92      22       4.0
# 4      Bob  English      88      22       5.0
# 5  Charlie     Math      95      23       6.0

#------
## highest score = 1
#------

print(
    tb_raw 
    >> dr.mutate(row_num = dr.row_number(dr.desc(f.score)))
)
#       name  subject   score     age   row_num
#   <object> <object> <int64> <int64> <float64>
# 0    Alice     Math      85      20       5.0
# 1    Alice  English      90      20       3.0
# 2    Alice  Science      78      20       6.0
# 3      Bob     Math      92      22       2.0
# 4      Bob  English      88      22       4.0
# 5  Charlie     Math      95      23       1.0 (highest score)

###################
## dr.min_rank() ##
###################
'''
Assigns the minimum rank to each row within a partition of a result set.
Ties receive the same rank, and the next rank(s) are skipped.
'''

print(
    tb_raw 
    >> dr.mutate(min_rank = dr.min_rank(f.score))
)
#       name  subject   score     age  min_rank
#   <object> <object> <int64> <int64> <float64>
# 0    Alice     Math      85      20       2.0
# 1    Alice  English      90      20       4.0
# 2    Alice  Science      78      20       1.0
# 3      Bob     Math      92      22       5.0
# 4      Bob  English      88      22       3.0
# 5  Charlie     Math      95      23       6.0

print(
    tb_raw 
    >> dr.mutate(min_rank = dr.min_rank(f.age))
)
#       name  subject   score     age  min_rank
#   <object> <object> <int64> <int64> <float64>
# 0    Alice     Math      85      20       1.0
# 1    Alice  English      90      20       1.0
# 2    Alice  Science      78      20       1.0
# 3      Bob     Math      92      22       4.0
# 4      Bob  English      88      22       4.0
# 5  Charlie     Math      95      23       6.0

#---
## highest age = 1
#---

print(
    tb_raw 
    >> dr.mutate(min_rank = dr.min_rank(dr.desc(f.age)))
)
#       name  subject   score     age  min_rank
#   <object> <object> <int64> <int64> <float64>
# 0    Alice     Math      85      20       4.0
# 1    Alice  English      90      20       4.0
# 2    Alice  Science      78      20       4.0
# 3      Bob     Math      92      22       2.0
# 4      Bob  English      88      22       2.0
# 5  Charlie     Math      95      23       1.0

#####################
## dr.dense_rank() ##
#####################
'''
Assigns ranks to rows within a partition of a result set, with no gaps in ranking values.
Ties receive the same rank, and the next rank is the next consecutive integer.
'''

print(
    tb_raw 
    >> dr.mutate(dense_rank = dr.dense_rank(f.age))
)
#       name  subject   score     age  dense_rank
#   <object> <object> <int64> <int64>   <float64>
# 0    Alice     Math      85      20         1.0
# 1    Alice  English      90      20         1.0
# 2    Alice  Science      78      20         1.0
# 3      Bob     Math      92      22         2.0
# 4      Bob  English      88      22         2.0
# 5  Charlie     Math      95      23         3.0

#---
## highest age = 1
#---

print(
    tb_raw 
    >> dr.mutate(dense_rank = dr.dense_rank(dr.desc(f.age)))
)
#       name  subject   score     age  dense_rank
#   <object> <object> <int64> <int64>   <float64>
# 0    Alice     Math      85      20         3.0
# 1    Alice  English      90      20         3.0
# 2    Alice  Science      78      20         3.0
# 3      Bob     Math      92      22         2.0
# 4      Bob  English      88      22         2.0
# 5  Charlie     Math      95      23         1.0

#######################
## dr.percent_rank() ##
#######################
'''
Calculates the relative rank of a row within a partition of a result set as a percentage.
The formula used is (rank - 1) / (total rows in the partition - 1).
The result is a value between 0 and 1, inclusive.
'''

print(
    tb_raw 
    >> dr.mutate(percent_rank = dr.percent_rank(f.score))
)
#       name  subject   score     age  percent_rank
#   <object> <object> <int64> <int64>     <float64>
# 0    Alice     Math      85      20           0.2
# 1    Alice  English      90      20           0.6
# 2    Alice  Science      78      20           0.0
# 3      Bob     Math      92      22           0.8
# 4      Bob  English      88      22           0.4
# 5  Charlie     Math      95      23           1.0

print(
    tb_raw 
    >> dr.mutate(percent_rank = dr.percent_rank(f.age))
)
#       name  subject   score     age  percent_rank
#   <object> <object> <int64> <int64>     <float64>
# 0    Alice     Math      85      20           0.0
# 1    Alice  English      90      20           0.0
# 2    Alice  Science      78      20           0.0
# 3      Bob     Math      92      22           0.6
# 4      Bob  English      88      22           0.6
# 5  Charlie     Math      95      23           1.0

#---
## highest age = 0
#---

print(
    tb_raw 
    >> dr.mutate(percent_rank = dr.percent_rank(dr.desc(f.age)))
)
#       name  subject   score     age  percent_rank
#   <object> <object> <int64> <int64>     <float64>
# 0    Alice     Math      85      20      1.000000
# 1    Alice  English      90      20      1.000000
# 2    Alice  Science      78      20      1.000000
# 3      Bob     Math      92      22      0.333333
# 4      Bob  English      88      22      0.333333
# 5  Charlie     Math      95      23      0.000000