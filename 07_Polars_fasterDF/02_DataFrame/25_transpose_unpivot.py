'''
Polars transpose / wide-to-long summary patterns

Main ideas:
1. For LazyFrame workflows, prefer expression-based reshaping such as `.unpivot()`.
   This keeps the query lazy and avoids collecting just to rotate a one-row summary.
2. `DataFrame.transpose()` is an eager-only operation. Use it only after `.collect()`
   when you truly need a matrix-style transpose.
3. Many pandas-style "transpose a summary table" workflows are better written in Polars as:
      lf.select(summary expressions).unpivot(...)
   instead of:
      lf.select(summary expressions).collect().transpose(...)

This file prioritizes LazyFrame operations and falls back to eager DataFrame transpose only when needed.
'''

from pathlib import Path

import polars as pl
from polars import col as c
from polars import selectors as cs

# Optional display settings
pl.Config.set_tbl_rows(15)
pl.Config.set_tbl_cols(12)
pl.Config.set_tbl_width_chars(120)
pl.Config.set_float_precision(6)

data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))


#----------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 0. Setup Data --------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

lf_mkt = (
    pl.scan_csv(
        source=data_dir / 'marketing_data.csv',
        schema_overrides={
            'week': pl.Categorical,
            'Year': pl.Categorical,
        },
    )
    .rename(lambda col: col.lower().strip())
    .select(pl.all().name.replace(r"[^a-zA-Z]", "_"))
)

print(lf_mkt.head(5).collect())
# shape: (5, 26)
# columns include: week, year, market_share, av_price_per_kg, ..., share_of_spend

print(lf_mkt.collect_schema())
# Schema([...])


#----------------------------------------------------------------------------------------------------------------------#
#----------------------------- 1. One-row wide summary: stay lazy before reshaping ------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
'''
A common first step is to summarize every column.

This produces a one-row wide LazyFrame:
+ one column per original variable
+ one value per column, such as null count or non-null count

This part is fully lazy.
'''

lf_null_count_wide = lf_mkt.select(
    pl.all().is_null().sum()
)

print(lf_null_count_wide.collect())
# shape: (1, 26)
# one row, one null-count column per original column

lf_not_null_count_wide = lf_mkt.select(
    pl.all().is_not_null().sum()
)

print(lf_not_null_count_wide.collect())
# shape: (1, 26)
# one row, one non-null-count column per original column


#----------------------------------------------------------------------------------------------------------------------#
#-------------------------------- 2. Lazy alternative to transpose: use unpivot() -------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
'''
For summary tables, we often want this shape instead:

    column          null_count
    week            0
    year            0
    market_share    0
    ...             ...

In pandas you might call `.T` or `.transpose()`.
In Polars LazyFrame, the better approach is `.unpivot()`.

`unpivot()` turns columns into rows and can run in a lazy query plan.
'''

lf_null_count_long = (
    lf_mkt
    .select(pl.all().is_null().sum())
    .unpivot(
        variable_name="column",
        value_name="null_count",
    )
)

print(lf_null_count_long.collect())
# shape: (26, 2)
# ┌──────────────────────────┬────────────┐
# │ column                   ┆ null_count │
# │ ---                      ┆ ---        │
# │ str                      ┆ u32        │
# ╞══════════════════════════╪════════════╡
# │ week                     ┆ 0          │
# │ year                     ┆ 0          │
# │ market_share             ┆ 0          │
# │ ...                      ┆ ...        │
# └──────────────────────────┴────────────┘


#----------------------------------------------------------------------------------------------------------------------#
#----------------------------------- 3. Filter after reshaping: still lazy --------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
'''
Because the result from `.unpivot()` is still a LazyFrame, we can continue filtering lazily.

Example: return only columns that contain at least one null.
'''

lf_cols_with_nulls = (
    lf_mkt
    .select(pl.all().is_null().sum())
    .unpivot(variable_name="column", value_name="null_count")
    .filter(c("null_count") > 0)
    .sort("null_count", descending=True)
)

print(lf_cols_with_nulls.collect())
# Columns having at least one null, sorted by null_count

'''
Example: return only columns that are not complete.

Important:
Do NOT write `c.height` here. `c.height` means `pl.col("height")`, so Polars will
look for a real column named "height". Instead, create a row-count expression and
join/cross join it, or collect the scalar separately.
'''

lf_incomplete_cols = (
    lf_mkt
    .select(pl.all().is_not_null().sum())
    .unpivot(variable_name="column", value_name="n_not_null")
    .join(
        lf_mkt.select(pl.len().alias("n_rows")),
        how="cross",
    )
    .filter(c("n_not_null") < c("n_rows"))
    .sort("n_not_null")
)

