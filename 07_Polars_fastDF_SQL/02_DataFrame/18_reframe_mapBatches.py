'''
In pandas, "reframing" means returning a DataFrame with a completely different shape
(e.g., reducing columns to summary statistics, or generating new rows from distributions).
Unlike `.with_columns()` (which preserves row count) or `.group_by()` (which preserves column semantics),
reframing changes both dimensions.

In Polars, reframing is achieved via:
1. Native LazyFrame aggregations + `pl.concat()` (fully lazy, highly optimized).
2. `.collect().pipe(...)` + Python/SciPy functions (simple fallback for external libraries).
3. `.map_batches(...)` + Python/SciPy functions (keeps the step inside a LazyFrame pipeline, but needs schema).

##--------------------------------##

1. Using `pl.concat()` for native operations that produce single-row dataframe (like `.quantile`)

2. Use `pl.Expr.map_batches()` for mapping custom functions to selected columns as realized Series

3. Use `pl.LazyFrame.map_batches()` to apply a custom function with a realized DataFrame

4. Use `pl.LazyFrame.collect().pipe()` as an alternative to `pl.LazyFrame.map_batches`

5. Native polars operations vs `.pipe(...)` vs `.map_batches(...)`
'''

from pathlib import Path

import numpy as np
import polars as pl
from polars import col as c
from scipy import stats

# Optional display settings
pl.Config.set_tbl_rows(10)
pl.Config.set_float_precision(6)

# =========================================================================================
# 0. Setup Data
# =========================================================================================

data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))

lf_boston = (
    pl.scan_csv(data_dir / "BostonHousing.csv")
    .drop(["CHAS", "RAD", "CAT. MEDV"])
    # Polars natively supports passing a callable to .rename() to clean column names
    .rename(lambda col: col.lower())
)

print(lf_boston.head().collect())
# shape: (5, 11)
# ┌─────────┬──────┬───────┬───────┬───────┬──────┬──────────┬──────┬─────────┬───────┬──────┐
# │ crim    ┆ zn   ┆ indus ┆ nox   ┆ rm    ┆ age  ┆ dis      ┆ tax  ┆ ptratio ┆ lstat ┆ medv │
# │ ---     ┆ ---  ┆ ---   ┆ ---   ┆ ---   ┆ ---  ┆ ---      ┆ ---  ┆ ---     ┆ ---   ┆ ---  │
# │ f64     ┆ f64  ┆ f64   ┆ f64   ┆ f64   ┆ f64  ┆ f64      ┆ i64  ┆ f64     ┆ f64   ┆ f64  │
# ╞═════════╪══════╪═══════╪═══════╪═══════╪══════╪══════════╪══════╪═════════╪═══════╪══════╡
# │ 0.00632 ┆ 18.0 ┆ 2.31  ┆ 0.538 ┆ 6.575 ┆ 65.2 ┆ 4.0900   ┆ 296  ┆ 15.3    ┆ 4.98  ┆ 24.0 │
# │ 0.02731 ┆ 0.0  ┆ 7.07  ┆ 0.469 ┆ 6.421 ┆ 78.9 ┆ 4.9671   ┆ 242  ┆ 17.8    ┆ 9.14  ┆ 21.6 │
# │ 0.02729 ┆ 0.0  ┆ 7.07  ┆ 0.469 ┆ 7.185 ┆ 61.1 ┆ 4.9671   ┆ 242  ┆ 17.8    ┆ 4.03  ┆ 34.7 │
# │ 0.03237 ┆ 0.0  ┆ 2.18  ┆ 0.458 ┆ 6.998 ┆ 45.8 ┆ 6.0622   ┆ 222  ┆ 18.7    ┆ 2.94  ┆ 33.4 │
# │ 0.06905 ┆ 0.0  ┆ 2.18  ┆ 0.458 ┆ 7.147 ┆ 54.2 ┆ 6.0622   ┆ 222  ┆ 18.7    ┆ 5.33  ┆ 36.2 │
# └─────────┴──────┴───────┴───────┴───────┴──────┴──────────┴──────┴─────────┴───────┴──────┘

# =====================================================================================================
# 1. Using `pl.concat()` for native operations that produce single-row dataframe (like `.quantile`)
# =====================================================================================================
'''
Here, we natively compute the quantiles inside `select()`
and use `pl.concat()` to stack them into rows.

This remains 100% lazy and highly optimized!
'''

qs = [0.25, 0.50, 0.75, 1.00]
labels = ["Q1", "Q2", "Q3", "Q4"]

lf_quantiles = pl.concat([
    lf_boston.select(
        pl.lit(label).alias("index"),
        c("rm", "lstat", "medv").quantile(q),
    )
    for q, label in zip(qs, labels)
])

