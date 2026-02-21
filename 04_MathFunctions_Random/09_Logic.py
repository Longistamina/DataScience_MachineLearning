'''
1. Truth value testing
   + np.all(): tests whether all array elements along a given axis evaluate to True.
   + np.any(): tests whether any array element along a given axis evaluates to True.

2. Array contents
   + np.isfinite(): tests element-wise for finiteness (not infinity and not NaN).
   + np.isinf(): tests element-wise for positive or negative infinity.
   + np.isnan(): tests element-wise for NaN and returns result as a boolean array.
   + np.isnat(): tests element-wise for NaT (not a time) and returns result as a boolean array.
   + np.isneginf(): tests element-wise for negative infinity, returns result as bool array.
   + np.isposinf(): tests element-wise for positive infinity, returns result as bool array.

3. Array type testing
   + np.iscomplex(): returns a bool array, where True if input element is complex.
   + np.iscomplexobj(): checks for a complex type or an array of complex numbers.
   + np.isfortran(): checks if the array is Fortran contiguous.
   + np.isreal(): returns a bool array, where True if input element is real.
   + np.isrealobj(): returns True if x is not a complex type or an array of complex numbers.
   + np.isscalar(): returns True if the type of element is a scalar type.

4. Logical operations
   + np.logical_and(): computes the truth value of x1 AND x2 element-wise.
   + np.logical_or(): computes the truth value of x1 OR x2 element-wise.
   + np.logical_not(): computes the truth value of NOT x element-wise.
   + np.logical_xor(): computes the truth value of x1 XOR x2, element-wise.

5. Comparison
   + np.allclose(): returns True if two arrays are element-wise equal within a tolerance.
   + np.isclose(): returns a boolean array where two arrays are element-wise equal within a tolerance.
   + np.array_equal(): returns True if two arrays have the same shape and elements, False otherwise.
   + np.array_equiv(): returns True if input arrays are shape consistent and all elements equal.
   + np.greater(): returns the truth value of (x1 > x2) element-wise.
   + np.greater_equal(): returns the truth value of (x1 >= x2) element-wise.
   + np.less(): returns the truth value of (x1 < x2) element-wise.
   + np.less_equal(): returns the truth value of (x1 <= x2) element-wise.
   + np.equal(): returns (x1 == x2) element-wise.
   + np.not_equal(): returns (x1 != x2) element-wise.

6. Application in boolean indexing and masking
'''

import numpy as np

np.random.seed(10)
v1 = np.random.randint(-10, 11, 5)
# array([ -1,  -6,   5, -10,   7])

np.random.seed(11)
v2 = np.random.randint(-10, 11, 5)
# array([ 6,  7,  3,  2, -9])

np.random.seed(12)
M1 = np.random.randint(-10, 11, (3, 4))
# array([[ 1, -4,  7, -8],
#        [-7, -7,  2,  6],
#        [ 7, 10, -5,  3]])

np.random.seed(13)
M2 = np.random.randint(-10, 11, (3, 4))
# array([[ 8,  6,  0,  6],
#        [-4, -8, 10,  2],
#        [-7, 10, -8,  4]])


#-------------------------------------------------------------------------------------------------#
#------------------------------------- 1. Truth value testing ------------------------------------#
#-------------------------------------------------------------------------------------------------#

all_true = np.array([True, True, True])
all_false = np.array([False, False, False])
mix_bool = np.array([True, False, True])

##############
## np.all() ##
##############
'''
np.all() tests whether all array elements along a given axis evaluate to True.
Returns True if all elements are True (or non-zero for numeric arrays).
'''

print(np.all(all_true))
# True (because all elements are True)

print(np.all(all_false))
# False (because no elements are True)

print(np.all(mix_bool))
# False (because there is at least one element that is not True)

# With numeric arrays (0 is False, non-zero is True)
print(np.all(v1))
# True (because all elements are non-zero)

v_zeros = np.zeros(5)
print(np.all(v_zeros))
# False (because all elements are zero, which is False)

