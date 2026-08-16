'''
1. Using s.iloc[]
2. dictionary style s[]
3. Using s.get() method
4. Using .head() and .tail()
5. Using .item()
'''

import pandas as pd


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 1. Using .iloc() -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
.iloc[] is used for integer-location based indexing,
which means you can access elements by their integer position.
'''

s_index = pd.Series(data=[10, 20, 30, 40, 50], index=['a', 'b', 'c', 'd', 'e'])

print(s_index.iloc[0])  # Accessing the first element
# 10

print(s_index.iloc[1:3])  # Accessing a range of elements
# b    20
# c    30
# dtype: int64

print(s_index.iloc[:3]) # Accessing from the start to the 2-indexed element (first three elements)
# a    10
# b    20
# c    30
# dtype: int64

print(s_index.iloc[2:])  # Accessing from the 2-indexed element to the end (third element and beyond)
# c    30
# d    40
# e    50
# dtype: int64

print(s_index.iloc[-1])  # Accessing the last element
# 50

print(s_index.iloc[-3:])  # Accessing the last three elements
# c    30
# d    40
# e    50
# dtype: int64

print(s_index.iloc[[0, 2, 4]])  # Accessing specific elements by their integer positions
# a    10
# c    30
# e    50
# dtype: int64


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 2. Using dictionary style ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

s_index = pd.Series(data=[10, 20, 30, 40, 50], index=['a', 'b', 'c', 'd', 'e'])

print(s_index['a'])  # Accessing by index label
# 10

print(s_index[['a', 'c', 'e']])  # Accessing multiple elements by index labels
# a    10
# c    30
# e    50
# dtype: int64

print(s_index['b':'e'])  # Accessing a range of elements by index labels (inclusive)
# b    20
# c    30
# d    40
# e    50
# dtype: int64

print(s_index['c':])  # Accessing from a specific index label to the end
# c    30
# d    40
# e    50
# dtype: int64

print(s_index[:'c'])  # Accessing from the start to a specific index label (inclusive)
# a    10
# b    20
# c    30
# dtype: int64

# print(s_index["f"]) # Raises KeyError because "f" is not in the index
''' KeyError: 'f' '''

print(s_index.get('d', 'Not Found'))  # Using get() to access an element with a default value if not found
# 40

print(s_index.get('z', 'Not Found'))  # Accessing a non-existent index label with a default value
# 'Not Found'

print(s_index.get('z')) # Accessing a non-existent index label without a default value returns None
# None

print(s_index.get(['a', 'c', 'e']))  # Accessing multiple elements using get()
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

print(s_no_index.iloc[0])  # Accessing the first element
# 2

print(s_no_index[0])  # Accessing the first element using index label
# 2

'''
These two methods result in the same output.
However, they are fundamentally different:
- .iloc[] is used for positional indexing, which means it accesses elements based on their integer position in the Series.
- Using index labels (like 0) accesses elements based on their label
This case is just a coincidence because the default index labels are integers starting from 0.
If the Series had a different index, using .iloc[] would still work based on position,
while using index labels would require the exact label to be present.
'''

# print(s_index[0])
# <stdin>:1: FutureWarning: Series.__getitem__ treating keys as positions is deprecated.
#            In a future version, integer keys will always be treated as labels (consistent with DataFrame behavior).
#            To access a value by position, use `ser.iloc[pos]`
# 10

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


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------- 4. Using .head() and .tail() ---------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
.head(n) returns the first n elements (default is 5).
.tail(n) returns the last n elements (default is 5).
'''

s_index = pd.Series(data=[10, 20, 30, 40, 50], index=['a', 'b', 'c', 'd', 'e'])

print(s_index.head())  # First 5 elements (default)
# a    10
# b    20
# c    30
# d    40
# e    50
# dtype: int64

print(s_index.head(2))  # First 2 elements
# a    10
# b    20
# dtype: int64

print(s_index.tail())  # Last 5 elements (default)
# a    10
# b    20
# c    30
# d    40
# e    50
# dtype: int64

print(s_index.tail(2))  # Last 2 elements
# d    40
# e    50
# dtype: int64


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 5. Using .item() ---------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
.item() is used to extract a native Python scalar from a Series.

NOTE: Unlike Polars (where .item(-1) works), pandas' .item() DOES NOT accept an index argument.
It strictly only works on Series of exactly length 1.
'''

s_single = pd.Series([42], index=['x'])
s_multi = pd.Series([10, 20, 30], index=['a', 'b', 'c'])

print(s_single.item())  # Extracting the only element as a native Python scalar
# 42

# print(s_multi.item())  # Raises ValueError: can only convert an array of size 1 to a Python scalar
''' ValueError: can only convert an array of size 1 to a Python scalar '''
