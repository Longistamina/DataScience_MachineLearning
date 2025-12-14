'''
Boolean Indexing Boolean Filtering is a powerful technique
that allows you to filter data based on specific conditions. 

###############################

Flow of contents:

0. Mask: a boolean array created using a condition

1. Single Condition Examples:
   + Logic Operators: >, <, >=, <=, ==, !=
   + np.isin()

2. Negation of Condition: ~ (tilde) operator

3. Combine Multiple Conditions:
   + & (and),
   + | (or)
   + Combine & and |

4. Boolean Compression: arr.compress(mask)
'''

import numpy as np

vector = np.load('03_Vector_Matrix_Sparse/01_Vector_1D/data/timeseries.npy')

print(vector[:21])
# [49. 49. 49. 49. 49. 50. 50. 50. 51. 56. 61. 66. 70. 72. 74. 76. 75. 73.
#  70. 67. 64.]


#--------------------------------------------------------------------------------------------------------#
#-------------------------- 0. Mask: a boolean array created using a condition --------------------------#
#--------------------------------------------------------------------------------------------------------#

mask = vector > 70
print(mask[:21])
# [False False False False False False False False False False False False
#  False  True  True  True  True  True False False False]

print(vector <= 50)
# [ True  True  True  True  True  True  True  True False False False False
#  False False False False False False False False False False False False
#  False False False False False False False  True  True  True  True  True
#   True  True  True  True  True  True  True  True  True  True  True  True
#   True  True  True  True  True  True  True  True  True  True  True  True
#   True  True  True  True  True  True  True  True  True  True  True  True
#   True  True  True  True  True  True  True  True  True  True  True  True
#   True  True  True  True  True  True  True  True  True False False False
#  False False False False False False False False False False False False
#  False False False  True  True  True False False False False False False
#   True  True  True  True False False False False False False False False
#  False False False False False False False False False False False False
#  False False False False False False False False False False False False
#  False False False False False False False False False False False False
#  False False False False False False False False False False False False
#  False False False False False False False False False False False False
#  False False False False False False False False False False False False
#  False False False False False False False False False False False False
#  False False False False False False False False False False False False
#  False False False False False False False False False False False False
#  False False False False False False False False False False False False
#  False False False False False False False False False False False False
#  False False False False False False False False False False False False
#  False False False False False False False False False False False False
#  False False False False False False False False False False False False
#  False False False False False]

'''
So Mask is a boolean array where each element indicates whether the corresponding
element in the original vector satisfies the given condition (True) or not (False).
'''


#--------------------------------------------------------------------------------------------------------#
#------------------------------ 1. Single Condition Examples: np.isin() ---------------------------------#
#--------------------------------------------------------------------------------------------------------#

######################
## > (greater than) ##
######################

mask_gt_70 = vector > 70

print(vector[mask_gt_70])
# [72. 74. 76. 75. 73.]

print(vector[vector > 70])
# [72. 74. 76. 75. 73.]

###################
## < (less than) ##
###################

print(vector[vector < 49])
# [48. 48. 48. 48. 48. 48. 48. 47. 47. 47. 47. 47. 47. 47. 48. 48. 48. 48.
#  48. 48. 48.]

'''
>= (greater than or equal to)
<= (less than or equal to)

They work similarly to > and < but include equality.
'''

################
## == (equal) ##
################

print(vector[vector == 56])
# [56. 56.]

####################
## != (not equal) ##
####################

print(vector[vector != 49])
# [50. 50. 50. 51. 56. 61. 66. 70. 72. 74. 76. 75. 73. 70. 67. 64. 62. 60.
#  59. 57. 56. 54. 53. 52. 52. 51. 50. 50. 48. 48. 48. 48. 48. 48. 48. 47.
#  47. 47. 47. 47. 47. 47. 48. 48. 48. 48. 48. 48. 48. 50. 50. 50. 50. 50.
#  50. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51.
#  51. 50. 50. 50. 51. 51. 51. 51. 51. 51. 50. 50. 50. 50. 51. 51. 51. 51.
#  51. 51. 51. 51. 52. 52. 52. 52. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51.
#  51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 53. 53. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.]

###############
## np.isin() ##
###############
'''
np.isin() checks whether each element in your input array is present in a test array, 
returning a boolean array with the same shape

Key Parameters for 1D Arrays
# element: Your 1D numeric array to check
# test_elements: Values to search for (can be list, array, or other iterable)
# assume_unique: Set True if both arrays have unique values for faster computation
# invert: Set True to find elements NOT in test_elements
'''

test_values = [50, 56, 70]
mask_isin = np.isin(element=vector, test_elements=test_values)
print(vector[mask_isin])
# [50. 50. 50. 56. 70. 70. 56. 50. 50. 50. 50. 50. 50. 50. 50. 50. 50. 50.
#  50. 50. 50. 50.]