print(lf_quantiles.collect())
# shape: (4, 4)
# ┌───────┬──────────┬───────────┬──────────┐
# │ index ┆ rm       ┆ lstat     ┆ medv     │
# │ ---   ┆ ---      ┆ ---       ┆ ---      │
# │ str   ┆ f64      ┆ f64       ┆ f64      │
# ╞═══════╪══════════╪═══════════╪══════════╡
# │ Q1    ┆ 5.8845   ┆ 6.885     ┆ 17.025   │
# │ Q2    ┆ 6.2085   ┆ 11.36     ┆ 21.2     │
# │ Q3    ┆ 6.6235   ┆ 16.955    ┆ 25.0     │
# │ Q4    ┆ 8.725    ┆ 37.97     ┆ 50.0     │
# └───────┴──────────┴───────────┴──────────┘

# ========================================================================================================
# 2. Use `pl.Expr.map_batches()` for mapping custom functions to selected columns as realized Series
# =========================================================================================================
'''
When we use `pl.col("name1", "name2", "name3").map_batches(lambda x: custom_func(x), return_type=pl.Float64)`,
the `x` in the `map_batches` is the realized Series evaluated from pl.col("name") expression!!!
This meaning the input for the function will be a Series representing that column, not a column expression.

The good thing is that `pl.Series` is compatible with `numpy` functions,
hence also compatible with `scipy` functions!!!

However, since polars has to realize the column expressions into Series,
the performance is reduced significantly, meaning it is less optimized.

Moreover, we also need to provide `return_type` for the `pl.Expr.map_batches()`
'''

##----------------------------##
## Example with `np.quantile` ##
##----------------------------##

qs = [0.25, 0.50, 0.75, 1.00]
labels = ["Q1", "Q2", "Q3", "Q4"]

print(
    lf_boston
    .select(
        c("rm", "lstat", "medv")
        .map_batches(lambda x: pl.Series(np.quantile(x, qs)), return_dtype=pl.Float64),
    )
    .select(
        pl.Series("index", labels),
        pl.all()
    )
    .collect()
)

##------------------------------------##
## Example with `scipy.stats.shapiro` ##
##------------------------------------##

print(
    lf_boston
    .select(
        c("rm", "lstat", "medv")
        .map_batches(lambda x: pl.Series(stats.shapiro(x.to_numpy())), return_dtype=pl.Float64), # Don't actually need `to_numpy` here
    )
    .select(
        pl.Series("stat", ["W-statistic", "p-value"]),
        pl.all()
    )
    .collect()
)
# shape: (2, 4)
# ┌─────────────┬──────────┬──────────┬──────────┐
# │ stat        ┆ rm       ┆ lstat    ┆ medv     │
# │ ---         ┆ ---      ┆ ---      ┆ ---      │
# │ str         ┆ f64      ┆ f64      ┆ f64      │
# ╞═════════════╪══════════╪══════════╪══════════╡
# │ W-statistic ┆ 0.960872 ┆ 0.936906 ┆ 0.917176 │
# │ p-value     ┆ 0.000000 ┆ 0.000000 ┆ 0.000000 │
# └─────────────┴──────────┴──────────┴──────────┘

##-------------------------------------------------##
## Example with many other `scipy.stats` functions ##
##-------------------------------------------------##
'''
The cumulative distribution function (CDF) takes a value and returns the probability
that a random variable is less than or equal to that value;

The percent-point function (PPF), also called the inverse CDF or quantile function,
takes a probability and returns the corresponding value whose CDF equals that probability.

In short: CDF input is a value and output is a probability;
PPF input is a probability in and output is a value on the distribution's scale.

##--------------------##

In this example,  for the sake of reframing demonstration,
we will calculate the PPF values for the 25th, 50th, 75th, and 100th percentiles,
but for different distributions: normal, exponential and gamma.

rm ~ normal distribution
lstat ~ exponential distribution
medv ~ gamma distribution
'''

qs = [0.25, 0.50, 0.75, 1.00]
ppfs = ["25th", "50th", "75th", "100th"]

