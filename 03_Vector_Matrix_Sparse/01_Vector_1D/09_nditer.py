'''
np.nditer() - A Simple Guide for 1-D Arrays

1. Basic Loop: Just iterate through values
2. Get Index While Looping: Know the position
3. Modify Values: Change array elements
4. Process in Chunks: Faster for large arrays

'''

import numpy as np

#-------------------------------------------------------------------------------------------------------#
#------------------------------------- 1. Basic Loop (READ ONLY) ---------------------------------------#
#-------------------------------------------------------------------------------------------------------#

arr = np.array([10, 20, 30, 40, 50])

# Simple iteration - just like a regular for loop
for value in np.nditer(arr):
    print(value)
# 10 20 30 40 50

############################

# Honestly? For simple cases, regular Python loop works fine too:
for value in arr:
    print(value)
# 10 20 30 40 50

#--------------------------------------------------------------------------------------------------------#
#---------------------------------- 2. Get Index While Looping ------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

# When you need both value AND position
arr2 = np.array([100, 200, 300])

it = np.nditer(arr2, flags=['c_index'])

for value in it:
    print(f"Index {it.index}: value = {value}")
# Index 0: value = 100
# Index 1: value = 200
# Index 2: value = 300

############################

# Again, regular enumerate() is often clearer:
for i, value in enumerate(arr2):
    print(f"Index {i}: value = {value}")
# Index 0: value = 100
# Index 1: value = 200
# Index 2: value = 300

#--------------------------------------------------------------------------------------------------------#
#------------------------------------ 3. Modify Values --------------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

# This is where nditer becomes useful!
arr3 = np.array([1.0, 2.0, 3.0, 4.0])
print("Before:", arr3)
# Before: [1. 2. 3. 4.]

# MUST use 'with' statement when modifying
with np.nditer(arr3, op_flags=['readwrite']) as it:
    for x in it:
        x[...] = x * 2  # Double each value

print("After:", arr3)
# After: [2. 4. 6. 8.]

############################

# With index-based modification:
arr4 = np.zeros(5)
with np.nditer(arr4, flags=['c_index'], op_flags=['writeonly']) as it:
    for x in it:
        x[...] = it.index ** 2  # Set to index squared

print("\nIndex squared:", arr4)
# Index squared: [ 0.  1.  4.  9. 16.]

    
#--------------------------------------------------------------------------------------------------------#
#----------------------------- 4. Process in Chunks (For Performance) -----------------------------------#
#--------------------------------------------------------------------------------------------------------#

# For large arrays, processing chunks is faster
arr5 = np.arange(12, dtype=float)

with np.nditer(arr5, flags=['external_loop'], op_flags=['readwrite']) as it:
    for chunk in it:
        print(f"Processing chunk of size {len(chunk)}")
        chunk[...] = chunk ** 2  # Square all values in chunk at once

print("Result:", arr5)
# Processing chunk of size 12
# Result: [  0.   1.   4.   9.  16.  25.  36.  49.  64.  81. 100. 121.]


#--------------------------------------------------------------------------------------------------------#
#------------------------------- Real-World Examples ---------------------------------------------------- #
#--------------------------------------------------------------------------------------------------------#

# Example: Running average with window
print("\n\nExample - Moving average:")
data = np.array([1, 2, 3, 4, 5], dtype=float)
result = np.zeros_like(data)

with np.nditer(data, flags=['c_index']) as it:
    for val in it:
        idx = it.index
        # Average with neighbors
        if idx == 0:
            result[idx] = (val + data[idx+1]) / 2
        elif idx == len(data) - 1:
            result[idx] = (data[idx-1] + val) / 2
        else:
            result[idx] = (data[idx-1] + val + data[idx+1]) / 3

print("Original:", data)
print("Smoothed:", result)
# Original: [1. 2. 3. 4. 5.]
# Smoothed: [1.5 2.  3.  4.  4.5]

#--------------------------------------------------------------------------------------------------------#
#--------------------------------- When to Actually Use nditer ------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

'''
HONEST TRUTH:

✓ USE nditer when:
  - You need to modify array while iterating with index
  - Processing multiple arrays together (not shown here - that's multi-array)
  - Building blocks for more complex operations
  - Working with non-contiguous memory layouts

✗ DON'T USE nditer for:
  - Simple loops → Just use: for x in arr
  - Element-wise math → Use: arr * 2, arr + 5, etc.
  - Getting indices → Use: for i, x in enumerate(arr)
  - Most common tasks → NumPy has built-in functions!

SIMPLE ALTERNATIVES:
  arr * 2              instead of   nditer with x[...] = x * 2
  np.sqrt(arr)         instead of   nditer with x[...] = sqrt(x)
  arr[arr > 0]         instead of   nditer with conditions
  enumerate(arr)       instead of   nditer with c_index

nditer is powerful but often overkill for 1-D arrays!
'''
