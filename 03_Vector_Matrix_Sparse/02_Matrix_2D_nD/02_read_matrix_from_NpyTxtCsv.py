'''
1. np.load(): Read 2D matrix from .npy file
   + Basic example
   + np.load(allow_pickle=True) for object arrays

2. np.loadtxt(): Read 2D matrix from .txt and .csv files
   + From whitespace / delimiter-separated .txt file
   + From numeric .csv file with header (skiprows)
   + From multi-column .csv file (select subset of columns with usecols)

3. np.genfromtxt() for more control with TXT and CSV
   + Handle missing values and fill them
   + Read named columns (names=True) and convert to plain 2D matrix
'''

import numpy as np


#--------------------------------------------------------------------------------------------------------#
#------------------------------ Small helper for consistent inspection/printing --------------------------#
#--------------------------------------------------------------------------------------------------------#

def show_matrix_info(A, name="matrix", max_rows=8, max_cols=8):
    A = np.asarray(A)
    print(f"\n[{name}]")
    print(f"shape={A.shape}, dtype={A.dtype}")
    r = min(A.shape[0], max_rows) if A.ndim >= 1 else 1
    c = min(A.shape[1], max_cols) if A.ndim >= 2 else 1
    if A.ndim == 2:
        print(A[:r, :c])
        if A.shape[0] > r or A.shape[1] > c:
            print(f"... (showing top-left {r}x{c})")
    else:
        print(A)


#--------------------------------------------------------------------------------------------------------#
#------------------------------- 1. np.load(): Read matrix from .npy file -------------------------------#
#--------------------------------------------------------------------------------------------------------#

###################
## Basic example ##
###################

matrix_npy = np.load('03_Vector_Matrix_Sparse/02_Matrix_2D/data/adjMat.npy')
show_matrix_info(matrix_npy)
# [matrix]
# shape=(60, 60), dtype=float64
# [[0. 1. 1. 0. 1. 0. 0. 1.]
#  [1. 0. 0. 1. 1. 0. 0. 0.]
#  [1. 0. 0. 0. 1. 0. 0. 1.]
#  [0. 1. 0. 0. 0. 1. 1. 1.]
#  [1. 1. 1. 0. 0. 0. 1. 0.]
#  [0. 0. 0. 1. 0. 0. 1. 0.]
#  [0. 0. 0. 1. 1. 1. 0. 0.]
#  [1. 0. 1. 1. 0. 0. 0. 0.]]
# ... (showing top-left 8x8)

################################
## np.load(allow_pickle=True) ##
################################

matrix_obj = np.load('03_Vector_Matrix_Sparse/02_Matrix_2D/data/landmark_embedding.npy')
'''ValueError: Object arrays cannot be loaded when allow_pickle=False'''

matrix_obj = np.load('03_Vector_Matrix_Sparse/02_Matrix_2D/data/landmark_embedding.npy', allow_pickle=True)
show_matrix_info(matrix_obj, "matrix_obj")
# [matrix_obj]
# shape=(), dtype=object
# {'static_lmk_faces_idx': array([6365, 3772, 2857, 8839, 8777, 3822, 8905, 2262, 8891, 5249, 8626, 1180, 3742, 8800, 2238, 7341, 8803, 5920, 6229, 6768, 7532, 3729, 8731, 1582, 8542, 6409, 8231, 6080,  268, 3695, 5739, 7423,
#        7390, 2354, 8768, 5997,  885,  917, 6026, 6069, 8799, 2452, 7446, 7418, 3575, 8635,  509,  917, 6052, 8668, 7493]), 'static_lmk_bary_coords': array([[ 4.58957872e-01,  3.61623699e-01,  1.79418429e-01],
#        [ 5.36975363e-01,  4.57327891e-01,  5.69674607e-03],
#        [ 2.23368931e-01,  3.61421136e-02,  7.40488955e-01],
#        [ 3.48219843e-01,  2.05820120e-01,  4.45960037e-01],
#        [ 2.04693861e-01,  3.58752187e-01,  4.36553953e-01],
#        [ 2.04693861e-01,  4.36553953e-01,  3.58752187e-01],
# ... (truncated for brevity) ...

# Use .item() to get the dict first, then access specific matrix.
static_lmk_bary_coords = matrix_obj.item().get('static_lmk_bary_coords')
show_matrix_info(static_lmk_bary_coords, "static_lmk_bary_coords")
# [static_lmk_bary_coords]
# shape=(51, 3), dtype=float64
# [[0.45895787 0.3616237  0.17941843]
#  [0.53697536 0.45732789 0.00569675]
#  [0.22336893 0.03614211 0.74048896]
#  [0.34821984 0.20582012 0.44596004]
#  [0.20469386 0.35875219 0.43655395]
#  [0.20469386 0.43655395 0.35875219]
#  [0.44596004 0.20582012 0.34821984]
#  [0.03614211 0.22336893 0.74048896]]
# ... (showing top-left 8x3)


