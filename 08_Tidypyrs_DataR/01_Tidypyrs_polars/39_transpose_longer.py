'''
Tidypyrs transpose / wide-to-long summary patterns

Main ideas:
1. For TibbleLazy workflows, prefer expression-based reshaping such as `.pivot_longer()`.
   This keeps the query lazy and avoids collecting just to rotate a one-row summary.
2. `TibbleFrame.transpose()` is an eager-only operation. Use it only after `.collect()`
   when you truly need a matrix-style transpose.
3. Many pandas-style "transpose a summary table" workflows are better written in tidypyrs as:
      tl.select(summary expressions).pivot_longer(...)
   instead of:
      tl.select(summary expressions).collect().transpose(...)

This file prioritizes TibbleLazy operations and falls back to eager TibbleFrame transpose only when needed.
'''

from pathlib import Path

import tidypyrs as tp
import tidypyrs.selectors as cs
from tidypyrs import f

# Requires the marketing_data.csv tutorial dataset.
# Output tables are illustrative; ties may appear in a different order.
# Optional display settings
tp.Config.set_tbl_rows(15)
tp.Config.set_tbl_cols(12)
tp.Config.set_tbl_width_chars(120)
tp.Config.set_float_precision(6)

data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))

# =========================================================================================
# 0. Setup Data
# =========================================================================================

tl_mkt = (
    tp.scan_csv(
        source=data_dir / 'marketing_data.csv',
        schema_overrides={
            'week': tp.Categorical,
            'Year': tp.Categorical,
        },
    )
    .rename(lambda col: col.lower().strip())
    .select(f.all().name.replace(r"[^a-zA-Z]", "_"))
)

print(tl_mkt.head(5).collect())
# shape: (5, 26)
# columns include: week, year, market_share, av_price_per_kg, ..., share_of_spend

print(tl_mkt.collect_schema())
# Schema([...])

# =========================================================================================
# 1. One-row wide summary: stay lazy before reshaping
# =========================================================================================
'''
A common first step is to summarize every column.

This produces a one-row wide TibbleLazy:
+ one column per original variable
+ one value per column, such as null count or non-null count

This part is fully lazy.
'''

print(
    tl_mkt
    .select(
        f.all().is_null().sum()
    )
    .collect()
)
# shape: (1, 26)
# one row, one null-count column per original column

print(
    tl_mkt
    .select(
        f.all().is_not_null().sum()
    )
    .collect()
)
# shape: (1, 26)
# one row, one non-null-count column per original column

# =========================================================================================
# 2. Lazy alternative to transpose: use pivot_longer()
# =========================================================================================
'''
For summary tables, we often want this shape instead:

    column          null_count
    week            0
    year            0
    market_share    0
    ...             ...

In pandas you might call `.T` or `.transpose()`.
In tidypyrs TibbleLazy, the better approach is `.pivot_longer()`.

`pivot_longer()` turns columns into rows and can run in a lazy query plan.
'''

print(
    tl_mkt
    .select(f.all().is_null().sum())
    .pivot_longer(
        names_to="column",
        values_to="null_count",
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
Because the result from `.pivot_longer()` is still a TibbleLazy, we can continue filtering lazily.

Example: return only columns that contain at least one null.
'''

print(
    tl_mkt
    .select(f.all().is_null().sum())
    .pivot_longer(names_to="column", values_to="null_count")
    .filter(f("null_count") > 0)
    .arrange(tp.desc("null_count"))
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
Do NOT use f.height as a row count: it represents a column named "height".
Use f("week").len() to count all rows, including rows with null week values.
Join that one-row summary lazily, or explicitly pull the scalar separately.
'''

print(
    tl_mkt
    .select(f.all().is_not_null().sum())
    .pivot_longer(names_to="column", values_to="n_not_null")
    .join(
        tl_mkt.select(f("week").len().alias("n_rows")),
        how="cross",
    )
    .filter(f("n_not_null") < f("n_rows"))
    .arrange("n_not_null")
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
    tl_mkt
    .select(f.all().is_null().sum())
    .pivot_longer(names_to="column", values_to="null_count")
    .join(
        tl_mkt
        .select(f.all().is_not_null().sum())
        .pivot_longer(names_to="column", values_to="n_not_null"),
        on="column",
        how="inner",
    )
    .join(
        tl_mkt.select(f("week").len().alias("n_rows")),
        how="cross",
    )
    .mutate(
        (f("null_count") / f("n_rows")).alias("null_rate"),
        (f("n_not_null") / f("n_rows")).alias("not_null_rate"),
    )
    .arrange(tp.desc("null_rate"))
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
# 5. Numeric summary report: lazy pivot_longer + split names
# =========================================================================================
'''
A slightly more advanced pattern:
1. Select numeric columns.
2. Compute several statistics.
3. Give each output a structured name like "mean__market_share".
4. Pivot longer to long format.
5. Split the structured name into statistic and original column.

This is the lazy equivalent of transposing a block of summary statistics.
'''

print(
    tl_mkt
    .select(
        cs.numeric().mean().name.prefix("mean__"),
        cs.numeric().std().name.prefix("std__"),
        cs.numeric().min().name.prefix("min__"),
        cs.numeric().max().name.prefix("max__"),
    )
    .pivot_longer(names_to="metric_column", values_to="value")
    .mutate(
        f("metric_column").str.split_exact("__", 1).struct.rename_fields(["metric", "column"]).alias("parts")
    )
    .unnest("parts") # Requires the unnest() wrapper on TibbleLazy.
    .select("metric", "column", "value")
    .arrange("column", "metric")
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
# 6. Eager fallback: TibbleFrame.transpose()
# =========================================================================================
'''
`transpose()` is a TibbleFrame method, not a TibbleLazy method.
Use it only after `.collect()`.

This is useful when you truly want a matrix-style rotation, or when you specifically
want the `include_header`, `header_name`, and `column_names` behavior.
'''

print(
    tl_mkt
    .select(f.all().is_null().sum())
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
    tl_mkt
    .select(f.all().is_not_null().sum())
    .collect()
    .transpose(
        include_header=True,
        header_name="column",
        column_names=["n_not_null"],
    )
    .filter(f("n_not_null") < tl_mkt.select(f("week").len().alias("n_rows")).pull("n_rows")[0])
)
# Filter columns whose non-null count is less than the total row count.

# =========================================================================================
# 7. True matrix-style transpose
# =========================================================================================
'''
A true transpose swaps rows and columns.
This usually requires eager materialization because the output schema depends on row values/counts.

For teaching/demo purposes, use a small collected TibbleFrame.
'''

print(
    tl_mkt
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
