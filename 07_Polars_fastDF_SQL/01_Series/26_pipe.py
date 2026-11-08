'''
Pandas uses .pipe() to pass DataFrames/Series into custom functions for method chaining.

While Polars Series objects do NOT have a .pipe() method, Polars Expressions (pl.Expr),
DataFrames (pl.DataFrame), and LazyFrames (pl.LazyFrame) ALL have .pipe()!
This offers a structured way to apply a sequence of user-defined functions (UDFs).

-> use `pl.select(pl.lit(series).pipe())` or `series.to_frame().pipe()``
'''

import numpy as np
import polars as pl
import scipy.stats as stats

##------------------------------------------##
## 1. Use `pl.select(pl.lit(series).pipe()) ##
##------------------------------------------##

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

##-----------------------------------##
## 2. Use `series.to_frame().pipe()` ##
##-----------------------------------##

def filter_df(df: pl.DataFrame, threshold: float) -> pl.DataFrame:
    return df.filter(df[:, 0] < threshold)

result = (
    s_normal
    .to_frame()
    .pipe(filter_df, threshold=2.0)
    .pipe(lambda df: df.mean())
)
print(result)
# shape: (1, 1)
# ┌───────┐
# │ vals  │
# │ ---   │
# │ f64   │
# ╞═══════╡
# │ 0.749 │
# └───────┘

##----------------------------------##
## 2. Example with `value_counts()` ##
##----------------------------------##
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
    s_gender
    .value_counts()
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

##-----------------------##
## 3. Piping with lambda ##
##-----------------------##
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
    s_normal
    .to_frame()
    .pipe(lambda df: df.filter(pl.col("vals") < 2.9))       # df is a DataFrame, pl.col works
    .pipe(lambda df: stats.shapiro(df["vals"].to_numpy()))   # df["vals"] extracts the Series
)

print(query)
# ShapiroResult(statistic=np.float64(0.8865328120075993), pvalue=np.float64(0.033671906069434675))