#--------------------------------------------------------------------------------------------------------#
#------------------------- 2. np.loadtxt(): Read matrix from .txt and .csv files ------------------------#
#--------------------------------------------------------------------------------------------------------#

##############################
## From delimiter .txt file ##
##############################

# Example: comma-separated txt (rows of numbers)
matrix_txt = np.loadtxt(
    fname='03_Vector_Matrix_Sparse/02_Matrix_2D/data/heights.txt',
    delimiter=',',
    ndmin=2,         # important: always return 2D even if it's 1 row or 1 column
)

show_matrix_info(matrix_txt, "matrix_txt")
# shape=(1, 1015), dtype=float64
# [[74. 74. 72. 72. 73. 69. 69. 71.]]
# ... (showing top-left 1x8)
'''This is a vector, but with ndmin=2 it is treated as a 2D matrix with 1 row.'''

#############################

# Example: whitespace-separated txt (delimiter can be omitted)
matrix_txt_ws = np.loadtxt(
    fname='03_Vector_Matrix_Sparse/02_Matrix_2D/data/heights_2D_space.txt',
    ndmin=2,
)

show_matrix_info(matrix_txt_ws, "matrix_txt_ws")
# [matrix_txt_ws]
# shape=(5, 203), dtype=float64
# [[74. 74. 72. 72. 73. 69. 69. 71.]
#  [77. 73. 74. 71. 72. 74. 75. 73.]
#  [70. 73. 74. 73. 71. 75. 71. 72.]
#  [72. 73. 73. 72. 69. 73. 78. 71.]
#  [71. 72. 70. 72. 72. 73. 72. 74.]]
# ... (showing top-left 5x8)

#########################################

# Example with semicolon delimiter
matrix_txt_semicolon = np.loadtxt(
    fname='03_Vector_Matrix_Sparse/02_Matrix_2D/data//heights_2D_semicolon.txt',
    delimiter=';',
    ndmin=2,
)

show_matrix_info(matrix_txt_semicolon, "matrix_txt_semicolon")
# [matrix_txt_semicolon]
# shape=(5, 203), dtype=float64
# [[74. 74. 72. 72. 73. 69. 69. 71.]
#  [77. 73. 74. 71. 72. 74. 75. 73.]
#  [70. 73. 74. 73. 71. 75. 71. 72.]
#  [72. 73. 73. 72. 69. 73. 78. 71.]
#  [71. 72. 70. 72. 72. 73. 72. 74.]]
# ... (showing top-left 5x8)

####################################################
## From multi-column .csv (select subset of cols) ##
####################################################
'''
Example: keep only specific columns to form a matrix
usecols can be list/tuple, range, or a single int (but single int gives 1D unless ndmin=2).

NOTE: the chosen columns must be all numeric or all string (meaning, must be consistent dtype).
'''

matrix_csv_usecols = np.loadtxt(
    fname='03_Vector_Matrix_Sparse/02_Matrix_2D/data/drinks.csv',
    delimiter=',',
    skiprows=1,
    usecols=(2, 4, 5),   # example: take columns 3, 5, 6 (0-based indexing)
    ndmin=2,             
)

show_matrix_info(matrix_csv_usecols, "matrix_csv_usecols")
# [matrix_csv_usecols]
# shape=(193, 3), dtype=float64
# [[  0.    0.    0. ]
#  [ 89.   54.    4.9]
#  [ 25.   14.    0.7]
#  [245.  312.   12.4]
#  [217.   45.    5.9]
#  [102.   45.    4.9]
#  [193.  221.    8.3]
#  [ 21.   11.    3.8]]
# ... (showing top-left 8x3)


#--------------------------------------------------------------------------------------------------------#
#------------------------- 3. np.genfromtxt() for more control with TXT and CSV -------------------------#
#--------------------------------------------------------------------------------------------------------#

A = np.loadtxt("03_Vector_Matrix_Sparse/02_Matrix_2D/data/adjacency_matrix.txt", delimiter=",")
'''
ValueError: could not convert string ' ' to float64 at row 0, column 52.

=> Use np.genfromtxt() to handle missing values.
'''

###############################################
## From .txt file with missing values filled ##
###############################################

