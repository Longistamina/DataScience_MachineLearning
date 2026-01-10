'''
1. np.apply_along_axis(func, axis=0, arr): Applies a function to a 1D vector

2. np.vectorize(func): Vectorizes a function to apply it element-wise on arrays

3. np.frompyfunc(func, nin, nout): Creates a ufunc from a Python function
'''

import numpy as np

np.set_printoptions(linewidth=200)

#-------------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 1. np.apply_along_axis() -------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#
'''
This function applies a given function to 1D slices along the specified axis of an array.

NOTE: the function must accept arrays and return arrays.
'''

np.random.seed(0)
vector_nums = np.random.randint(1e6, 2e6, size=5)
print(vector_nums)
# [1985772 1305711 1435829 1117952 1963395]

print(np.apply_along_axis(np.log10, axis=0, arr=vector_nums))
# [6.29792938 6.11584706 6.15710272 6.04842316 6.29300768]

print(np.apply_along_axis(lambda x: x / 1e6, axis=0, arr=vector_nums))
# [1.985772 1.305711 1.435829 1.117952 1.963395]

def custom_func(x):
    return np.sqrt(x) + 10
print(np.apply_along_axis(custom_func, axis=0, arr=vector_nums))
# [1419.17422628 1152.67711975 1208.26082303 1067.33249264 1411.2119754 ]

import math
print(np.apply_along_axis(math.log2, axis=0, arr=vector_nums))
'''TypeError: only length-1 arrays can be converted to Python scalars'''
# It returns an error because math.log2 expects a single scalar value, not an array.


#-------------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 2. np.vectorize() -----------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#
'''
This function vectorizes a given function to apply it element-wise on arrays.
It's useful for functions that are not inherently vectorized (only accept scalars).
'''

np.random.seed(2)
time_stamps = np.random.randint(1e9, 2e9, size=5)
print(time_stamps)
# [1798842024 1794921487 1111352301 1779712072 1213298710]

import time

ctime_vectorized = np.vectorize(time.ctime)
print(ctime_vectorized(time_stamps))
# ['Sat Jan  2 07:20:24 2027' 'Tue Nov 17 22:18:07 2026' 'Mon Mar 21 05:58:21 2005' 
# 'Mon May 25 21:27:52 2026' 'Fri Jun 13 04:25:10 2008']

def hour_stamps(ts):
    return ts / (60 * 60)
hour_stamps_vectorized = np.vectorize(hour_stamps)
print(hour_stamps_vectorized(time_stamps))
# [499678.34       498589.30194444 308708.9725     494364.46444444 337027.41944444]


#-------------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 3. np.frompyfunc() ------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#
'''
Creates a universal function (ufunc) from any Python function, enabling broadcasting. 
NOTE: Unlike vectorize(), you must specify the number of inputs (nin) and outputs (nout).
'''

#################################
## Single input, Single output ##
#################################

oct(25)
# '0o31'
# This function converts an integer to its octal string representation.

octal_ufunc = np.frompyfunc(oct, nin=1, nout=1)

print(octal_ufunc([8, 16, 32, 64, 128]))
# ['0o10' '0o20' '0o40' '0o100' '0o200']

'''
octal_ufunc() takes ONLY ONE array-like input and returns ONE array-like output.
'''

####################################
## Multiple inputs, Single output ##
####################################

def power_mod(base, exp, mod):
    return pow(base, exp, mod)

bases = np.array([2, 3, 4, 5])
exps = np.array([3, 2, 2, 3])
mods = np.array([5, 7, 6, 8]) # modulus values

power_mod_func = np.frompyfunc(power_mod, 3, 1)

result = power_mod_func(bases, exps, mods)
# Result: array([3, 2, 4, 5], dtype=object)

'''
power_mod_func() takes THREE array-like inputs and returns ONE array-like output.

3 = 2^3 % 5
2 = 3^2 % 7
4 = 4^2 % 6
5 = 5^3 % 8
'''

####################################
## Single input, Multiple outputs ##
####################################

def powers(x):
    return x, x**2, x**3

power_func = np.frompyfunc(powers, 1, 3)

numbers = np.array([2, 3, 4, 5])

vals, squares, cubes = power_func(numbers)

print("Values:", vals.astype(int))      # [2, 3, 4, 5]
print("Squares:", squares.astype(int))  # [4, 9, 16, 25]
print("Cubes:", cubes.astype(int))      # [8, 27, 64, 125]

'''power_func() takes ONE array-like input and returns THREE array-like outputs.'''

#######################################
## Multiple inputs, Multiple outputs ##
#######################################

def arithmetic_ops(x, y):
    return x + y, x - y, x * y

arith_func = np.frompyfunc(arithmetic_ops, 2, 3)

a = np.array([10, 20, 30])
b = np.array([1, 2, 3])

sums, diffs, prods = arith_func(a, b)

print("Sums:", sums.astype(int))       # [11, 22, 33]
print("Diffs:", diffs.astype(int))     # [9, 18, 27]
print("Products:", prods.astype(int))  # [10, 40, 90]

'''arith_func() takes TWO array-like inputs and returns THREE array-like outputs.'''