v_with_zero = np.array([1, 2, 0, 4, 5])
print(np.all(v_with_zero))
# False (because of the zero element)

# Along specific axis
M_bool = np.array([[True, True, True], [True, False, True]])
print(np.all(M_bool, axis=0))
# [ True False  True]

print(np.all(M_bool, axis=1))
# [ True False]

##############
## np.any() ##
##############
'''
np.any() tests whether any array element along a given axis evaluates to True.
Returns True if at least one element is True (or non-zero for numeric arrays).
'''

print(np.any(all_true))
# True (because there is at least one True element)

print(np.any(all_false))
# False (because no elements are True)

print(np.any(mix_bool))
# True (because is at least one True element)

# With numeric arrays
print(np.any(v_with_zero))
# True (because there are non-zero elements)

print(np.any(v_zeros))
# False (because all elements are zero, which is False)

# Along specific axis
print(np.any(M_bool, axis=0))
# [True True True]

print(np.any(M_bool, axis=1))
# [True True]


#-------------------------------------------------------------------------------------------------#
#------------------------------------ 2. Array contents ------------------------------------------#
#-------------------------------------------------------------------------------------------------#

##################
## np.isfinite() ##
##################

'''
np.isfinite() tests element-wise for finiteness (not infinity and not NaN).
Returns True for finite numbers, False for inf, -inf, and NaN.
'''

v_special = np.array([1.0, np.inf, -np.inf, np.nan, 0.0])
print(np.isfinite(v_special))
# [ True False False False  True]

M_special = np.array([[1.0, np.inf], [np.nan, 3.0]])
print(np.isfinite(M_special))
# [[ True False]
#  [False  True]]

################
## np.isinf() ##
################

'''
np.isinf() tests element-wise for positive or negative infinity.
Returns True for inf or -inf, False otherwise.
'''

print(np.isinf(v_special))
# [False  True  True False False]

print(np.isinf(M_special))
# [[False  True]
#  [False False]]

################
## np.isnan() ##
################

'''
np.isnan() tests element-wise for NaN and returns result as a boolean array.
Returns True for NaN values, False otherwise.
'''

print(np.isnan(v_special))
# [False False False  True False]

print(np.isnan(M_special))
# [[False False]
#  [ True False]]

################
## np.isnat() ##
################

'''
np.isnat() tests element-wise for NaT (not a time) and returns result as a boolean array.
This is specifically for datetime64 and timedelta64 types.
'''

dates = np.array(['2023-01-01', 'NaT', '2023-12-31'], dtype='datetime64')
print(np.isnat(dates))
# [False  True False]

timedeltas = np.array([1, np.timedelta64('NaT'), 3], dtype='timedelta64[D]')
print(np.isnat(timedeltas))
# [False  True False]

##################
## np.isneginf() ##
##################

'''
np.isneginf() tests element-wise for negative infinity, returns result as bool array.
Returns True only for -inf, False otherwise.
'''

print(np.isneginf(v_special))
# [False False  True False False]

out = np.zeros(v_special.shape, dtype=bool)
np.isneginf(v_special, out=out)
print(out)
# [False False  True False False]

##################
## np.isposinf() ##
##################

'''
np.isposinf() tests element-wise for positive infinity, returns result as bool array.
Returns True only for +inf, False otherwise.
'''

print(np.isposinf(v_special))
# [False  True False False False]

out = np.zeros(v_special.shape, dtype=bool)
np.isposinf(v_special, out=out)
print(out)
# [False  True False False False]

#-------------------------------------------------------------------------------------------------#
#---------------------------- 3. Array type testing ----------------------------------------------#
#-------------------------------------------------------------------------------------------------#

####################
## np.iscomplex() ##
####################
'''
np.iscomplex() returns a bool array, where True if input element is complex.
Returns True if the imaginary part is non-zero.
'''

complex_array = np.array([1+2j, 3+0j, 4, 5+1j])
print(np.iscomplex(complex_array))
# [ True False False  True]

