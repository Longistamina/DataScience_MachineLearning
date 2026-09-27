'''
1. Element-wise Function Application (.map_elements)
2. Dictionary Mapping (.replace / .replace_strict)
'''

import numpy as np
import polars as pl

# Setup data
np.random.seed(42)
s_nums = pl.Series("nums", np.random.normal(loc=3, scale=2, size=5)).round(2)
print(s_nums)
# shape: (5,)
# Series: 'nums' [f64]
# [
# 	3.99
# 	2.72
# 	4.3
# 	6.05
# 	2.53
# ]

# Polars strictly types data. True mixed types require pl.Object (which is slow).
# Here we use strings to represent the mixed data for mapping.
s_mixed = pl.Series("mixed", ["apple", "banana", "cherry", "42", "3.14", None], dtype=pl.String)

# =========================================================================================
# 1. Element-wise Application
# =========================================================================================
'''
In pandas, you use .apply().
In Polars, the equivalent is .map_elements().

WARNING: .map_elements() forces Polars to drop down to a slow Python loop.
Always prefer native Polars expressions (like .log(), .exp()) when possible!
'''

# Native Polars expression (Fast & Recommended)
print(s_nums.log()) # Applying natural logarithm natively

# Sigmoid function using native expressions
s_sigmoid = 1 / (1 + (-s_nums).exp())
print(s_sigmoid)

# Using .map_elements() (Slow, use only for complex custom Python logic)
print(
    s_nums.map_elements(lambda x: x**2, return_dtype=pl.Float64)
)

# =========================================================================================
# 2. Dictionary Mapping
# =========================================================================================
'''
In pandas, you use .map() with a dictionary.
In Polars, you use .replace() or .replace_strict().
'''

mapping_dict = {"apple": "A", "banana": "B", "cherry": "C"}

# .replace() keeps original values if they are not in the dictionary
s_replaced = s_mixed.replace(mapping_dict)
print(s_replaced)
# shape: (6,)
# Series: 'mixed' [str]
# [
# 	"A"
# 	"B"
# 	"C"
# 	"42"
# 	"3.14"
# 	null
# ]

# .replace_strict() to map unmapped values to null (similar to pandas .map() behavior):
s_replaced_nulls = s_mixed.replace_strict(mapping_dict, default=None)
print(s_replaced_nulls)
# shape: (6,)
# Series: 'mixed' [str]
# [
# 	"A"
# 	"B"
# 	"C"
# 	null
# 	null
# 	null
# ]
