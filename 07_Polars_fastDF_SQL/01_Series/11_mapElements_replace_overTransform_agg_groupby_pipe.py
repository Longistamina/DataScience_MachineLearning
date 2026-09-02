'''
In Polars, the functional/declarative expression API replaces many of the
pandas Series-specific methods like .apply(), .transform(), and .agg().
Grouping is strictly a DataFrame operation (.group_by()), and dictionary
mapping is handled via .replace().

##--------------------------------------##
1. Element-wise Function Application (.map_elements)
2. Dictionary Mapping (.replace / .replace_strict)
3. Preserving Shape & Group-wise Transform (.over)
4. Aggregation Functions (.agg in DataFrame context)
5. Grouping Data (.group_by)
6. Method Chaining (via pl.select() or .to_frame())
'''

import numpy as np
import polars as pl
import scipy.stats as stats

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
s_applied_native = s_nums.log() # Applying natural logarithm natively
print(s_applied_native)

# Sigmoid function using native expressions
s_sigmoid = 1 / (1 + (-s_nums).exp())
print(s_sigmoid)

# Using .map_elements() (Slow, use only for complex custom Python logic)
s_applied_slow = s_nums.map_elements(lambda x: x**2, return_dtype=pl.Float64)
print(s_applied_slow)


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


# =========================================================================================
# 3. Transform & .over()
# =========================================================================================
'''
Pandas uses .transform() to apply functions while preserving shape,
especially with groupby().
In Polars, you use expressions inside .with_columns() and the .over() method
for group-wise transformations.
'''

df_date_value = pl.DataFrame({
    "Date": ["1st", "2nd", "3rd", "4th", "1st", "2nd", "3rd", "4th"],
    "Data": [5, 8, 6, 1, 50, 100, 60, 120],
})

# Apply multiple transformations preserving shape (No groupby)
df_transformed = df_date_value.with_columns(
    (pl.col("Data") + 1).alias("Data_plus_1"),
    (pl.col("Data") * 2).alias("Data_times_2")
)
print(df_transformed)
# shape: (8, 4)
# ┌──────┬──────┬─────────────┬──────────────┐
# │ Date ┆ Data ┆ Data_plus_1 ┆ Data_times_2 │
# │ ---  ┆ ---  ┆ ---         ┆ ---          │
# │ str  ┆ i64  ┆ i64         ┆ i64          │
# ╞══════╪══════╪═════════════╪══════════════╡
# │ 1st  ┆ 5    ┆ 6           ┆ 10           │
# │ 2nd  ┆ 8    ┆ 9           ┆ 16           │
# │ 3rd  ┆ 6    ┆ 7           ┆ 12           │
# │ 4th  ┆ 1    ┆ 2           ┆ 2            │
# │ 1st  ┆ 50   ┆ 51          ┆ 100          │
# │ 2nd  ┆ 100  ┆ 101         ┆ 200          │
# │ 3rd  ┆ 60   ┆ 61          ┆ 120          │
# │ 4th  ┆ 120  ┆ 121         ┆ 240          │
# └──────┴──────┴─────────────┴──────────────┘

# Group-wise transform (Equivalent to pandas df.groupby("Date").transform("sum"))
# The .over() method calculates the aggregation per group but broadcasts
# the result back to the original shape of the DataFrame!
df_group_transformed = df_date_value.with_columns(
    pl.col("Data").sum().over("Date").alias("Data_group_sum")
)
print(df_group_transformed)
# shape: (8, 3)
# ┌──────┬──────┬────────────────┐
# │ Date ┆ Data ┆ Data_group_sum │
# │ ---  ┆ ---  ┆ ---            │
# │ str  ┆ i64  ┆ i64            │
# ╞══════╪══════╪════════════════╡
# │ 1st  ┆ 5    ┆ 55             │
# │ 2nd  ┆ 8    ┆ 108            │
# │ 3rd  ┆ 6    ┆ 66             │
# │ 4th  ┆ 1    ┆ 121            │
# │ 1st  ┆ 50   ┆ 55             │
# │ 2nd  ┆ 100  ┆ 108            │
# │ 3rd  ┆ 60   ┆ 66             │
# │ 4th  ┆ 120  ┆ 121            │
# └──────┴──────┴────────────────┘


# =========================================================================================
# 4. .agg() & 5. .group_by()
# =========================================================================================
'''
In Polars, aggregation and grouping are combined into a single, highly expressive
DataFrame API: .group_by().agg().
Unlike pandas, Polars does not create messy MultiIndex columns. You explicitly
name your output columns using .alias().
'''

# Multiple aggregations on a Series (Using pl.select)
s_agg = pl.select(
    pl.col("nums").mean(),
    pl.col("nums").std(),
    pl.col("nums").min(),
    pl.col("nums").max()
).with_columns(pl.lit(s_nums).alias("dummy")) # Just to show how to apply to series context

# Actually, simpler for a standalone series:
print(pl.select(
    pl.lit(s_nums.mean()).alias("mean"),
    pl.lit(s_nums.std()).alias("std"),
    pl.lit(s_nums.min()).alias("min"),
    pl.lit(s_nums.max()).alias("max")
))
# shape: (1, 4)
# ┌───────┬──────────┬──────┬──────┐
# │ mean  ┆ std      ┆ min  ┆ max  │
# │ ---   ┆ ---      ┆ ---  ┆ ---  │
# │ f64   ┆ f64      ┆ f64  ┆ f64  │
# ╞═══════╪══════════╪══════╪══════╡
# │ 3.918 ┆ 1.419355 ┆ 2.53 ┆ 6.05 │
# └───────┴──────────┴──────┴──────┘

