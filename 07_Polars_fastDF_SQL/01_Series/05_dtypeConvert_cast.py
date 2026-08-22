'''
Converting and casting data types is a fundamental operation in Polars data manipulation.
Unlike Pandas, Polars is strictly typed and does not allow mixed-type Series (like [1, 'a', 3.0]).
The primary method for type conversion in Polars is `.cast()`.

##--------------------------------------##
1. .cast(): pl.Int64, pl.Float64, pl.String, pl.Categorical, pl.Boolean
2. Safe Numeric Conversion (strict=False equivalent to errors='coerce')
3. Categorical & Enum Data Types (Ordered categories)
4. String to Datetime Conversion (.str.to_datetime)
5. Timedelta / Duration Handling (pl.Duration)
6. String conversion (.cast(pl.String))
'''

import polars as pl


# =========================================================================================
# 1. .cast()
# =========================================================================================
'''
NOTE: Polars enforces strict typing upon Series creation.
A list like [1, 'a', 3.0] will either be cast to all Strings or raise an error upon creation.
To demonstrate parsing errors, we use a homogeneous String series containing non-numeric characters.
'''

s_nums = pl.Series([1, 2, 3, 4, 5])
s_str_int = pl.Series(['1', '2', '3', '4', '5'])
s_str_float = pl.Series(['1.5', '2.3', '3.6', '4.2', '5.0'])

s_mixed_str = pl.Series(['1', 'a', '3.0', '4.5', 'False'])

##-----------------##
## .cast(pl.Int64) ##
##-----------------##

s_convert = s_str_int.cast(pl.Int64)
print(s_convert)
# shape: (5,)
# Series: '' [i64]
# [
# 	1
# 	2
# 	3
# 	4
# 	5
# ]

s_convert = s_str_float.cast(pl.Int64)
"""polars.exceptions.InvalidOperationError: conversion from `str` to `i64` failed in column '' for 5 out of 5 values"""

##-------------------##
## .cast(pl.Float64) ##
##-------------------##

s_convert = s_nums.cast(pl.Float64)
print(s_convert)
# shape: (5,)
# Series: '' [f64]
# [
# 	1.0
# 	2.0
# 	3.0
# 	4.0
# 	5.0
# ]

s_convert = s_str_float.cast(pl.Float64)
print(s_convert)
# shape: (5,)
# Series: '' [f64]
# [
# 	1.5
# 	2.3
# 	3.6
# 	4.2
# 	5.0
# ]

s_convert = s_mixed_str.cast(pl.Float64)
"""polars.exceptions.InvalidOperationError: conversion from `str` to `f64` failed..."""

##------------------##
## .cast(pl.String) ##
##------------------##

s_convert = s_nums.cast(pl.String)
print(s_convert)
# shape: (5,)
# Series: '' [str]
# [
# 	"1"
# 	"2"
# 	"3"
# 	"4"
# 	"5"
# ]

##-------------------##
## .cast(pl.Boolean) ##
##-------------------##
'''
How Boolean conversion works in Polars:
- Polars is much stricter than Pandas.
- Numeric values: 0 is False, all other numbers are True (using .cast(pl.Boolean)).
- Strings: Direct casting from String to Boolean (e.g., .cast(pl.Boolean)) is NOT SUPPORTED
  in modern Polars due to ambiguity (e.g., how to handle "yes", "1", "T", "true"?).
  Instead, you must use string evaluation methods.
'''

s_bool_num = pl.Series([0, 1, 2, -1, 0])
s_convert = s_bool_num.cast(pl.Boolean)
print(s_convert)
# shape: (5,)
# Series: '' [bool]
# [
# 	false
# 	true
# 	true
# 	true
# 	false
# ]

s_bool_str = pl.Series(["true", "false", "True", "False"])
print(s_bool_str.cast(pl.Boolean))
"""InvalidOperationError: casting from Utf8View to Boolean not supported"""

# Correct idiomatic way to convert string booleans:
s_convert = s_bool_str.str.to_lowercase() == "true"
print(s_convert)
# shape: (4,)
# Series: '' [bool]
# [
# 	true
# 	false
# 	true
# 	false
# ]

# If you have multiple truthy string values (e.g., "yes", "1", "t"):
s_bool_str_multi = pl.Series(["yes", "no", "1", "0", "T", "F"])
s_convert_multi = s_bool_str_multi.str.to_lowercase().is_in(["true", "yes", "1", "t"])
print(s_convert_multi)
# shape: (6,)
# Series: '' [bool]
# [
# 	true
# 	false
# 	true
# 	false
# 	true
# 	false
# ]