# Note: 3+0j has zero imaginary part, so it's considered real
print(np.iscomplex(3+0j))
# False

#######################
## np.iscomplexobj() ##
#######################
'''
np.iscomplexobj() checks for a complex type or an array of complex numbers.
Returns True if the array is of complex type, regardless of values.
'''

real_array = np.array([1, 2, 3, 4])
print(np.iscomplexobj(real_array))
# False

print(np.iscomplexobj(complex_array))
# True

# Even if all imaginary parts are zero
all_real_complex = np.array([1+0j, 2+0j, 3+0j])
print(np.iscomplexobj(all_real_complex))
# True (because dtype is complex)

####################
## np.isfortran() ##
####################
'''
np.isfortran() checks if the array is Fortran contiguous.
Fortran contiguous means column-major order (columns are contiguous in memory).
'''

# C-contiguous (row-major, default in NumPy)
c_array = np.array([[1, 2, 3], [4, 5, 6]])
print(np.isfortran(c_array))
# False

# Fortran-contiguous (column-major)
f_array = np.array([[1, 2, 3], [4, 5, 6]], order='F')
print(np.isfortran(f_array))
# True

# Transpose creates Fortran-contiguous arrays
print(np.isfortran(c_array.T))
# True

#################
## np.isreal() ##
#################
'''
np.isreal() returns a bool array, where True if input element is real.
Returns True if the imaginary part is zero.
'''

print(np.isreal(complex_array))
# [False  True  True False]

print(np.isreal(3+0j))
# True (because the imaginary part is zero)

mixed_array = np.array([1, 2+0j, 3+1j, 4.5])
print(np.isreal(mixed_array))
# [ True  True False  True]

####################
## np.isrealobj() ##
####################
'''
np.isrealobj() returns True if x is not a complex type or an array of complex numbers.
Returns True if the array is of real type, regardless of values.
'''

print(np.isrealobj(real_array))
# True

print(np.isrealobj(complex_array))
# False

print(np.isrealobj(3 + 0j))
# False (because it's a complex type, even though the imaginary part is zero)

print(np.isrealobj(3.14))
# True

###################
## np.isscalar() ##
###################
'''
np.isscalar() returns True if the type of element is a scalar type.
Scalars include numbers, strings, and other non-array types.
'''

print(np.isscalar(5))
# True

print(np.isscalar(3.14))
# True

print(np.isscalar([1, 2, 3]))
# False

print(np.isscalar(np.array(5)))
# False (NumPy array, even 0-d, is not considered scalar)

print(np.isscalar("hello"))
# True


#-------------------------------------------------------------------------------------------------#
#----------------------------------- 4. Logical operations ---------------------------------------#
#-------------------------------------------------------------------------------------------------#

######################
## np.logical_and() ##
######################
'''
np.logical_and() computes the truth value of x1 AND x2 element-wise.
Returns True where both x1 and x2 are True (or non-zero).
'''

bool1 = np.array([True, True, False, False])
bool2 = np.array([True, False, True, False])

print(np.logical_and(bool1, bool2))
# [ True False False False]

# With numeric arrays (non-zero is True)
print(np.logical_and(v1, v2))
# [ True  True  True  True True] (because all elements are non-zero)

print(np.logical_and(M1 > 0, M2 > 0))
# [[ True False False False]
#  [False False  True  True]
#  [False  True False  True]]

#####################
## np.logical_or() ##
#####################
'''
np.logical_or() computes the truth value of x1 OR x2 element-wise.
Returns True where at least one of x1 or x2 is True (or non-zero).
'''

print(np.logical_or(bool1, bool2))
# [ True  True  True False]

print(np.logical_or(v1, v2))
# [ True  True  True  True  True]

print(np.logical_or(M1 > 5, M2 > 5))
# [[ True  True  True  True]
#  [False False  True  True]
#  [ True  True False False]]

