'''
1. Create a 2D matrix using np.array():
   + from nested list
   + from tuple of tuples

2. Create a 2D matrix using other NumPy functions:
   + np.arange() + reshape()
   + np.reshape()
   + np.zeros()
   + np.ones()
   + np.full()
   + np.eye()
   + np.identity()
   + np.diag()
   + np.tril(), np.triu()
   + np.fromfunction()
   + np.meshgrid() (build coordinate grids)
   
3. Create matrix using _like() functions
   + np.zeros_like(a)
   + np.ones_like(a)
   + np.full_like(a, fill_value)
   + np.empty_like(a)

4. Create random 2D matrices:
   + np.random.rand()
   + np.random.randn()
   + np.random.uniform()
   + np.random.randint()
   + np.random.seed(): for reproducibility
   + np.random.choice() + reshape()

5. Create a 2D matrix with dtype specified (int, float, complex, bool, etc.)

6. Create nD matrix (example with 3D and 4D matrices)
   + 3D matrix: (channel, height, width)
   + 4D matrix: (number_of_images, channel, height, width)
'''

import numpy as np

#-----------------------------------------------------------------------------------------------------------------#
#----------------------------------- 1. Create 2D matrix using np.array() ----------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

########################
## From a nested list ##
########################

matrix_list = np.array([
    [10, 20, 30],
    [40, 50, 60]
])

print(matrix_list)
# [[10 20 30]
#  [40 50 60]]

print(matrix_list.shape)  # (2, 3)
print(matrix_list.ndim)   # 2

##########################
## From tuple of tuples ##
##########################

matrix_tuple = np.array((
    (1.5, 2.7, 3.9),
    (4.1, 5.6, 6.2)
))

print(matrix_tuple)
# [[1.5 2.7 3.9]
#  [4.1 5.6 6.2]]


#-----------------------------------------------------------------------------------------------------------------#
#------------------------------ 2. Create 2D matrix using other numpy functions ----------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

#################################
## Using np.arange() + reshape ##
#################################
'''np.arange(start, stop, step).reshape(rows, cols)'''

matrix_arange_reshape = np.arange(0, 12, 1).reshape(3, 4)
print(matrix_arange_reshape)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

########################
## Using np.reshape() ##
########################
'''np.reshape(a, newshape)'''

a = np.arange(1, 10) # [1..9]

matrix_reshape = np.reshape(a, (3, 3))
print(matrix_reshape)
# [[1 2 3]
#  [4 5 6]
#  [7 8 9]]

###########################
## Using np.zeros(shape) ##
###########################
'''np.zeros((rows, cols))'''

matrix_zeros = np.zeros((2, 5))
print(matrix_zeros)
# [[0. 0. 0. 0. 0.]
#  [0. 0. 0. 0. 0.]]

##########################
## Using np.ones(shape) ##
##########################
'''np.ones((rows, cols))'''

matrix_ones = np.ones((3, 2))
print(matrix_ones)
# [[1. 1.]
#  [1. 1.]
#  [1. 1.]]

###############################
## Using np.full(shape, val) ##
###############################
'''np.full((rows, cols), fill_value)'''

matrix_full = np.full((2, 3), 7)
print(matrix_full)
# [[7 7 7]
#  [7 7 7]]

########################
## Using np.eye(N, M) ##
########################
'''
np.eye(N, M=None, k=0)
Creates a 2D array with ones on the k-th diagonal and zeros elsewhere.
'''

matrix_eye = np.eye(4)     # 4x4 identity-like
print(matrix_eye)
# [[1. 0. 0. 0.]
#  [0. 1. 0. 0.]
#  [0. 0. 1. 0.]
#  [0. 0. 0. 1.]]

matrix_eye_rect = np.eye(3, 5, k=1)  # 3x5, diagonal shifted right by 1
print(matrix_eye_rect)
# [[0. 1. 0. 0. 0.]
#  [0. 0. 1. 0. 0.]
#  [0. 0. 0. 1. 0.]]

