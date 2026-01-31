'''
Saving and Loading:
   + save_npz() and load_npz(): NumPy compressed format
   + mmwrite() and mmread(): Matrix Market format
   + pickle: General Python serialization
'''

import numpy as np
from scipy import sparse
from scipy.sparse import (csr_array, csc_array, random_array)

import os
import pickle

#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ Saving and Loading ------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

###############################
## save_npz() and load_npz() ##
###############################
'''
Save to NumPy compressed format (.npz)
Efficient, preserves format and dtype
'''

# Create sparse array to save
A_save = random_array((100, 100), density=0.1, format='csr', random_state=42)
print(f"Original matrix: {A_save.shape}, nnz={A_save.nnz}")
# Original matrix: (100, 100), nnz=1000

# Save
filename_npz = 'sparse_matrix.npz'
sparse.save_npz(filename_npz, A_save)

# Load
A_loaded = sparse.load_npz(filename_npz)

print(f"\nLoaded matrix: {A_loaded.shape}, nnz={A_loaded.nnz}")
print(f"Format: {type(A_loaded)}")
print(f"Matrices equal: {np.allclose(A_save.toarray(), A_loaded.toarray())}")

# Cleanup
os.remove(filename_npz)
print(f"Cleaned up {filename_npz}")

##########################
## Matrix Market format ##
##########################
'''
Save/load in Matrix Market format (.mtx)
Portable text format
Compatible with other software (MATLAB, etc.)
'''

from scipy.io import mmwrite, mmread

A_mm = csr_array([[1, 0, 2],
                  [0, 3, 0],
                  [4, 0, 5]])

filename_mtx = 'sparse_matrix.mtx'

# Save
mmwrite(filename_mtx, A_mm)
print(f"Saved to {filename_mtx}")

# Load
A_mm_loaded = mmread(filename_mtx)

print(f"Loaded matrix: {A_mm_loaded.shape}")
print("Matrix content:")
print(A_mm_loaded.toarray())

# Cleanup
os.remove(filename_mtx)
print(f"\nCleaned up {filename_mtx}")

####################################
## Pickle (general serialization) ##
####################################
'''
Use pickle for general Python serialization
Can save multiple arrays in one file
'''

A_pickle = csr_array([[1, 2], [3, 4]])
B_pickle = csc_array([[5, 6], [7, 8]])

filename_pkl = 'sparse_matrices.pkl'

# Save multiple arrays
with open(filename_pkl, 'wb') as f:
    pickle.dump({'A': A_pickle, 'B': B_pickle}, f)

print(f"Saved to {filename_pkl}")

# Load
with open(filename_pkl, 'rb') as f:
    data = pickle.load(f)

print(f"Loaded {len(data)} matrices")
print("A:", data['A'].toarray())
print("B:", data['B'].toarray())

# Cleanup
os.remove(filename_pkl)
print(f"\nCleaned up {filename_pkl}")