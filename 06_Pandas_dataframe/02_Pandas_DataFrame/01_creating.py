'''
There are many ways to create a DataFrame in Pandas. Here are some of the most common methods:

1. From a dictionary of series: {"column_name": pd.Series(data, index=index)}

2. From a dictionary of lists or ndarrays: {"column_name": list_or_ndarray}

3. From 2D-List or 2D-Array: [[row1], [row2], ...] or np.array([[row1], [row2], ...])

4. From a structured or record array: np.array([(data1), (data2)], dtype=[("col1", type1), ("col2", type2)])

5. From a list of dictionaries: [{"col1": val1, "col2": val2}, ...]

6. From a dictionary of tuples: {("col1", "col2"): {("row1", "row2"): val, ...}, ...}

7. From a list of namedtuples: [namedtuple1, namedtuple2, ...]

8. From a list of dataclasses: [dataclass1, dataclass2, ...]

9. Other constructors: .from_dict(), .from_records()
'''

import pandas as pd
import numpy as np

#-------------------------------------------------------------------------------------------------------------#
#------------------------------------- 1. From a dictionary of series ----------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

##################
## Step-by-step ##
##################

data_dict = {
    "one": pd.Series([1.0, 2.0, 3.0], index=["a", "b", "c"]),
    "two": pd.Series([1.0, 2.0, 3.0, 4.0], index=["a", "b", "c", "d"]),
}

df = pd.DataFrame(data_dict)
print(df)
#    one  two
# a  1.0  1.0
# b  2.0  2.0
# c  3.0  3.0
# d  NaN  4.0
'''Here, the dictionary keys become the column names'''

#####################
## Shorter version ##
#####################

df = pd.DataFrame(
    data ={
        "one": pd.Series([1.0, 2.0, 3.0], index=["a", "b", "c"]),
        "two": pd.Series([1.0, 2.0, 3.0, 4.0], index=["a", "b", "c", "d"]),
    }
)

print(df)
#    one  two
# a  1.0  1.0
# b  2.0  2.0
# c  3.0  3.0
# d  NaN  4.0


#-------------------------------------------------------------------------------------------------------------#
#--------------------------------- 2. From a dictionary of lists or ndarrays ---------------------------------#
#-------------------------------------------------------------------------------------------------------------#

################
## from lists ##
################

df = pd.DataFrame(
    data = {
        "column_1": [1, 3, 5, 7],
        "column_2": [2.0, 4.0, 6.0, 8.0],
        "column_3": ["a", "b", "c", "d"],
    }
)

print(df)
#    column_1  column_2 column_3
# 0         1       2.0        a
# 1         3       4.0        b
# 2         5       6.0        c
# 3         7       8.0        d

###################
## from ndarrays ##
###################

df = pd.DataFrame(
    data = {
        "column_1": np.array([1.5, 3.2, 5.7, 6.8]),
        "column_2": np.array([2, 4.9, 2.3, 1.2]),
    }
)

print(df)
#    column_1  column_2
# 0       1.5       2.0
# 1       3.2       4.9
# 2       5.7       2.3
# 3       6.8       1.2

##################
## Advanced way ##
##################

df_score = pd.DataFrame(
    data = {
        "name": ["Alice"]*3 + ["Susan"]*3,
        "subject": ["Math", "Science", "English"]*2,
        "score": np.array([85, 90, 88, 92, 95, 89]),
    }
)

print(df_score)
#     name  subject  score
# 0  Alice     Math     85
# 1  Alice  Science     90
# 2  Alice  English     88
# 3  Susan     Math     92
# 4  Susan  Science     95
# 5  Susan  English     89


#-------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 3. From 2D-List or 2D-Array -----------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

##################
## from 2D-List ##
##################

df_3d_list = pd.DataFrame(
    data = [
        [1, 2.0, "a"],
        [3, 4.0, "b"],
        [5, 6.0, "c"],
        [7, 8.0, "d"]
    ],
    columns = ["column_1", "column_2", "column_3"],
    index = ["row_1", "row_2", "row_3", "row_4"]
)

print(df_3d_list)
#        column_1  column_2 column_3
# row_1         1       2.0        a
# row_2         3       4.0        b

# row_3         5       6.0        c
# row_4         7       8.0        d

###################
## from 2D-Array ##
###################

df_3d_array = pd.DataFrame(
    data = np.array([
        [1.5, 2, "a"],
        [3.2, 4, "b"],
        [5.7, 6, "c"],
        [6.8, 8, "d"]
    ]),
    columns = ["col_1", "col_2", "col_3"],
    index = ["idx_1", "idx_2", "idx_3", "idx_4"]
)

print(df_3d_array)
#       col_1 col_2 col_3
# idx_1   1.5     2     a
# idx_2   3.2     4     b
# idx_3   5.7     6     c
# idx_4   6.8     8     d


#-------------------------------------------------------------------------------------------------------------#
#--------------------------------- 4. From a structured or record array --------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

# Create an empty structured record
record = np.zeros(
    shape = (2,), # 1D array with 2 elements
    dtype = [("A", "i4"), ("B", "f4"), ("C", "a10")] # Define the data types for each field "A", "B", "C"
)                                                    # "i4" means 4-byte integer, 
                                                     # "f4" means 4-byte float, 
                                                     # "a10" means string of length 10 (bytes