print(
    lf_boston
    .select(
        c("rm").map_batches(lambda x: stats.norm.ppf(q=qs, loc=x.mean(), scale=x.std()), pl.Float64).alias("rm_norm"),
        c("lstat").map_batches(lambda x: stats.expon.ppf(q=qs, scale=x.mean()), pl.Float64).alias("lstat_expon"),
        c("medv").map_batches(lambda x: stats.gamma.ppf(q=qs, a=2, scale=x.mean()/2), pl.Float64).alias("medv_gamma")
    )
    .select(
        pl.Series("ppf", ppfs),
        pl.all()
    )
    .collect()
)
# shape: (4, 4)
# ┌───────┬──────────┬─────────────┬────────────┐
# │ ppf   ┆ rm_norm  ┆ lstat_expon ┆ medv_gamma │
# │ ---   ┆ ---      ┆ ---         ┆ ---        │
# │ str   ┆ f64      ┆ f64         ┆ f64        │
# ╞═══════╪══════════╪═════════════╪════════════╡
# │ 25th  ┆ 5.810726 ┆ 3.640059    ┆ 10.830154  │
# │ 50th  ┆ 6.284634 ┆ 8.770435    ┆ 18.908934  │
# │ 75th  ┆ 6.758542 ┆ 17.540870   ┆ 30.336306  │
# │ 100th ┆ inf      ┆ inf         ┆ inf        │
# └───────┴──────────┴─────────────┴────────────┘

# ===============================================================================================
# 3. Use `pl.LazyFrame.map_batches()` to apply a custom function with a realized DataFrame
# ===============================================================================================
'''
When we write `lf.map_batches(lambda df: custom_function(df))`,
the `df` here is the realized DataFrame from the given LazyFrame.

Only by doing so, other custom functions can access realized data to process.

However, since polars has to realize the LazyFrame into DataFrame,
the performance is reduced significantly, meaning it is less optimized.

Moreover, we have to provide the `schema` for the whole `lf.map_batches()`,
just like when we provide `return_type` for `pl.Expr.map_batches()`
'''

##------------------------------------##
## Example with `scipy.stats.shapiro` ##
##------------------------------------##

lf_shapiro_map_batches = (
    lf_boston
    .select("rm", "lstat", "medv")
    .map_batches(
        lambda df:
            pl.DataFrame({
                col: list(stats.shapiro(df[col].to_numpy()))
                for col in df.columns
            })
            .select(
                pl.Series("stat", ["W-statistic", "p-value"]),
                pl.all()
            ),
        schema={
            "stat": pl.String,
            "rm": pl.Float64,
            "lstat": pl.Float64,
            "medv": pl.Float64,
        },
    )
)

print(lf_shapiro_map_batches.collect())
# shape: (2, 4)
# ┌─────────────┬──────────┬──────────┬──────────┐
# │ stat        ┆ rm       ┆ lstat    ┆ medv     │
# │ ---         ┆ ---      ┆ ---      ┆ ---      │
# │ str         ┆ f64      ┆ f64      ┆ f64      │
# ╞═════════════╪══════════╪══════════╪══════════╡
# │ W-statistic ┆ 0.960872 ┆ 0.936906 ┆ 0.917176 │
# │ p-value     ┆ 0.000000 ┆ 0.000000 ┆ 0.000000 │
# └─────────────┴──────────┴──────────┴──────────┘

##--------------------------------------------##
## Example with other `scipy.stats` functions ##
##--------------------------------------------##

qs = [0.25, 0.50, 0.75, 1.00]
ppfs = ["25th", "50th", "75th", "100th"]

lf_ppf_map_batches = (
    lf_boston
    .select("rm", "lstat", "medv")
    .map_batches(
        lambda df:
            pl.DataFrame({
                "ppf": ppfs,
                "rm_norm": stats.norm.ppf(q=qs, loc=df.select("rm").mean().item(), scale=df.select("rm").std().item()),
                "lstat_expon": stats.expon.ppf(q=qs, scale=df.select("lstat").mean().item()),
                "medv_gamma": stats.gamma.ppf(q=qs, a=2, scale=df.select("medv").mean().item()/2),
            }),
        schema={
            "ppf": pl.String,
            "rm_norm": pl.Float64,
            "lstat_expon": pl.Float64,
            "medv_gamma": pl.Float64,
        },
    )
)

print(lf_ppf_map_batches.collect())
# shape: (4, 4)
# ┌───────────┬──────────┬─────────────┬────────────┐
# │ index     ┆ rm_norm  ┆ lstat_expon ┆ medv_gamma │
# │ ---       ┆ ---      ┆ ---         ┆ ---        │
# │ str       ┆ f64      ┆ f64         ┆ f64        │
# ╞═══════════╪══════════╪═════════════╪════════════╡
# │ ppf_25th  ┆ 5.810726 ┆ 3.640059    ┆ 10.830154  │
# │ ppf_50th  ┆ 6.284634 ┆ 8.770435    ┆ 18.908934  │
# │ ppf_75th  ┆ 6.758542 ┆ 17.540870   ┆ 30.336306  │
# │ ppf_100th ┆ inf      ┆ inf         ┆ inf        │
# └───────────┴──────────┴─────────────┴────────────┘