##########################
## Using np.identity(N) ##
##########################
'''np.identity(n) creates an n x n identity matrix.'''

matrix_identity = np.identity(3)
print(matrix_identity)
# [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]]

#####################
## Using np.diag() ##
#####################
'''
np.diag(v) turns a 1D array into a diagonal matrix.
np.diag(A, k=0) extracts the k-th diagonal from A.
'''

diag_vals = np.array([3, 6, 9, 12])

matrix_diag = np.diag(diag_vals)
print(matrix_diag)
# [[ 3  0  0  0]
#  [ 0  6  0  0]
#  [ 0  0  9  0]
#  [ 0  0  0 12]]

#############

matrix_arange_reshape = np.arange(0, 12, 1).reshape(3, 4)
print(matrix_arange_reshape)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

extracted_main_diag = np.diag(matrix_arange_reshape)  # extract main diagonal
print(extracted_main_diag)
# [ 0  5 10]

################################
## Using np.tril(), np.triu() ##
################################
'''
np.tril(A, k=0): lower triangle of A
np.triu(A, k=0): upper triangle of A
'''

A = np.arange(1, 17).reshape(4, 4)
print(A)
# [[ 1  2  3  4]
#  [ 5  6  7  8]
#  [ 9 10 11 12]
#  [13 14 15 16]]

lower = np.tril(A)
print(lower)
# [[ 1  0  0  0]
#  [ 5  6  0  0]
#  [ 9 10 11  0]
#  [13 14 15 16]]


upper = np.triu(A)
print(upper)
# [[ 1  2  3  4]
#  [ 0  6  7  8]
#  [ 0  0 11 12]
#  [ 0  0  0 16]]

###########################
## Using np.fromfunction ##
###########################
'''
np.fromfunction(function, shape, dtype=float)
Builds an array by calling a function with coordinate arrays.
'''

matrix_fromfunction = np.fromfunction(lambda i, j: (i + 1) * 10 + (j + 1), (3, 4), dtype=int)
print(matrix_fromfunction)
# [[11 12 13 14]
#  [21 22 23 24]
#  [31 32 33 34]]

#########################
## Using np.meshgrid() ##
#########################
'''
np.meshgrid creates coordinate matrices from coordinate vectors.
Useful for building 2D coordinate grids or evaluating functions over a grid.
'''

x = np.linspace(-1, 1, 5)
print(x)  # [ -1.  -0.5  0.   0.5  1. ]

y = np.linspace(-2, 2, 3)
print(y)  # [ -2.   0.   2. ]

X, Y = np.meshgrid(x, y)  # shapes: (len(y), len(x))

print(X)
# [[-1.  -0.5  0.   0.5  1. ]
#  [-1.  -0.5  0.   0.5  1. ]
#  [-1.  -0.5  0.   0.5  1. ]]

print(Y)
# [[-2. -2. -2. -2. -2.]
#  [ 0.  0.  0.  0.  0.]
#  [ 2.  2.  2.  2.  2.]]

'''
These outputs mean generated a grid of (x, y) coordinates:
(-1, -2), (-0.5, -2), (0, -2), (0.5, -2), (1, -2)
(-1, 0),  (-0.5, 0),  (0, 0),  (0.5, 0),  (1, 0)
(-1, 2),  (-0.5, 2),  (0, 2),  (0.5, 2),  (1, 2)
'''

#-----------------------------------------------------------------------------------------------------------#
#------------------------------ 3. Create matrix using _like() functions -----------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
_like() functions create new arrays with the same shape (and usually dtype) as a reference array.

