'''
1. Pivot: long to wide
   + df.pivot(on=..., index=..., values=...)
   + df.pivot(..., aggregate_function=...)  # pandas pivot_table equivalent
   + lf.pivot(..., on_columns=...)          # lazy pivot; output columns must be known

2. Unpivot: wide to long
   + df.unpivot(on=..., index=...)
   + lf.unpivot(on=..., index=...)
   + pandas wide_to_long equivalent: unpivot -> parse variable names -> pivot back
'''

import datetime as dt

import numpy as np
import polars as pl
import polars.selectors as cs
from polars import col as c

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

### Basic usage ###
print(
    df_sales
    .pivot(
        on="region",      # Values in this column become new column names.
        index="ID",       # This remains a normal column in Polars.
        values="sales",   # Values used to fill the new wide columns.
        sort_columns=True # Sort the generated region columns alphabetically.
    )
    .head()
)
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

### Restrict or order generated pivot columns with on_columns= ###
'''
If you know the desired output columns, use on_columns=.
This is useful for stable column order and for lazy pivot examples later.
'''
print(
    df_sales
    .pivot(
        on="region",
        on_columns=["North", "South", "East", "West"],
        index="ID",
        values="sales",
    )
    .head()
)
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

### Using multiple variables for `on=` ###
'''
Pandas can create MultiIndex columns after pivoting with multiple columns=.
Polars does not create MultiIndex columns; it creates flat column names (cartesian product).

Pandas:
    columns=["region", "product"]

Polars:
    on=["region", "product"]
'''
print(
    df_sales
    .pivot(
        on=["region", "product"],
        index="ID",
        values="sales",
        separator="_",
        sort_columns=True,
    )
    .head()
)
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

### Using multiple variables for `values=` ###
'''
Pandas may create MultiIndex columns when values=[...].
Polars creates flat names using separator=.

Use column_naming="combine" if you always want value-name + pivot-column-name.
'''

print(
    df_sales
    .pivot(
        on="region",
        index="ID",
        values=["sales", "date"],
        separator="_",
        column_naming="combine",
        sort_columns=True,
    )
    .head()
)
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

### Duplicate cells without aggregation raise an error ###
try:
    df_duplicates.pivot(
        on="class",
        index="ID",
        values="scores",
    )
except Exception as err:
    print(type(err).__name__)
    # Example: ComputeError / DuplicateError depending on Polars version.

### Use aggregate_function= to handle duplicates ###
print(
    df_duplicates
    .pivot(
        on="class",
        index="ID",
        values="scores",
        aggregate_function="mean",
        sort_columns=True,
    )
    .head()
)
# shape: (2, 3)
# ┌─────┬───────┬───────┐
# │ ID  ┆ bar   ┆ foo   │
# │ --- ┆ ---   ┆ ---   │
# │ str ┆ f64   ┆ f64   │
# ╞═════╪═══════╪═══════╡
# │ one ┆ 4.500 ┆ 1.667 │
# │ two ┆ 6.500 ┆ 3.000 │
# └─────┴───────┴───────┘

### Multiple values with the same aggregation ###
print(
    df_duplicates
    .pivot(
        on="size",
        index="ID",
        values=["scores", "measurements"],
        aggregate_function="mean",
        separator="_",
        sort_columns=True,
    )
)
# shape: (2, 5)
# ┌─────┬──────────────┬──────────────┬────────────────────┬────────────────────┐
# │ ID  ┆ scores_large ┆ scores_small ┆ measurements_large ┆ measurements_small │
# │ --- ┆ ---          ┆ ---          ┆ ---                ┆ ---                │
# │ str ┆ f64          ┆ f64          ┆ f64                ┆ f64                │
# ╞═════╪══════════════╪══════════════╪════════════════════╪════════════════════╡
# │ one ┆ 2.667        ┆ 3.000        ┆ 5.000              ┆ 5.000              │
# │ two ┆ 7.000        ┆ 4.000        ┆ 9.000              ┆ 6.667              │
# └─────┴──────────────┴──────────────┴────────────────────┴────────────────────┘

### Multiple aggregation functions: pre-aggregate, then pivot ###
'''
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

### Multiple grouping columns for the pivoted columns ###
'''
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

### LazyFrame pivot ###
'''
LazyFrame.pivot() needs on_columns= because Polars must know the output schema
before executing the lazy plan.
'''

print(
    df_duplicates
    .lazy() # convert to lazy
    .pivot(
        on="class",
        on_columns=["bar", "foo"],
        index="ID",
        values="scores",
        aggregate_function="mean",
    )
    .collect()
)
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

### Selector-based unpivot ###
'''
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

### LazyFrame unpivot ###
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