######################
## np.logical_not() ##
######################
'''
np.logical_not() computes the truth value of NOT x element-wise.
Returns True where x is False (or zero), and vice versa.
'''

print(np.logical_not(bool1))
# [False False  True  True]

print(np.logical_not(v_with_zero))
# [False False  True False False]

print(np.logical_not(M1 > 0))
# [[False  True False  True]
#  [ True  True False False]
#  [False False  True False]]

######################
## np.logical_xor() ##
######################
'''
np.logical_xor() computes the truth value of x1 XOR x2, element-wise.
Returns True where exactly one of x1 or x2 is True (or non-zero).
'''

print(np.logical_xor(bool1, bool2))
# [False  True  True False]

print(np.logical_xor(v1 > 0, v2 > 0))
# [ True  True False  True  True]

###################################
## Difference between OR and XOR ##
###################################

bool1 = np.array([True, True, False, False])
bool2 = np.array([True, False, True, False])

print(np.logical_or(bool1, bool2))
# [ True  True  True False]

print(np.logical_xor(bool1, bool2))
# [False  True  True False]

'''
The first element is True in OR because at least one is True, 
but False in XOR because both are True.

(XOR requires that only exact one of the inputs is True, while OR allows for both to be True.)
'''


#-------------------------------------------------------------------------------------------------#
#--------------------------------- 5. Comparison -------------------------------------------------#
#-------------------------------------------------------------------------------------------------#

###################
## np.allclose() ##
###################
'''
np.allclose() returns True if two arrays are element-wise equal within a tolerance.
Returns a single boolean value.
Default tolerances: rtol=1e-5, atol=1e-8
'''

a = np.array([1.0, 2.0, 3.0])
b = np.array([1.0, 2.0, 3.000001])

print(np.allclose(a, b))
# True

c = np.array([1.0, 2.0, 3.1])
print(np.allclose(a, c))
# False

# With NaN handling
a_nan = np.array([1.0, np.nan, 3.0])
b_nan = np.array([1.0, np.nan, 3.0])
print(np.allclose(a_nan, b_nan))
# False
'''NOTE: NaN != NaN, they are not considered close or equal by default.'''

print(np.allclose(a_nan, b_nan, equal_nan=True))
# True
'''set equal_nan=True to consider NaNs as equal for the purpose of closeness.'''

##################
## np.isclose() ##
##################
'''
np.isclose() returns a boolean array where two arrays are element-wise equal within a tolerance.
Returns an array of booleans (element-wise comparison).
'''

print(np.isclose(a, b))
# [ True  True  True]

print(np.isclose(a, c))
# [ True  True False]

# With tolerance adjustment
print(np.isclose(a, c, atol=0.2))
# [ True  True  True]

######################
## np.array_equal() ##
######################
'''
np.array_equal() returns True if two arrays have the same shape and elements, False otherwise.
This is an exact comparison (no tolerance).
'''

arr1 = np.array([1, 2, 3])
arr2 = np.array([1, 2, 3])
arr3 = np.array([1, 2, 4])

print(np.array_equal(arr1, arr2))
# True

print(np.array_equal(arr1, arr3))
# False

# Different shapes
arr4 = np.array([[1, 2, 3]]) # shape (1, 3) vs arr1 shape (3,)
print(np.array_equal(arr1, arr4))
# False

# With NaN handling
a_nan = np.array([1.0, np.nan, 3.0])
b_nan = np.array([1.0, np.nan, 3.0])
print(np.array_equal(a_nan, b_nan))
# False

print(np.array_equal(a_nan, b_nan, equal_nan=True))
# True

######################
## np.array_equiv() ##
######################
'''
np.array_equiv() returns True if input arrays are shape consistent and all elements equal.
Allows broadcasting - shapes don't need to be identical.
'''

print(np.array_equiv(arr1, arr2))
# True

# Broadcasting example
scalar = np.array([5])
vector = np.array([5, 5, 5])
print(np.array_equiv(scalar, vector))
# True

print(np.array_equiv([1, 2], [[1, 2], [1, 2]]))
# True

