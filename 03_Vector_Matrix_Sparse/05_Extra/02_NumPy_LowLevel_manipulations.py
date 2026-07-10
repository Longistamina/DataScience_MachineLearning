'''
1. Memory and structure information:
   + arr.base: Returns the base object if the array is a view, otherwise None.
   + arr.data: Returns a buffer containing the actual elements of the array.
   + arr.flags: Returns the memory layout information of the array.
   + arr.strides: Returns the number of bytes to step in each dimension when traversing an array.
   + arr.ctypes: Provides a ctypes interface to the array's data.

2. Structured array access:
   + arr.getfield(fieldname, dtype=None): Extracts a field from a structured array.
   + arr.setfield(val, fieldname, dtype=None): Sets field values in a structured array.
   + arr.setflags(write=True, align=False, uic=False): Modify array's memory layout flags.

3. Device switching (CPU/GPU):
   + arr.device: Returns the device on which the array is stored (CPU or GPU).
   + arr.to_device(device): Transfers the array to the specified device (CPU or GPU). Only "cpu" is supported now.
'''

import numpy as np

np.random.seed(0)
vector = np.random.uniform(0, 10, 10).round(2)

print(vector)
# [5.49 7.15 6.03 5.45 4.24 6.46 4.38 8.92 9.64 3.83]


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 1. Memory and structure information ----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

##############
## arr.base ##
##############
'''The base object if the array is a view, otherwise None.'''

print(vector.base)
# None

##############
## arr.data ##
##############
'''A buffer containing the actual elements of the array.'''

print(vector.data)
# <memory at 0x7fa0561fbd00>

###############
## arr.flags ##
###############
'''Information about the memory layout of the array.'''

print(vector.flags)
#   C_CONTIGUOUS : True       (this means the array is stored in a single, C-style contiguous segment of memory)
#   F_CONTIGUOUS : True       (this means the array is stored in a single, Fortran-style contiguous segment of memory)
#   OWNDATA : True            (the array owns the memory it uses)
#   WRITEABLE : True          (the array's data can be modified)
#   ALIGNED : True            (the data and strides are aligned appropriately for the hardware)
#   WRITEBACKIFCOPY : False   (the array is not a copy that needs to be written back to the original array)

#################
## arr.strides ##
#################
'''The number of bytes to step in each dimension when traversing an array.'''

print(vector.strides)
# (8,)
# This means that to move to the next element in the array, you need to step 8 bytes (which is the size of a float64).

################
## arr.ctypes ##
################
'''An object to access the array's data as a ctypes object.'''

print(vector.ctypes)
# <numpy._core._internal._ctypes object at 0x7fa0b5552a50>


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 2. Structured array access ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

####################
## arr.getfield() ##
####################
'''Extracts a field from a structured array.'''

structured_array = np.array([(1, 2.0), (3, 4.0)], dtype=[('x', 'i4'), ('y', 'f4')])

print(structured_array)
# [(1, 2.) (3, 4.)]

print(structured_array.getfield('i4', offset=0))
# [1 3]

####################
## arr.setfield() ##
####################
'''Sets field values in a structured array.'''

structured_array = np.array([(1, 2.0), (3, 4.0)], dtype=[('x', 'i4'), ('y', 'f4')])

structured_array.setfield(np.array([10, 20], dtype='i4'), np.dtype('i4'), offset=0)

print(structured_array)
# [(10, 2.) (20, 4.)]

####################
## arr.setflags() ##
####################
'''Modify array's memory layout flags.'''

print(vector.flags)
# WRITEABLE : True

vector.setflags(write=False)
print(vector.flags)
# WRITEABLE : False


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 3. Device switching (CPU/GPU) ----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

################
## arr.device ##
################
'''Returns the device on which the array is stored (CPU or GPU).'''

print(vector.device)
# cpu

###################
## arr.to_device ##
###################
'''Transfers the array to the specified device (CPU or GPU). Only "cpu" is supported now.'''

vector_cpu = vector.to_device("cpu")
print(vector_cpu.device)
# cpu

vector_gpu = vector.to_device("gpu")
# ValueError: Unsupported device: gpu. Only 'cpu' is accepted.

'''
CuPy is a GPU-accelerated library that implements a subset of NumPy and SciPy functionalities.

If you want to perform GPU computations, consider using CuPy.
'''