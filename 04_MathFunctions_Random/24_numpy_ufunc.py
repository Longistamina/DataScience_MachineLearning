'''
1. ufunc basics: out and where keyword arguments.
2. ufunc.reduce(): reduction along a specified axis.
3. ufunc.accumulate(): cumulative operations along an axis.
4. ufunc.reduceat(): local reductions over specified slices.
5. ufunc.outer(): outer product-like applications.
6. ufunc.at(): unbuffered in-place operations (scatter-reduce).
7. ufunc attributes: nin, nout, types, etc.
'''

import numpy as np

np.random.seed(1)
v1 = np.array([1, 2, 3, 4])
v2 = np.array([10, 20, 30, 40])
M1 = np.array([[1, 2, 3], [4, 5, 6]])
M2 = np.array([[10, 20, 30], [40, 50, 60]])

#--------------------------------------------------------------------------------------------------#
#----------------------------------- 1. 'out' and 'where' arguments -------------------------------#
#--------------------------------------------------------------------------------------------------#
'''
- out: allows specifying a destination array to store the result, avoiding extra allocations.
- where: a boolean mask. Operation is performed only where True.
'''

# Using 'out'
res = np.empty_like(v1)
np.add(v1, v2, out=res)
print(f"Result with 'out': {res}")
# [11 22 33 44]

# Using 'where'
res_where = np.zeros_like(v1)
# Only add where v1 > 2
np.add(v1, v2, out=res_where, where=(v1 > 2))
print(f"Result with 'where': {res_where}")
# [ 0  0 33 44]


#--------------------------------------------------------------------------------------------------#
#---------------------------------------- 2. ufunc.reduce() ---------------------------------------#
#--------------------------------------------------------------------------------------------------#
'''
ufunc.reduce(): reduces an array's dimension by applying the operation along the given axis.
Equivalent to np.sum(), np.prod(), etc.
'''

# Sum of elements (default axis 0)
print(f"Sum reduce: {np.add.reduce(v1)}")
# 10

# Sum along axis 1 of M1
print(f"Reduce M1 axis 1:\n{np.add.reduce(M1, axis=1)}")
# [ 6 15]


#--------------------------------------------------------------------------------------------------#
#-------------------------------------- 3. ufunc.accumulate() --------------------------------------#
#--------------------------------------------------------------------------------------------------#
'''
ufunc.accumulate(): returns an array of the same size as the input, containing 
the intermediate results of the reduction.
'''

print(f"Sum accumulate: {np.add.accumulate(v1)}")
# [ 1  3  6 10]

print(f"Accumulate M1 axis 0:\n{np.add.accumulate(M1, axis=0)}")
# [[1 2 3]
#  [5 7 9]]


#--------------------------------------------------------------------------------------------------#
#-------------------------------------- 4. ufunc.reduceat() ---------------------------------------#
#--------------------------------------------------------------------------------------------------#
'''
ufunc.reduceat(): performs reduction over specified slices.
For indices [i, j], it reduces slices [i:j] and [j:end].
'''

indices = [0, 2]
# v1[0:2] = [1, 2] -> sum=3
# v1[2:4] = [3, 4] -> sum=7
print(f"Reduceat: {np.add.reduceat(v1, indices)}")
# [3 7]


#--------------------------------------------------------------------------------------------------#
#----------------------------------------- 5. ufunc.outer() ---------------------------------------#
#--------------------------------------------------------------------------------------------------#
'''
ufunc.outer(): applies the operation to all pairs of elements from two input arrays.
'''

# Result[i, j] = v1[i] + v2[j]
print(f"Outer add:\n{np.add.outer(v1, v2)}")
# [[11 21 31 41]
#  [12 22 32 42]
#  [13 23 33 43]
#  [14 24 34 44]]


#--------------------------------------------------------------------------------------------------#
#------------------------------------------- 6. ufunc.at() ----------------------------------------#
#--------------------------------------------------------------------------------------------------#
'''
ufunc.at(): performs unbuffered in-place operations at specified indices.
Crucial for scatter-reduce tasks: handles duplicate indices correctly.
'''

src = np.array([5, 4, 8, 7, 3, 1])
idx = np.array([0, 0, 1, 1, 2, 1])
dst = np.zeros(3, dtype=int)

np.add.at(dst, idx, src)
print(f"Scatter-add (np.add.at): {dst}")
# [ 9 16  3]

# Example: Scatter-Max
dst_max = np.full(3, -1, dtype=int)
np.maximum.at(dst_max, idx, src)
print(f"Scatter-max (np.maximum.at): {dst_max}")
# [ 5  8  3]


#--------------------------------------------------------------------------------------------------#
#-------------------------------------- 7. ufunc Attributes ---------------------------------------#
#--------------------------------------------------------------------------------------------------#
'''
ufuncs have attributes describing their input/output capabilities.
'''

op = np.add
print(f"Ufunc: {op.__name__}")
print(f"Inputs (nin): {op.nin}")   # 2
print(f"Outputs (nout): {op.nout}") # 1
print(f"Identity: {op.identity}")   # 0
# Types shows supported input->output type signatures
# print(op.types) 
