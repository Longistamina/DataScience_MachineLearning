'''
1. split:
   + np.split(): by "number of sections", by "indices"
   + np.array_split()

2. np.repeat(arr, repeats): repeat elements of an array
   + Repeating with same count
   + Repeating with different counts

3. np.unique(arr): find the unique elements of an array
   + np.unique()
   + np.unique(return_counts=True)
'''

import numpy as np

arr = np.random.rand(3, 4, 5, 6)

# =========================================================================================
# 1. Split Operations
# =========================================================================================

##-----------------------------------------------##
## np.split(): Splitting by "number of sections" ##
##-----------------------------------------------##

print(
    np.split(ary=arr, indices_or_sections=2, axis=1)
)
# A list of 2 arrays whose shape is: [(3, 2, 5, 6), (3, 2, 5, 6)]

print(
    np.split(ary=arr, indices_or_sections=3, axis=-1)
)
# A list of 2 arrays whose shape is: [(3, 4, 5, 3), (3, 4, 5, 3)]

##------------------------------------##
## np.split(): Splitting by "indices" ##
##------------------------------------##

print(
    [a.shape for a in
    np.split(ary=arr, indices_or_sections=[1, 3], axis=2)]
)
# [(3, 4, 1, 6), (3, 4, 2, 6), (3, 4, 2, 6)]

##------------------##
## np.array_split() ##
##------------------##
'''
np.array_split() is similar to np.split(), but allows unequal splits.
If the array cannot be split evenly, it will not raise an error.
'''

print(
    [a.shape for a in
    np.array_split(ary=arr, indices_or_sections=3, axis=2)]
)
# [(3, 4, 2, 6), (3, 4, 2, 6), (3, 4, 1, 6)]

# =========================================================================================
# 2. np.repeat()
# =========================================================================================

##---------------------------##
## Repeating with same count ##
##---------------------------##

print(
    arr.repeat(repeats=2, axis=1).shape
)
# (3, 8, 5, 6)

##---------------------------------##
## Repeating with different counts ##
##---------------------------------##

print(
    arr.repeat(repeats=[1, 2, 3, 4, 5], axis=2).shape
)
# (3, 4, 15, 6)

##-----------------##
## Use np.repeat() ##
##-----------------##

print(
    np.repeat(a=arr, repeats=[2, 2, 3], axis=0).shape
)
# (7, 4, 5, 6)

# =========================================================================================
# 3. np.unique()
# =========================================================================================

matrix = np.array([[5, 2, 8, 2],
                   [5, 7, 5, 8],
                   [2, 7, 8, 5]])
print(matrix)
# [[5 2 8 2]
#  [5 7 5 8]
#  [2 7 8 5]]

##-------------##
## np.unique() ##
##-------------##

unique_elements = np.unique(matrix)
print(unique_elements)
# [2 5 7 8]
'''Returns a sorted 1D array of unique elements from the matrix.'''

##-------------------------------##
## np.unique(return_counts=True) ##
##-------------------------------##

unique_elements, counts = np.unique(matrix, return_counts=True)

print(unique_elements)
# [2 5 7 8]

print(counts)
# [3 4 2 3]

'''
Element 2 appears 3 times,
Element 5 appears 4 times,
Element 7 appears 2 times,
Element 8 appears 3 times.
'''

# Create a count dictionary
count_dict = dict(zip(unique_elements, counts))
print(count_dict)
# {2: 3, 5: 4, 7: 2, 8: 3}

##---------------------##
## np.unique(axis=...) ##
##---------------------##

yin_yang = np.random.choice(a=[0, 1], size=(10, 2))
print(yin_yang)
# [[0 0]
#  [0 1]
#  [0 0]
#  [1 0]
#  [0 0]
#  [1 0]
#  [1 1]
#  [1 0]
#  [1 0]
#  [1 0]]

print(
    np.unique(yin_yang, axis=0)
)
# [[0 0]
#  [0 1]
#  [1 0]
#  [1 1]]