print(np.array_equiv([1, 2], [[1, 2], [1, 3]]))
# False

##################
## np.greater() ##
##################
'''
np.greater() returns the truth value of (x1 > x2) element-wise.
Equivalent to the > operator.
'''

print(np.greater(v1, v2))
# [False False  True False  True]

print(np.greater(M1, M2))
# [[False False  True False]
#  [False  True False  True]
#  [ True False  True False]]

print(v1 > v2)
# [False False  True False  True]

########################
## np.greater_equal() ##
########################
'''
np.greater_equal() returns the truth value of (x1 >= x2) element-wise.
Equivalent to the >= operator.
'''

print(np.greater_equal(v1, v2))
# [False False  True False  True]

print(np.greater_equal(M1, M2))
# [[False False  True False]
#  [False  True False  True]
#  [ True  True  True False]]

print(v1 >= v2)
# [False False  True False  True]

###############
## np.less() ##
###############
'''
np.less() returns the truth value of (x1 < x2) element-wise.
Equivalent to the < operator.
'''

print(np.less(v1, v2))
# [ True  True False  True False]

print(np.less(M1, M2))
# [[ True  True False  True]
#  [ True False  True False]
#  [False False False  True]]

print(v1 < v2)
# [ True  True False  True False]

#####################
## np.less_equal() ##
#####################
'''
np.less_equal() returns the truth value of (x1 <= x2) element-wise.
Equivalent to the <= operator.
'''

print(np.less_equal(v1, v2))
# [ True  True False  True False]

print(np.less_equal(M1, M2))
# [[ True  True False  True]
#  [ True False  True False]
#  [False  True False  True]]

print(v1 <= v2)
# [ True  True False  True False]

################
## np.equal() ##
################
'''
np.equal() returns (x1 == x2) element-wise.
Equivalent to the == operator.
'''

print(np.equal(v1, v2))
# [False False False False False]

print(np.equal(M1, M2))
# [[False False False False]
#  [False False False False]
#  [False  True False False]]

print(v1 == v2)
# [False False False False  True]

####################
## np.not_equal() ##
####################
'''
np.not_equal() returns (x1 != x2) element-wise.
Equivalent to the != operator.
'''

print(np.not_equal(v1, v2))
# [ True  True  True  True  True]

print(np.not_equal(M1, M2))
# [[ True  True  True  True]
#  [ True  True  True  True]
#  [ True False  True  True]]

print(v1 != v2)
# [ True  True  True  True False]


#-----------------------------------------------------------------------------------------------------------#
#---------------------------- 6. Application in boolean indexing and masking -------------------------------#
#-----------------------------------------------------------------------------------------------------------#

v1 = np.array([-1, -6, 5, -10, 7])
v2 = np.array([6, 7, 3, 2, -9])

M1 = np.array([[1, -4, 7, -8], [-7 -7, 2, 6], [7, 10, -5, 3]])
print(M1)
# [[ 1 -4  7 -8]
#  [-7 -7  2  6]
#  [ 7 10 -5  3]]

M2 = np.array([[8, 6, 0, 6], [-4, -8, 10, 2], [-7, 10, -8, 4]])
print(M2)
# [[ 8  6  0  6]
#  [-4 -8 10  2]
#  [-7 10 -8  4]]

############################################

print(v1[v1 > 0])
# [5 7]

print(v2[v2 < v1])
# [3 -9]

print(M1[M1 > 0])
# [ 1  7  2  6  7 10  3]
'''Return as a 1D array of all positive elements in M1.'''

print(M2[np.logical_and(M2 > 0, M2 < 5)])
# [2, 4]

print(M1[:, np.any(M1 > 6, axis=0)]) # Select columns where any element is greater than 6
# [[ 1 -4  7]
#  [-7 -7  2]
#  [ 7 10 -5]]

print(M2[np.all(M2 >= -7, axis=1), :]) # Select rows where all elements are greater than or equal to -7
# [[8 6 0 6]]