'''
1. Sorting:
   + Ascending sort: arr.sort() ||| np.sort(arr)
   + Descending sort: arr.sort() -> arr[::-1] ||| np.sort(arr)[::-1]
   + Sort with "kind" parameter: arr.sort(kind="...") {"quicksort", "mergesort", "heapsort", "stable"} (optional)
                                 np.sort(arr, kind="...") {"quicksort", "mergesort", "heapsort", "stable"} (optional)

2. Argument Sort:
   + Ascending arg sort: arr.argsort() ||| np.argsort(arr)
   + Descending arg sort: arr.argsort()[::-1] ||| np.argsort(arr)[::-1]
   + Sort with "kind" parameter: arr.argsort(kind="...") {"quicksort", "mergesort", "heapsort", "stable"} (optional)
                                 np.argsort(arr, kind="...") {"quicksort", "mergesort", "heapsort", "stable"} (optional)
   + Get the index of maximum: arr.argmax() ||| np.argmax(arr)
   + Get the index of minimum: arr.argmin() ||| np.argmin(arr)
   + Partial sort (k smallest elements): arr.argpartition(k) ||| np.argpartition(arr, k)

3. Searching (Binary Search): Find indices where elements should be inserted to maintain order.
   + arr.searchsorted(value)
   + np.searchsorted(arr, value)
   + (The array must be sorted first)
'''

import numpy as np

vector_heights = (
    (np.loadtxt(fname='03_Vector_Matrix_Sparse/01_Vector_1D/data/heights.txt', delimiter=',')*0.0254) # Inches to Meters
    .round(2)
)

print(vector_heights)
# [1.88 1.88 1.83 ... 1.9  1.9  1.85]


#-----------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 1. Sorting ------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
'''
Using methods like arr.sort() will modify the original array in-place, does not return a new array,
and does not allow assignment as well

Using functions like np.sort(arr) will return a new sorted array, does not modify the original array,
and allows assignment
'''

############################
##     Ascending sort     ##
############################

#-----
## using method
#-----

asc_heights = vector_heights.copy() # Create a copy to avoid modifying the original array

asc_heights.sort()
print(asc_heights)
# [1.7  1.7  1.73 ... 2.08 2.08 2.11]

#-----
## using function
#-----

asc_heights = np.sort(vector_heights)
print(asc_heights)
# [1.7  1.7  1.73 ... 2.08 2.08 2.11]

print(np.sort(vector_heights))
# [1.7  1.7  1.73 ... 2.08 2.08 2.11]

#############################
##     Descending sort     ##
#############################

#-----
## using method
#-----

desc_heights = vector_heights.copy() # Create a copy to avoid modifying the original array

desc_heights.sort()
desc_heights = desc_heights[::-1]
print(desc_heights)
# [2.11 2.08 2.08 ... 1.7  1.7 ]

#-----
## using function
#-----

desc_heights = np.sort(vector_heights)[::-1]
print(desc_heights)
# [2.11 2.08 2.08 ... 1.7  1.7 ]

print(np.sort(vector_heights)[::-1])
# [2.11 2.08 2.08 ... 1.7  1.7 ]

########################################
##     Sort with "kind" parameter     ##
########################################
'''
kind: {"quicksort", "mergesort", "heapsort", "stable"} (optional)
- Default is "quicksort"
- "stable" is a stable sort algorithm
'''

#-----
## using method
#-----

kind_heights = vector_heights.copy() # Create a copy to avoid modifying the original array

kind_heights.sort(kind="mergesort")
print(kind_heights)
# [1.7  1.7  1.73 ... 2.08 2.08 2.11]

#-----
## using function
#-----

kind_heights = np.sort(vector_heights, kind="heapsort")[::-1]
print(kind_heights)
# [2.11 2.08 2.08 ... 1.7  1.7 ]

print(np.sort(vector_heights, kind="heapsort")[::-1])
# [2.11 2.08 2.08 ... 1.7  1.7 ]


#-----------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 2. Argument Sort ---------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
'''
Argument sort returns the indices that would sort an array.

Since it returns indices, it does not modify the original array, hence allows assignment, and no need to create a copy.
'''

################################
##     Ascending arg sort     ##
################################

#-----
## using method
#-----

asc_indices = vector_heights.argsort()
print(asc_indices)
# [989 988 849 ... 558 862 909]

print(vector_heights.argsort())
# [989 988 849 ... 558 862 909]

print(vector_heights[asc_indices])
# [1.7  1.7  1.73 ... 2.08 2.08 2.11]

'''
989 -> index of the smallest element (1.7)
988 -> index of the second smallest element (1.7)
849 -> index of the third smallest element (1.73)
...
909 -> index of the largest element (2.11)
'''

#-----
## using function
#-----

asc_indices = np.argsort(vector_heights)
print(asc_indices)
# [989 988 849 ... 558 862 909]

print(np.argsort(vector_heights))
# [989 988 849 ... 558 862 909]

#################################
##     Descending arg sort     ##
#################################

#-----
## using method
#-----

