'''
Pivot, Unpivot and Cross-Table are powerful techniques allowing you to reshape
and summarize data in Polars.

Polars naming is slightly different from pandas:

##-----------------------------------------------------------##

1. Pivot: long to wide
   + df.pivot(on=..., index=..., values=...)
   + df.pivot(..., aggregate_function=...)  # pandas pivot_table equivalent
   + lf.pivot(..., on_columns=...)          # lazy pivot; output columns must be known

2. Unpivot: wide to long
   + df.unpivot(on=..., index=...)
   + lf.unpivot(on=..., index=...)
   + df.melt(...) exists but is deprecated; prefer df.unpivot(...)
   + pandas wide_to_long equivalent: unpivot -> parse variable names -> pivot back

3. Cross-Table / Contingency Table
   + Polars does not have a dedicated pl.crosstab() function.
   + Use group_by(...).agg(pl.len()) + pivot(...), then fill nulls with 0.
   + Margins and normalizations are built explicitly with expressions.

Important differences from pandas:
+ Polars has no row index or MultiIndex. Index-like columns remain normal columns.
+ Polars pivoted columns are flat column names, not MultiIndex columns.
+ `DataFrame.pivot()` is eager. `LazyFrame.pivot()` needs `on_columns=` so that
  Polars knows the output schema before execution.
'''

import datetime as dt

import numpy as np
import polars as pl
import polars.selectors as cs


# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(16)
pl.Config.set_float_precision(3)
pl.Config.set_tbl_width_chars(120)


# =========================================================================================
# 1. Pivot: long to wide
# =========================================================================================

##--------------------------------##
## df.pivot(): basic long -> wide ##
##--------------------------------##
'''
The .pivot() method converts unique values from one column into multiple columns.

Pandas:
    pd.pivot(data=df, index="ID", columns="region", values="sales")

Polars:
    df.pivot(on="region", index="ID", values="sales")

NOTE:
+ pandas uses columns= for the variable that becomes new columns.
+ Polars uses on= for the variable that becomes new columns.
+ pandas puts index= into the DataFrame index.
+ Polars keeps index= as a normal column because Polars has no custom row index.
+ If there are duplicate index/on combinations and aggregate_function=None,
  Polars raises an error, just like pandas pivot raises an error.
'''

dates = [dt.date(2024, 1, 1) + dt.timedelta(days=i) for i in range(30)]
regions = ["North", "South", "East", "West"]
products = ["Widget", "Gadget", "Doohickey"]

np.random.seed(42)
selected_dates = [dates[i] for i in np.random.randint(0, len(dates), size=200)]

df_sales = pl.DataFrame(
    {
        "ID": range(1, 201),
        "date": selected_dates,
        "region": np.random.choice(regions, size=200),
        "product": np.random.choice(products, size=200),
        "quantity": np.random.randint(1, 20, size=200),
        "unit_price": np.round(np.random.uniform(5, 50, size=200), 2),
    }
).with_columns(
    (pl.col("quantity") * pl.col("unit_price")).round(2).alias("sales")
)

print(df_sales.head())
# shape: (5, 7)
# ┌─────┬────────────┬────────┬───────────┬──────────┬────────────┬─────────┐
# │ ID  ┆ date       ┆ region ┆ product   ┆ quantity ┆ unit_price ┆ sales   │
# │ --- ┆ ---        ┆ ---    ┆ ---       ┆ ---      ┆ ---        ┆ ---     │
# │ i64 ┆ date       ┆ str    ┆ str       ┆ i64      ┆ f64        ┆ f64     │
# ╞═════╪════════════╪════════╪═══════════╪══════════╪════════════╪═════════╡
# │ 1   ┆ 2024-01-07 ┆ East   ┆ Gadget    ┆ 5        ┆ 6.190      ┆ 30.950  │
# │ 2   ┆ 2024-01-20 ┆ North  ┆ Widget    ┆ 10       ┆ 21.940     ┆ 219.400 │
# │ 3   ┆ 2024-01-29 ┆ East   ┆ Doohickey ┆ 5        ┆ 41.470     ┆ 207.350 │
# │ 4   ┆ 2024-01-15 ┆ East   ┆ Widget    ┆ 4        ┆ 49.430     ┆ 197.720 │
# │ 5   ┆ 2024-01-11 ┆ North  ┆ Widget    ┆ 2        ┆ 11.770     ┆ 23.540  │
# └─────┴────────────┴────────┴───────────┴──────────┴────────────┴─────────┘

# ## Basic usage
# 
df_pivoted = df_sales.pivot(
    on="region",      # Values in this column become new column names.
    index="ID",       # This remains a normal column in Polars.
    values="sales",   # Values used to fill the new wide columns.
    sort_columns=True # Sort the generated region columns alphabetically.
)

print(df_pivoted.head())
# shape: (5, 5)
# ┌─────┬─────────┬─────────┬───────┬──────┐
# │ ID  ┆ East    ┆ North   ┆ South ┆ West │
# │ --- ┆ ---     ┆ ---     ┆ ---   ┆ ---  │
# │ i64 ┆ f64     ┆ f64     ┆ f64   ┆ f64  │
# ╞═════╪═════════╪═════════╪═══════╪══════╡
# │ 1   ┆ 30.950  ┆ null    ┆ null  ┆ null │
# │ 2   ┆ null    ┆ 219.400 ┆ null  ┆ null │
# │ 3   ┆ 207.350 ┆ null    ┆ null  ┆ null │
# │ 4   ┆ 197.720 ┆ null    ┆ null  ┆ null │
# │ 5   ┆ null    ┆ 23.540  ┆ null  ┆ null │
# └─────┴─────────┴─────────┴───────┴──────┘

