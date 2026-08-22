'''
numpy has an options API to configure and customize global behavior related to array display,

printing behavior, error handling and more.

##-------------------------------------##

1. All available print options: np.get_printoptions()

2. Getting, Setting and Resetting options:
   + Getting: np.get_printoptions()
   + Setting: np.set_printoptions()
   + Resetting: np.set_printoptions() with default values

3. Setting startup options in Python/IPython environment

4. Frequently used options: threshold, precision, linewidth, edgeitems

5. Number formatting: np.set_printoptions() with formatter parameter

6. Error handling and warnings: np.seterr()

Detailed documentation: https://numpy.org/doc/stable/reference/generated/numpy.set_printoptions.html
'''

import numpy as np

# Create a sample array for demonstration
np.random.seed(0)
arr_large = np.random.randn(100, 10)
arr_small = np.random.randn(5, 5)

print(arr_small[:3])
# [[ 0.49671415 -0.1382643   0.64768854  1.52302986 -0.23415337]
#  [-0.23413696  1.57921282  0.76743473 -0.46947439  0.54256004]
#  [-0.46341769 -0.46572975  0.24196227 -1.91328024 -1.72491783]]

print(arr_small.shape) # (5, 5)


# =========================================================================================
# 1. All available options
# =========================================================================================
'''Use np.get_printoptions() to see all available print options in numpy.'''

print(np.get_printoptions())
# {'edgeitems': 3,
#  'threshold': 1000,
#  'floatmode': 'maxprec',
#  'precision': 8,
#  'suppress': False,
#  'linewidth': 75,
#  'nanstr': 'nan',
#  'infstr': 'inf',
#  'sign': '-',
#  'formatter': None,
#  'legacy': False,
#  'override_repr': None}

'''
Key options:
- linewidth: Number of characters per line for the purpose of inserting line breaks
- threshold: Total number of array elements which trigger summarization
- precision: Number of digits of precision for floating point output
- suppress: Whether to suppress small floating point values using scientific notation
- edgeitems: Number of array items in summary at beginning and end of each dimension
'''


# =========================================================================================
# 2. Getting, Setting and Resetting options
# =========================================================================================

##-----------------------##
## np.get_printoptions() ##
##-----------------------##
'''Use np.get_printoptions() to get the current value of all print options.'''

print(np.get_printoptions()['threshold'])  # 1000
print(np.get_printoptions()['precision'])  # 8
print(np.get_printoptions()['linewidth'])  # 75
print(np.get_printoptions()['suppress'])   # False
print(np.get_printoptions()['edgeitems'])  # 3

##-----------------------##
## np.set_printoptions() ##
##-----------------------##
'''Use np.set_printoptions() to set specific options to new values.'''

np.get_printoptions()['threshold']  # 1000

# Set new threshold option
np.set_printoptions(threshold=50)

# Check the updated value
np.get_printoptions()['threshold']  # 50

##-----------------------##
## Resetting to defaults ##
##-----------------------##
'''Reset options by calling np.set_printoptions() with default values.'''

print(np.get_printoptions()['suppress'])  # False

np.set_printoptions(suppress=True)
print(np.get_printoptions()['suppress'])  # True

# Reset to default value
np.set_printoptions(suppress=False)

# Check the reset value
print(np.get_printoptions()['suppress'])  # False


# =========================================================================================
# 3. Setting startup options in Python/IPython environment
# =========================================================================================
'''
NumPy and Python support setting startup options via configuration files.
So that you don't have to set them manually every time you start a new session.
You can add np.set_printoptions() calls to your Python startup file:

- For Python: Create/edit PYTHONSTARTUP environment variable to point to a .py file
- For IPython: Edit ~/.ipython/profile_default/startup/ files

Check the tutorial here:

https://numpy.org/doc/stable/reference/generated/numpy.set_printoptions.html
'''


# =========================================================================================
# 4. Frequently used options
# =========================================================================================

##------------------##
## linewidth option ##
##------------------##

np.set_printoptions(linewidth=50)
print(arr_large)
# [[ 0.37710159 -1.93120108 -0.50635607 ...
#    0.42398111  0.01647996  0.54036692]
#  [-0.89900563  0.36683676 -1.14387012 ...
#    2.03092065  0.03458387  2.03011815]
#  [ 0.97741049 -0.22296066  0.73184969 ...
#    0.19214448  0.1911831   0.5616129 ]
#  ...
#  [-0.72650107 -0.64680054 -0.81272205 ...
#   -1.22455176  0.62093696  0.06896606]
#  [-0.75526221  0.57094993 -0.03856273 ...
#    1.43408794 -0.38952117 -0.56208319]
#  [-0.31487046 -0.40836298 -0.69456197 ...
#   -0.302127   -0.3843384   0.24684914]]

np.set_printoptions(linewidth=200)  # Increase linewidth
print(arr_large)
# [[ 0.37710159 -1.93120108 -0.50635607 ...  0.42398111  0.01647996  0.54036692]
#  [-0.89900563  0.36683676 -1.14387012 ...  2.03092065  0.03458387  2.03011815]
#  [ 0.97741049 -0.22296066  0.73184969 ...  0.19214448  0.1911831   0.5616129 ]
#  ...
#  [-0.72650107 -0.64680054 -0.81272205 ... -1.22455176  0.62093696  0.06896606]
#  [-0.75526221  0.57094993 -0.03856273 ...  1.43408794 -0.38952117 -0.56208319]
#  [-0.31487046 -0.40836298 -0.69456197 ... -0.302127   -0.3843384   0.24684914]]

##------------------##
## threshold option ##
##------------------##

