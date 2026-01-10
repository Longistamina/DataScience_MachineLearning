'''
1. split:
   + np.split() by "number of sections"
   + np.split() by "indices"
   + np.array_split(): supports unequal splits

2. np.repeat(arr, repeats): repeat elements of an array
   + Repeating with same count
   + Repeating with different counts

3. np.unique(arr): find the unique elements of an array
   + np.unique()
   + np.unique(return_counts=True)
'''

import numpy as np


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 1. np.split() -----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

np.random.seed(0)
vector = np.random.randint(1, 11, size=9)
print(vector)
# [ 6  1  4  4  8 10  4  6  3]

#######################################
## np.split() by "number of sections ##
#######################################

split_vectors = np.split(ary=vector, indices_or_sections=3)

print(split_vectors)
# [array([6, 1, 4]), array([4, 8, 4]), array([6, 3, 5])]
'''Returns a list of 3 arrays, each containing 3 elements.'''

for i, vec in enumerate(split_vectors):
    print(f"Vector {i+1}: {vec}")
# Vector 1: [6 1 4]
# Vector 2: [4 8 4]
# Vector 3: [6 3 5]

'''NOTE: If the array cannot be split evenly, a ValueError will be raised.'''

#############################
## np.split() by "indices" ##
#############################

split_vectors = np.split(ary=vector, indices_or_sections=[2, 5])

print(split_vectors)
# [array([6, 1]), array([4, 4, 8]), array([10,  4,  6,  3])]

for i, vec in enumerate(split_vectors):
    print(f"Vector {i+1}: {vec}")
# Vector 1: [6 1]
# Vector 2: [4 4 8]
# Vector 3: [10  4  6  3]
'''Using specified indices allows unequal splits.'''

#############################################
## np.array_split() supports unequal split ##
#############################################

vector_uneven = np.array([1, 2, 3, 4, 5, 6, 7])

split_vectors = np.array_split(ary=vector_uneven, indices_or_sections=3)

print(split_vectors)
# [array([1, 2, 3]), array([4, 5]), array([6, 7])]
'''Returns a list of 3 arrays with unequal sizes.'''

for i, vec in enumerate(split_vectors):
    print(f"Vector {i+1}: {vec}")
# Vector 1: [1 2 3]
# Vector 2: [4 5]
# Vector 3: [6 7]
'''NOTE: np.array_split() handles uneven divisions gracefully, unlike np.split().'''


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 2. arr.repeat() ---------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

vector = np.array([3, 6, 9])

###############################
## Repeating with same count ##
###############################

print(vector.repeat(repeats=2))
# [3 3 6 6 9 9]

#####################################
## Repeating with different counts ##
#####################################

print(vector.repeat(repeats=[1, 2, 3]))
# [3 6 6 9 9 9]
'''
The 1st element (3) is repeated once,
the 2nd element (6) is repeated twice,
the 3rd element (9) is repeated three times.
'''


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 3. np.unique() ----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

vector_npy = np.load('03_Vector_Matrix_Sparse/01_Vector_1D/data/timeseries.npy')
print(vector_npy)
# [49. 49. 49. 49. 49. 50. 50. 50. 51. 56. 61. 66. 70. 72. 74. 76. 75. 73.
#  70. 67. 64. 62. 60. 59. 57. 56. 54. 53. 52. 52. 51. 50. 50. 49. 49. 49.
#  48. 48. 48. 48. 48. 48. 48. 47. 47. 47. 47. 47. 47. 47. 48. 48. 48. 48.
#  48. 48. 48. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49.
#  49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 50. 50. 50.
#  50. 50. 50. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51.
#  51. 51. 51. 50. 50. 50. 51. 51. 51. 51. 51. 51. 50. 50. 50. 50. 51. 51.
#  51. 51. 51. 51. 51. 51. 52. 52. 52. 52. 51. 51. 51. 51. 51. 51. 51. 51.
#  51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 53. 53. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.]

#################
## np.unique() ##
#################

unique_elements = np.unique(vector_npy)

print(unique_elements)
# [47. 48. 49. 50. 51. 52. 53. 54. 56. 57. 59. 60. 61. 62. 64. 66. 67. 70.
#  72. 73. 74. 75. 76.]

###################################
## np.unique(return_counts=True) ##
###################################

unique_elements, counts = np.unique(vector_npy, return_counts=True)

print(unique_elements)
# [47. 48. 49. 50. 51. 52. 53. 54. 56. 57. 59. 60. 61. 62. 64. 66. 67. 70.
#  72. 73. 74. 75. 76.]

print(counts)
# [  7  14  38  18  59 148   3   1   2   1   1   1   1   1   1   1   1   2
#    1   1   1   1   1]