# ## Restrict or order generated pivot columns with on_columns=
# '''
If you know the desired output columns, use on_columns=.
This is useful for stable column order and for lazy pivot examples later.
'''

df_pivoted_ordered = df_sales.pivot(
    on="region",
    on_columns=["North", "South", "East", "West"],
    index="ID",
    values="sales",
)

print(df_pivoted_ordered.head())
# shape: (5, 5)
# ┌─────┬─────────┬───────┬─────────┬──────┐
# │ ID  ┆ North   ┆ South ┆ East    ┆ West │
# │ --- ┆ ---     ┆ ---   ┆ ---     ┆ ---  │
# │ i64 ┆ f64     ┆ f64   ┆ f64     ┆ f64  │
# ╞═════╪═════════╪═══════╪═════════╪══════╡
# │ 1   ┆ null    ┆ null  ┆ 30.950  ┆ null │
# │ 2   ┆ 219.400 ┆ null  ┆ null    ┆ null │
# │ 3   ┆ null    ┆ null  ┆ 207.350 ┆ null │
# │ 4   ┆ null    ┆ null  ┆ 197.720 ┆ null │
# │ 5   ┆ 23.540  ┆ null  ┆ null    ┆ null │
# └─────┴─────────┴───────┴─────────┴──────┘

# ## Using multiple variables for on=
# '''
Pandas can create MultiIndex columns after pivoting with multiple columns=.
Polars does not create MultiIndex columns; it creates flat column names (cartesian product).

Pandas:
    columns=["region", "product"]

Polars:
    on=["region", "product"]
'''

df_pivoted_multi_on = df_sales.pivot(
    on=["region", "product"],
    index="ID",
    values="sales",
    separator="_",
    sort_columns=True,
)

print(df_pivoted_multi_on.head())
# shape: (5, 13)
# ┌─────┬─────────┬─────────┬─────────┬─────────┬─────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┐
# │ ID  ┆ {"East" ┆ {"East" ┆ {"East" ┆ {"North ┆ {"North ┆ {"Nort ┆ {"Sout ┆ {"Sout ┆ {"Sout ┆ {"West ┆ {"West ┆ {"West │
# │ --- ┆ ,"Doohi ┆ ,"Gadge ┆ ,"Widge ┆ ","Dooh ┆ ","Gadg ┆ h","Wi ┆ h","Do ┆ h","Ga ┆ h","Wi ┆ ","Doo ┆ ","Gad ┆ ","Wid │
# │ i64 ┆ ckey"}  ┆ t"}     ┆ t"}     ┆ ickey"} ┆ et"}    ┆ dget"} ┆ ohicke ┆ dget"} ┆ dget"} ┆ hickey ┆ get"}  ┆ get"}  │
# │     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---    ┆ y"}    ┆ ---    ┆ ---    ┆ "}     ┆ ---    ┆ ---    │
# │     ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64    ┆ ---    ┆ f64    ┆ f64    ┆ ---    ┆ f64    ┆ f64    │
# │     ┆         ┆         ┆         ┆         ┆         ┆        ┆ f64    ┆        ┆        ┆ f64    ┆        ┆        │
# ╞═════╪═════════╪═════════╪═════════╪═════════╪═════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╡
# │ 1   ┆ null    ┆ 30.950  ┆ null    ┆ null    ┆ null    ┆ null   ┆ null   ┆ null   ┆ null   ┆ null   ┆ null   ┆ null   │
# │ 2   ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    ┆ 219.40 ┆ null   ┆ null   ┆ null   ┆ null   ┆ null   ┆ null   │
# │     ┆         ┆         ┆         ┆         ┆         ┆ 0      ┆        ┆        ┆        ┆        ┆        ┆        │
# │ 3   ┆ 207.350 ┆ null    ┆ null    ┆ null    ┆ null    ┆ null   ┆ null   ┆ null   ┆ null   ┆ null   ┆ null   ┆ null   │
# │ 4   ┆ null    ┆ null    ┆ 197.720 ┆ null    ┆ null    ┆ null   ┆ null   ┆ null   ┆ null   ┆ null   ┆ null   ┆ null   │
# │ 5   ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    ┆ 23.540 ┆ null   ┆ null   ┆ null   ┆ null   ┆ null   ┆ null   │
# └─────┴─────────┴─────────┴─────────┴─────────┴─────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┘
# columns look like: ID, East_Doochickey, East_Gadget, East_Widget, ...

# ## Using multiple variables for values=
# '''
Pandas may create MultiIndex columns when values=[...].
Polars creates flat names using separator=.

Use column_naming="combine" if you always want value-name + pivot-column-name.
'''

df_pivoted_multi_values = df_sales.pivot(
    on="region",
    index="ID",
    values=["sales", "date"],
    separator="_",
    column_naming="combine",
    sort_columns=True,
)

print(df_pivoted_multi_values.head())
# shape: (5, 9)
# ┌─────┬────────────┬─────────────┬─────────────┬────────────┬────────────┬────────────┬────────────┬───────────┐
# │ ID  ┆ sales_East ┆ sales_North ┆ sales_South ┆ sales_West ┆ date_East  ┆ date_North ┆ date_South ┆ date_West │
# │ --- ┆ ---        ┆ ---         ┆ ---         ┆ ---        ┆ ---        ┆ ---        ┆ ---        ┆ ---       │
# │ i64 ┆ f64        ┆ f64         ┆ f64         ┆ f64        ┆ date       ┆ date       ┆ date       ┆ date      │
# ╞═════╪════════════╪═════════════╪═════════════╪════════════╪════════════╪════════════╪════════════╪═══════════╡
# │ 1   ┆ 30.950     ┆ null        ┆ null        ┆ null       ┆ 2024-01-07 ┆ null       ┆ null       ┆ null      │
# │ 2   ┆ null       ┆ 219.400     ┆ null        ┆ null       ┆ null       ┆ 2024-01-20 ┆ null       ┆ null      │
# │ 3   ┆ 207.350    ┆ null        ┆ null        ┆ null       ┆ 2024-01-29 ┆ null       ┆ null       ┆ null      │
# │ 4   ┆ 197.720    ┆ null        ┆ null        ┆ null       ┆ 2024-01-15 ┆ null       ┆ null       ┆ null      │
# │ 5   ┆ null       ┆ 23.540      ┆ null        ┆ null       ┆ null       ┆ 2024-01-11 ┆ null       ┆ null      │
# └─────┴────────────┴─────────────┴─────────────┴────────────┴────────────┴────────────┴────────────┴───────────┘

##-----------------------------------------------------##
##  df.pivot(..., aggregate_function=...): pivot table ##
##-----------------------------------------------------##
'''
Pandas:
    pd.pivot_table(..., aggfunc="mean")

