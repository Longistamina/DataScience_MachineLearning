'''
1. TibbleFrame attributes:
    + `colnames`
    + `ncol`
    + `nrow`
    + `plot`

2. TibbleLazy attributes:
    + `colnames`
'''

import tidypyrs as tp

tf = tp.TibbleFrame(
    x = [1, 3, 5, 7],
    y = [2., 4., 6., 9.],
    z = ["a", "b", "c", "d"]
)

tl = tf.lazy()

# ===============================================
# 1. TibbleFrame attributes
# ===============================================

##------------##
## `colnames` ##
##------------##

print(tf.colnames)
# shape: (3,)
# Series: '' [str]
# [
# 	"x"
# 	"y"
# 	"z"
# ]

##--------##
## `ncol` ##
##--------##

print(tf.ncol)
# 3

##--------##
## `nrow` ##
##--------##

print(tf.nrow)
# 4

##--------##
## `plot` ##
##--------##

print(tf.plot)
# <polars.dataframe.plotting.DataFramePlot object at 0x7f83a0339010>
'''Use for polars plotting utilities'''

# ===============================================
# 2. TibbleLazy attributes
# ===============================================

##------------##
## `colnames` ##
##------------##

print(tl.colnames)
# shape: (3,)
# Series: '' [str]
# [
# 	"x"
# 	"y"
# 	"z"
# ]
