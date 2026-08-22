'''
In Polars, Series DO NOT have custom indices (like 'a', 'b', 'c' in Pandas).
They are strictly 1-dimensional arrays with a name and positional row numbers.

1. Using bracket notation s[] (Positional Indexing & Slicing)
2. Using .slice(), .head(), and .tail() methods
3. Using .gather() for fancy indexing
4. Extracting scalar values using .item()
'''

import polars as pl


# =========================================================================================
# 1. Positional Indexing & Slicing
# =========================================================================================
'''
In Polars, bracket notation s[] is used for positional indexing and slicing,
which is conceptually identical to .iloc[] in Pandas.
'''

s = pl.Series("my_series", [10, 20, 30, 40, 50])

print(s[0])  # Accessing the first element
# 10

print(s[1:3])  # Accessing a range of elements
# shape: (2,)
# Series: 'my_series' [i64]
# [
# 	20
# 	30
# ]

print(s[:3])  # Accessing from the start to the 2-indexed element (first three elements)
# shape: (3,)
# Series: 'my_series' [i64]
# [
# 	10
# 	20
# 	30
# ]

print(s[2:])  # Accessing from the 2-indexed element to the end (third element and beyond)
# shape: (3,)
# Series: 'my_series' [i64]
# [
# 	30
# 	40
# 	50
# ]

print(s[-1])  # Accessing the last element
# 50

print(s[-3:])  # Accessing the last three elements
# shape: (3,)
# Series: 'my_series' [i64]
# [
# 	30
# 	40
# 	50
# ]


# =========================================================================================
# 2. Using .slice(), .head(), and .tail()
# =========================================================================================
'''
The .slice(offset, length) method extracts a subset of the Series.
- offset: The starting index (0-based).
- length: The number of elements to select. (Optional; defaults to the end of the Series).

This method is highly optimized and is the standard way to slice data inside Polars expressions.
For simply grabbing the first or last N elements, .head(n) and .tail(n) are more idiomatic.
'''

s = pl.Series("my_series", [10, 20, 30, 40, 50])

print(s.slice(1, 2))  # Start at index 1, take 2 elements (Equivalent to s[1:3])
# shape: (2,)
# Series: 'my_series' [i64]
# [
# 	20
# 	30
# ]

print(s.slice(2))  # Start at index 2, take the rest (Equivalent to s[2:])
# shape: (3,)
# Series: 'my_series' [i64]
# [
# 	30
# 	40
# 	50
# ]

print(s.head(3))  # First 3 elements (Equivalent to s[:3])
# shape: (3,)
# Series: 'my_series' [i64]
# [
# 	10
# 	20
# 	30
# ]

print(s.tail(2))  # Last 2 elements (Equivalent to s[-2:])
# shape: (2,)
# Series: 'my_series' [i64]
# [
# 	40
# 	50
# ]


# =========================================================================================
# 3. Fancy Indexing (.gather)
# =========================================================================================
'''Accessing specific elements by their integer positions'''

s = pl.Series("my_series", [10, 20, 30, 40, 50])

print(s[[0, 2, 4]])  # Passing a list of indices to brackets
# shape: (3,)
# Series: 'my_series' [i64]
# [
# 	10
# 	30
# 	50
# ]

print(s.gather([0, 2, 4]))  # Using the explicit .gather() method (Recommended for clarity)
# shape: (3,)
# Series: 'my_series' [i64]
# [
# 	10
# 	30
# 	50
# ]


# =========================================================================================
# 4. Extracting Scalars (.item)
# =========================================================================================
'''
.item() is used to extract a native Python scalar from a Series.
You can pass an index, or call it without arguments if the Series has exactly length 1.
'''

s = pl.Series("my_series", [10, 20, 30, 40, 50])

print(s.item(0))  # Accessing the first element as a Python int
# 10

print(s.item(-1))  # Accessing the last element
# 50

s_single = pl.Series([42])
print(s_single.item())  # Extracting the only element without specifying an index
# 42