# =========================================================================================
# 2. Safe Numeric Conversion
# =========================================================================================
'''
In Pandas, you use pd.to_numeric(errors='coerce').
In Polars, you simply use .cast(dtype, strict=False).
When strict=False, any values that cannot be parsed are converted to `null` instead of raising an error.
'''

s_mixed_str = pl.Series(['1.5', 'a', '3.6', '4.2', 'False'])

# ## Try with mixed data (will raise an error if strict=True, which is the default)
# s_mixed_str.cast(pl.Float64)
"""InvalidOperationError: conversion from `str` to `f64` failed..."""

# ## Try with mixed data, but coerce errors to null (strict=False)
# 
s_convert = s_mixed_str.cast(pl.Float64, strict=False)
print(s_convert)
# shape: (5,)
# Series: '' [f64]
# [
# 	1.5
# 	null
# 	3.6
# 	4.2
# 	null
# ]


# =========================================================================================
# 3. Categorical & Enum Data Types
# =========================================================================================
'''
Polars has two distinct types for categorical data:
1. pl.Categorical: Unordered, dictionary-encoded strings. Great for memory efficiency.
2. pl.Enum: Ordered, fixed set of categories. Equivalent to Pandas' ordered Categorical.
'''

lst_gender = ["M", "M", "F", "M", "LGBTQ", "F", "M", "F", "LGBTQ", "M"]
s_gender = pl.Series(lst_gender)

# ## Unordered Categorical (pl.Categorical)
# 
s_cat = s_gender.cast(pl.Categorical)
print(s_cat)
# shape: (10,)
# Series: '' [cat]
# [
# 	"M"
# 	"M"
# 	"F"
# 	"M"
# 	"LGBTQ"
# 	"F"
# 	"M"
# 	"F"
# 	"LGBTQ"
# 	"M"
# ]

