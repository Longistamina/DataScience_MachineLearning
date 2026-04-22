'''
1. Sorting:
   + Sort along axis: 
        arr.sort(axis=0 or 1)
        np.sort(arr, axis=0 or 1)
   + Sort along axis with ascending/descending: 
        arr.sort(axis=...) -> arr[::-1] for axis 0, arr[:, ::-1] for axis 1 
        np.sort(arr, axis=...)[::-1] or np.sort(arr, axis=...)[:, ::-1]
    + Sort with "kind" parameter: 
        arr.sort(axis=..., kind="...") {" quicksort", "mergesort", "heapsort", "stable"} (optional)
        np.sort(arr, axis=..., kind="...") {"quicksort", "mergesort", "heapsort", "stable"} (optional)
    + Flatten and sort: 
        arr.flatten().sort()
        np.sort(arr, axis=None)

2. Argument Sort:
   + Ascending arg sort: 
        arr.argsort(axis=0 or 1)
        np.argsort(arr, axis=0 or 1)
   + Descending arg sort: 
        arr.argsort(axis=...)[::-1] or arr.argsort(axis=...)[:, ::-1]
        np.argsort(arr, axis=...)[::-1] or np.argsort(arr, axis=...)[:, ::-1]
   + Sort with "kind" parameter: 
        arr.argsort(axis=..., kind="...") {"quicksort", "mergesort", "heapsort", "stable"} (optional)
        np.argsort(arr, axis=..., kind="...") {"quicksort", "mergesort", "heapsort", "stable"} (optional)
   + Get the index of maximum: 
        arr.argmax(axis=0 or 1 or None)
        np.argmax(arr, axis=0 or 1 or None)
   + Get the index of minimum: 
        arr.argmin(axis=0 or 1 or None)
        np.argmin(arr, axis=0 or 1 or None)
   + Partial sort (k smallest elements): 
        arr.argpartition(k, axis=0 or 1)
        np.argpartition(arr, k, axis=0 or 1)

3. Examples on 3D and 4D matrices:
   + np.sort(arr3d, axis=0) # Sort along the first dimension
   + np.argsort(arr4d, axis=2) # Argsort along the third dimension
   + np.argmax(arr3d, axis=(0, 1)) # Get argmax along first two dimensions (returns flat index)
'''

import numpy as np

matrix_scores = np.array([
    [85, 92, 78, 95, 88],
    [76, 88, 91, 84, 79],
    [93, 81, 87, 90, 85],
    [88, 79, 94, 77, 92]
])

print(matrix_scores)
# [[85 92 78 95 88]
#  [76 88 91 84 79]
#  [93 81 87 90 85]
#  [88 79 94 77 92]]


#-----------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 1. Sorting ------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
'''
Using methods like arr.sort() will modify the original array in-place, does not return a new array,
and does not allow assignment as well

Using functions like np.sort(arr) will return a new sorted array, does not modify the original array,
and allows assignment

axis=0: Sort vertically along columns (within each column)
axis=1: Sort horizontally along rows (within each row)
axis=None: Flatten and sort the entire array
'''

#######################
## Sort along axis=0 ##
#######################
'''axis=0 means vertical direction (columns)'''

#-----
## using method
#-----

sorted_axis0 = matrix_scores.copy() # Create a copy to avoid modifying the original array
sorted_axis0.sort(axis=0)
print(sorted_axis0)
# [[76 79 78 77 79]
#  [85 81 87 84 85]
#  [88 88 91 90 88]
#  [93 92 94 95 92]]

#-----
## using function
#-----

sorted_axis0 = np.sort(matrix_scores, axis=0)
print(sorted_axis0)
# [[76 79 78 77 79]
#  [85 81 87 84 85]
#  [88 88 91 90 88]
#  [93 92 94 95 92]]

print(np.sort(matrix_scores, axis=0))
# [[76 79 78 77 79]
#  [85 81 87 84 85]
#  [88 88 91 90 88]
#  [93 92 94 95 92]]

#######################
## Sort along axis=1 ##
#######################
'''axis=1 means horizontal direction (rows)'''

#-----
## using method
#-----

sorted_axis1 = matrix_scores.copy() # Create a copy to avoid modifying the original array
sorted_axis1.sort(axis=1)
print(sorted_axis1)
# [[78 85 88 92 95]
#  [76 79 84 88 91]
#  [81 85 87 90 93]
#  [77 79 88 92 94]]