desc_indices = vector_heights.argsort()[::-1]
print(desc_indices)
# [909 862 558 ... 849 988 989]

print(vector_heights.argsort()[::-1])
# [909 862 558 ... 849 988 989]

print(vector_heights[desc_indices])
# [2.11 2.08 2.08 ... 1.73 1.7  1.7 ]

'''
909 -> index of the largest element (2.11)
862 -> index of the second largest element (2.08)
558 -> index of the third largest element (2.08)
...
989 -> index of the smallest element (1.7)
'''

#-----
## using function
#-----

desc_indices = np.argsort(vector_heights)[::-1]
print(desc_indices)
# [909 862 558 ... 849 988 989]

print(np.argsort(vector_heights)[::-1])
# [909 862 558 ... 849 988 989]

########################################
##     Sort with "kind" parameter     ##
########################################
'''
kind: {"quicksort", "mergesort", "heapsort", "stable"} (optional)
- Default is "quicksort"
- "stable" is a stable sort algorithm
'''

#-----
## using method
#-----

kind_indices = vector_heights.argsort(kind="mergesort")
print(kind_indices)
# [988 989  76 ... 558 862 909]

print(vector_heights.argsort(kind="mergesort"))
# [988 989  76 ... 558 862 909]

print(vector_heights[kind_indices])
# [1.7  1.7  1.73 ... 2.08 2.08 2.11]

'''
Here, we can notice the different outcomes of indices.

Using arr.argsort() with default "quicksort" => [989 988 849 ... 558 862 909]
Using arr.argsort(kind="mergesort")          => [988 989  76 ... 558 862 909]

The final sorted array remains the same.
'''

#-----
## using function
#-----

kind_indices = np.argsort(vector_heights, kind="heapsort")[::-1]
print(kind_indices)
# [909 558 862 ... 784 988 989]

print(np.argsort(vector_heights, kind="heapsort")[::-1])
# [909 558 862 ... 784 988 989]

print(vector_heights[kind_indices])
# [2.11 2.08 2.08 ... 1.73 1.7  1.7 ]

######################################
##     Get the index of maximum     ##
######################################

#-----
## using method
#-----

max_index = vector_heights.argmax()
print(max_index)
# 909

print(vector_heights[max_index])
# 2.11

#-----
## using function
#-----

max_index = np.argmax(vector_heights)
print(max_index)
# 909

print(vector_heights[max_index])
# 2.11

######################################
##     Get the index of minimum     ##
######################################

#-----
## using method
#-----

min_index = vector_heights.argmin()
print(min_index)
# 988

print(vector_heights[min_index])
# 1.7

#-----
## using function
#-----

min_index = np.argmin(vector_heights)
print(min_index)
# 988

print(vector_heights[min_index])
# 1.7

#####################################
##     Partial sort (k smallest)   ##
#####################################

#-----
## using method
#-----

heights_5th = vector_heights.argpartition(kth=5)
print(heights_5th)
# [ 989  988  849 ... 1013 1014    0]

print(vector_heights.argpartition(kth=5))

print(vector_heights[heights_5th])
# [1.7  1.7  1.73 ... 1.85 1.85 1.88]
'''Only the first 5 elements are sorted, the rest are not guaranteed to be sorted.'''

#-----
## using function
#-----

heights_2nd = np.argpartition(vector_heights, kth=2)
print(heights_2nd)
# [ 989  988  849 ... 1013 1014    0]

print(np.argpartition(vector_heights, kth=2))
# [ 989  988  849 ... 1013 1014    0]

print(vector_heights[heights_2nd])
# [1.7  1.7  1.73 ... 1.85 1.85 1.88]
'''Only the first 2 elements are sorted, the rest are not guaranteed to be sorted.'''


#-----------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 3. Searching (Binary Search) ------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
'''
Binary search finds the indices where elements should be inserted to maintain order.
The array must be sorted first.

side: {'left', 'right'}, optional
- 'left': the insertion point will be of the first suitable location found.
- 'right': the insertion point will be of the last suitable location found.
By default, 'left' is used.
'''

asc_heights = np.sort(vector_heights)
print(asc_heights)
# [1.7  1.7  1.73 ... 2.08 2.08 2.11]

print(np.unique(asc_heights))
# [1.7  1.73 1.75 1.78 1.8  1.83 1.85 1.88 1.9  1.93 1.96 1.98 2.01 2.03
#  2.06 2.08 2.11]

##########################
##     Using method     ##
##########################

index_1m91 = asc_heights.searchsorted(1.91)
print(index_1m91)
# 808

print(asc_heights[808-1:808+1])
# [1.9  1.93]

'''
Meaning that, if we insert 1.91 to the array at index 808, the array will remain its order.
'''

############################
##     Using function     ##
############################

index_1m82 = np.searchsorted(asc_heights, 1.82, side='right')
print(index_1m82)
# 168

print(asc_heights[168-1:168+1])
# [1.8  1.83]

'''
Meaning that, if we insert 1.82 to the array at index 168, the array will remain its order.
Using 'right' side means that if there are duplicate values, the insertion point will be after the existing values.
'''