# ## Ordered Categories (pl.Enum)
# '''
To specify the exact order of categories (like Pandas' pd.Categorical(..., ordered=True, categories=[...])),
Polars uses the `pl.Enum` data type.
'''

enum_dtype = pl.Enum(["LGBTQ", "F", "M"])
s_enum = s_gender.cast(enum_dtype)
print(s_enum)
shape: (10,)
# Series: '' [enum]
# [
# 	"M"
# 	"M"
# 	"F"
# 	"M"
# 	"LGBTQ"
# 	"F"
# 	"M"
# 	"F"
# 	"LGBTQ"
# 	"M"
# ]

print(s_enum.dtype)
# Enum(categories=['LGBTQ', 'F', 'M'])

##------------------------------------------------##
##            numeric example with nulls          ##
##------------------------------------------------##

lst_price_levels = [1, 1, 3, 2, 5, 2, None, 4, 4, None, 3]
s_price = pl.Series(lst_price_levels)

# Cast to Enum with defined levels
price_enum_dtype = pl.Enum(["1", "2", "3", "4", "5"])

# Note: Enum requires string categories, so we cast the integers to strings first
s_price_enum = s_price.cast(pl.String).cast(price_enum_dtype)
print(s_price_enum)
# shape: (11,)
# Series: '' [enum]
# [
# 	"1"
# 	"1"
# 	"3"
# 	"2"
# 	"5"
# 	…
# 	null
# 	"4"
# 	"4"
# 	null
# 	"3"
# ]


# =========================================================================================
# 4. String to Datetime Conversion
# =========================================================================================
'''
In Pandas, you use pd.to_datetime().
In Polars, string parsing is accessed via the `.str` namespace using `.str.to_datetime()`.
'''

s_dates = pl.Series(['2023-01-01', '2023-02-15', '2023-03-10', '2023-04-20'])
s_dates_invalid = pl.Series(['2023-01-01', '2023-02-15', '2023-03-10', 'invalid_date'])

# ## Convert valid date strings to datetime
# 
s_dates_converted = s_dates.str.to_datetime(format="%Y-%m-%d")
print(s_dates_converted)
# shape: (4,)
# Series: '' [datetime[μs]]
# [
# 	2023-01-01 00:00:00
# 	2023-02-15 00:00:00
# 	2023-03-10 00:00:00
# 	2023-04-20 00:00:00
# ]

# ## Convert invalid date strings (strict=True will raise an error)
# 
s_dates_invalid.str.to_datetime(format="%Y-%m-%d")
"""polars.exceptions.ComputeError: conversion from `str` to `datetime[μs]` failed..."""

# ## Coerce errors to null (strict=False)
# 
s_dates_converted = s_dates_invalid.str.to_datetime(
    format="%Y-%m-%d",
    strict=False
)
print(s_dates_converted)
# shape: (4,)
# Series: '' [datetime[μs]]
# [
# 	2023-01-01 00:00:00
# 	2023-02-15 00:00:00
# 	2023-03-10 00:00:00
# 	null
# ]


# =========================================================================================
# 5. Timedelta / Duration Handling
# =========================================================================================
'''
In Pandas, pd.to_timedelta() can parse arbitrary strings like "2 days 3 hours".
Polars handles durations via the `pl.Duration` type, but it DOES NOT have a built-in
string parser for arbitrary human-readable duration strings.

Instead, Polars expects:
1. Numeric values cast to Duration (representing microseconds, milliseconds, etc.)
2. Constructing durations programmatically using `pl.duration()` in an expression context.
'''

# ## 1. Casting numeric values to Duration
# # By default, casting integers to Duration assumes microseconds (us)

s_microseconds = pl.Series([1000000, 2000000, 3000000])
s_duration = s_microseconds.cast(pl.Duration)
print(s_duration)
# shape: (3,)
# Series: '' [duration[μs]]
# [
# 	1s
# 	2s
# 	3s
# ]

# ## 2. Creating durations from components (Days, Hours, Minutes)
# '''
If you have separate columns/series for days, hours, etc., you use `pl.duration()`
inside a DataFrame context.
'''

df_time = pl.DataFrame({
    "days": [2, 4, 6],
    "hours": [0, 3, 1],
    "minutes": [0, 0, 15]
})

df_with_duration = df_time.with_columns(
    pl.duration(
        days="days",
        hours="hours",
        minutes="minutes"
    ).alias("duration")
)
print(df_with_duration)
# shape: (3, 4)
# ┌──────┬───────┬─────────┬──────────────┐
# │ days ┆ hours ┆ minutes ┆ duration     │
# │ ---  ┆ ---   ┆ ---     ┆ ---          │
# │ i64  ┆ i64   ┆ i64     ┆ duration[μs] │
# ╞══════╪═══════╪═════════╪══════════════╡
# │ 2    ┆ 0     ┆ 0       ┆ 2d           │
# │ 4    ┆ 3     ┆ 0       ┆ 4d 3h        │
# │ 6    ┆ 1     ┆ 15      ┆ 6d 1h 15m    │
# └──────┴───────┴─────────┴──────────────┘


# =========================================================================================
# 6. String conversion
# =========================================================================================

s_nums = pl.Series([1.3, 5.4, 2.7, 8.6, 10.0])
print(s_nums.dtype)
# Float64

##------------------##
## .cast(pl.String) ##
##------------------##
'''
In Polars, the ONLY idiomatic and vectorized way to convert a Series to strings is `.cast(pl.String)`.
'''

s_str = s_nums.cast(pl.String)
print(s_str)
# shape: (5,)
# Series: '' [str]
# [
# 	"1.3"
# 	"5.4"
# 	"2.7"
# 	"8.6"
# 	"10.0"
# ]

##------------------------------------##
## NOTE on .map_elements() / .apply() ##
##------------------------------------##
'''
Pandas users often use .map(str) or .apply(str).
In Polars, `.map_elements(str)` exists, but it is considered an ANTI-PATTERN.
It forces Polars to drop down to a slow Python loop, completely bypassing
the Rust-based vectorized engine. Always use `.cast(pl.String)`.
'''

# Slow anti-pattern (Do not use unless applying complex custom Python logic):
print(s_nums.map_elements(str, return_dtype=pl.String))
# shape: (5,)
# Series: '' [str]
# [
# 	"1.3"
# 	"5.4"
# 	"2.7"
# 	"8.6"
# 	"10.0"
# ]
# /tmp/ipykernel_3519963/2273435177.py:1: PolarsInefficientMapWarning:
# Series.map_elements is significantly slower than the native series API.
# Only use if you absolutely CANNOT implement your logic otherwise.
# Replace this expression...
#   - s.map_elements(str)
# with this one instead:
#   + s.cast(pl.String)
#   print(s_nums.map_elements(str, return_dtype=pl.String))