Common ones:
- np.zeros_like(a)
- np.ones_like(a)
- np.full_like(a, fill_value)
- np.empty_like(a)
'''

ref = np.arange(1, 13).reshape(3, 4)
print(ref)
# [[ 1  2  3  4]
#  [ 5  6  7  8]
#  [ 9 10 11 12]]

print(ref.shape)
# (3, 4)

print(ref.dtype)
# int64

###########################
## Using np.zeros_like() ##
###########################

matrix_zeros_like = np.zeros_like(ref)
print(matrix_zeros_like)
# [[0 0 0 0]
#  [0 0 0 0]
#  [0 0 0 0]]

print(matrix_zeros_like.shape)
# (3, 4)

print(matrix_zeros_like.dtype)
# int64

#########################
## Using np.ones_like()##
#########################

matrix_ones_like = np.ones_like(ref)
print(matrix_ones_like)
# [[1 1 1 1]
#  [1 1 1 1]
#  [1 1 1 1]]

##########################
## Using np.full_like() ##
##########################

matrix_full_like = np.full_like(ref, fill_value=7)
print(matrix_full_like)
# [[7 7 7 7]
#  [7 7 7 7]
#  [7 7 7 7]]

###########################
## Using np.empty_like() ##
###########################
'''
np.empty_like(a) allocates the array but does NOT initialize entries.
So the values are whatever was already in memory (don't assume zeros).
'''

np.set_printoptions(linewidth=200)

matrix_empty_like = np.empty_like(ref)
print(matrix_empty_like)
# [[          658114661                   0 7304689514905362797 7739836591928275053]
#  [7290888465049002085 7739836591928275053 1947570883626412133 3475446558499223133]
#  [4700406931139664647 3917317076179369479         31175947059                  41]]

'''
These numbers are just garbage values from memory.
Do NOT rely on the contents of an uninitialized array.
'''


#-----------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 4. Create random 2D matrices ---------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

############################
## Using np.random.rand() ##
############################
'''
np.random.rand(rows, cols)
Uniform random samples over [0, 1).
'''

matrix_rand = np.random.rand(2, 4)
print(matrix_rand)
# [[0.88443831 0.68078692 0.26143229 0.09252833]
#  [0.04652919 0.67900385 0.05179128 0.71653221]]

#############################
## Using np.random.randn() ##
#############################
'''
np.random.randn(rows, cols)
Standard normal random samples (mean=0, std=1).
'''

matrix_randn = np.random.randn(3, 3)
print(matrix_randn)
# [[ 0.74123416 -0.25461331  0.41454671]
#  [ 1.41266446 -0.75574305  0.28115116]
#  [-0.90930384  0.64018782  0.23725092]]

###############################
## Using np.random.uniform() ##
###############################
'''
np.random.uniform(low, high, size=(rows, cols))
Uniform random samples over [low, high).
'''

matrix_uniform = np.random.uniform(5.0, 15.0, size=(2, 3))
print(matrix_uniform)
# [[ 7.74273365  6.05881761  9.81261664]
#  [ 6.0621939  11.17337789  7.13174585]]

###############################
## Using np.random.randint() ##
###############################
'''
np.random.randint(low, high, size=(rows, cols))
Random integers in [low, high).
'''

matrix_randint = np.random.randint(10, 50, size=(3, 4))
print(matrix_randint)
# [[29 37 25 33]
#  [10 17 41 36]
#  [16 45 12 46]]

############################
## Using np.random.seed() ##
############################
'''
np.random.seed(seed)
Sets seed for reproducibility.
'''

np.random.seed(42)
matrix_seeded = np.random.rand(2, 3)

print(matrix_seeded)
# [[0.37454012 0.95071431 0.73199394]
#  [0.59865848 0.15601864 0.15599452]]
'''Always the same output with the same seed.'''

##############################
## Using np.random.choice() ##
##############################
'''
np.random.choice(a, size, replace=True, p=None)
Draw samples from a 1D array-like, then reshape into a matrix if desired.
'''

symbols = np.array(list("ABCDEFGH"))

np.random.seed(7)
matrix_choice = np.random.choice(symbols, size=12, replace=True).reshape(3, 4)
print(matrix_choice)
# [['H' 'E' 'B' 'G']
#  ['D' 'D' 'H' 'H']
#  ['E' 'B' 'G' 'H']]


#-----------------------------------------------------------------------------------------------------------------#
#------------------------------- 5. Create a 2D matrix with dtype specified --------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

matrix_float32 = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32)

print(matrix_float32)
# [[1. 2. 3.]
#  [4. 5. 6.]]

print(matrix_float32.dtype)  # float32

#################################

matrix_int64 = np.array([[1.5, 2.7, 3.9], [4.1, 5.6, 6.2]], dtype=np.int64)

print(matrix_int64)          # values are truncated toward zero
# [[1 2 3]
#  [4 5 6]]

print(matrix_int64.dtype)    # int64

#################################

matrix_complex = np.array([[1, 2], [3, 4]], dtype=np.complex64)

print(matrix_complex)
# [[1.+0.j 2.+0.j]
#  [3.+0.j 4.+0.j]]

print(matrix_complex.dtype)  # complex64

#################################

matrix_bool = np.array([[0, 1, 2], [0, -4, 5]], dtype=bool)

print(matrix_bool)
# [[False  True  True]
#  [False  True  True]]
'''0 is False; non-zero is True'''

print(matrix_bool.dtype) # bool


#-----------------------------------------------------------------------------------------------------------------#
#---------------------------- 6. Create nD matrix (example with 3D and 4D matrices) ------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

#########################################
## 3D matrix: (channel, height, width) ##
#########################################
'''
Modern digital images often use 3D arrays to represent color images.
For example, an RGB image with 3 channels (Red, Green, Blue) can be represented as a 3D array.

Each R, G and B channel is a 2D matrix representing pixel intensities.
Combining these 2D matrices along a new dimension (channel) forms a 3D matrix.
'''

CHANNELS = 3  # RGB
HEIGHT = 4
WIDTH = 8

np.random.seed(0)
image_3d = np.random.randint(0, 256, size=(CHANNELS, HEIGHT, WIDTH), dtype=np.uint8)

print(image_3d)
'''
[[[172  10 127 140  47 170 196 151]
  [117 166  22 183 192 204  33 216]               # Red channel
  [ 67 179  78 154 251  82 162 219]
  [195 118 125 139 103 125 229 216]]

 [[  9 164 116 108 211 222 161 159]
  [ 21  81  89 165 242 214 102  98]               # Green channel
  [ 36 183   5 112  87  58  43  76]
  [ 70  60  75 228 216 189 132  14]]

 [[ 88 154 178 246 140 205 204  69]
  [ 58  57  41  98 193  66  72 122]               # Blue channel
  [230 125 174 202  39  74 234 207]
  [ 87 168 101 135 174 200 223 122]]]
'''
# Can use matplotlib to visualize this 3D array as an image if needed.

print(image_3d.shape)  
# (3, 4, 8)

###########################################################
## 4D matrix: (number_of_images, channel, height, width) ##
###########################################################
'''
Each image is represented as a 3D array (channel, height, width).
Stacking multiple images along a new dimension (number_of_images) forms a 4D matrix.
'''

NUM_IMAGES = 4
CHANNELS = 3  # RGB
HEIGHT = 2
WIDTH = 3

np.random.seed(1)
images_4d = np.random.randint(0, 256, size=(NUM_IMAGES, CHANNELS, HEIGHT, WIDTH), dtype=np.uint8)

print(images_4d)
'''
[[[[ 37 244 193]
   [106 235 128]]

  [[ 71 255 140]
   [ 47 103 184]]                     # Image 1

  [[ 72  20 188]
   [238 255 126]]]


 [[[  7   0 137]
   [195 204  32]]

  [[203 170 101]
   [ 77 133  30]]                     # Image 2

  [[193 255  79]
   [203 145  37]]]


 [[[192  83 112]
   [ 60 144 128]]

  [[163  23 129]
   [ 80 134 101]]                     # Image 3

  [[204 191 174]
   [ 47  71  30]]]


 [[[ 78  99 237]
   [170 118  88]]

  [[252 121 116]
   [171 134 141]]                    # Image 4

  [[146 101  25]
   [125 127 239]]]]
'''

print(images_4d.shape)
# (4, 3, 2, 3)