print(vector[np.isin(vector, [49, 50, 52], invert=True)]) # Negation of Condition (values NOT in test_elements)
# [51. 56. 61. 66. 70. 72. 74. 76. 75. 73. 70. 67. 64. 62. 60. 59. 57. 56.
#  54. 53. 51. 48. 48. 48. 48. 48. 48. 48. 47. 47. 47. 47. 47. 47. 47. 48.
#  48. 48. 48. 48. 48. 48. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51.
#  51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51.
#  51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51.
#  51. 51. 51. 51. 51. 51. 51. 51. 51. 53. 53.]


#--------------------------------------------------------------------------------------------------------#
#--------------------------- 2. Negation of Condition: ~ (tilde) operator -------------------------------#
#--------------------------------------------------------------------------------------------------------#

print(vector[~(vector >= 52)])
# [49. 49. 49. 49. 49. 50. 50. 50. 51. 51. 50. 50. 49. 49. 49. 48. 48. 48.
#  48. 48. 48. 48. 47. 47. 47. 47. 47. 47. 47. 48. 48. 48. 48. 48. 48. 48.
#  49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49.
#  49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 50. 50. 50. 50. 50. 50.
#  51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51.
#  50. 50. 50. 51. 51. 51. 51. 51. 51. 50. 50. 50. 50. 51. 51. 51. 51. 51.
#  51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51.
#  51. 51. 51. 51. 51. 51. 51. 51. 51. 51.]
'''Values that are NOT greater than or equal to 52'''

print(vector[~np.isin(vector, [49, 52, 70])])
# [50. 50. 50. 51. 56. 61. 66. 72. 74. 76. 75. 73. 67. 64. 62. 60. 59. 57.
#  56. 54. 53. 51. 50. 50. 48. 48. 48. 48. 48. 48. 48. 47. 47. 47. 47. 47.
#  47. 47. 48. 48. 48. 48. 48. 48. 48. 50. 50. 50. 50. 50. 50. 51. 51. 51.
#  51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 50. 50. 50.
#  51. 51. 51. 51. 51. 51. 50. 50. 50. 50. 51. 51. 51. 51. 51. 51. 51. 51.
#  51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51.
#  51. 51. 51. 51. 51. 51. 51. 53. 53.]
'''Values that are NOT in the list [49, 52, 70]'''


#--------------------------------------------------------------------------------------------------------#
#----------------------- 3. Combine Multiple Conditions: & (and), | (or) --------------------------------#
#--------------------------------------------------------------------------------------------------------#

######################
## & (and) operator ##
######################

print(vector[(vector > 52) & (vector < 60)])
# [56. 59. 57. 56. 54. 53. 53. 53.]

#####################
## | (or) operator ##
#####################

print(vector[(vector < 49) | (vector > 75)])
# [76. 48. 48. 48. 48. 48. 48. 48. 47. 47. 47. 47. 47. 47. 47. 48. 48. 48.
#  48. 48. 48. 48.]

#####################
## Combine & and | ##
#####################

print(vector[((vector >= 60) & (vector <= 70)) | (vector == 48)])
# [61. 66. 70. 70. 67. 64. 62. 60. 48. 48. 48. 48. 48. 48. 48. 48. 48. 48.
#  48. 48. 48. 48.]


#--------------------------------------------------------------------------------------------------------#
#----------------------------- 4. Boolean Compression: arr.compress(mask) -------------------------------#
#--------------------------------------------------------------------------------------------------------#

print(vector.compress(vector > 70))
# [72. 74. 76. 75. 73.]

print(vector.compress(((vector >= 60) & (vector <= 70)) | (vector == 48)))
# [61. 66. 70. 70. 67. 64. 62. 60. 48. 48. 48. 48. 48. 48. 48. 48. 48. 48.
# 48. 48. 48. 48.]

print(vector.compress(np.isin(vector, [48, 50, 51])))
# [50. 50. 50. 51. 51. 50. 50. 48. 48. 48. 48. 48. 48. 48. 48. 48. 48. 48.
#  48. 48. 48. 50. 50. 50. 50. 50. 50. 51. 51. 51. 51. 51. 51. 51. 51. 51.
#  51. 51. 51. 51. 51. 51. 51. 51. 51. 50. 50. 50. 51. 51. 51. 51. 51. 51.
#  50. 50. 50. 50. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51.
#  51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51.
#  51.]

print(vector.compress(~np.isin(vector, [49, 52, 70])))
# [50. 50. 50. 51. 56. 61. 66. 72. 74. 76. 75. 73. 67. 64. 62. 60. 59. 57.
#  56. 54. 53. 51. 50. 50. 48. 48. 48. 48. 48. 48. 48. 47. 47. 47. 47. 47.
#  47. 47. 48. 48. 48. 48. 48. 48. 48. 50. 50. 50. 50. 50. 50. 51. 51. 51.
#  51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 50. 50. 50.
#  51. 51. 51. 51. 51. 51. 50. 50. 50. 50. 51. 51. 51. 51. 51. 51. 51. 51.
#  51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51.
#  51. 51. 51. 51. 51. 51. 51. 53. 53.]

vector_10 = vector[:10]
print(vector_10.compress([True, False, True, False, True, False, True, False, True, False]))
# [49. 49. 50. 50. 51.]