# Groupby and Aggregation (Equivalent to pandas df.groupby("Date").agg(...))
df_agg = df_date_value.group_by("Date", maintain_order=True).agg(
    pl.col("Data").count().alias("Data_count"),
    pl.col("Data").mean().alias("Data_mean"),
    pl.col("Data").sum().alias("Data_sum"),
    # Custom aggregation function using standard expressions
    (pl.col("Data").max() - pl.col("Data").min()).alias("Data_range")
)
print(df_agg)
# shape: (4, 5)
# ┌──────┬────────────┬───────────┬──────────┬────────────┐
# │ Date ┆ Data_count ┆ Data_mean ┆ Data_sum ┆ Data_range │
# │ ---  ┆ ---        ┆ ---       ┆ ---      ┆ ---        │
# │ str  ┆ u32        ┆ f64       ┆ i64      ┆ i64        │
# ╞══════╪════════════╪═══════════╪══════════╪════════════╡
# │ 1st  ┆ 2          ┆ 27.5      ┆ 55       ┆ 45         │
# │ 2nd  ┆ 2          ┆ 54.0      ┆ 108      ┆ 92         │
# │ 3rd  ┆ 2          ┆ 33.0      ┆ 66       ┆ 54         │
# │ 4th  ┆ 2          ┆ 60.5      ┆ 121      ┆ 119        │
# └──────┴────────────┴───────────┴──────────┴────────────┘


# =========================================================================================
# 6. Method Chaining
# =========================================================================================
'''
Pandas uses .pipe() to pass DataFrames/Series into custom functions for method chaining.

While Polars Series objects do NOT have a .pipe() method, Polars Expressions (pl.Expr),
DataFrames (pl.DataFrame), and LazyFrames (pl.LazyFrame) ALL have .pipe()!
This offers a structured way to apply a sequence of user-defined functions (UDFs).

-> use ``pl.select(pl.lit(series).pipe()) or series.to_frame().pipe()``
'''

##-----------------------##
## 1. Piping Expressions ##
##-----------------------##

np.random.seed(42)
s_normal = pl.Series("vals", np.random.normal(loc=3, scale=2, size=30)).round(2)

# 1. Define functions that take and return an EXPRESSION (pl.Expr)
def filter_small(expr: pl.Expr, threshold: float) -> pl.Expr:
    return expr.filter(expr < threshold)

def custom_agg(expr: pl.Expr) -> pl.Expr:
    return expr.mean().alias("mean_of_small_vals")

# 2. Convert Series -> Expr using pl.lit(), pipe the Expr, THEN evaluate with pl.select()
result = pl.select(
    pl.lit(s_normal)
      .pipe(filter_small, threshold=2.9)
      .pipe(custom_agg)
)
print(result)
# shape: (1, 1)
# ┌────────────────────┐
# │ mean_of_small_vals │
# │ ---                │
# │ f64                │
# ╞════════════════════╡
# │ 1.468889           │
# └────────────────────┘

##----------------------##
## 2. Piping DataFrames ##
##----------------------##
'''
If you are doing operations that return a DataFrame (like .value_counts()),
you can use DataFrame.pipe() to continue the chain exactly like pandas!
'''

s_gender = pl.Series("gender", ["F", "LGBTQ", "M", "F", "M", "LGBTQ", "F", "M", "F", "M", "M", "LGBTQ"])

def add_percentage(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.format("{}%", (pl.col("count") / pl.col("count").sum() * 100).round(2)).alias("percentage")
    )

# value_counts() on a Series returns a DataFrame, so we can immediately .pipe() it!
df_gender_stats = (
    s_gender.value_counts()
    .pipe(add_percentage)
)
print(df_gender_stats)
# shape: (3, 3)
# ┌────────┬───────┬────────────┐
# │ gender ┆ count ┆ percentage │
# │ ---    ┆ ---   ┆ ---        │
# │ str    ┆ u32   ┆ str        │
# ╞════════╪═══════╪════════════╡
# │ LGBTQ  ┆ 3     ┆ 25.0%      │
# │ F      ┆ 4     ┆ 33.33%     │
# │ M      ┆ 5     ┆ 41.67%     │
# └────────┴───────┴────────────┘

##------------------------##
## 3. Piping with lambada ##
##------------------------##
'''
Just like in pandas, you can use lambda functions inside .pipe() for quick,
inline transformations. Since pl.Series lacks .pipe(), we wrap the Series
in a DataFrame to leverage DataFrame.pipe(), filter the data, and finally
convert it to a NumPy array for scipy.stats.shapiro().
'''

np.random.seed(42)
s_normal = pl.Series("vals", np.random.normal(loc=3, scale=2, size=30)).round(2)

# 1. .to_frame() converts the Series into a DataFrame.
# 2. DataFrame.pipe() passes actual DataFrames to your lambdas.
# 3. Because we aren't using pl.select(), returning a Python object (ShapiroResult) is perfectly fine!
query = (
    s_normal.to_frame()
    .pipe(lambda df: df.filter(pl.col("vals") < 2.9))       # df is a DataFrame, pl.col works
    .pipe(lambda df: stats.shapiro(df["vals"].to_numpy()))   # df["vals"] extracts the Series
)

print(query)
# ShapiroResult(statistic=np.float64(0.8865328120075993), pvalue=np.float64(0.033671906069434675))
