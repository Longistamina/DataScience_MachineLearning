'''
1. Using s.iloc[]

2. dictionary style s[]

3. Using s.get() method

'''

import pandas as pd

#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 1. Using .iloc() -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

s_index = pd.Series(data=[10, 20, 30, 40, 50], index=['a', 'b', 'c', 'd', 'e'])

'''
.iloc[] is used for integer-location based indexing, 
which means you can access elements by their integer position.
'''

s_index.iloc[0]  # Accessing the first element
# np.int64(10)

s_index.iloc[1:3]  # Accessing a range of elements
# b    20
# c    30
# dtype: int64

s_index.iloc[:3] # Accessing from the start to the 2-indexed element (first three elements)
# a    10
# b    20
# c    30
# dtype: int64

s_index.iloc[2:]  # Accessing from the 2-indexed element to the end (third element and beyond)
# c    30
# d    40
# e    50
# dtype: int64

s_index.iloc[-1]  # Accessing the last element
# np.int64(50)

s_index.iloc[-3:]  # Accessing the last three elements
# c    30
# d    40
# e    50
# dtype: int64

s_index.iloc[[0, 2, 4]]  # Accessing specific elements by their integer positions
# a    10
# c    30
# e    50
# dtype: int64


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 2. Using dictionary style ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

s_index = pd.Series(data=[10, 20, 30, 40, 50], index=['a', 'b', 'c', 'd', 'e'])

s_index['a']  # Accessing by index label
# np.int64(10)

s_index[['a', 'c', 'e']]  # Accessing multiple elements by index labels
# a    10
# c    30
# e    50
# dtype: int64

s_index['b':'e']  # Accessing a range of elements by index labels (inclusive)
# b    20
# c    30
# d    40
# e    50
# dtype: int64

s_index['c':]  # Accessing from a specific index label to the end
# c    30
# d    40
# e    50
# dtype: int64

s_index[:'c']  # Accessing from the start to a specific index label (inclusive)
# a    10
# b    20
# c    30
# dtype: int64

s_index["f"] # Raises KeyError because "f" is not in the index
''' KeyError: 'f' '''

s_index.get('d', 'Not Found')  # Using get() to access an element with a default value if not found
# np.int64(40)

s_index.get('z', 'Not Found')  # Accessing a non-existent index label with a default value
# 'Not Found'

s_index.get('z') # Accessing a non-existent index label without a default value returns None
# None

s_index.get(['a', 'c', 'e'])  # Accessing multiple elements using get()
# a    10
# c    30
# e    50
# dtype: int64


##########################################
## NOTE on default integer index Series ##
##########################################

s_no_index = pd.Series(data=[2, 3, 5, 7, 11])

print(s_no_index)
# 0     2
# 1     3
# 2     5
# 3     7
# 4    11
# dtype: int64

s_no_index.iloc[0]  # Accessing the first element
# np.int64(2)

s_no_index[0]  # Accessing the first element using index label
# np.int64(2)

'''
These two methods result in the same output.
However, they are fundamentally different:
- .iloc[] is used for positional indexing, which means it accesses elements based on their integer position in the Series.
- Using index labels (like 0) accesses elements based on their label

This case is just a coincidence because the default index labels are integers starting from 0.
If the Series had a different index, using .iloc[] would still work based on position,
while using index labels would require the exact label to be present.
'''

s_index[0]
# <stdin>:1: FutureWarning: Series.__getitem__ treating keys as positions is deprecated. 
#            In a future version, integer keys will always be treated as labels (consistent with DataFrame behavior). 
#            To access a value by position, use `ser.iloc[pos]`
# np.int64(10)

'''
Here, the s_index series has a custom index, and using an integer key (like 0) raises a FutureWarning.
This is because in future versions of pandas, using integer keys will always be treated as labels,
not positions, to maintain consistency with DataFrame behavior.
'''


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 3. Using .get() method ---------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

s_index = pd.Series(data=[10, 20, 30, 40, 50], index=['a', 'b', 'c', 'd', 'e'])
s_no_index = pd.Series(data=[2, 3, 5, 7, 11])

print(s_index.get('c'))  # Accessing an existing index label
# 30

print(s_index.get('z'))  # Accessing a non-existent index label without a default value
# None

print(s_index.get('z', 'Not Found'))  # Accessing a non-existent index label with a default value
# 'Not Found'

print(s_index.get(['a', 'c', 'e']))  # Accessing multiple elements using get()
# a    10
# c    30
# e    50
# dtype: int64

print(s_no_index.get(2))  # Accessing the 3rd element in a default integer index Series
# 5