#-----
## using function
#-----

sorted_axis1 = np.sort(matrix_scores, axis=1)
print(sorted_axis1)
# [[78 85 88 92 95]
#  [76 79 84 88 91]
#  [81 85 87 90 93]
#  [77 79 88 92 94]]

print(np.sort(matrix_scores, axis=1))
# [[78 85 88 92 95]
#  [76 79 84 88 91]
#  [81 85 87 90 93]
#  [77 79 88 92 94]]

#####################
## Descending sort ##
#####################

#-----
## using method (axis=0)
#-----

desc_axis0 = matrix_scores.copy() # Create a copy to avoid modifying the original array
desc_axis0.sort(axis=0)
desc_axis0 = desc_axis0[::-1]
print(desc_axis0)
# [[93 92 94 95 92]
#  [88 88 91 90 88]
#  [85 81 87 84 85]
#  [76 79 78 77 79]]

#-----
## using function (axis=1)
#-----

desc_axis1 = np.sort(matrix_scores, axis=1)[:, ::-1]
print(desc_axis1)
# [[95 92 88 85 78]
#  [91 88 84 79 76]
#  [93 90 87 85 81]
#  [94 92 88 79 77]]

print(np.sort(matrix_scores, axis=1)[:, ::-1])
# [[95 92 88 85 78]
#  [91 88 84 79 76]
#  [93 90 87 85 81]
#  [94 92 88 79 77]]

######################
## Flatten and sort ##
######################

#-----
## using method
#-----

flattened = matrix_scores.copy().flatten() # Create a copy to avoid modifying the original array
flattened.sort()
print(flattened)
# [76 77 78 79 79 81 84 85 85 87 88 88 88 90 91 92 92 93 94 95]

#-----
## using function
#-----

flattened = np.sort(matrix_scores, axis=None)
print(flattened)
# [76 77 78 79 79 81 84 85 85 87 88 88 88 90 91 92 92 93 94 95]

print(np.sort(matrix_scores, axis=None)[::-1]) # Descending order
# [95 94 93 92 92 91 90 88 88 88 87 85 85 84 81 79 79 78 77 76]

################################
## Sort with "kind" parameter ##
################################
'''
kind: {"quicksort", "mergesort", "heapsort", "stable"} (optional)
- Default is "quicksort"
- "stable" is a stable sort algorithm
'''

#-----
## using method
#-----

kind_scores = matrix_scores.copy() # Create a copy to avoid modifying the original array
kind_scores.sort(axis=1, kind="mergesort")
print(kind_scores)
# [[78 85 88 92 95]
#  [76 79 84 88 91]
#  [81 85 87 90 93]
#  [77 79 88 92 94]]

#-----
## using function
#-----

kind_scores = np.sort(matrix_scores, axis=0, kind="heapsort")
print(kind_scores)
# [[76 79 78 77 79]
#  [85 81 87 84 85]
#  [88 88 91 90 88]
#  [93 92 94 95 92]]

print(np.sort(matrix_scores, axis=0, kind="heapsort"))
# [[76 79 78 77 79]
#  [85 81 87 84 85]
#  [88 88 91 90 88]
#  [93 92 94 95 92]]


#-----------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 2. Argument Sort ---------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
'''
Argument sort returns the indices that would sort an array.
Since it returns indices, it does not modify the original array, hence allows assignment, and no need to create a copy.

axis=0: Return indices that would sort vertically along columns
axis=1: Return indices that would sort horizontally along rows
axis=None: Return indices that would sort the flattened array
'''

#################################
## Ascending arg sort (axis=0) ##
#################################

#-----
## using method
#-----

asc_indices_axis0 = matrix_scores.argsort(axis=0)
print(asc_indices_axis0)
# [[1 3 0 3 1]
#  [0 2 2 1 2]
#  [3 1 1 2 0]
#  [2 0 3 0 3]]

print(matrix_scores.argsort(axis=0))
# [[1 3 0 3 1]
#  [0 2 2 1 2]
#  [3 1 1 2 0]
#  [2 0 3 0 3]]

print(np.take_along_axis(matrix_scores, asc_indices_axis0, axis=0))
# [[76 79 78 77 79]
#  [85 81 87 84 85]
#  [88 88 91 90 88]
#  [93 92 94 95 92]]

'''
For column 0: [1, 0, 3, 2] means 
+ row 1 has smallest value (76) 
+ then row 0 (85) 
+ then row 3 (88) 
+ then row 2 (93)
'''

