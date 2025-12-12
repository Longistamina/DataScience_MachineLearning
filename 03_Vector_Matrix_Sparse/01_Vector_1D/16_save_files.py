'''
1. Using functions:
   + np.save(): save a single Numpy array to a binary file in .npy format.
   + np.savez(): save multiple Numpy arrays to a single compressed .npz file.
   + np.save_compressed(): save a single Numpy array to a compressed .npz file.
   + np.savetxt(): save a Numpy array to a text file, with options for formatting.

2. Using methods:
   + arr.dump(): save a Numpy array to a binary file using pickle serialization.
   + arr.tofile(): save a Numpy array to a binary file without any metadata.
'''

import numpy as np
from pathlib import Path

np.random.seed(0)
vector_1 = np.random.randint(1, 100, size=10)
print(vector_1)
# [45 48 65 68 68 10 84 22 37 88]

np.random.seed(0)
vector_2 = np.random.uniform(0, 100, size=10).round(2)
print(vector_2)
# [54.88 71.52 60.28 54.49 42.37 64.59 43.76 89.18 96.37 38.34]

save_path = Path('03_Vector_Matrix_Sparse/01_Vector_1D/save')
print(save_path)
# 03_Vector_Matrix_Sparse/01_Vector_1D/save

#-----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------ 1. Using functions ---------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------#

###############
## np.save() ##
###############
'''Save a single Numpy array to a binary file in .npy format.'''

np.save(file=save_path/'vector_1.npy', arr=vector_1) # Full syntax

np.save(save_path/'vector_2.npy', vector_2) # Shortcut syntax

################
## np.savez() ##
################
'''Save multiple Numpy arrays to a single compressed .npz file.'''

np.savez(file=save_path/'vectors.npz', vec1=vector_1, vec2=vector_2) # Full syntax (with named arrays as vec1 and vec2)

np.savez(save_path/'vectors.npz', vector_1, vector_2) # Shortcut syntax (with unnamed arrays)

#----
## Load .npz file again
#----

loaded = np.load(save_path/'vectors.npz')
print(loaded.files)
# ['vec1', 'vec2']

print(loaded['vec1'])
# [45 48 65 68 68 10 84 22 37 88]

print(loaded['vec2'])
# [54.88 71.52 60.28 54.49 42.37 64.59 43.76 89.18 96.37 38.34]

##########################
## np.save_compressed() ##
##########################
'''
Save multiple Numpy arrays to a compressed .npz file.
but applies stronger ZIP compression (specifically zipfile.ZIP_DEFLATED), resulting in significantly smaller file sizes
'''

np.savez_compressed(file=save_path/'vector_compressed.npz', vec1=vector_1, vec2=vector_2) # Full syntax

np.savez_compressed(save_path/'vector_compressed.npz', vector_1, vector_2) # Shortcut syntax

##################
## np.savetxt() ##
##################
'''Save a Numpy array to a text file, with options for formatting.'''

np.savetxt(fname=save_path/'vector_1.txt', X=vector_1, fmt='%d', delimiter=', ') # Full syntax

np.savetxt(save_path/'vector_2.txt', vector_2, fmt='%.1f', delimiter=', ') # Shortcut syntax