Polars:
    df.pivot(..., aggregate_function="mean")

Polars supports these predefined aggregate function strings for DataFrame.pivot:
    "min", "max", "first", "last", "sum", "mean", "median", "len"

For more specialized aggregations, pre-aggregate with group_by().agg(...),
or use an expression with pl.element() when appropriate.
'''

df_duplicates = pl.DataFrame(
    {
        "ID": ["one", "one", "one", "two", "two", "one", "one", "two", "two"],
        "class": ["foo", "foo", "foo", "foo", "foo", "bar", "bar", "bar", "bar"],
        "size": ["small", "large", "large", "small", "small", "large", "small", "small", "large"],
        "scores": [1, 2, 2, 3, 3, 4, 5, 6, 7],
        "measurements": [2, 4, 5, 5, 6, 6, 8, 9, 9],
    }
)

print(df_duplicates)
# shape: (9, 5)
# ┌─────┬───────┬───────┬────────┬──────────────┐
# │ ID  ┆ class ┆ size  ┆ scores ┆ measurements │
# │ --- ┆ ---   ┆ ---   ┆ ---    ┆ ---          │
# │ str ┆ str   ┆ str   ┆ i64    ┆ i64          │
# ╞═════╪═══════╪═══════╪════════╪══════════════╡
# │ one ┆ foo   ┆ small ┆ 1      ┆ 2            │
# │ one ┆ foo   ┆ large ┆ 2      ┆ 4            │
# │ one ┆ foo   ┆ large ┆ 2      ┆ 5            │
# │ two ┆ foo   ┆ small ┆ 3      ┆ 5            │
# │ two ┆ foo   ┆ small ┆ 3      ┆ 6            │
# │ one ┆ bar   ┆ large ┆ 4      ┆ 6            │
# │ one ┆ bar   ┆ small ┆ 5      ┆ 8            │
# │ two ┆ bar   ┆ small ┆ 6      ┆ 9            │
# │ two ┆ bar   ┆ large ┆ 7      ┆ 9            │
# └─────┴───────┴───────┴────────┴──────────────┘

# ## Duplicate cells without aggregation raise an error
# 
try:
    df_duplicates.pivot(
        on="class",
        index="ID",
        values="scores",
    )
except Exception as err:
    print(type(err).__name__)
    # Example: ComputeError / DuplicateError depending on Polars version.

# ## Use aggregate_function= to handle duplicates
# 
df_pivoted_tbl = df_duplicates.pivot(
    on="class",
    index="ID",
    values="scores",
    aggregate_function="mean",
    sort_columns=True,
)

print(df_pivoted_tbl)
# shape: (2, 3)
# ┌─────┬───────┬───────┐
# │ ID  ┆ bar   ┆ foo   │
# │ --- ┆ ---   ┆ ---   │
# │ str ┆ f64   ┆ f64   │
# ╞═════╪═══════╪═══════╡
# │ one ┆ 4.500 ┆ 1.667 │
# │ two ┆ 6.500 ┆ 3.000 │
# └─────┴───────┴───────┘

# ## Multiple values with the same aggregation
# 
df_pivoted_tbl_multi_values = df_duplicates.pivot(
    on="size",
    index="ID",
    values=["scores", "measurements"],
    aggregate_function="mean",
    separator="_",
    sort_columns=True,
)

print(df_pivoted_tbl_multi_values)
# shape: (2, 5)
# ┌─────┬──────────────┬──────────────┬────────────────────┬────────────────────┐
# │ ID  ┆ scores_large ┆ scores_small ┆ measurements_large ┆ measurements_small │
# │ --- ┆ ---          ┆ ---          ┆ ---                ┆ ---                │
# │ str ┆ f64          ┆ f64          ┆ f64                ┆ f64                │
# ╞═════╪══════════════╪══════════════╪════════════════════╪════════════════════╡
# │ one ┆ 2.667        ┆ 3.000        ┆ 5.000              ┆ 5.000              │
# │ two ┆ 7.000        ┆ 4.000        ┆ 9.000              ┆ 6.667              │
# └─────┴──────────────┴──────────────┴────────────────────┴────────────────────┘

# ## Multiple aggregation functions: pre-aggregate, then pivot
# '''
Polars pivot accepts one aggregate_function at a time.
To reproduce pandas aggfunc=["mean", "sum"], first build those summaries with
GroupBy.agg(), then pivot the summary columns.
'''

df_measurement_summary = (
    df_duplicates
    .group_by(["ID", "size"])
    .agg(
        pl.col("measurements").mean().alias("measurements_mean"),
        pl.col("measurements").sum().alias("measurements_sum"),
    )
)
print(df_measurement_summary)
# shape: (4, 4)
# ┌─────┬───────┬───────────────────┬──────────────────┐
# │ ID  ┆ size  ┆ measurements_mean ┆ measurements_sum │
# │ --- ┆ ---   ┆ ---               ┆ ---              │
# │ str ┆ str   ┆ f64               ┆ i64              │
# ╞═════╪═══════╪═══════════════════╪══════════════════╡
# │ two ┆ large ┆ 9.000             ┆ 9                │
# │ one ┆ small ┆ 5.000             ┆ 10               │
# │ two ┆ small ┆ 6.667             ┆ 20               │
# │ one ┆ large ┆ 5.000             ┆ 15               │
# └─────┴───────┴───────────────────┴──────────────────┘

df_pivoted_tbl_multi_agg = df_measurement_summary.pivot(
    on="size",
    index="ID",
    values=["measurements_mean", "measurements_sum"],
    aggregate_function="first",
    separator="_",
    sort_columns=True,
)
print(df_pivoted_tbl_multi_agg)
# shape: (2, 5)
# ┌─────┬─────────────────────────┬─────────────────────────┬────────────────────────┬────────────────────────┐
# │ ID  ┆ measurements_mean_large ┆ measurements_mean_small ┆ measurements_sum_large ┆ measurements_sum_small │
# │ --- ┆ ---                     ┆ ---                     ┆ ---                    ┆ ---                    │
# │ str ┆ f64                     ┆ f64                     ┆ i64                    ┆ i64                    │
# ╞═════╪═════════════════════════╪═════════════════════════╪════════════════════════╪════════════════════════╡
# │ one ┆ 5.000                   ┆ 5.000                   ┆ 15                     ┆ 10                     │
# │ two ┆ 9.000                   ┆ 6.667                   ┆ 9                      ┆ 20                     │
# └─────┴─────────────────────────┴─────────────────────────┴────────────────────────┴────────────────────────┘

# ## Multiple grouping columns for the pivoted columns
# '''
Pandas:
    columns=["size", "class"]