# ===============================================================================================
# 4. Use `pl.LazyFrame.collect().pipe()` as an alternative to `pl.LazyFrame.map_batches`
# ===============================================================================================
'''
After calling `.collect()`, we materialize everything, meaning the performance cost is significant.

However, when using `.collect().pipe()`, we don't need to provide the schema.
'''

##------------------------------------##
## Example with `scipy.stats.shapiro` ##
##------------------------------------##

lf_shapiro_pipe = (
    lf_boston
    .select("rm", "lstat", "medv")
    .collect()
    .pipe(
        lambda df:
            pl.LazyFrame({
                col: list(stats.shapiro(df[col].to_numpy()))
                for col in df.columns
            })
            .select(
                pl.Series("stat", ["W-statistic", "p-value"]),
                pl.all()
            ),
    )
)

print(lf_shapiro_pipe.collect())
# shape: (2, 4)
# ┌─────────────┬──────────┬──────────┬──────────┐
# │ stat        ┆ rm       ┆ lstat    ┆ medv     │
# │ ---         ┆ ---      ┆ ---      ┆ ---      │
# │ str         ┆ f64      ┆ f64      ┆ f64      │
# ╞═════════════╪══════════╪══════════╪══════════╡
# │ W-statistic ┆ 0.960872 ┆ 0.936906 ┆ 0.917176 │
# │ p-value     ┆ 0.000000 ┆ 0.000000 ┆ 0.000000 │
# └─────────────┴──────────┴──────────┴──────────┘

##--------------------------------------------##
## Example with other `scipy.stats` functions ##
##--------------------------------------------##

qs = [0.25, 0.50, 0.75, 1.00]
ppfs = ["25th", "50th", "75th", "100th"]

lf_ppf_pipe = (
    lf_boston
    .select("rm", "lstat", "medv")
    .collect()
    .pipe(
        lambda df:
            pl.LazyFrame({
                "ppf": ppfs,
                "rm_norm": stats.norm.ppf(q=qs, loc=df.select("rm").mean().item(), scale=df.select("rm").std().item()),
                "lstat_expon": stats.expon.ppf(q=qs, scale=df.select("lstat").mean().item()),
                "medv_gamma": stats.gamma.ppf(q=qs, a=2, scale=df.select("medv").mean().item()/2),
            }),
    )
)

print(lf_ppf_pipe.collect())
# shape: (4, 4)
# ┌───────┬──────────┬─────────────┬────────────┐
# │ ppf   ┆ rm_norm  ┆ lstat_expon ┆ medv_gamma │
# │ ---   ┆ ---      ┆ ---         ┆ ---        │
# │ str   ┆ f64      ┆ f64         ┆ f64        │
# ╞═══════╪══════════╪═════════════╪════════════╡
# │ 25th  ┆ 5.810726 ┆ 3.640059    ┆ 10.830154  │
# │ 50th  ┆ 6.284634 ┆ 8.770435    ┆ 18.908934  │
# │ 75th  ┆ 6.758542 ┆ 17.540870   ┆ 30.336306  │
# │ 100th ┆ inf      ┆ inf         ┆ inf        │
# └───────┴──────────┴─────────────┴────────────┘

# =========================================================================================
# 5. Native polars operations vs `.pipe(...)` vs `.map_batches(...)`
# =========================================================================================
'''
Summary:

1. Native Polars expressions are best when available.
   - They stay fully lazy.
   - They are optimized by Polars.
   - They avoid Python-level callbacks.

2. `.collect().pipe(...)` is usually best for final SciPy/Python summary tables.
   Pros:
   - Simple and readable.
   - No manual output schema is needed.
   - Good when the external Python function needs fully materialized data.
   - Good when the output is a small reframed table.

   Cons:
   - `.collect()` ends the lazy query at that point.
   - Anything after `.collect()` is outside Polars' lazy optimizer.
   - Less suitable in the middle of a larger lazy pipeline.

3. `.map_batches(...)` is usually best when you want to keep the custom Python step
   inside a LazyFrame chain.
   Pros:
   - Keeps the operation inside the lazy pipeline.
   - Allows Polars optimizations before the Python callback, such as projection pushdown.
   - More composable if later LazyFrame steps depend on the reframed result.

   Cons:
   - The Python callback is a black box to Polars.
   - You must specify `schema=...` when the output shape or column names change.
   - Be careful with statistical functions that require the full dataset; do not treat
     arbitrary batches as independent samples.

Rule of thumb:
- Use native Polars expressions first.
- Use `.collect().pipe(...)` for clean, final SciPy/Python summaries.
- Use `.map_batches(..., schema=...)` when the custom Python step should remain inside
  a LazyFrame pipeline.
'''