print(record)                          
# [(0, 0., b'') (0, 0., b'')]

# Fill the structured record with data
record[:] = [(1, 2.0, "Hello"), (2, 3.0, "World")]
print(record)
# [(1, 2., b'Hello') (2, 3., b'World')]

# Create DataFrame from the structured record
df = pd.DataFrame(record, index=["first", "second"])
print(df)
#         A    B         C
# first   1  2.0  b'Hello'
# second  2  3.0  b'World'


#-------------------------------------------------------------------------------------------------------------#
#------------------------------------- 5. From a list of dictionaries ----------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

##################
## Step-by-step ##
##################

list_of_dicts = [
    {"a": 1, "b": 2}, 
    {"a": 5, "b": 10, "c": 20}
]

df = pd.DataFrame(list_of_dicts, index=["row_1", "row_2"])
print(df)
#        a   b     c
# row_1  1   2   NaN
# row_2  5  10  20.0


#####################
## Shorter version ##
#####################

df = pd.DataFrame(
    data = [
        {"a": 1.4, "b": 2.3}, 
        {"a": 5, "b": 10, "c": 20}
    ],
    index = ["row_1", "row_2"]
)

print(df)
#          a     b     c
# row_1  1.4   2.3   NaN
# row_2  5.0  10.0  20.0


#-------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 6. From a dictionary of tuples --------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

df = pd.DataFrame(
    {
        ("a", "b"): {("A", "B"): 1, ("A", "C"): 2},
        ("a", "a"): {("A", "C"): 3, ("A", "B"): 4},
        ("a", "c"): {("A", "B"): 5, ("A", "C"): 6},
        ("b", "a"): {("A", "C"): 7, ("A", "B"): 8},
        ("b", "b"): {("A", "D"): 9, ("A", "B"): 10},
    }
)

print(df)
#        a              b      
#        b    a    c    a     b
# A B  1.0  4.0  5.0  8.0  10.0
#   C  2.0  3.0  6.0  7.0   NaN
#   D  NaN  NaN  NaN  NaN   9.0


#-------------------------------------------------------------------------------------------------------------#
#------------------------------------- 7. From a list of namedtuples -----------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

from collections import namedtuple

###############
## 2D points ##
###############

point_2d = namedtuple("Point", "x y")

df = pd.DataFrame(
    data = [point_2d(0, 0), point_2d(1, 2), point_2d(2, 4), point_2d(3, 6)],

)

print(df)
#    x  y
# 0  0  0
# 1  1  2
# 2  2  4
# 3  3  6

###############
## 3D points ##
###############

point_3d = namedtuple("Point3D", "x y z")

df = pd.DataFrame(
    data = [point_3d(0, 0, 0), point_3d(1, 2, 3), point_3d(2, 4, 6), point_3d(3, 6, 9)],
)

print(df)
#    x  y  z
# 0  0  0  0
# 1  1  2  3
# 2  2  4  6
# 3  3  6  9


#-------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 8. From a list of dataclasses ---------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

from dataclasses import make_dataclass

point_2d = make_dataclass("Point", [("x", int), ("y", int)])

df = pd.DataFrame(
    data = [point_2d(0, 0), point_2d(3, 5), point_2d(4, 7), point_2d(2, 2)],
)

print(df)
#    x  y
# 0  0  0
# 1  3  5
# 2  4  7
# 3  2  2


#-------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 9. Other constructors -----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

##################
## .from_dict() ##
##################

df = pd.DataFrame.from_dict(
    data = dict([("A", [1, 2, 3]), ("B", [4, 5, 6])])
)
print(df)
#    A  B
# 0  1  4
# 1  2  5
# 2  3  6

df = pd.DataFrame.from_dict(
    data = dict([("A", [1, 2, 3]), ("B", [4, 5, 6])]),
    orient = "index", # "index" means the keys of the dictionary will be the row indices
    columns = ["one", "two", "three"]
)
print(df)
#    one  two  three
# A    1    2      3
# B    4    5      6

#####################
## .from_records() ##
#####################

# Create an empty structured record
record = np.zeros(
    shape = (2,), # 1D array with 2 elements
    dtype = [("A", "i4"), ("B", "f4"), ("C", "a10")] # Define the data types for each field "A", "B", "C"
)                                                    # "i4" means 4-byte integer, 
                                                     # "f4" means 4-byte float, 
                                                     # "a10" means string of length 10 (bytes

# Fill the structured record with data
record[:] = [(1, 2.0, "Hello"), (2, 3.0, "World")]


# Use .from_records() to create DataFrame
df = pd.DataFrame.from_records(data=record)
print(df)
#    A    B         C
# 0  1  2.0  b'Hello'
# 1  2  3.0  b'World'


# Use .from_records() to create with index=
df = pd.DataFrame.from_records(
    data = record,
    index = ["first", "second"]
)
print(df)
#         A    B         C
# first   1  2.0  b'Hello'
# second  2  3.0  b'World'


# Specify index from a specific column
df = pd.DataFrame.from_records(
    data = record,
    index = "C" # Use column "C" as the index
)
print(df)
#           A    B
# C               
# b'Hello'  1  2.0
# b'World'  2  3.0