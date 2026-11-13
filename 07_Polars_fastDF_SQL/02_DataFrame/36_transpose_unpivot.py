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

data_dir = next(Path.home().rglob("*/DataScience_MachineLearning/data"))

# =========================================================================================
# 0. Setup Data
# =========================================================================================

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

# =========================================================================================
# 1. One-row wide summary: stay lazy before reshaping
# =========================================================================================
'''
A common first step is to summarize every column.

This produces a one-row wide LazyFrame:
+ one column per original variable
+ one value per column, such as null count or non-null count

This part is fully lazy.
'''

print(
    lf_mkt
    .select(
        pl.all().is_null().sum()
    )
    .collect()
)
# shape: (1, 26)
# one row, one null-count column per original column

print(
    lf_mkt
    .select(
        pl.all().is_not_null().sum()
    )
    .collect()
)
# shape: (1, 26)
# one row, one non-null-count column per original column

# =========================================================================================
# 2. Lazy alternative to transpose: use unpivot()
# =========================================================================================
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

print(
    lf_mkt
    .select(pl.all().is_null().sum())
    .unpivot(
        variable_name="column",
        value_name="null_count",
    )
    .collect()
)
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

# =========================================================================================
# 3. Filter after reshaping: still lazy
# =========================================================================================
'''
Because the result from `.unpivot()` is still a LazyFrame, we can continue filtering lazily.

Example: return only columns that contain at least one null.
'''

print(
    lf_mkt
    .select(pl.all().is_null().sum())
    .unpivot(variable_name="column", value_name="null_count")
    .filter(c("null_count") > 0)
    .sort("null_count", descending=True)
    .collect()
)
# Columns having at least one null, sorted by null_count
# shape: (13, 2)
# ┌────────────────┬────────────┐
# │ column         ┆ null_count │
# │ ---            ┆ ---        │
# │ str            ┆ u32        │
# ╞════════════════╪════════════╡
# │ grp_outdoor    ┆ 155        │
# │ grp_radio      ┆ 142        │
# │ reach_radio    ┆ 142        │
# │ reach_cinema   ┆ 138        │
# │ grp_print      ┆ 134        │
# │ grp_tv         ┆ 104        │
# │ reach_tv       ┆ 104        │
# │ competitor     ┆ 45         │
# │ share_of_spend ┆ 40         │
# │ top_of_mind    ┆ 33         │
# │ spontaneous    ┆ 33         │
# │ aided          ┆ 33         │
# │ penetration    ┆ 33         │
# └────────────────┴────────────┘

'''
Example: return only columns that are not complete.

Important:
Do NOT write `c.height` here. `c.height` means `pl.col("height")`, so Polars will
look for a real column named "height". Instead, create a row-count expression and
join/cross join it, or collect the scalar separately.
'''

print(
    lf_mkt
    .select(pl.all().is_not_null().sum())
    .unpivot(variable_name="column", value_name="n_not_null")
    .join(
        lf_mkt.select(pl.len().alias("n_rows")),
        how="cross",
    )
    .filter(c("n_not_null") < c("n_rows"))
    .sort("n_not_null")
    .collect()
)
# shape: (13, 3)
# ┌────────────────┬────────────┬────────┐
# │ column         ┆ n_not_null ┆ n_rows │
# │ ---            ┆ ---        ┆ ---    │
# │ str            ┆ u32        ┆ u32    │
# ╞════════════════╪════════════╪════════╡
# │ grp_outdoor    ┆ 1          ┆ 156    │
# │ grp_radio      ┆ 14         ┆ 156    │
# │ reach_radio    ┆ 14         ┆ 156    │
# │ reach_cinema   ┆ 18         ┆ 156    │
# │ grp_print      ┆ 22         ┆ 156    │
# │ grp_tv         ┆ 52         ┆ 156    │
# │ reach_tv       ┆ 52         ┆ 156    │
# │ competitor     ┆ 111        ┆ 156    │
# │ share_of_spend ┆ 116        ┆ 156    │
# │ top_of_mind    ┆ 123        ┆ 156    │
# │ spontaneous    ┆ 123        ┆ 156    │
# │ aided          ┆ 123        ┆ 156    │
# │ penetration    ┆ 123        ┆ 156    │
# └────────────────┴────────────┴────────┘

# =========================================================================================
# 4. Multiple summary metrics in long format
# =========================================================================================
'''
If you need more than one metric, do not force everything through transpose.
Build separate lazy summaries and join them by the `column` name.
'''