print(lf_incomplete_cols.collect())
# shape: (..., 3)
# columns: column, n_not_null, n_rows


#----------------------------------------------------------------------------------------------------------------------#
#---------------------------------- 4. Multiple summary metrics in long format ----------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
'''
If you need more than one metric, do not force everything through transpose.
Build separate lazy summaries and join them by the `column` name.
'''

lf_missing_report = (
    lf_mkt
    .select(pl.all().is_null().sum())
    .unpivot(variable_name="column", value_name="null_count")
    .join(
        lf_mkt
        .select(pl.all().is_not_null().sum())
        .unpivot(variable_name="column", value_name="n_not_null"),
        on="column",
        how="inner",
    )
    .join(
        lf_mkt.select(pl.len().alias("n_rows")),
        how="cross",
    )
    .with_columns(
        (c("null_count") / c("n_rows")).alias("null_rate"),
        (c("n_not_null") / c("n_rows")).alias("not_null_rate"),
    )
    .sort("null_rate", descending=True)
)

print(lf_missing_report.collect())
# shape: (26, 5)
# columns: column, null_count, n_not_null, n_rows, null_rate, not_null_rate


#----------------------------------------------------------------------------------------------------------------------#
#----------------------------- 5. Numeric summary report: lazy unpivot + split names ----------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
'''
A slightly more advanced pattern:
1. Select numeric columns.
2. Compute several statistics.
3. Give each output a structured name like "mean__market_share".
4. Unpivot to long format.
5. Split the structured name into statistic and original column.

This is the lazy equivalent of transposing a block of summary statistics.
'''

lf_numeric_summary_long = (
    lf_mkt
    .select(
        cs.numeric().mean().name.prefix("mean__"),
        cs.numeric().std().name.prefix("std__"),
        cs.numeric().min().name.prefix("min__"),
        cs.numeric().max().name.prefix("max__"),
    )
    .unpivot(variable_name="metric_column", value_name="value")
    .with_columns(
        c("metric_column").str.split_exact("__", 1).struct.rename_fields(["metric", "column"]).alias("parts")
    )
    .unnest("parts")
    .select("metric", "column", "value")
    .sort("column", "metric")
)

print(lf_numeric_summary_long.collect())
# shape: (..., 3)
# columns: metric, column, value


#----------------------------------------------------------------------------------------------------------------------#
#----------------------------------- 6. Eager fallback: DataFrame.transpose() -----------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
'''
`transpose()` is a DataFrame method, not a LazyFrame method.
Use it only after `.collect()`.

This is useful when you truly want a matrix-style rotation, or when you specifically
want the `include_header`, `header_name`, and `column_names` behavior.
'''

print(
    lf_mkt
    .select(pl.all().is_null().sum())
    .collect()
    .transpose(
        include_header=True,
        header_name="column",
        column_names=["null_count"],
    )
)
# shape: (26, 2)
# columns: column, null_count

print(
    lf_mkt
    .select(pl.all().is_not_null().sum())
    .collect()
    .transpose(
        include_header=True,
        header_name="column",
        column_names=["n_not_null"],
    )
    .filter(c("n_not_null") < lf_mkt.select(pl.len()).collect().item())
)
# Filter columns whose non-null count is less than the total row count.


#----------------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 7. True matrix-style transpose -----------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
'''
A true transpose swaps rows and columns.
This usually requires eager materialization because the output schema depends on row values/counts.

For teaching/demo purposes, use a small collected DataFrame.
'''

print(
    lf_mkt
    .select("market_share", "av_price_per_kg", "promo_vol_share")
    .head(5)
    .collect()
    .transpose(
        include_header=True,
        header_name="original_column",
        column_names=[f"row_{i}" for i in range(5)],
    )
)
# shape: (3, 6)
# original numeric columns become rows; the original 5 observations become row_0 ... row_4 columns.


#----------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 8. Quick summary -------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
'''
Polars mental map

1. One-row wide summary
   lf.select(pl.all().is_null().sum())

2. Lazy "transpose-like" summary reshaping
   lf.select(pl.all().is_null().sum()).unpivot(variable_name="column", value_name="null_count")

3. Continue filtering lazily after reshaping
   ...unpivot(...).filter(c("null_count") > 0)

4. Eager true transpose
   lf.select(...).collect().transpose(...)

Rule of thumb:
+ Use `.unpivot()` for summary-table reshaping. It keeps the workflow lazy.
+ Use `.transpose()` only after `.collect()` when you truly need to rotate rows and columns.
+ Avoid `c.height` unless there is actually a column named "height". For row counts, use `pl.len()`.
'''
