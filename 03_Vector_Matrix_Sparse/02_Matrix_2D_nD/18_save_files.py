'''
1. Using functions:
   + np.save(): save a single Numpy array to a binary file in .npy format.
   + np.savez(): save multiple Numpy arrays to a single compressed .npz file.
   + np.save_compressed(): save a single Numpy array to a compressed .npz file.
   + np.savetxt(): save a Numpy array to a text file, with options for formatting.

2. Using methods:
   + arr.dump(): save a Numpy array to a binary file using pickle serialization.
   + arr.tofile(): save a Numpy array to a text file with specified separator.'
'''

from pathlib import Path

import numpy as np

np.random.seed(0)
matrix_1 = np.random.randint(1, 100, size=(4, 5))
print(matrix_1)
# [[45 48 65 68 68]
#  [10 84 22 37 88]
#  [71 89 89 13 59]
#  [66 40 88 47 89]]

np.random.seed(0)
matrix_2 = np.random.uniform(0, 100, size=(4, 5)).round(2)
print(matrix_2)
# [[54.88 71.52 60.28 54.49 42.37]
#  [64.59 43.76 89.18 96.37 38.34]
#  [79.17 52.89 56.8  92.56  7.1 ]
#  [ 8.71  2.02 83.26 77.82 87.  ]]

save_path = next(Path('/home/').glob("**/02_Matrix_2D_nD/save"))
save_path.mkdir(parents=True, exist_ok=True)
print(save_path)
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/03_Vector_Matrix_Sparse/02_Matrix_2D_nD/save


# =========================================================================================
# 1. Using functions
# =========================================================================================

##-----------##
## np.save() ##
##-----------##
'''Save a single Numpy array to a binary file in .npy format.'''

np.save(file=save_path/'matrix_1.npy', arr=matrix_1) # Full syntax

np.save(save_path/'matrix_2.npy', matrix_2) # Shortcut syntax

##------------##
## np.savez() ##
##------------##
'''Save multiple Numpy arrays to a single compressed .npz file.'''

np.savez(file=save_path/'matrices.npz', mat1=matrix_1, mat2=matrix_2) # Full syntax (with named arrays as mat1 and mat2)

np.savez(save_path/'matrices.npz', matrix_1, matrix_2) # Shortcut syntax (with unnamed arrays)
                                                       # default names: arr_0, arr_1

# ## Load .npz file again
# 
loaded = np.load(save_path/'matrices.npz')

print(loaded.files)
# ['mat1', 'mat2']

print(loaded['mat1'])
# [[45 48 65 68 68]
#  [10 84 22 37 88]
#  [71 89 89 13 59]
#  [66 40 88 47 89]]

print(loaded['mat2'])
# [[54.88 71.52 60.28 54.49 42.37]
#  [64.59 43.76 89.18 96.37 38.34]
#  [79.17 52.89 56.8  92.56  7.1 ]
#  [ 8.71  2.02 83.26 77.82 87.  ]]

##----------------------##
## np.save_compressed() ##
##----------------------##
'''
Save multiple Numpy arrays to a compressed .npz file.

but applies stronger ZIP compression (specifically zipfile.ZIP_DEFLATED),
resulting in significantly smaller file sizes
'''

np.savez_compressed(file=save_path/'matrix_compressed.npz', mat1=matrix_1, mat2=matrix_2) # Full syntax

np.savez_compressed(save_path/'matrix_compressed.npz', matrix_1, matrix_2) # Shortcut syntax

##--------------##
## np.savetxt() ##
##--------------##
'''Save a Numpy array to a text file, with options for formatting.'''

np.savetxt(fname=save_path/'matrix_1.txt', X=matrix_1, fmt='%d', delimiter=', ') # Full syntax

np.savetxt(save_path/'matrix_2.txt', matrix_2, fmt='%.2f', delimiter=', ') # Shortcut syntax


# =========================================================================================
# 2. Using methods
# =========================================================================================

##------------##
## arr.dump() ##
##------------##
'''Save a Numpy array to a binary file using pickle serialization.'''

matrix_1.dump(file=save_path/'matrix_1_dump.pkl') # Full syntax

matrix_2.dump(save_path/'matrix_2_dump.pkl') # Shortcut syntax

##--------------##
## arr.tofile() ##
##--------------##
'''Save a Numpy array to a text file with specified separator.'''

matrix_1.tofile(file=save_path/'matrix_1_tofile.txt', sep=', ') # Full syntax

matrix_2.tofile(save_path/'matrix_2_tofile.txt', sep=', ') # Shortcut syntax