np.set_printoptions(threshold=1000)  # Reset to default value
print(np.get_printoptions()['threshold'])  # 1000

# 1D array - threshold works directly
arr_1d = np.arange(20)
print(arr_1d)
# [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19]

# ## Change threshold
# 
np.set_printoptions(threshold=10)
print(arr_1d)
# [ 0  1  2 ... 17 18 19]
'''The array is summarized because it exceeds the threshold of 10 elements.'''

print(arr_small)
# [[-0.64545551 -1.90324749  0.78045009  0.59288473 -0.90260525]
#  [ 0.36205196  1.03319039  0.71463915 -0.16278986  1.227468  ]
#  [ 1.86713902  1.00002004 -0.85628339  0.51902531 -1.31343602]
#  [ 0.15982805 -0.57092792  1.11825228 -0.72542611 -2.04426633]
#  [-1.4502758   0.23669499 -2.01157522 -0.01651778  1.25162587]]
'''
Even though arr_small has 25 elements, it is displayed in full
because it does not exceed the threshold of 10 elements per dimension.
'''

print(arr_large)
# [[ 1.76405235  0.40015721  0.97873798 ... -0.15135721 -0.10321885  0.4105985 ]
#  [ 0.14404357  1.45427351  0.76103773 ... -0.20515826  0.3130677  -0.85409574]
#  [-2.55298982  0.6536186   0.8644362  ... -0.18718385  1.53277921  1.46935877]
#  ...
#  [-0.65792609  0.96888264  0.22558166 ... -0.86404499 -0.14357951 -0.38202545]
#  [ 0.3595044  -0.14456682 -0.36159928 ...  0.7243685   1.38526155 -0.30309825]
#  [ 0.44103291  0.17879287 -0.7994224  ...  0.0941923  -1.14761094 -0.35811408]]
'''
arr_large has 10x100 shapes,
each dimension exceeds the threshold of 10 elements, so it is summarized.
'''

np.set_printoptions(threshold=1000)  # Reset to default value
print(arr_large)

##------------------##
## precision option ##
##------------------##

print(np.get_printoptions()['precision'])  # 8

arr = np.array([np.pi, np.e, np.sqrt(2)])
print(arr)
# [3.14159265 2.71828183 1.41421356]

np.set_printoptions(precision=3)
print(arr)
# [3.142 2.718 1.414]

np.set_printoptions(precision=8)  # Reset to default value

##-----------------##
## suppress option ##
##-----------------##

print(np.get_printoptions()['suppress'])  # False

arr_small_vals = np.array([1e-8, 1e-7, 1e-6, 1.0])
print(arr_small_vals)
# [1.e-08 1.e-07 1.e-06 1.e+00]

np.set_printoptions(suppress=True)
print(arr_small_vals)
# [0.00000001 0.0000001  0.000001   1.        ]

np.set_printoptions(suppress=False)  # Reset to default value

##------------------##
## edgeitems option ##
##------------------##

print(np.get_printoptions()['edgeitems'])  # 3

np.set_printoptions(threshold=10, edgeitems=2)
print(arr_large)
# [[ 1.76405235  0.40015721 ... -0.10321885  0.4105985 ]
#  [ 0.14404357  1.45427351 ...  0.3130677  -0.85409574]
#  ...
#  [ 0.3595044  -0.14456682 ...  1.38526155 -0.30309825]
#  [ 0.44103291  0.17879287 ... -1.14761094 -0.35811408]]
'''Only displays 2 items from the beginning and end of each dimension.'''

np.set_printoptions(threshold=1000, edgeitems=3)  # Reset to default value


# =========================================================================================
# 5. Number formatting
# =========================================================================================
'''
numpy allows you to set custom formatters for different data types.
Use the formatter parameter in np.set_printoptions() to alter the formatting.
'''

# Custom formatter for floating point numbers
np.set_printoptions(formatter={'float': lambda x: f'{x:,.2f}'})
np.random.seed(1)
arr = np.random.uniform(1000, 20000, size=(3, 3))
print(arr)
# [[8,923.42 14,686.17 1,002.17]
#  [6,744.32 3,788.36 2,754.43]
#  [4,538.94 7,565.65 8,538.58]]

# Scientific notation formatter
np.set_printoptions(formatter={'float': lambda x: f'{x:0.2e}'})
arr_sci = np.array([1234.5678, 0.0001234, 9876543.21])
print(arr_sci)
# [1.23e+03 1.23e-04 9.88e+06]

# Reset formatter
np.set_printoptions(formatter=None)


# =========================================================================================
# 6. Error handling
# =========================================================================================
'''
NumPy provides np.seterr() to control how floating-point errors are handled.
This is separate from the print options but equally important for configuring NumPy behavior.
'''

# Get current error handling settings
print(np.geterr())
# {'divide': 'warn', 'over': 'warn', 'under': 'ignore', 'invalid': 'warn'}

# ## Change error handling
# 
# Ignore division by zero warnings
np.seterr(divide='ignore')
result = np.array([1, 2, 3]) / 0
print(result)
# [inf inf inf]

# Raise exception on division by zero
np.seterr(divide='raise')
try:
    result = np.array([1, 2, 3]) / 0
except FloatingPointError as e:
    print(f"Error caught: {e}")
# Error caught: divide by zero encountered in divide

# Reset to default
np.seterr(divide='warn')

'''
Error handling options:
- 'ignore': Take no action
- 'warn': Print a RuntimeWarning
- 'raise': Raise a FloatingPointError
- 'call': Call a custom function
- 'print': Print a warning directly to stdout
- 'log': Record error in a Log object
'''