#-----
## using function
#-----

asc_indices_axis0 = np.argsort(matrix_scores, axis=0)
print(asc_indices_axis0)
# [[1 3 0 3 1]
#  [0 2 2 1 2]
#  [3 1 1 2 0]
#  [2 0 3 0 3]]

print(np.argsort(matrix_scores, axis=0))
# [[1 3 0 3 1]
#  [0 2 2 1 2]
#  [3 1 1 2 0]
#  [2 0 3 0 3]]

#################################
## Ascending arg sort (axis=1) ##
#################################

#-----
## using method
#-----

asc_indices_axis1 = matrix_scores.argsort(axis=1)
print(asc_indices_axis1)
# [[2 0 4 1 3]
#  [0 4 3 1 2]
#  [1 4 2 3 0]
#  [3 1 0 4 2]]

print(matrix_scores.argsort(axis=1))
# [[2 0 4 1 3]
#  [0 4 3 1 2]
#  [1 4 2 3 0]
#  [3 1 0 4 2]]

print(np.take_along_axis(matrix_scores, asc_indices_axis1, axis=1))
# [[78 85 88 92 95]
#  [76 79 84 88 91]
#  [81 85 87 90 93]
#  [77 79 88 92 94]]

'''
For row 0: [2, 0, 4, 1, 3] means 
+ column 2 has smallest value (78)
+ then column 0 (85)
+ then column 4 (88)
'''

#-----
## using function
#-----

asc_indices_axis1 = np.argsort(matrix_scores, axis=1)
print(asc_indices_axis1)
# [[2 0 4 1 3]
#  [0 4 3 1 2]
#  [1 4 2 3 0]
#  [3 1 0 4 2]]

print(np.argsort(matrix_scores, axis=1))
# [[2 0 4 1 3]
#  [0 4 3 1 2]
#  [1 4 2 3 0]
#  [3 1 0 4 2]]

#########################
## Descending arg sort ##
#########################

#-----
## using method (axis=0)
#-----

desc_indices_axis0 = matrix_scores.argsort(axis=0)[::-1]
print(desc_indices_axis0)
# [[2 0 3 0 3]
#  [3 1 1 2 0]
#  [0 2 2 1 2]
#  [1 3 0 3 1]]

print(matrix_scores.argsort(axis=0)[::-1])
# [[2 0 3 0 3]
#  [3 1 1 2 0]
#  [0 2 2 1 2]
#  [1 3 0 3 1]]

print(np.take_along_axis(matrix_scores, desc_indices_axis0, axis=0))
# [[93 92 94 95 92]
#  [88 88 91 90 88]
#  [85 81 87 84 85]
#  [76 79 78 77 79]]

#-----
## using function (axis=1)
#-----

desc_indices_axis1 = np.argsort(matrix_scores, axis=1)[:, ::-1]
print(desc_indices_axis1)
# [[3 1 4 0 2]
#  [2 1 3 4 0]
#  [0 3 2 4 1]
#  [2 4 0 1 3]]

print(np.argsort(matrix_scores, axis=1)[:, ::-1])
# [[3 1 4 0 2]
#  [2 1 3 4 0]
#  [0 3 2 4 1]
#  [2 4 0 1 3]]

print(np.take_along_axis(matrix_scores, desc_indices_axis1, axis=1))
# [[95 92 88 85 78]
#  [91 88 84 79 76]
#  [93 90 87 85 81]
#  [94 92 88 79 77]]

################################
## Sort with "kind" parameter ##
################################
'''
kind: {"quicksort", "mergesort", "heapsort", "stable"} (optional)
- Default is "quicksort"
- "stable" is a stable sort algorithm
'''

#-----
## using method
#-----

kind_indices = matrix_scores.argsort(axis=1, kind="mergesort")
print(kind_indices)
# [[2 0 4 1 3]
#  [0 4 3 1 2]
#  [1 4 2 3 0]
#  [3 1 0 4 2]]

print(matrix_scores.argsort(axis=1, kind="mergesort"))
# [[2 0 4 1 3]
#  [0 4 3 1 2]
#  [1 4 2 3 0]
#  [3 1 0 4 2]]

print(np.take_along_axis(matrix_scores, kind_indices, axis=1))
# [[78 85 88 92 95]
#  [76 79 84 88 91]
#  [81 85 87 90 93]
#  [77 79 88 92 94]]

