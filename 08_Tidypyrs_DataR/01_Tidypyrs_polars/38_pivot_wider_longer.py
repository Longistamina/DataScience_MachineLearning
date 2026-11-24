'''
1. pivot_wider(): long to wide
   + tl.pivot_wider(names_from=..., id_cols=..., values_from=...)
   + values_fn= selects how duplicate cells are aggregated (default: "first").
   + names_list= supplies output categories; omitting it runs category discovery.
   + values_fill= fills missing pivot cells.

2. pivot_longer(): wide to long
   + tl.pivot_longer(cols=..., names_to=..., values_to=...)
   + Columns not selected by cols remain identifier columns.
   + pandas wide_to_long equivalent: pivot_longer -> parse names -> pivot_wider.

All examples use TibbleLazy and collect only for display, except that
pivot_wider may execute category discovery when names_list is omitted.
Output tables illustrate values; row order is unspecified unless sorted.
'''

import datetime as dt

import numpy as np
import tidypyrs as tp
import tidypyrs.selectors as cs
from tidypyrs import f

# Optional display settings for tutorial output.
tp.Config.set_tbl_rows(12)
tp.Config.set_tbl_cols(16)
tp.Config.set_float_precision(3)
tp.Config.set_tbl_width_chars(120)

# =========================================================================================
# 1. Pivot: long to wide
# =========================================================================================

##--------------------------------------##
## tl.pivot_wider(): basic long -> wide ##
##--------------------------------------##
'''
The .pivot_wider() method converts unique values from one column into multiple columns.

Pandas:
    pd.pivot(data=df, index="ID", columns="region", values="sales")

Tidypyrs:
    tl.pivot_wider(names_from="region", id_cols="ID", values_from="sales")

NOTE:
+ pandas columns= maps to names_from=; pandas values= maps to values_from=.
+ id_cols= remains ordinary columns; tidypyrs has no custom row index.
+ values_fn defaults to "first", so duplicate cells select their first value.
+ Use values_fn=None to reject duplicate cells instead of aggregating them.
+ Supply names_list for predictable category order without category discovery.
'''

dates = [dt.date(2024, 1, 1) + dt.timedelta(days=i) for i in range(30)]
regions = ["North", "South", "East", "West"]
products = ["Widget", "Gadget", "Doohickey"]

np.random.seed(42)
selected_dates = [dates[i] for i in np.random.randint(0, len(dates), size=200)]

tl_sales = tp.TibbleLazy(
    {
        "ID": range(1, 201),
        "date": selected_dates,
        "region": np.random.choice(regions, size=200),
        "product": np.random.choice(products, size=200),
        "quantity": np.random.randint(1, 20, size=200),
        "unit_price": np.round(np.random.uniform(5, 50, size=200), 2),
    }
).mutate(
    (f("quantity") * f("unit_price")).round(2).alias("sales")
)

print(tl_sales.head().collect())
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
    tl_sales
    .pivot_wider(
        names_from="region",      # Values in this column become new column names.
        names_list=["East", "North", "South", "West"],
        id_cols="ID",       # This remains an ordinary identifier column.
        values_from="sales",   # Values used to fill the new wide columns.
    )
    .head()
    .collect()
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