Polars:
    on=["size", "class"]
'''

df_std_summary = (
    df_duplicates
    .group_by(["ID", "size", "class"])
    .agg(pl.col("scores").std().alias("scores_std"))
)

df_pivoted_tbl_multi_on = df_std_summary.pivot(
    on=["size", "class"],
    index="ID",
    values="scores_std",
    aggregate_function="first",
    separator="_",
    sort_columns=True,
)

print(df_pivoted_tbl_multi_on)
# shape: (2, 5)
# ┌─────┬─────────────────┬─────────────────┬─────────────────┬─────────────────┐
# │ ID  ┆ {"large","bar"} ┆ {"large","foo"} ┆ {"small","bar"} ┆ {"small","foo"} │
# │ --- ┆ ---             ┆ ---             ┆ ---             ┆ ---             │
# │ str ┆ f64             ┆ f64             ┆ f64             ┆ f64             │
# ╞═════╪═════════════════╪═════════════════╪═════════════════╪═════════════════╡
# │ one ┆ null            ┆ 0.000           ┆ null            ┆ null            │
# │ two ┆ null            ┆ null            ┆ null            ┆ 0.000           │
# └─────┴─────────────────┴─────────────────┴─────────────────┴─────────────────┘

# ## LazyFrame pivot
# '''
LazyFrame.pivot() needs on_columns= because Polars must know the output schema
before executing the lazy plan.
'''

lf_pivoted = (
    df_duplicates
    .lazy()
    .pivot(
        on="class",
        on_columns=["bar", "foo"],
        index="ID",
        values="scores",
        aggregate_function="mean",
    )
)

print(lf_pivoted.collect())
# shape: (2, 3)
# ┌─────┬───────┬───────┐
# │ ID  ┆ bar   ┆ foo   │
# │ --- ┆ ---   ┆ ---   │
# │ str ┆ f64   ┆ f64   │
# ╞═════╪═══════╪═══════╡
# │ one ┆ 4.500 ┆ 1.667 │
# │ two ┆ 6.500 ┆ 3.000 │
# └─────┴───────┴───────┘


# =========================================================================================
# 2. Unpivot: wide to long
# =========================================================================================

##--------------------------##
## Create example DataFrame ##
##--------------------------##

n_patients = 8
patient_ids = [f"P{i:03d}" for i in range(1, n_patients + 1)]

np.random.seed(42)
df_measurements = pl.DataFrame(
    {
        "patient_id": patient_ids,
        "age": np.random.randint(20, 80, size=n_patients),
        # Day-specific columns in wide format.
        "BP_day1": np.random.randint(110, 150, size=n_patients), # BP = Blood Pressure
        "HR_day1": np.random.randint(60, 100, size=n_patients),  # HR = Heart Rate
        "BP_day2": np.random.randint(110, 150, size=n_patients),
        "HR_day2": np.random.randint(60, 100, size=n_patients),
        "BP_day3": np.random.randint(110, 150, size=n_patients),
        "HR_day3": np.random.randint(60, 100, size=n_patients),
    }
)

print(df_measurements)
# shape: (8, 8)
# ┌────────────┬─────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
# │ patient_id ┆ age ┆ BP_day1 ┆ HR_day1 ┆ BP_day2 ┆ HR_day2 ┆ BP_day3 ┆ HR_day3 │
# │ ---        ┆ --- ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     │
# │ str        ┆ i64 ┆ i64     ┆ i64     ┆ i64     ┆ i64     ┆ i64     ┆ i64     │
# ╞════════════╪═════╪═════════╪═════════╪═════════╪═════════╪═════════╪═════════╡
# │ P001       ┆ 58  ┆ 128     ┆ 62      ┆ 142     ┆ 62      ┆ 134     ┆ 67      │
# │ P002       ┆ 71  ┆ 132     ┆ 81      ┆ 121     ┆ 96      ┆ 123     ┆ 94      │
# │ P003       ┆ 48  ┆ 120     ┆ 61      ┆ 131     ┆ 66      ┆ 118     ┆ 73      │
# │ P004       ┆ 34  ┆ 120     ┆ 83      ┆ 134     ┆ 80      ┆ 135     ┆ 76      │
# │ P005       ┆ 62  ┆ 133     ┆ 89      ┆ 136     ┆ 68      ┆ 111     ┆ 95      │
# │ P006       ┆ 27  ┆ 145     ┆ 97      ┆ 137     ┆ 98      ┆ 129     ┆ 99      │
# │ P007       ┆ 40  ┆ 149     ┆ 61      ┆ 125     ┆ 77      ┆ 137     ┆ 63      │
# │ P008       ┆ 58  ┆ 133     ┆ 80      ┆ 124     ┆ 63      ┆ 116     ┆ 61      │
# └────────────┴─────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘

##-----------------------------##
##  df.unpivot(): wide -> long ##
##-----------------------------##
'''
Pandas:
    pd.melt(frame=df, id_vars=[...], value_vars=[...])