'''
Here, we can notice the different outcomes of indices depending on the sorting algorithm.
Using arr.argsort(axis=1) with default "quicksort" vs arr.argsort(axis=1, kind="mergesort")
The final sorted array remains the same.
'''

#-----
## using function
#-----

kind_indices = np.argsort(matrix_scores, axis=0, kind="heapsort")
print(kind_indices)
# [[1 3 0 3 1]
#  [0 2 2 1 2]
#  [3 1 1 2 0]
#  [2 0 3 0 3]]

print(np.argsort(matrix_scores, axis=0, kind="heapsort"))
# [[1 3 0 3 1]
#  [0 2 2 1 2]
#  [3 1 1 2 0]
#  [2 0 3 0 3]]

print(np.take_along_axis(matrix_scores, kind_indices, axis=0))
# [[76 79 78 77 79]
#  [85 81 87 84 85]
#  [88 88 91 90 88]
#  [93 92 94 95 92]]

##############################
## Get the index of maximum ##
##############################

#-----
## using method (axis=0)
#-----

max_index_axis0 = matrix_scores.argmax(axis=0)
print(max_index_axis0)
# [2 0 3 0 3]

print(np.take_along_axis(matrix_scores, max_index_axis0[np.newaxis, :], axis=0))
# [[93 92 94 95 92]]
'''np.newaxis is used to convert 1D array argmax_indices to 2D for proper broadcasting'''

#-----
## using method (axis=1)
#-----

max_index_axis1 = matrix_scores.argmax(axis=1)
print(max_index_axis1)
# [3 2 0 2]

print(np.take_along_axis(matrix_scores, max_index_axis1[:, np.newaxis], axis=1))
# [[95]
#  [91]
#  [93]
#  [94]]
'''np.newaxis is used to convert 1D array argmax_indices to 2D for proper broadcasting'''

#-----
## using method (axis=None, flatten)
#-----

max_index_flat = matrix_scores.argmax()
print(max_index_flat)
# 3

print(matrix_scores.flatten()[max_index_flat])
# 95

#-----
## using function
#-----

max_index_axis0 = np.argmax(matrix_scores, axis=0)
print(max_index_axis0)
# [2 0 3 0 3]

max_index_flat = np.argmax(matrix_scores)
print(max_index_flat)
# 3

print(matrix_scores.flatten()[max_index_flat])
# 95

##############################
## Get the index of minimum ##
##############################

#-----
## using method (axis=0)
#-----

min_index_axis0 = matrix_scores.argmin(axis=0)
print(min_index_axis0)
# [1 3 0 3 1]

print(np.take_along_axis(matrix_scores, min_index_axis0[np.newaxis, :], axis=0))
# [[76 79 78 77 79]]
'''np.newaxis is used to convert 1D array argmax_indices to 2D for proper broadcasting'''

#-----
## using method (axis=1)
#-----

min_index_axis1 = matrix_scores.argmin(axis=1)
print(min_index_axis1)
# [2 0 1 3]

print(np.take_along_axis(matrix_scores, min_index_axis1[:, np.newaxis], axis=1))
# [[78]
#  [76]
#  [81]
#  [77]]
'''np.newaxis is used to convert 1D array argmax_indices to 2D for proper broadcasting'''

#-----
## using method (axis=None, flatten)
#-----

min_index_flat = matrix_scores.argmin()
print(min_index_flat)
# 5

print(matrix_scores.flatten()[min_index_flat])
# 76

#-----
## using function
#-----

min_index_axis0 = np.argmin(matrix_scores, axis=0)
print(min_index_axis0)
# [1 3 0 3 1]

min_index_flat = np.argmin(matrix_scores)
print(min_index_flat)
# 5

print(matrix_scores.flatten()[min_index_flat])
# 76

###############################
## Partial sort (k smallest) ##
###############################

#-----
## using method (axis=1)
#-----

scores_2nd = matrix_scores.argpartition(kth=2, axis=1)
print(scores_2nd)
# [[2 0 4 1 3]
#  [0 4 3 1 2]
#  [1 4 2 3 0]
#  [3 1 0 4 2]]

print(matrix_scores.argpartition(kth=2, axis=1))
# [[2 0 4 1 3]
#  [0 4 3 1 2]
#  [1 4 2 3 0]
#  [3 1 0 4 2]]