### Restrict or order generated pivot columns with names_list= ###
'''
If you know the desired output columns, use names_list=.
This is useful for stable column order and for lazy pivot examples later.
'''
print(
    tl_sales
    .pivot_wider(
        names_from="region",
        names_list=["North", "South", "East", "West"],
        id_cols="ID",
        values_from="sales",
    )
    .head()
    .collect()
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

### Automatically infer output columns ###
'''
When names_list is omitted, pivot_wider() discovers the unique values
in names_from by executing a query immediately. The returned result
is still a TibbleLazy; collecting it executes the pivot query.

The order of inferred columns is unspecified. Supply names_list when
you need a specific order or want to avoid category discovery.
'''

print(
    tl_sales
    .pivot_wider(
        names_from="region",
        id_cols="ID",
        values_from="sales",
    )
    .arrange("ID")
    .head()
    .collect()
)
# shape: (5, 5)
# ┌─────┬──────┬─────────┬─────────┬───────┐
# │ ID  ┆ West ┆ East    ┆ North   ┆ South │
# │ --- ┆ ---  ┆ ---     ┆ ---     ┆ ---   │
# │ i64 ┆ f64  ┆ f64     ┆ f64     ┆ f64   │
# ╞═════╪══════╪═════════╪═════════╪═══════╡
# │ 1   ┆ null ┆ 30.950  ┆ null    ┆ null  │
# │ 2   ┆ null ┆ null    ┆ 219.400 ┆ null  │
# │ 3   ┆ null ┆ 207.350 ┆ null    ┆ null  │
# │ 4   ┆ null ┆ 197.720 ┆ null    ┆ null  │
# │ 5   ┆ null ┆ null    ┆ 23.540  ┆ null  │
# └─────┴──────┴─────────┴─────────┴───────┘

### Using multiple variables for `names_from=` ###
'''
Pandas can create MultiIndex columns with columns=["region", "product"].
Here we explicitly combine region and product into a single names_from column.
The resulting names are flat labels such as East_Gadget.
Values containing "_" can produce ambiguous labels; choose another separator
when the data requires it.
'''
print(
    tl_sales
    .mutate((f("region") + tp.lit("_") + f("product")).alias("region_product"))
    .pivot_wider(
        names_from="region_product",
        id_cols="ID",
        values_from="sales",
    )
    .head()
    .collect()
)
# Output contains ID and combined category columns such as East_Gadget.
# Column order depends on discovered categories unless names_list is supplied.

### Using multiple variables for `values_from=` ###
'''
Pandas may create MultiIndex columns when values_from=[...].
Tidypyrs delegates multi-value naming to Polars and returns flat names such as
sales_East and date_East. This wrapper does not expose separator or column_naming.
'''

print(
    tl_sales
    .pivot_wider(
        names_from="region",
        names_list=["East", "North", "South", "West"],
        id_cols="ID",
        values_from=["sales", "date"],
    )
    .head()
    .collect()
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

##--------------------------------------------------##
##  tl.pivot_wider(..., values_fn=...): pivot table ##
##--------------------------------------------------##
'''
Pandas:
    pd.pivot_table(..., aggfunc="mean")

Tidypyrs:
    df.pivot_wider(..., values_fn="mean")

Common values_fn strings supported by the underlying pivot include:
    "min", "max", "first", "last", "sum", "mean", "median", "len"

For more specialized aggregations, pre-aggregate with group_by().agg(...),
or use an expression with tp.element() when appropriate.
'''

tl_duplicates = tp.TibbleLazy(
    {
        "ID": ["one", "one", "one", "two", "two", "one", "one", "two", "two"],
        "class": ["foo", "foo", "foo", "foo", "foo", "bar", "bar", "bar", "bar"],
        "size": ["small", "large", "large", "small", "small", "large", "small", "small", "large"],
        "scores": [1, 2, 2, 3, 3, 4, 5, 6, 7],
        "measurements": [2, 4, 5, 5, 6, 6, 8, 9, 9],
    }
)

print(tl_duplicates.collect())
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
    tl_duplicates.pivot_wider(
        names_from="class",
        names_list=["bar", "foo"],
        id_cols="ID",
        values_from="scores",
        values_fn=None,
    ).collect()
except Exception as err:
    print(type(err).__name__)
    # Example: ComputeError / DuplicateError depending on Polars version.

### Use values_fn= to handle duplicates ###
print(
    tl_duplicates
    .pivot_wider(
        names_from="class",
        names_list=["bar", "foo"],
        id_cols="ID",
        values_from="scores",
        values_fn="mean",
    )
    .head()
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

### Multiple values with the same aggregation ###
print(
    tl_duplicates
    .pivot_wider(
        names_from="size",
        names_list=["large", "small"],
        id_cols="ID",
        values_from=["scores", "measurements"],
        values_fn="mean",
    )
    .collect()
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
pivot_wider accepts one values_fn at a time.
To reproduce pandas aggfunc=["mean", "sum"], first build those summaries with
GroupBy.agg(), then pivot the summary columns.
'''

tl_measurement_summary = (
    tl_duplicates
    .group_by(["ID", "size"])
    .agg(
        f("measurements").mean().alias("measurements_mean"),
        f("measurements").sum().alias("measurements_sum"),
    )
)
print(tl_measurement_summary.collect())
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

tl_pivoted_tbl_multi_agg = tl_measurement_summary.pivot_wider(
    names_from="size",
    names_list=["large", "small"],
    id_cols="ID",
    values_from=["measurements_mean", "measurements_sum"],
    values_fn="first",
)
print(tl_pivoted_tbl_multi_agg.collect())
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
Combine size and class into a single names_from column before pivoting.
Each output column represents one observed combination, such as large_foo.
'''

tl_std_summary = (
    tl_duplicates
    .group_by(["ID", "size", "class"])
    .agg(f("scores").std().alias("scores_std"))
)

tl_pivoted_tbl_multi_on = tl_std_summary.mutate(
    (f("size") + tp.lit("_") + f("class")).alias("size_class")
).pivot_wider(
    names_from="size_class",
    id_cols="ID",
    values_from="scores_std",
    values_fn="first",
)

print(tl_pivoted_tbl_multi_on.collect())
# Output contains ID and the combined large_bar, large_foo,
# small_bar, and small_foo columns. Discovered column order may vary.

### TibbleLazy pivot ###
'''
Supply names_list= to avoid executing a category-discovery query while building
this lazy plan. Omitting names_list is allowed, but it collects the name column.
'''

print(
    tl_duplicates
    .pivot_wider(
        names_from="class",
        names_list=["bar", "foo"],
        id_cols="ID",
        values_from="scores",
        values_fn="mean",
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

##----------------------##
## Create example frame ##
##----------------------##

n_patients = 8
patient_ids = [f"P{i:03d}" for i in range(1, n_patients + 1)]

np.random.seed(42)
tl_measurements = tp.TibbleLazy(
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

print(tl_measurements.collect())
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

##----------------------------------##
##  tl.pivot_longer(): wide -> long ##
##----------------------------------##
'''
Pandas:
    pd.melt(frame=df, id_vars=[...], value_vars=[...])

Tidypyrs:
    tl.pivot_longer(cols=[...], names_to="name", values_to="value")

Parameter mapping:
    pandas value_vars -> tidypyrs cols
    pandas var_name   -> tidypyrs names_to
    pandas value_name -> tidypyrs values_to

There is no id_cols parameter on pivot_longer: all unselected columns
are retained automatically, here patient_id and age.
'''

value_cols = [col for col in tl_measurements.colnames if col.startswith(("BP_", "HR_"))]

tl_unpivoted = tl_measurements.pivot_longer(
    cols=value_cols,
    names_to="measurement_day",
    values_to="measured_value",
)

print(tl_unpivoted.head().collect())
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
Tidypyrs accepts Polars selectors through tidypyrs.selectors.
Here, cs.matches(...) selects all columns whose names look like BP_day1, HR_day2, etc.
'''

tl_unpivoted_selector = tl_measurements.pivot_longer(
    cols=cs.matches(r"^(BP|HR)_day\d+$"),
    names_to="measurement_day",
    values_to="measured_value",
)

print(tl_unpivoted_selector.head().collect())
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

Tidypyrs does this explicitly:
1. unpivot wide columns into rows
2. split the original column name into metric and day label
3. extract the day number
4. pivot metric back into separate BP and HR columns
'''

tl_wtl_long = (
    tl_measurements
    .pivot_longer(
        cols=cs.matches(r"^(BP|HR)_day\d+$"),
        names_to="measurement_day",
        values_to="measured_value",
    )
    .mutate(
        f("measurement_day").str.split_exact("_", 1).alias("parts")
    )
    .unnest("parts")
    .rename({"field_0": "metric", "field_1": "day_label"})
    .mutate(
        f("day_label").str.extract(r"(\d+)$", 1).cast(tp.Int64).alias("day")
    )
    .drop(["measurement_day", "day_label"])
)
print(tl_wtl_long.head().collect())
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
tl_wtl = (
    tl_wtl_long
    .pivot_wider(
        names_from="metric",
        names_list=["BP", "HR"],
        id_cols=["patient_id", "age", "day"],
        values_from="measured_value",
        values_fn="first",
    )
    .sort(["patient_id", "day"])
)
print(tl_wtl.head(10).collect())
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

### TibbleLazy unpivot ###
tl_lazy_unpivoted = (
    tl_measurements
    .pivot_longer(
        cols=cs.matches(r"^(BP|HR)_day\d+$"),
        names_to="measurement_day",
        values_to="measured_value",
    )
)
print(tl_lazy_unpivoted.head().collect())
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
