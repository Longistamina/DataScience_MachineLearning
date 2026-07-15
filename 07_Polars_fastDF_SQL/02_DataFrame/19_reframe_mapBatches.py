'''
In pandas, "reframing" means returning a DataFrame with a completely different shape
(e.g., reducing columns to summary statistics, or generating new rows from distributions).
Unlike `.with_columns()` (which preserves row count) or `.group_by()` (which preserves column semantics),
reframing changes both dimensions.

In Polars, reframing is achieved via:
1. Native LazyFrame aggregations + `pl.concat()` (fully lazy, highly optimized).
2. `.collect().pipe(...)` + Python/SciPy functions (simple fallback for external libraries).
3. `.map_batches(...)` + Python/SciPy functions (keeps the step inside a LazyFrame pipeline, but needs schema).

####################################
1. Native LazyFrame Reframing: Quantiles as Rows
2. External Function Fallback: SciPy Statistical Tests (Shapiro-Wilk)
   - `.collect().pipe(...)` version
   - `.map_batches(...)` version
3. External Function Fallback: SciPy Distribution PPFs
   - `.collect().pipe(...)` version
   - `.map_batches(...)` version
4. Summary: `.pipe(...)` vs `.map_batches(...)`
'''

import polars as pl
from pathlib import Path
from scipy import stats

# Optional display settings
pl.Config.set_tbl_rows(10)
pl.Config.set_float_precision(6)


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 0. Setup Data ----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

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


#--------------------------------------------------------------------------------------------------------------#
#----------------------------- 1. Native LazyFrame Reframing: Quantiles as Rows -------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Pandas:
df[["rm", "lstat", "medv"]].apply(lambda col: np.quantile(col, q=[0.25, 0.5, 0.75, 1]), axis=0)

Polars:
Because Polars is columnar and lazy, we do NOT use `.apply()` with `axis=0`.
Instead, we natively compute the quantiles inside `select()` and use `pl.concat()`
to stack them into rows. This remains 100% lazy and highly optimized!
'''

qs = [0.25, 0.50, 0.75, 1.00]
labels = ["Q1", "Q2", "Q3", "Q4"]

lf_quantiles = pl.concat([
    lf_boston.select(
        pl.lit(label).alias("index"),
        pl.col("rm").quantile(q),
        pl.col("lstat").quantile(q),
        pl.col("medv").quantile(q)
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


#---------------------------------------------------------------------------------------------------------------------#
#-------------------- 2. External Function Fallback: SciPy Statistical Tests (Shapiro-Wilk) --------------------------#
#---------------------------------------------------------------------------------------------------------------------#
'''
Pandas:
df[["rm", "lstat", "medv"]].apply(stats.shapiro, axis=0)

Polars:
Since `scipy.stats.shapiro` is an external Python statistical test, it is not a
native Polars expression. It needs each selected column as a fully materialized
1D array and returns Python values.

Two practical Polars patterns are shown below:
1. `.collect().pipe(...)`: collect the selected columns, then construct the reframed result.
2. `.map_batches(...)`: keep the operation inside the LazyFrame chain, but specify the output schema.
'''

#-------------
# 2A. `.collect().pipe(...)` version: simple and explicit.
#-------------

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
            .with_columns(pl.Series("stat", ["W-statistic", "p-value"]))
            .select(["stat", *df.columns])
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

#-------------
# 2B. `.map_batches(...)` version: stays inside the LazyFrame chain.
#-------------

lf_shapiro_map_batches = (
    lf_boston
    .select("rm", "lstat", "medv")
    .map_batches(
        lambda df:
            pl.DataFrame({
                col: list(stats.shapiro(df[col].to_numpy()))
                for col in df.columns
            })
            .with_columns(pl.Series("stat", ["W-statistic", "p-value"]))
            .select(["stat", *df.columns]),
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


#-----------------------------------------------------------------------------------------------------------------------#
#---------------------------- 3. External Function Fallback: SciPy Distribution PPFs -----------------------------------#
#-----------------------------------------------------------------------------------------------------------------------#
'''
Pandas:
df.pipe(lambda df: pd.DataFrame({
    "rm_norm": stats.norm.ppf(q=[...], loc=df["rm"].mean(), scale=df["rm"].std()),
    ...
}))

Polars:
The SciPy PPF functions are external Python functions, so the final PPF values
are not native Polars expressions. However, the parameters passed into SciPy are
just scalar summaries such as mean and standard deviation.

Two practical Polars patterns are shown below:
1. `.collect().pipe(...)`: collect the selected columns, compute scalar summaries, then build a new LazyFrame.
2. `.map_batches(...)`: keep the operation inside the LazyFrame chain, but specify the output schema.

Note: `q=1` returns `inf` for these distributions because the 100th percentile is
the upper bound of unbounded continuous distributions. Use `0.99` for a finite value.
'''

#-------------
# 3A. `.collect().pipe(...)` version: simple and avoids manually specifying schema.
#-------------

lf_ppf_pipe = (
    lf_boston
    .select("rm", "lstat", "medv")
    .collect()
    .pipe(
        lambda df:
            pl.LazyFrame({
                "index": ["ppf_25th", "ppf_50th", "ppf_75th", "ppf_100th"],
                "rm_norm": stats.norm.ppf(
                    q=[0.25, 0.5, 0.75, 1],
                    loc=df.select("rm").mean().item(),
                    scale=df.select("rm").std().item(),
                ),
                "lstat_expon": stats.expon.ppf(
                    q=[0.25, 0.5, 0.75, 1],
                    scale=df.select("lstat").mean().item(),
                ),
                "medv_gamma": stats.gamma.ppf(
                    q=[0.25, 0.5, 0.75, 1],
                    a=2,
                    scale=df.select("medv").mean().item() / 2,
                ),
            })
    )
)

print(lf_ppf_pipe.collect())
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

#-------------
# 3B. `.map_batches(...)` version: stays inside the LazyFrame chain.
#-------------

lf_ppf_map_batches = (
    lf_boston
    .select("rm", "lstat", "medv")
    .map_batches(
        lambda df:
            pl.DataFrame({
                "index": ["ppf_25th", "ppf_50th", "ppf_75th", "ppf_100th"],
                "rm_norm": stats.norm.ppf(
                    q=[0.25, 0.5, 0.75, 1],
                    loc=df.select("rm").mean().item(),
                    scale=df.select("rm").std().item(),
                ),
                "lstat_expon": stats.expon.ppf(
                    q=[0.25, 0.5, 0.75, 1],
                    scale=df.select("lstat").mean().item(),
                ),
                "medv_gamma": stats.gamma.ppf(
                    q=[0.25, 0.5, 0.75, 1],
                    a=2,
                    scale=df.select("medv").mean().item() / 2,
                ),
            }),
        schema={
            "index": pl.String,
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


#----------------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 4. `.pipe(...)` vs `.map_batches(...)` ----------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
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