print(np.take_along_axis(matrix_scores, scores_2nd, axis=1))
# [[78 85 88 92 95]
#  [76 79 84 88 91]
#  [81 85 87 90 93]
#  [77 79 88 92 94]]

'''Only the first 2 elements in each row are sorted, the rest are not guaranteed to be sorted.'''

#-----
## using function (axis=0)
#-----

scores_3rd = np.argpartition(matrix_scores, kth=3, axis=0)
print(scores_3rd)
# [[1 3 0 3 1]
#  [0 2 2 1 2]
#  [3 1 1 2 0]
#  [2 0 3 0 3]]

print(np.argpartition(matrix_scores, kth=3, axis=0))
# [[1 3 0 3 1]
#  [0 2 2 1 2]
#  [3 1 1 2 0]
#  [2 0 3 0 3]]

print(np.take_along_axis(matrix_scores, scores_3rd, axis=0))
# [[76 79 78 77 79]
#  [85 81 87 84 85]
#  [88 88 91 90 88]
#  [93 92 94 95 92]]

'''Only the first 3 elements in each column are sorted, the rest are not guaranteed to be sorted.'''


#-----------------------------------------------------------------------------------------------------------------#
#----------------------------------- 3. Examples on 3D and 4D matrices -------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

'''
For higher dimensional arrays, the same principles apply with the axis parameter.
axis can be any dimension index, or None to flatten the entire array.
'''

#######################
## 3D array examples ##
#######################

np.random.seed(0)  # For reproducibility
arr3d = np.random.randint(10, 100, size=(3, 4, 5))
print(arr3d)
# [[[54 57 74 77 77]
#   [19 93 31 46 97]
#   [80 98 98 22 68]
#   [75 49 97 56 98]]

#  [[91 47 35 87 82]
#   [19 30 90 79 89]
#   [57 74 92 98 59]
#   [39 29 29 24 49]]

#  [[42 75 19 67 42]
#   [41 84 33 45 85]
#   [65 38 44 10 10]
#   [46 63 15 48 27]]]

#-------#

# Sort along axis 0 (across the first dimension)
sorted_3d_axis0 = np.sort(arr3d, axis=0)
print(sorted_3d_axis0)
# [[[42 47 19 67 42]
#   [19 30 31 45 85]
#   [57 38 44 10 10]
#   [39 29 15 24 27]]

#  [[54 57 35 77 77]
#   [19 84 33 46 89]
#   [65 74 92 22 59]
#   [46 49 29 48 49]]

#  [[91 75 74 87 82]
#   [41 93 90 79 97]
#   [80 98 98 98 68]
#   [75 63 97 56 98]]]

'''
In this case, for each (i,j) position in the 4x5 slices, 
we sort the values across the 3 slices (along axis 0).

at position (0,0): [54, 91, 42] -> sorted to [42, 54, 91]
at position (1,0): [19, 19, 41] -> sorted to [19, 19, 41]
...
'''

#-------#

# Argsort along axis 2 (within each 4x5 slice)
argsorted_3d_axis2 = np.argsort(arr3d, axis=2)
print(argsorted_3d_axis2.shape)
# (3, 4, 5)

#-------#

# Get argmax along axis 1
argmax_3d_axis1 = np.argmax(arr3d, axis=1)
print(argmax_3d_axis1.shape)
# (3, 5)

#-------#

# Get argmin across entire array
argmin_3d_flat = np.argmin(arr3d)
print(argmin_3d_flat)
# 53

#######################
## 4D array examples ##
#######################

np.random.seed(0)  # For reproducibility
arr4d = np.random.randint(50, 150, size=(2, 3, 4, 5))
print(arr4d.shape)
# (2, 3, 4, 5)

# Sort along axis 3 (last dimension)
sorted_4d_axis3 = np.sort(arr4d, axis=3)
print(sorted_4d_axis3.shape)
# (2, 3, 4, 5)

# Argsort along axis 1
argsorted_4d_axis1 = np.argsort(arr4d, axis=1)
print(argsorted_4d_axis1.shape)
# (2, 3, 4, 5)

# Get argmax along axis 0
argmax_4d_axis0 = np.argmax(arr4d, axis=0)
print(argmax_4d_axis0.shape)
# (3, 4, 5)

# Flatten and sort
sorted_4d_flat = np.sort(arr4d, axis=None)
print(sorted_4d_flat.shape)
# (120,)  # 2*3*4*5 = 120