Polars:
    df.unpivot(index=[...], on=[...])

Parameter mapping:
    pandas id_vars    -> Polars index
    pandas value_vars -> Polars on
    pandas var_name   -> Polars variable_name
    pandas value_name -> Polars value_name
'''

value_cols = [col for col in df_measurements.columns if col.startswith(("BP_", "HR_"))]

df_unpivoted = df_measurements.unpivot(
    on=value_cols,
    index=["patient_id", "age"],
    variable_name="measurement_day",
    value_name="measured_value",
)

print(df_unpivoted.head())
# shape: (5, 4)
# ┌────────────┬─────┬─────────────────┬────────────────┐
# │ patient_id ┆ age ┆ measurement_day ┆ measured_value │
# │ ---        ┆ --- ┆ ---             ┆ ---            │
# │ str        ┆ i64 ┆ str             ┆ i64            │
# ╞════════════╪═════╪═════════════════╪════════════════╡
# │ P001       ┆ 58  ┆ BP_day1         ┆ 128            │
# │ P002       ┆ 71  ┆ BP_day1         ┆ 132            │
# │ P003       ┆ 48  ┆ BP_day1         ┆ 120            │
# │ P004       ┆ 34  ┆ BP_day1         ┆ 120            │
# │ P005       ┆ 62  ┆ BP_day1         ┆ 133            │
# └────────────┴─────┴─────────────────┴────────────────┘

# ## Selector-based unpivot
# '''
Selectors are very useful in Polars.
Here, cs.matches(...) selects all columns whose names look like BP_day1, HR_day2, etc.
'''

df_unpivoted_selector = df_measurements.unpivot(
    on=cs.matches(r"^(BP|HR)_day\d+$"),
    index=["patient_id", "age"],
    variable_name="measurement_day",
    value_name="measured_value",
)

print(df_unpivoted_selector.head())
# shape: (5, 4)
# ┌────────────┬─────┬─────────────────┬────────────────┐
# │ patient_id ┆ age ┆ measurement_day ┆ measured_value │
# │ ---        ┆ --- ┆ ---             ┆ ---            │
# │ str        ┆ i64 ┆ str             ┆ i64            │
# ╞════════════╪═════╪═════════════════╪════════════════╡
# │ P001       ┆ 58  ┆ BP_day1         ┆ 128            │
# │ P002       ┆ 71  ┆ BP_day1         ┆ 132            │
# │ P003       ┆ 48  ┆ BP_day1         ┆ 120            │
# │ P004       ┆ 34  ┆ BP_day1         ┆ 120            │
# │ P005       ┆ 62  ┆ BP_day1         ┆ 133            │
# └────────────┴─────┴─────────────────┴────────────────┘

# ## Legacy df.melt() note
# '''
Polars still has df.melt(id_vars=..., value_vars=...), but it is deprecated.
Use df.unpivot(index=..., on=...) for new code.

Legacy equivalent, not recommended for new code:

    df_measurements.melt(
        id_vars=["patient_id", "age"],
        value_vars=value_cols,
        variable_name="measurement_day",
        value_name="measured_value",
    )
'''

##-----------------------------------##
##  pandas wide_to_long() equivalent ##
##-----------------------------------##
'''
pandas wide_to_long() can split columns like BP_day1, HR_day1, BP_day2, HR_day2
into separate metric and day columns.

Polars does this explicitly:
1. unpivot wide columns into rows
2. split the original column name into metric and day label
3. extract the day number
4. pivot metric back into separate BP and HR columns
'''

df_wtl_long = (
    df_measurements
    .unpivot(
        on=cs.matches(r"^(BP|HR)_day\d+$"),
        index=["patient_id", "age"],
        variable_name="measurement_day",
        value_name="measured_value",
    )
    .with_columns(
        pl.col("measurement_day").str.split_exact("_", 1).alias("parts")
    )
    .unnest("parts")
    .rename({"field_0": "metric", "field_1": "day_label"})
    .with_columns(
        pl.col("day_label").str.extract(r"(\d+)$", 1).cast(pl.Int64).alias("day")
    )
    .drop(["measurement_day", "day_label"])
)

print(df_wtl_long.head())
# shape: (5, 5)
# ┌────────────┬─────┬────────────────┬────────┬─────┐
# │ patient_id ┆ age ┆ measured_value ┆ metric ┆ day │
# │ ---        ┆ --- ┆ ---            ┆ ---    ┆ --- │
# │ str        ┆ i64 ┆ i64            ┆ str    ┆ i64 │
# ╞════════════╪═════╪════════════════╪════════╪═════╡
# │ P001       ┆ 58  ┆ 128            ┆ BP     ┆ 1   │
# │ P002       ┆ 71  ┆ 132            ┆ BP     ┆ 1   │
# │ P003       ┆ 48  ┆ 120            ┆ BP     ┆ 1   │
# │ P004       ┆ 34  ┆ 120            ┆ BP     ┆ 1   │
# │ P005       ┆ 62  ┆ 133            ┆ BP     ┆ 1   │
# └────────────┴─────┴────────────────┴────────┴─────┘

# Pivot metric back to BP and HR columns.
df_wtl = (
    df_wtl_long
    .pivot(
        on="metric",
        index=["patient_id", "age", "day"],
        values="measured_value",
        aggregate_function="first",
        sort_columns=True,
    )
    .sort(["patient_id", "day"])
)

print(df_wtl.head(10))
# shape: (10, 5)
# ┌────────────┬─────┬─────┬─────┬─────┐
# │ patient_id ┆ age ┆ day ┆ BP  ┆ HR  │
# │ ---        ┆ --- ┆ --- ┆ --- ┆ --- │
# │ str        ┆ i64 ┆ i64 ┆ i64 ┆ i64 │
# ╞════════════╪═════╪═════╪═════╪═════╡
# │ P001       ┆ 58  ┆ 1   ┆ 128 ┆ 62  │
# │ P001       ┆ 58  ┆ 2   ┆ 142 ┆ 62  │
# │ P001       ┆ 58  ┆ 3   ┆ 134 ┆ 67  │
# │ P002       ┆ 71  ┆ 1   ┆ 132 ┆ 81  │
# │ P002       ┆ 71  ┆ 2   ┆ 121 ┆ 96  │
# │ P002       ┆ 71  ┆ 3   ┆ 123 ┆ 94  │
# │ P003       ┆ 48  ┆ 1   ┆ 120 ┆ 61  │
# │ P003       ┆ 48  ┆ 2   ┆ 131 ┆ 66  │
# │ P003       ┆ 48  ┆ 3   ┆ 118 ┆ 73  │
# │ P004       ┆ 34  ┆ 1   ┆ 120 ┆ 83  │
# └────────────┴─────┴─────┴─────┴─────┘

# ## LazyFrame unpivot
# 
lf_unpivoted = (
    df_measurements
    .lazy()
    .unpivot(
        on=cs.matches(r"^(BP|HR)_day\d+$"),
        index=["patient_id", "age"],
        variable_name="measurement_day",
        value_name="measured_value",
    )
)

print(lf_unpivoted.collect().head())
# shape: (5, 4)
# ┌────────────┬─────┬─────────────────┬────────────────┐
# │ patient_id ┆ age ┆ measurement_day ┆ measured_value │
# │ ---        ┆ --- ┆ ---             ┆ ---            │
# │ str        ┆ i64 ┆ str             ┆ i64            │
# ╞════════════╪═════╪═════════════════╪════════════════╡
# │ P001       ┆ 58  ┆ BP_day1         ┆ 128            │
# │ P002       ┆ 71  ┆ BP_day1         ┆ 132            │
# │ P003       ┆ 48  ┆ BP_day1         ┆ 120            │
# │ P004       ┆ 34  ┆ BP_day1         ┆ 120            │
# │ P005       ┆ 62  ┆ BP_day1         ┆ 133            │
# └────────────┴─────┴─────────────────┴────────────────┘


# =========================================================================================
# 3. Cross-Table
# =========================================================================================
'''
A cross-tabulation, or contingency table, displays the frequency distribution
of categorical variables.