A = np.genfromtxt(
    "03_Vector_Matrix_Sparse/02_Matrix_2D/data/adjacency_matrix.txt",
    delimiter=",",
    dtype=float,                 # or dtype=np.int8 if it's 0/1
    missing_values=["", " "],    # treat empty field and single-space as missing
    filling_values=np.nan,       # fill missing with np.nan (or 0, or other value)
    autostrip=True,              # strip whitespace around tokens
    ndmin=2,
    skip_header=1                # skip header row if present
)

show_matrix_info(A, "A")
# [A]
# shape=(50, 52), dtype=float64
# [[123.   0. 125.   0. 100.   0.   0.   0.]
#  [ 62. 125.   0. 120.   0.   0.   0.   0.]
#  [  0.   0. 120.   0.  73. 133.   0.   0.]
#  [  0. 100.   0.  73.   0. 108.   0.   0.]
#  [  0.   0.   0. 133. 108.   0.  45.   0.]
#  [  0.   0.   0.   0.   0.  45.   0. 103.]
#  [  0.   0.   0.   0.   0.   0. 103.   0.]
#  [  0.   0.   0.   0.   0.   0.   0.  70.]]
# ... (showing top-left 8x8)

#####################################################################
## From multi-column .csv with names=True (structured -> plain 2D) ##
#####################################################################
'''
names=True returns a structured array, which is not a regular 2D float matrix.
Convert it to a plain 2D matrix by stacking fields.
'''

############## Read only numeric columns without names=True ##############

table_struct = np.genfromtxt(
    fname='03_Vector_Matrix_Sparse/02_Matrix_2D/data/drinks.csv',
    delimiter=',',
    dtype=None,          # allow numpy to infer types; can be float if purely numeric
    encoding='utf-8',
    missing_values=["", " "],
    filling_values=np.nan,
    usecols=(2, 3, 4),
    autostrip=True,
    #names = True,
    ndmin=2
)

show_matrix_info(table_struct, "table_struct")
# [table_struct]
# shape=(194, 3), dtype=<U15
# [['beer_servings' 'spirit_servings' 'wine_servings']
#  ['0' '0' '0']
#  ['89' '132' '54']
#  ['25' '0' '14']
#  ['245' '138' '312']
#  ['217' '57' '45']
#  ['102' '128' '45']
#  ['193' '25' '221']]
# ... (showing top-left 8x3

############## Read named columns with names=True ##############

table_struct = np.genfromtxt(
    fname='03_Vector_Matrix_Sparse/02_Matrix_2D/data/drinks.csv',
    delimiter=',',
    dtype=None,          # allow numpy to infer types; can be float if purely numeric
    encoding='utf-8',
    missing_values=["", " "],
    filling_values=np.nan,
    usecols=(1, 2, 3),
    names=True,         # read header names
    autostrip=True,
    ndmin=2
)

show_matrix_info(table_struct, "table_struct")
# [table_struct]
# shape=(193, 1), dtype=[('beer_servings', '<U28'), ('spirit_servings', '<i8'), ('wine_servings', '<i8')]
# [[('Afghanistan',   0,   0)]
#  [('Albania',  89, 132)]
#  [('Algeria',  25,   0)]
#  [('Andorra', 245, 138)]
#  [('Angola', 217,  57)]
#  [('Antigua & Barbuda', 102, 128)]
#  [('Argentina', 193,  25)]
#  [('Armenia',  21, 179)]]
# ... (showing top-left 8x1)

######## skip_header=1 to avoid reading header as data ########

table_struct = np.genfromtxt(
    fname='03_Vector_Matrix_Sparse/02_Matrix_2D/data/drinks.csv',
    delimiter=',',
    dtype=None,          # allow numpy to infer types; can be float if purely numeric
    encoding='utf-8',
    missing_values=["", " "],
    filling_values=np.nan,
    usecols=(1, 2, 3),
    skip_header=1,         # skip header row
    autostrip=True,
    ndmin=2
)

show_matrix_info(table_struct, "table_struct")
# [table_struct]
# shape=(193, 1), dtype=[('f0', '<U28'), ('f1', '<i8'), ('f2', '<i8')]
# [[('Afghanistan',   0,   0)]
#  [('Albania',  89, 132)]
#  [('Algeria',  25,   0)]
#  [('Andorra', 245, 138)]
#  [('Angola', 217,  57)]
#  [('Antigua & Barbuda', 102, 128)]
#  [('Argentina', 193,  25)]
#  [('Armenia',  21, 179)]]
# ... (showing top-left 8x1)
'''The fild names are now f0, f1, f2 since we skipped the header.'''