print(
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
    .collect()
)
# shape: (26, 6)
# ┌────────────────────────┬────────────┬────────────┬────────┬───────────┬───────────────┐
# │ column                 ┆ null_count ┆ n_not_null ┆ n_rows ┆ null_rate ┆ not_null_rate │
# │ ---                    ┆ ---        ┆ ---        ┆ ---    ┆ ---       ┆ ---           │
# │ str                    ┆ u32        ┆ u32        ┆ u32    ┆ f64       ┆ f64           │
# ╞════════════════════════╪════════════╪════════════╪════════╪═══════════╪═══════════════╡
# │ grp_outdoor            ┆ 155        ┆ 1          ┆ 156    ┆ 0.993590  ┆ 0.006410      │
# │ reach_radio            ┆ 142        ┆ 14         ┆ 156    ┆ 0.910256  ┆ 0.089744      │
# │ grp_radio              ┆ 142        ┆ 14         ┆ 156    ┆ 0.910256  ┆ 0.089744      │
# │ reach_cinema           ┆ 138        ┆ 18         ┆ 156    ┆ 0.884615  ┆ 0.115385      │
# │ grp_print              ┆ 134        ┆ 22         ┆ 156    ┆ 0.858974  ┆ 0.141026      │
# │ grp_tv                 ┆ 104        ┆ 52         ┆ 156    ┆ 0.666667  ┆ 0.333333      │
# │ reach_tv               ┆ 104        ┆ 52         ┆ 156    ┆ 0.666667  ┆ 0.333333      │
# │ competitor             ┆ 45         ┆ 111        ┆ 156    ┆ 0.288462  ┆ 0.711538      │
# │ …                      ┆ …          ┆ …          ┆ …      ┆ …         ┆ …             │
# │ shelf_share            ┆ 0          ┆ 156        ┆ 156    ┆ 0.000000  ┆ 1.000000      │
# │ non_promo_price_per_kg ┆ 0          ┆ 156        ┆ 156    ┆ 0.000000  ┆ 1.000000      │
# │ week                   ┆ 0          ┆ 156        ┆ 156    ┆ 0.000000  ┆ 1.000000      │
# │ share_of_ean_weigh     ┆ 0          ┆ 156        ┆ 156    ┆ 0.000000  ┆ 1.000000      │
# │ total_weigh            ┆ 0          ┆ 156        ┆ 156    ┆ 0.000000  ┆ 1.000000      │
# │ non_promo_price_vs_plb ┆ 0          ┆ 156        ┆ 156    ┆ 0.000000  ┆ 1.000000      │
# │ avg_price_vs_plb       ┆ 0          ┆ 156        ┆ 156    ┆ 0.000000  ┆ 1.000000      │
# └────────────────────────┴────────────┴────────────┴────────┴───────────┴───────────────┘

# =========================================================================================
# 5. Numeric summary report: lazy unpivot + split names
# =========================================================================================
'''
A slightly more advanced pattern:
1. Select numeric columns.
2. Compute several statistics.
3. Give each output a structured name like "mean__market_share".
4. Unpivot to long format.
5. Split the structured name into statistic and original column.

This is the lazy equivalent of transposing a block of summary statistics.
'''

print(
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
    .collect()
)
# shape: (96, 3)
# ┌────────┬─────────────────┬───────────────┐
# │ metric ┆ column          ┆ value         │
# │ ---    ┆ ---             ┆ ---           │
# │ str    ┆ str             ┆ f64           │
# ╞════════╪═════════════════╪═══════════════╡
# │ max    ┆ aided           ┆ 100.000000    │
# │ mean   ┆ aided           ┆ 98.201626     │
# │ min    ┆ aided           ┆ 95.700000     │
# │ std    ┆ aided           ┆ 0.998604      │
# │ max    ┆ av_price_per_kg ┆ 7.750000      │
# │ mean   ┆ av_price_per_kg ┆ 7.447628      │
# │ min    ┆ av_price_per_kg ┆ 6.980000      │
# │ std    ┆ av_price_per_kg ┆ 0.139442      │
# │ …      ┆ …               ┆ …             │
# │ mean   ┆ total_cm_shelf  ┆ 644728.268718 │
# │ min    ┆ total_cm_shelf  ┆ 596060.000000 │
# │ std    ┆ total_cm_shelf  ┆ 49605.212762  │
# │ max    ┆ total_weigh     ┆ 90.000000     │
# │ mean   ┆ total_weigh     ┆ 85.692308     │
# │ min    ┆ total_weigh     ┆ 81.000000     │
# │ std    ┆ total_weigh     ┆ 1.865183      │
# └────────┴─────────────────┴───────────────┘

# =========================================================================================
# 6. Eager fallback: DataFrame.transpose()
# =========================================================================================
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

# =========================================================================================
# 7. True matrix-style transpose
# =========================================================================================
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