Pandas:
    pd.crosstab(index=df["gender"], columns=df["favorite_color"])

Polars:
    df.group_by(["gender", "favorite_color"]).agg(pl.len())
      .pivot(on="favorite_color", index="gender", values="count")
      .fill_null(0)
'''

##--------------------------##
## Create example DataFrame ##
##--------------------------##

n_resp = 250

np.random.seed(42)
df_survey = pl.DataFrame(
    {
        "respondent_id": range(1, n_resp + 1),
        "gender": np.random.choice(
            ["Male", "Female", "Other"],
            size=n_resp,
            p=[0.48, 0.48, 0.04],
        ),
        "favorite_color": np.random.choice(
            ["Red", "Blue", "Green", "Yellow", "Purple"],
            size=n_resp,
        ),
        "purchase_intent": np.random.choice(
            ["Definitely", "Probably", "Maybe", "Unlikely", "Never"],
            size=n_resp,
            p=[0.15, 0.25, 0.30, 0.20, 0.10],
        ),
    }
)

print(df_survey.head())
# shape: (5, 4)
# ┌───────────────┬────────┬────────────────┬─────────────────┐
# │ respondent_id ┆ gender ┆ favorite_color ┆ purchase_intent │
# │ ---           ┆ ---    ┆ ---            ┆ ---             │
# │ i64           ┆ str    ┆ str            ┆ str             │
# ╞═══════════════╪════════╪════════════════╪═════════════════╡
# │ 1             ┆ Male   ┆ Purple         ┆ Probably        │
# │ 2             ┆ Female ┆ Purple         ┆ Unlikely        │
# │ 3             ┆ Female ┆ Red            ┆ Never           │
# │ 4             ┆ Female ┆ Green          ┆ Never           │
# │ 5             ┆ Male   ┆ Blue           ┆ Unlikely        │
# └───────────────┴────────┴────────────────┴─────────────────┘

##-----------------------------------##
## Helper: Polars crosstab as counts ##
##-----------------------------------##

def crosstab_counts(df, row, col, col_order=None):
    '''Create a pandas.crosstab-like count table in Polars.'''

    counts = (
        df
        .group_by([row, col])
        .agg(pl.len().alias("count"))
    )

    table = (
        counts
        .pivot(
            on=col,
            on_columns=col_order,
            index=row,
            values="count",
            aggregate_function="first",
            sort_columns=col_order is None,
        )
        .fill_null(0)
        .sort(row)
    )

    value_cols = [name for name in table.columns if name != row]
    return table.with_columns([pl.col(name).cast(pl.Int64) for name in value_cols])


def add_margins(table, row, total_name="All"):
    '''Add row and column totals, similar to pandas crosstab(margins=True).'''

    value_cols = [name for name in table.columns if name != row]

    body = table.with_columns(
        pl.sum_horizontal(*[pl.col(name) for name in value_cols]).alias(total_name)
    )

    totals = body.select(
        pl.lit(total_name).alias(row),
        *[pl.col(name).sum().alias(name) for name in body.columns if name != row],
    )

    return body.vstack(totals)


def normalize_rows(table, row, digits=3):
    '''Normalize counts within each row, like pandas crosstab(normalize="index").'''

    value_cols = [name for name in table.columns if name != row]
    row_total = pl.sum_horizontal(*[pl.col(name) for name in value_cols])

    return table.with_columns(
        [(pl.col(name) / row_total).round(digits).alias(name) for name in value_cols]
    )


def normalize_columns(table, row, digits=3):
    '''Normalize counts within each column, like pandas crosstab(normalize="columns").'''

    value_cols = [name for name in table.columns if name != row]

    return table.with_columns(
        [(pl.col(name) / pl.col(name).sum()).round(digits).alias(name) for name in value_cols]
    )


def normalize_all(table, row, digits=3):
    '''Normalize counts by the grand total, like pandas crosstab(normalize="all").'''

    value_cols = [name for name in table.columns if name != row]
    grand_total = table.select(
        pl.sum_horizontal(*[pl.col(name) for name in value_cols]).sum().alias("total")
    ).item()

    return table.with_columns(
        [(pl.col(name) / grand_total).round(digits).alias(name) for name in value_cols]
    )

##-----------------------------##
## Basic cross-table of counts ##
##-----------------------------##

color_order = ["Blue", "Green", "Purple", "Red", "Yellow"]

contingency_table = crosstab_counts(
    df=df_survey,
    row="gender",
    col="favorite_color",
    col_order=color_order,
)

print(contingency_table)
# shape: (3, 6)
# ┌────────┬──────┬───────┬────────┬─────┬────────┐
# │ gender ┆ Blue ┆ Green ┆ Purple ┆ Red ┆ Yellow │
# │ ---    ┆ ---  ┆ ---   ┆ ---    ┆ --- ┆ ---    │
# │ str    ┆ i64  ┆ i64   ┆ i64    ┆ i64 ┆ i64    │
# ╞════════╪══════╪═══════╪════════╪═════╪════════╡
# │ Female ┆ 24   ┆ 19    ┆ 31     ┆ 21  ┆ 26     │
# │ Male   ┆ 35   ┆ 15    ┆ 25     ┆ 23  ┆ 21     │
# │ Other  ┆ 1    ┆ 4     ┆ 2      ┆ 3   ┆ 0      │
# └────────┴──────┴───────┴────────┴─────┴────────┘

# ## With margins=True equivalent
# 
contingency_with_margins = add_margins(
    table=contingency_table,
    row="gender",
    total_name="All",
)

print(contingency_with_margins)
# shape: (4, 7)
# ┌────────┬──────┬───────┬────────┬─────┬────────┬─────┐
# │ gender ┆ Blue ┆ Green ┆ Purple ┆ Red ┆ Yellow ┆ All │
# │ ---    ┆ ---  ┆ ---   ┆ ---    ┆ --- ┆ ---    ┆ --- │
# │ str    ┆ i64  ┆ i64   ┆ i64    ┆ i64 ┆ i64    ┆ i64 │
# ╞════════╪══════╪═══════╪════════╪═════╪════════╪═════╡
# │ Female ┆ 24   ┆ 19    ┆ 31     ┆ 21  ┆ 26     ┆ 121 │
# │ Male   ┆ 35   ┆ 15    ┆ 25     ┆ 23  ┆ 21     ┆ 119 │
# │ Other  ┆ 1    ┆ 4     ┆ 2      ┆ 3   ┆ 0      ┆ 10  │
# │ All    ┆ 60   ┆ 38    ┆ 58     ┆ 47  ┆ 47     ┆ 250 │
# └────────┴──────┴───────┴────────┴─────┴────────┴─────┘

# ## normalize='index' equivalent: row percentages
# 
intent_order = ["Definitely", "Maybe", "Never", "Probably", "Unlikely"]

intent_counts = crosstab_counts(
    df=df_survey,
    row="gender",
    col="purchase_intent",
    col_order=intent_order,
)

row_percentages = normalize_rows(intent_counts, row="gender")

print(row_percentages)
# shape: (3, 6)
# ┌────────┬────────────┬───────┬───────┬──────────┬──────────┐
# │ gender ┆ Definitely ┆ Maybe ┆ Never ┆ Probably ┆ Unlikely │
# │ ---    ┆ ---        ┆ ---   ┆ ---   ┆ ---      ┆ ---      │
# │ str    ┆ f64        ┆ f64   ┆ f64   ┆ f64      ┆ f64      │
# ╞════════╪════════════╪═══════╪═══════╪══════════╪══════════╡
# │ Female ┆ 0.190      ┆ 0.289 ┆ 0.132 ┆ 0.240    ┆ 0.149    │
# │ Male   ┆ 0.134      ┆ 0.319 ┆ 0.109 ┆ 0.252    ┆ 0.185    │
# │ Other  ┆ 0.100      ┆ 0.300 ┆ 0.100 ┆ 0.500    ┆ 0.000    │
# └────────┴────────────┴───────┴───────┴──────────┴──────────┘
# Each row sums to approximately 1.0.

# ## normalize='columns' equivalent: column percentages
# 
column_percentages = normalize_columns(intent_counts, row="gender")

print(column_percentages)
# shape: (3, 6)
# ┌────────┬────────────┬───────┬───────┬──────────┬──────────┐
# │ gender ┆ Definitely ┆ Maybe ┆ Never ┆ Probably ┆ Unlikely │
# │ ---    ┆ ---        ┆ ---   ┆ ---   ┆ ---      ┆ ---      │
# │ str    ┆ f64        ┆ f64   ┆ f64   ┆ f64      ┆ f64      │
# ╞════════╪════════════╪═══════╪═══════╪══════════╪══════════╡
# │ Female ┆ 0.575      ┆ 0.461 ┆ 0.533 ┆ 0.453    ┆ 0.450    │
# │ Male   ┆ 0.400      ┆ 0.500 ┆ 0.433 ┆ 0.469    ┆ 0.550    │
# │ Other  ┆ 0.025      ┆ 0.039 ┆ 0.033 ┆ 0.078    ┆ 0.000    │
# └────────┴────────────┴───────┴───────┴──────────┴──────────┘
# Each purchase_intent column sums to approximately 1.0.

# ## normalize='all' equivalent: share of all observations
# 
all_percentages = normalize_all(intent_counts, row="gender")

print(all_percentages)
# shape: (3, 6)
# ┌────────┬────────────┬───────┬───────┬──────────┬──────────┐
# │ gender ┆ Definitely ┆ Maybe ┆ Never ┆ Probably ┆ Unlikely │
# │ ---    ┆ ---        ┆ ---   ┆ ---   ┆ ---      ┆ ---      │
# │ str    ┆ f64        ┆ f64   ┆ f64   ┆ f64      ┆ f64      │
# ╞════════╪════════════╪═══════╪═══════╪══════════╪══════════╡
# │ Female ┆ 0.092      ┆ 0.140 ┆ 0.064 ┆ 0.116    ┆ 0.072    │
# │ Male   ┆ 0.064      ┆ 0.152 ┆ 0.052 ┆ 0.120    ┆ 0.088    │
# │ Other  ┆ 0.004      ┆ 0.012 ┆ 0.004 ┆ 0.020    ┆ 0.000    │
# └────────┴────────────┴───────┴───────┴──────────┴──────────┘
# The entire numeric part sums to approximately 1.0.

# ## Multiple columns= equivalent
# '''
Pandas crosstab can use multiple columns= and create MultiIndex columns.
Polars does not create MultiIndex columns. A simple Polars approach is to
combine the categorical columns into a single flat key, then crosstab that key.
'''

df_survey_combo = df_survey.with_columns(
    pl.concat_str(["favorite_color", "purchase_intent"], separator="_").alias("color_intent")
)

combo_order = [
    f"{color}_{intent}"
    for color in color_order
    for intent in intent_order
]

contingency_multi_columns = crosstab_counts(
    df=df_survey_combo,
    row="gender",
    col="color_intent",
    col_order=combo_order,
)

print(contingency_multi_columns)
# columns look like:
# gender, Blue_Definitely, Blue_Maybe, ..., Yellow_Probably, Yellow_Unlikely

# ## Long-form frequency table: often better than a very wide crosstab
# '''
For statistical modeling and plotting, long-form counts are often more useful
than a very wide crosstab.
'''

freq_long = (
    df_survey
    .group_by(["gender", "favorite_color", "purchase_intent"])
    .agg(pl.len().alias("count"))
    .sort(["gender", "favorite_color", "purchase_intent"])
)

print(freq_long.head(10))
# shape: (10, 4)
# ┌────────┬────────────────┬─────────────────┬───────┐
# │ gender ┆ favorite_color ┆ purchase_intent ┆ count │
# │ ---    ┆ ---            ┆ ---             ┆ ---   │
# │ str    ┆ str            ┆ str             ┆ u32   │
# ╞════════╪════════════════╪═════════════════╪═══════╡
# │ Female ┆ Blue           ┆ Definitely      ┆ 7     │
# │ Female ┆ Blue           ┆ Maybe           ┆ 7     │
# │ Female ┆ Blue           ┆ Never           ┆ 1     │
# │ Female ┆ Blue           ┆ Probably        ┆ 4     │
# │ Female ┆ Blue           ┆ Unlikely        ┆ 5     │
# │ Female ┆ Green          ┆ Definitely      ┆ 2     │
# │ Female ┆ Green          ┆ Maybe           ┆ 7     │
# │ Female ┆ Green          ┆ Never           ┆ 4     │
# │ Female ┆ Green          ┆ Probably        ┆ 4     │
# │ Female ┆ Green          ┆ Unlikely        ┆ 2     │
# └────────┴────────────────┴─────────────────┴───────┘

# ## Lazy cross-table
# '''
For lazy crosstabs, build the counts lazily, then use LazyFrame.pivot().
As with any lazy pivot, you must provide on_columns=.
'''

lazy_crosstab = (
    df_survey
    .lazy()
    .group_by(["gender", "purchase_intent"])
    .agg(pl.len().alias("count"))
    .pivot(
        on="purchase_intent",
        on_columns=intent_order,
        index="gender",
        values="count",
        aggregate_function="first",
    )
    .fill_null(0)
    .sort("gender")
)

print(lazy_crosstab.collect())
# shape: (3, 6)
# ┌────────┬────────────┬───────┬───────┬──────────┬──────────┐
# │ gender ┆ Definitely ┆ Maybe ┆ Never ┆ Probably ┆ Unlikely │
# │ ---    ┆ ---        ┆ ---   ┆ ---   ┆ ---      ┆ ---      │
# │ str    ┆ u32        ┆ u32   ┆ u32   ┆ u32      ┆ u32      │
# ╞════════╪════════════╪═══════╪═══════╪══════════╪══════════╡
# │ Female ┆ 23         ┆ 35    ┆ 16    ┆ 29       ┆ 18       │
# │ Male   ┆ 16         ┆ 38    ┆ 13    ┆ 30       ┆ 22       │
# │ Other  ┆ 1          ┆ 3     ┆ 1     ┆ 5        ┆ 0        │
# └────────┴────────────┴───────┴───────┴──────────┴──────────┘


# =========================================================================================
# 4. Quick pandas -> Polars map
# =========================================================================================
'''
Pandas idea                                      Polars equivalent
--------------------------------------------------------------------------------------
pd.pivot(..., columns="x")                    df.pivot(on="x", ...)
df.pivot(index="id", columns="x")            df.pivot(index="id", on="x")
pd.pivot_table(..., aggfunc="mean")           df.pivot(..., aggregate_function="mean")
pd.pivot_table(..., aggfunc=["mean", "sum"])  group_by().agg(...).pivot(...)
MultiIndex columns after pivot                  flat column names with separator="_"
pd.melt(id_vars=..., value_vars=...)            df.unpivot(index=..., on=...)
df.melt(...)                                    df.unpivot(...); melt is deprecated
pd.wide_to_long(...)                            unpivot -> split names -> pivot
pd.crosstab(row, col)                           group_by([row, col]).agg(pl.len()).pivot(...)
pd.crosstab(..., margins=True)                  add totals manually with expressions
pd.crosstab(..., normalize="index")             divide columns by row totals
pd.crosstab(..., normalize="columns")           divide columns by column totals
pd.crosstab(..., normalize="all")               divide columns by grand total
'''
