'''
In Polars, the closest equivalents to pandas pd.concat(), pd.merge(), and df.combine()
are usually pl.concat(), DataFrame.join(), and expression-based horizontal operations.

##------------------------------------------------------------------------------------##

1. Concatenation:
   + pl.concat([...], how="vertical"): stack DataFrames vertically, row-wise.
   + pl.concat([...], how="horizontal"): stack DataFrames horizontally, column-wise by row position.
   + pl.concat([...], how="diagonal"): stack DataFrames vertically while taking the union of columns.
   + pl.concat([...], how="vertical_relaxed" / "diagonal_relaxed"): allow compatible dtype coercion.
   + df.vstack(other): vertical stack two DataFrames.
   + df.hstack(other): horizontal stack columns to a DataFrame.

2. Joining / Merging:
   + df.join(other, on="key"): pandas pd.merge(on="key") equivalent.
   + df.join(other, suffix="_right"): suffix for duplicate column names from the RIGHT DataFrame.
   + df.join(other, how="inner"): only keys present in both DataFrames.
   + df.join(other, how="full"): pandas how="outer" equivalent.
   + df.join(other, how="left"): keep all rows from the left DataFrame.
   + df.join(other, how="right"): keep all rows from the right DataFrame.
   + df.join(other, left_on="key1", right_on="key2"): join on different key names.
   + Polars has no custom row index; use an explicit column for pandas left_index/right_index logic.
   + df.join(other, how="cross"): Cartesian product.
   + df.join_where(): non-equi joins
   + Polars has no pd.merge() top-level function; use the DataFrame .join() method.
   + Polars also supports how="semi" and how="anti" joins.

3. Combining values element-wise:
   + Polars has no direct df.combine(func=...) method.
   + Use expression-based operations such as pl.max_horizontal(), pl.min_horizontal(), arithmetic,
     pl.coalesce(), and pl.when().then().otherwise().

Key Polars differences from pandas:
+ Polars does not have a special row index or MultiIndex. Row labels should be normal columns.
+ Polars uses null for missing values, not NaN for general missing data.
+ Joins do not guarantee row order unless you explicitly use maintain_order=...
+ For full joins, use how="full" rather than pandas how="outer".
'''

import polars as pl

# =========================================================================================
# 1. Concatenation
# =========================================================================================

# Create sample DataFrames
# NOTE: Polars has no custom row index, so there is no ignore_index=True parameter.
df_origin = pl.DataFrame({
    "A": ["A0", "A1", "A2", "A3"],
    "B": ["B0", "B1", "B2", "B3"],
    "C": ["C0", "C1", "C2", "C3"],
})

df_ver_1 = pl.DataFrame({
    "A": ["A4", "A5", "A6", "A7"],
    "B": ["B4", "B5", "B6", "B7"],
    "C": ["C4", "C5", "C6", "C7"],
})

df_ver_2 = pl.DataFrame({
    "A": ["A8", "A9", "A10", "A11"],
    "B": ["B8", "B9", "B10", "B11"],
    "C": ["C8", "C9", "C10", "C11"],
})

df_hor_1 = pl.DataFrame({
    "D": ["D0", "D1", "D2", "D3"],
    "E": ["E0", "E1", "E2", "E3"],
    "F": ["F0", "F1", "F2", "F3"],
})

df_hor_2 = pl.DataFrame({
    "G": ["G0", "G1", "G2", "G3"],
    "H": ["H0", "H1", "H2", "H3"],
    "I": ["I0", "I1", "I2", "I3"],
})

##---------------------------------##
##    pl.concat(how="vertical")    ##
##---------------------------------##
'''Concatenate DataFrames vertically (row-wise).'''

# Original DataFrame
print(df_origin)
# shape: (4, 3)
# ┌─────┬─────┬─────┐
# │ A   ┆ B   ┆ C   │
# │ --- ┆ --- ┆ --- │
# │ str ┆ str ┆ str │
# ╞═════╪═════╪═════╡
# │ A0  ┆ B0  ┆ C0  │
# │ A1  ┆ B1  ┆ C1  │
# │ A2  ┆ B2  ┆ C2  │
# │ A3  ┆ B3  ┆ C3  │
# └─────┴─────┴─────┘

# Concatenate df_origin and df_ver_1 vertically
# Equivalent to pandas pd.concat([df_origin, df_ver_1], axis=0, ignore_index=True)
df_stack_ver = pl.concat(
    items=[df_origin, df_ver_1],
    how="vertical",
)
print(df_stack_ver)
# shape: (8, 3)
# ┌─────┬─────┬─────┐
# │ A   ┆ B   ┆ C   │
# │ --- ┆ --- ┆ --- │
# │ str ┆ str ┆ str │
# ╞═════╪═════╪═════╡
# │ A0  ┆ B0  ┆ C0  │
# │ A1  ┆ B1  ┆ C1  │
# │ A2  ┆ B2  ┆ C2  │
# │ A3  ┆ B3  ┆ C3  │
# │ A4  ┆ B4  ┆ C4  │
# │ A5  ┆ B5  ┆ C5  │
# │ A6  ┆ B6  ┆ C6  │
# │ A7  ┆ B7  ┆ C7  │
# └─────┴─────┴─────┘

# Concatenate df_ver_1, df_origin, and df_ver_2 vertically
df_stack_ver = pl.concat(
    items=[df_ver_1, df_origin, df_ver_2],
    how="vertical",
)
print(df_stack_ver)
# shape: (12, 3)
# ┌─────┬─────┬─────┐
# │ A   ┆ B   ┆ C   │
# │ --- ┆ --- ┆ --- │
# │ str ┆ str ┆ str │
# ╞═════╪═════╪═════╡
# │ A4  ┆ B4  ┆ C4  │
# │ A5  ┆ B5  ┆ C5  │
# │ A6  ┆ B6  ┆ C6  │
# │ A7  ┆ B7  ┆ C7  │
# │ A0  ┆ B0  ┆ C0  │
# │ ... ┆ ... ┆ ... │
# │ A11 ┆ B11 ┆ C11 │
# └─────┴─────┴─────┘

##-----------------------------------##
##    pl.concat(how="horizontal")    ##
##-----------------------------------##
'''Concatenate DataFrames horizontally (column-wise by row position).'''

# Equivalent to pandas pd.concat([df_origin, df_hor_1], axis=1)
df_stack_hor = pl.concat(
    items=[df_origin, df_hor_1],
    how="horizontal",
)
print(df_stack_hor)
# shape: (4, 6)
# ┌─────┬─────┬─────┬─────┬─────┬─────┐
# │ A   ┆ B   ┆ C   ┆ D   ┆ E   ┆ F   │
# │ --- ┆ --- ┆ --- ┆ --- ┆ --- ┆ --- │
# │ str ┆ str ┆ str ┆ str ┆ str ┆ str │
# ╞═════╪═════╪═════╪═════╪═════╪═════╡
# │ A0  ┆ B0  ┆ C0  ┆ D0  ┆ E0  ┆ F0  │
# │ A1  ┆ B1  ┆ C1  ┆ D1  ┆ E1  ┆ F1  │
# │ A2  ┆ B2  ┆ C2  ┆ D2  ┆ E2  ┆ F2  │
# │ A3  ┆ B3  ┆ C3  ┆ D3  ┆ E3  ┆ F3  │
# └─────┴─────┴─────┴─────┴─────┴─────┘

# Concatenate three DataFrames horizontally
df_stack_hor = pl.concat(
    items=[df_hor_1, df_origin, df_hor_2],
    how="horizontal",
)
print(df_stack_hor)
# shape: (4, 9)
# ┌─────┬─────┬─────┬─────┬───┬─────┬─────┬─────┬─────┐
# │ D   ┆ E   ┆ F   ┆ A   ┆ … ┆ C   ┆ G   ┆ H   ┆ I   │
# │ --- ┆ --- ┆ --- ┆ --- ┆   ┆ --- ┆ --- ┆ --- ┆ --- │
# │ str ┆ str ┆ str ┆ str ┆   ┆ str ┆ str ┆ str ┆ str │
# ╞═════╪═════╪═════╪═════╪═══╪═════╪═════╪═════╪═════╡
# │ D0  ┆ E0  ┆ F0  ┆ A0  ┆ … ┆ C0  ┆ G0  ┆ H0  ┆ I0  │
# │ D1  ┆ E1  ┆ F1  ┆ A1  ┆ … ┆ C1  ┆ G1  ┆ H1  ┆ I1  │
# │ D2  ┆ E2  ┆ F2  ┆ A2  ┆ … ┆ C2  ┆ G2  ┆ H2  ┆ I2  │
# │ D3  ┆ E3  ┆ F3  ┆ A3  ┆ … ┆ C3  ┆ G3  ┆ H3  ┆ I3  │
# └─────┴─────┴─────┴─────┴───┴─────┴─────┴─────┴─────┘

# If horizontal DataFrames have different heights, Polars pads shorter columns with nulls.
df_short = pl.DataFrame({"X": ["X0", "X1"]})
df_long = pl.DataFrame({"Y": ["Y0", "Y1", "Y2", "Y3"]})

print(pl.concat([df_short, df_long], how="horizontal"))
# shape: (4, 2)
# ┌──────┬─────┐
# │ X    ┆ Y   │
# │ ---  ┆ --- │
# │ str  ┆ str │
# ╞══════╪═════╡
# │ X0   ┆ Y0  │
# │ X1   ┆ Y1  │
# │ null ┆ Y2  │
# │ null ┆ Y3  │
# └──────┴─────┘

# Use strict=True if you want horizontal concatenation to fail when heights differ.
# pl.concat([df_short, df_long], how="horizontal", strict=True)  # raises an error

##-----------------------------------##
##    pl.concat(how="diagonal")      ##
##-----------------------------------##
'''
how="diagonal" is a very useful Polars-specific concat mode.
It stacks DataFrames vertically while taking the union of all column names.
Missing values are filled with null.
'''

df_schema_1 = pl.DataFrame({
    "A": ["A0", "A1"],
    "B": ["B0", "B1"],
})

df_schema_2 = pl.DataFrame({
    "A": ["A2", "A3"],
    "C": ["C2", "C3"],
})

print(pl.concat([df_schema_1, df_schema_2], how="diagonal"))
# shape: (4, 3)
# ┌─────┬──────┬──────┐
# │ A   ┆ B    ┆ C    │
# │ --- ┆ ---  ┆ ---  │
# │ str ┆ str  ┆ str  │
# ╞═════╪══════╪══════╡
# │ A0  ┆ B0   ┆ null │
# │ A1  ┆ B1   ┆ null │
# │ A2  ┆ null ┆ C2   │
# │ A3  ┆ null ┆ C3   │
# └─────┴──────┴──────┘

##--------------------------------------------##
##    how="vertical_relaxed" and dtype casts  ##
##--------------------------------------------##
'''
how="vertical" requires the same column names and compatible dtypes.
how="vertical_relaxed" coerces compatible columns to a common supertype.
'''

df_int = pl.DataFrame({"A": [1, 2], "B": [10, 20]})
df_float = pl.DataFrame({"A": [3.5, 4.5], "B": [30, 40]})

print(pl.concat([df_int, df_float], how="vertical_relaxed"))
# shape: (4, 2)
# ┌─────┬─────┐
# │ A   ┆ B   │
# │ --- ┆ --- │
# │ f64 ┆ i64 │
# ╞═════╪═════╡
# │ 1.0 ┆ 10  │
# │ 2.0 ┆ 20  │
# │ 3.5 ┆ 30  │
# │ 4.5 ┆ 40  │
# └─────┴─────┘

##----------------##
##    vstack()    ##
##----------------##
'''df.vstack(other) is a direct vertical stack method for two DataFrames.'''

print(df_origin.vstack(df_ver_1))
# Same result as pl.concat([df_origin, df_ver_1], how="vertical")

##----------------##
##    hstack()    ##
##----------------##
'''df.hstack(other) is a direct horizontal stack method.'''

print(df_origin.hstack(df_hor_1))
# Same result as pl.concat([df_origin, df_hor_1], how="horizontal")


# =========================================================================================
# 2. Joining
# =========================================================================================

# Create sample DataFrames for joining.
customers = pl.DataFrame(
    {
        "customer_id": [1, 2, 3, 4],
        "name"       : ["Alice", "Bob", "Charlie", "Diana"],
        "city"       : ["New York", "Boston", "Chicago", "Miami"],
    }
)

orders = pl.DataFrame(
    {
        "order_id"   : [101, 102, 103, 105],
        "customer_id": [1, 2, 1, 5],
        "amount"     : [250, 180, 320, 150],
        "city"       : ["NYC", "BOS", "NYC", "MIA"],
    }
)

##---------------------##
##    df.join(on=)     ##
##---------------------##
'''
Join DataFrames based on a common column/key.

Pandas:
    pd.merge(customers, orders, on="customer_id")

Polars:
    customers.join(orders, on="customer_id")
'''

# Default how="inner".
# maintain_order="left" is used here so the printed result is predictable.
df_joined_on = customers.join(
    orders,
    on="customer_id",
    maintain_order="left",
)

print(df_joined_on)
# shape: (3, 6)
# ┌─────────────┬───────┬──────────┬──────────┬────────┬────────────┐
# │ customer_id ┆ name  ┆ city     ┆ order_id ┆ amount ┆ city_right │
# │ ---         ┆ ---   ┆ ---      ┆ ---      ┆ ---    ┆ ---        │
# │ i64         ┆ str   ┆ str      ┆ i64      ┆ i64    ┆ str        │
# ╞═════════════╪═══════╪══════════╪══════════╪════════╪════════════╡
# │ 1           ┆ Alice ┆ New York ┆ 101      ┆ 250    ┆ NYC        │
# │ 1           ┆ Alice ┆ New York ┆ 103      ┆ 320    ┆ NYC        │
# │ 2           ┆ Bob   ┆ Boston   ┆ 102      ┆ 180    ┆ BOS        │
# └─────────────┴───────┴──────────┴──────────┴────────┴────────────┘

'''
NOTE:
Both DataFrames have a column named "city".
Polars keeps the left column name as "city" and appends the suffix to the right duplicate column.
The default suffix is "_right".
'''

##----------------------##
##    df.join(suffix)   ##
##----------------------##
'''Add a suffix to overlapping column names from the RIGHT DataFrame.'''

# In pandas, suffixes=('_cst', '_odr') lets you suffix both left and right.
# In Polars, suffix="_odr" applies to duplicate columns from the RIGHT DataFrame only.
df_joined_suffix = customers.join(
    orders,
    on="customer_id",
    suffix="_odr",
    maintain_order="left",
)

print(df_joined_suffix)
# shape: (3, 6)
# ┌─────────────┬───────┬──────────┬──────────┬────────┬──────────┐
# │ customer_id ┆ name  ┆ city     ┆ order_id ┆ amount ┆ city_odr │
# │ ---         ┆ ---   ┆ ---      ┆ ---      ┆ ---    ┆ ---      │
# │ i64         ┆ str   ┆ str      ┆ i64      ┆ i64    ┆ str      │
# ╞═════════════╪═══════╪══════════╪══════════╪════════╪══════════╡
# │ 1           ┆ Alice ┆ New York ┆ 101      ┆ 250    ┆ NYC      │
# │ 1           ┆ Alice ┆ New York ┆ 103      ┆ 320    ┆ NYC      │
# │ 2           ┆ Bob   ┆ Boston   ┆ 102      ┆ 180    ┆ BOS      │
# └─────────────┴───────┴──────────┴──────────┴────────┴──────────┘

# If you want pandas-like suffixes for BOTH sides, rename columns before joining.
customers_suffixed = customers.rename({"city": "city_cst"})
orders_suffixed = orders.rename({"city": "city_odr"})

print(
    customers_suffixed.join(
        orders_suffixed,
        on="customer_id",
        maintain_order="left",
    )
)
# shape: (3, 6)
# ┌─────────────┬───────┬──────────┬──────────┬────────┬──────────┐
# │ customer_id ┆ name  ┆ city_cst ┆ order_id ┆ amount ┆ city_odr │
# │ ---         ┆ ---   ┆ ---      ┆ ---      ┆ ---    ┆ ---      │
# │ i64         ┆ str   ┆ str      ┆ i64      ┆ i64    ┆ str      │
# ╞═════════════╪═══════╪══════════╪══════════╪════════╪══════════╡
# │ 1           ┆ Alice ┆ New York ┆ 101      ┆ 250    ┆ NYC      │
# │ 1           ┆ Alice ┆ New York ┆ 103      ┆ 320    ┆ NYC      │
# │ 2           ┆ Bob   ┆ Boston   ┆ 102      ┆ 180    ┆ BOS      │
# └─────────────┴───────┴──────────┴──────────┴────────┴──────────┘

##------------------------##
##    df.join(inner)      ##
##------------------------##
'''
how="inner": only keeps rows whose keys are present in both DataFrames.
This is the default join strategy.
'''

df_joined_inner = customers.join(
    orders,
    on="customer_id",
    how="inner",
    suffix="_odr",
    maintain_order="left",
)

print(df_joined_inner)
# shape: (3, 6)
# ┌─────────────┬───────┬──────────┬──────────┬────────┬──────────┐
# │ customer_id ┆ name  ┆ city     ┆ order_id ┆ amount ┆ city_odr │
# │ ---         ┆ ---   ┆ ---      ┆ ---      ┆ ---    ┆ ---      │
# │ i64         ┆ str   ┆ str      ┆ i64      ┆ i64    ┆ str      │
# ╞═════════════╪═══════╪══════════╪══════════╪════════╪══════════╡
# │ 1           ┆ Alice ┆ New York ┆ 101      ┆ 250    ┆ NYC      │
# │ 1           ┆ Alice ┆ New York ┆ 103      ┆ 320    ┆ NYC      │
# │ 2           ┆ Bob   ┆ Boston   ┆ 102      ┆ 180    ┆ BOS      │
# └─────────────┴───────┴──────────┴──────────┴────────┴──────────┘
'''Only customer_id 1 and 2 are returned, because only those keys exist in both DataFrames.'''

##-----------------------##
##    df.join(full)      ##
##-----------------------##
'''
Polars how="full" is the closest equivalent to pandas how="outer".
It keeps all rows from both DataFrames and fills missing matches with null.

NOTE:
For full joins, Polars does not coalesce join columns by default.
Use coalesce=True if you want one shared join-key column.
'''

df_joined_full = customers.join(
    orders,
    on="customer_id",
    how="full",
    suffix="_odr",
    coalesce=True,
    maintain_order="left_right",
)

print(df_joined_full)
# shape: (6, 6)
# ┌─────────────┬─────────┬──────────┬──────────┬────────┬──────────┐
# │ customer_id ┆ name    ┆ city     ┆ order_id ┆ amount ┆ city_odr │
# │ ---         ┆ ---     ┆ ---      ┆ ---      ┆ ---    ┆ ---      │
# │ i64         ┆ str     ┆ str      ┆ i64      ┆ i64    ┆ str      │
# ╞═════════════╪═════════╪══════════╪══════════╪════════╪══════════╡
# │ 1           ┆ Alice   ┆ New York ┆ 101      ┆ 250    ┆ NYC      │
# │ 1           ┆ Alice   ┆ New York ┆ 103      ┆ 320    ┆ NYC      │
# │ 2           ┆ Bob     ┆ Boston   ┆ 102      ┆ 180    ┆ BOS      │
# │ 3           ┆ Charlie ┆ Chicago  ┆ null     ┆ null   ┆ null     │
# │ 4           ┆ Diana   ┆ Miami    ┆ null     ┆ null   ┆ null     │
# │ 5           ┆ null    ┆ null     ┆ 105      ┆ 150    ┆ MIA      │
# └─────────────┴─────────┴──────────┴──────────┴────────┴──────────┘
'''Here, customer_id 3, 4, and 5 are included, although they are not present in both DataFrames.'''

##-----------------------##
##    df.join(left)      ##
##-----------------------##
'''how="left": keeps all rows from the left DataFrame and matched rows from the right DataFrame.'''

df_joined_left = customers.join(
    orders,
    on="customer_id",
    how="left",
    suffix="_odr",
    maintain_order="left",
)

print(df_joined_left)
# shape: (5, 6)
# ┌─────────────┬─────────┬──────────┬──────────┬────────┬──────────┐
# │ customer_id ┆ name    ┆ city     ┆ order_id ┆ amount ┆ city_odr │
# │ ---         ┆ ---     ┆ ---      ┆ ---      ┆ ---    ┆ ---      │
# │ i64         ┆ str     ┆ str      ┆ i64      ┆ i64    ┆ str      │
# ╞═════════════╪═════════╪══════════╪══════════╪════════╪══════════╡
# │ 1           ┆ Alice   ┆ New York ┆ 101      ┆ 250    ┆ NYC      │
# │ 1           ┆ Alice   ┆ New York ┆ 103      ┆ 320    ┆ NYC      │
# │ 2           ┆ Bob     ┆ Boston   ┆ 102      ┆ 180    ┆ BOS      │
# │ 3           ┆ Charlie ┆ Chicago  ┆ null     ┆ null   ┆ null     │
# │ 4           ┆ Diana   ┆ Miami    ┆ null     ┆ null   ┆ null     │
# └─────────────┴─────────┴──────────┴──────────┴────────┴──────────┘

##------------------------##
##    df.join(right)      ##
##------------------------##
'''how="right": keeps all rows from the right DataFrame and matched rows from the left DataFrame.'''

df_joined_right = customers.join(
    orders,
    on="customer_id",
    how="right",
    suffix="_odr",
    maintain_order="right",
)

print(df_joined_right)
# shape: (4, 6)
# ┌───────┬──────────┬─────────────┬──────────┬────────┬──────────┐
# │ name  ┆ city     ┆ customer_id ┆ order_id ┆ amount ┆ city_odr │
# │ ---   ┆ ---      ┆ ---         ┆ ---      ┆ ---    ┆ ---      │
# │ str   ┆ str      ┆ i64         ┆ i64      ┆ i64    ┆ str      │
# ╞═══════╪══════════╪═════════════╪══════════╪════════╪══════════╡
# │ Alice ┆ New York ┆ 1           ┆ 101      ┆ 250    ┆ NYC      │
# │ Bob   ┆ Boston   ┆ 2           ┆ 102      ┆ 180    ┆ BOS      │
# │ Alice ┆ New York ┆ 1           ┆ 103      ┆ 320    ┆ NYC      │
# │ null  ┆ null     ┆ 5           ┆ 105      ┆ 150    ┆ MIA      │
# └───────┴──────────┴─────────────┴──────────┴────────┴──────────┘

##----------------------------------##
##    df.join(left_on, right_on)    ##
##----------------------------------##
'''Join DataFrames based on different key names from each DataFrame.'''

customers_key = pl.DataFrame(
    {
        "customer_id": [1, 2, 3, 4],
        "name"       : ["Alice", "Bob", "Charlie", "Diana"],
        "city"       : ["New York", "Boston", "Chicago", "Miami"],
    }
)

orders_key = pl.DataFrame(
    {
        "order_id": [101, 102, 103, 105],
        "cst_id"  : [1, 2, 1, 5],
        "amount"  : [250, 180, 320, 150],
        "city"    : ["NYC", "BOS", "NYC", "MIA"],
    }
)

# coalesce=False keeps both key columns: customer_id and cst_id.
df_joined_diff_keys = customers_key.join(
    orders_key,
    left_on="customer_id",
    right_on="cst_id",
    how="inner",
    suffix="_odr",
    coalesce=False,
    maintain_order="left",
)

print(df_joined_diff_keys)
# shape: (3, 7)
# ┌─────────────┬───────┬──────────┬──────────┬────────┬────────┬──────────┐
# │ customer_id ┆ name  ┆ city     ┆ order_id ┆ cst_id ┆ amount ┆ city_odr │
# │ ---         ┆ ---   ┆ ---      ┆ ---      ┆ ---    ┆ ---    ┆ ---      │
# │ i64         ┆ str   ┆ str      ┆ i64      ┆ i64    ┆ i64    ┆ str      │
# ╞═════════════╪═══════╪══════════╪══════════╪════════╪════════╪══════════╡
# │ 1           ┆ Alice ┆ New York ┆ 101      ┆ 1      ┆ 250    ┆ NYC      │
# │ 1           ┆ Alice ┆ New York ┆ 103      ┆ 1      ┆ 320    ┆ NYC      │
# │ 2           ┆ Bob   ┆ Boston   ┆ 102      ┆ 2      ┆ 180    ┆ BOS      │
# └─────────────┴───────┴──────────┴──────────┴────────┴────────┴──────────┘

##------------------------------------------##
##    pandas left_index/right_index logic   ##
##------------------------------------------##
'''
Polars has no custom row index, so there is no left_index=True or right_index=True.
Use explicit columns instead.

Pandas idea:
    pd.merge(customers_idx, orders_idx, left_index=True, right_index=True)

Polars idea:
    Store the index values in a normal column, then join on that column.
'''

customers_idx = pl.DataFrame(
    {
        "customer_id": [1, 2, 3, 4],
        "name"       : ["Alice", "Bob", "Charlie", "Diana"],
        "city"       : ["New York", "Boston", "Chicago", "Miami"],
    }
)

orders_idx = pl.DataFrame(
    {
        "customer_id": [1, 2, 1, 5],
        "order_id"   : [101, 102, 103, 105],
        "amount"     : [250, 180, 320, 150],
        "city"       : ["NYC", "BOS", "NYC", "MIA"],
    }
)

df_joined_index_like = customers_idx.join(
    orders_idx,
    on="customer_id",
    how="inner",
    suffix="_odr",
    maintain_order="left",
)

print(df_joined_index_like)
# shape: (3, 6)
# ┌─────────────┬───────┬──────────┬──────────┬────────┬──────────┐
# │ customer_id ┆ name  ┆ city     ┆ order_id ┆ amount ┆ city_odr │
# │ ---         ┆ ---   ┆ ---      ┆ ---      ┆ ---    ┆ ---      │
# │ i64         ┆ str   ┆ str      ┆ i64      ┆ i64    ┆ str      │
# ╞═════════════╪═══════╪══════════╪══════════╪════════╪══════════╡
# │ 1           ┆ Alice ┆ New York ┆ 101      ┆ 250    ┆ NYC      │
# │ 1           ┆ Alice ┆ New York ┆ 103      ┆ 320    ┆ NYC      │
# │ 2           ┆ Bob   ┆ Boston   ┆ 102      ┆ 180    ┆ BOS      │
# └─────────────┴───────┴──────────┴──────────┴────────┴──────────┘

# If you truly need the physical row number, add it as a normal column.
customers_row_nr = customers.with_row_index("row_nr")
orders_row_nr = orders.with_row_index("row_nr")

print(
    customers_row_nr.join(
        orders_row_nr,
        on="row_nr",
        how="inner",
        suffix="_odr",
    )
)
# This joins by row position, not by a custom index label.

##-----------------------##
##    df.join(cross)     ##
##-----------------------##
'''
how="cross": creates the Cartesian product of both DataFrames.
Do not specify on=, left_on=, or right_on= with a cross join.
'''

df_left = pl.DataFrame({"left": ["foo", "bar"]})
print(df_left)
# shape: (2, 1)
# ┌──────┐
# │ left │
# │ ---  │
# │ str  │
# ╞══════╡
# │ foo  │
# │ bar  │
# └──────┘

df_right = pl.DataFrame({"right": [7, 8]})
print(df_right)
# shape: (2, 1)
# ┌───────┐
# │ right │
# │ ---   │
# │ i64   │
# ╞═══════╡
# │ 7     │
# │ 8     │
# └───────┘

df_joined_cross = df_left.join(
    df_right,
    how="cross",
)

print(df_joined_cross)
# shape: (4, 2)
# ┌──────┬───────┐
# │ left ┆ right │
# │ ---  ┆ ---   │
# │ str  ┆ i64   │
# ╞══════╪═══════╡
# │ foo  ┆ 7     │
# │ foo  ┆ 8     │
# │ bar  ┆ 7     │
# │ bar  ┆ 8     │
# └──────┴───────┘

##-----------------------##
##    df.join(semi)      ##
##-----------------------##
'''
how="semi": keep rows from the left DataFrame that have a match in the right DataFrame.
Unlike inner joins, semi joins do NOT include columns from the right DataFrame.
'''

df_joined_semi = customers.join(
    orders.select("customer_id").unique(),
    on="customer_id",
    how="semi",
    maintain_order="left",
)

print(df_joined_semi)
# shape: (2, 3)
# ┌─────────────┬───────┬──────────┐
# │ customer_id ┆ name  ┆ city     │
# │ ---         ┆ ---   ┆ ---      │
# │ i64         ┆ str   ┆ str      │
# ╞═════════════╪═══════╪══════════╡
# │ 1           ┆ Alice ┆ New York │
# │ 2           ┆ Bob   ┆ Boston   │
# └─────────────┴───────┴──────────┘

##-----------------------##
##    df.join(anti)      ##
##-----------------------##
'''
how="anti": keep rows from the left DataFrame that have NO match in the right DataFrame.
Useful for finding unmatched records.
'''

df_joined_anti = customers.join(
    orders.select("customer_id").unique(),
    on="customer_id",
    how="anti",
    maintain_order="left",
)

print(df_joined_anti)
# shape: (2, 3)
# ┌─────────────┬─────────┬─────────┐
# │ customer_id ┆ name    ┆ city    │
# │ ---         ┆ ---     ┆ ---     │
# │ i64         ┆ str     ┆ str     │
# ╞═════════════╪═════════╪═════════╡
# │ 3           ┆ Charlie ┆ Chicago │
# │ 4           ┆ Diana   ┆ Miami   │
# └─────────────┴─────────┴─────────┘

##-----------------------------##
##    DataFrame .join() only   ##
##-----------------------------##
'''
Polars does not have a top-level pl.merge() function like pandas pd.merge().
Use DataFrame.join() directly.
'''

print(
    customers.join(
        orders,
        on="customer_id",
        how="inner",
        suffix="_odr",
        maintain_order="left",
    )
)
# Same as the previous inner join examples.

##-----------------------##
##    df.join_where()    ##
##-----------------------##
'''
Polars `join_where()` is used for "non-equi" joins.
Unlike standard joins that require strict equality on specific keys (on="key"),
`join_where()` allows you to join DataFrames based on ANY arbitrary boolean expression,
such as inequalities (<, >), range overlaps, or complex custom logic.

This is incredibly powerful for tasks like:
+ Finding overlapping time ranges / events.
+ Matching records within a certain tolerance or distance.
+ As-of style inequality matching.

NOTE: Multiple expressions passed to join_where() are implicitly combined with AND (&).
'''
# Example: Finding overlapping events
events_a = pl.DataFrame({
    "event_a": ["A1", "A2", "A3"],
    "start_a": [1, 5, 20],
    "end_a": [10, 15, 30]
})
events_b = pl.DataFrame({
    "event_b": ["B1", "B2", "B3"],
    "start_b": [2, 12, 25],
    "end_b": [8, 20, 35]
})

# Two events overlap if: start_a < end_b AND start_b < end_a
df_overlaps = events_a.join_where(
    events_b,
    pl.col("start_a") < pl.col("end_b"),
    pl.col("start_b") < pl.col("end_a")
)
print(df_overlaps)
# shape: (4, 6)
# ┌─────────┬─────────┬───────┬─────────┬─────────┬───────┐
# │ event_a ┆ start_a ┆ end_a ┆ event_b ┆ start_b ┆ end_b │
# │ ---     ┆ ---     ┆ ---   ┆ ---     ┆ ---     ┆ ---   │
# │ str     ┆ i64     ┆ i64   ┆ str     ┆ i64     ┆ i64   │
# ╞═════════╪═════════╪═══════╪═════════╪═════════╪═══════╡
# │ A1      ┆ 1       ┆ 10    ┆ B1      ┆ 2       ┆ 8     │
# │ A2      ┆ 5       ┆ 15    ┆ B1      ┆ 2       ┆ 8     │
# │ A2      ┆ 5       ┆ 15    ┆ B2      ┆ 12      ┆ 20    │
# │ A3      ┆ 20      ┆ 30    ┆ B3      ┆ 25      ┆ 35    │
# └─────────┴─────────┴───────┴─────────┴─────────┴───────┘

'''
NOTE ON OVERLAPPING COLUMN NAMES:
If both DataFrames share column names (e.g., both have "value"), Polars applies
the suffix (default "_right") to the right DataFrame's columns in the evaluation context.
To avoid ambiguity in your expressions, it is highly recommended to either:
1. Use distinct column names before joining (as shown above).
2. Reference the right-side columns using the suffix in your expression:
   `pl.col("value") < pl.col("value_right")`
'''

##-----------------------------------##
##    Optional: lazy join pattern    ##
##-----------------------------------##
'''
Polars joins also work in LazyFrame pipelines.
The query is executed only when you call .collect().
'''

lf_joined = (
    customers.lazy()
    .join(
        orders.lazy(),
        on="customer_id",
        how="inner",
        suffix="_odr",
    )
    .select("customer_id", "name", "order_id", "amount")
)

print(lf_joined.collect())
# shape: (3, 4)
# ┌─────────────┬───────┬──────────┬────────┐
# │ customer_id ┆ name  ┆ order_id ┆ amount │
# │ ---         ┆ ---   ┆ ---      ┆ ---    │
# │ i64         ┆ str   ┆ i64      ┆ i64    │
# ╞═════════════╪═══════╪══════════╪════════╡
# │ 1           ┆ Alice ┆ 101      ┆ 250    │
# │ 1           ┆ Alice ┆ 103      ┆ 320    │
# │ 2           ┆ Bob   ┆ 102      ┆ 180    │
# └─────────────┴───────┴──────────┴────────┘


# =========================================================================================
# 3. Combining
# =========================================================================================
'''
Pandas df.combine(other, func=...) applies a function element-wise after aligning DataFrames.

Polars does not have a direct df.combine() method.
The Polars style is:
1. Put the values you want to compare/combine side-by-side.
2. Use expressions to calculate the combined result.

For same-shape DataFrames, horizontal concatenation by row position is often enough.
For label/key alignment, join first, then combine columns.
'''


df1 = pl.DataFrame({"A": [0, 0], "B": [4, 4]})
print(df1)
# shape: (2, 2)
# ┌─────┬─────┐
# │ A   ┆ B   │
# │ --- ┆ --- │
# │ i64 ┆ i64 │
# ╞═════╪═════╡
# │ 0   ┆ 4   │
# │ 0   ┆ 4   │
# └─────┴─────┘

df2 = pl.DataFrame({"A": [1, 1], "B": [3, 3]})
print(df2)
# shape: (2, 2)
# ┌─────┬─────┐
# │ A   ┆ B   │
# │ --- ┆ --- │
# │ i64 ┆ i64 │
# ╞═════╪═════╡
# │ 1   ┆ 3   │
# │ 1   ┆ 3   │
# └─────┴─────┘

##--------------------------------##
##    Element-wise max combine    ##
##--------------------------------##
'''Equivalent idea to pandas df1.combine(df2, func=np.maximum).'''

# Rename df2 columns so they do not collide with df1 columns during horizontal concatenation.
df2_renamed = df2.rename({"A": "A_2", "B": "B_2"})

df_side_by_side = pl.concat([df1, df2_renamed], how="horizontal")
print(df_side_by_side)
# shape: (2, 4)
# ┌─────┬─────┬─────┬─────┐
# │ A   ┆ B   ┆ A_2 ┆ B_2 │
# │ --- ┆ --- ┆ --- ┆ --- │
# │ i64 ┆ i64 ┆ i64 ┆ i64 │
# ╞═════╪═════╪═════╪═════╡
# │ 0   ┆ 4   ┆ 1   ┆ 3   │
# │ 0   ┆ 4   ┆ 1   ┆ 3   │
# └─────┴─────┴─────┴─────┘

df_combined_max = df_side_by_side.select(
    pl.max_horizontal("A", "A_2").alias("A"),
    pl.max_horizontal("B", "B_2").alias("B"),
)

print(df_combined_max)
# shape: (2, 2)
# ┌─────┬─────┐
# │ A   ┆ B   │
# │ --- ┆ --- │
# │ i64 ┆ i64 │
# ╞═════╪═════╡
# │ 1   ┆ 4   │
# │ 1   ┆ 4   │
# └─────┴─────┘

##---------------------------------##
##    Element-wise mean combine    ##
##---------------------------------##
'''Equivalent idea to pandas df1.combine(df2, func=lambda s1, s2: (s1 + s2) / 2).'''


df_combined_mean = df_side_by_side.select(
    ((pl.col("A") + pl.col("A_2")) / 2).alias("A"),
    ((pl.col("B") + pl.col("B_2")) / 2).alias("B"),
)

print(df_combined_mean)
# shape: (2, 2)
# ┌─────┬─────┐
# │ A   ┆ B   │
# │ --- ┆ --- │
# │ f64 ┆ f64 │
# ╞═════╪═════╡
# │ 0.5 ┆ 3.5 │
# │ 0.5 ┆ 3.5 │
# └─────┴─────┘

##-------------------------------------##
##    Custom combine with pl.when()    ##
##-------------------------------------##
'''
Use pl.when().then().otherwise() for custom element-wise logic.

Example rule:
+ For each column, choose df2's value if it is greater than df1's value.
+ Otherwise choose df1's value.
'''

df_combined_custom = df_side_by_side.select(
    pl.when(pl.col("A_2") > pl.col("A"))
      .then(pl.col("A_2"))
      .otherwise(pl.col("A"))
      .alias("A"),
    pl.when(pl.col("B_2") > pl.col("B"))
      .then(pl.col("B_2"))
      .otherwise(pl.col("B"))
      .alias("B"),
)

print(df_combined_custom)
# shape: (2, 2)
# ┌─────┬─────┐
# │ A   ┆ B   │
# │ --- ┆ --- │
# │ i64 ┆ i64 │
# ╞═════╪═════╡
# │ 1   ┆ 4   │
# │ 1   ┆ 4   │
# └─────┴─────┘

##------------------------------------##
##    combine_first with coalesce()   ##
##------------------------------------##
'''
Pandas has df.combine_first(other), which fills null/missing values from another DataFrame.

Polars style:
+ join or concatenate the columns side-by-side.
+ use pl.coalesce() to take the first non-null value from left to right.
'''

left_values = pl.DataFrame({
    "id": [1, 2, 3, 4],
    "value": [None, 20, None, 40],
})

right_values = pl.DataFrame({
    "id": [1, 2, 3, 5],
    "value": [10, None, 30, 50],
})

# Full join aligns by id. suffix="_right" keeps the right-side value as value_right.
df_aligned = left_values.join(
    right_values,
    on="id",
    how="full",
    suffix="_right",
    coalesce=True,
    maintain_order="left_right",
)

print(df_aligned)
# shape: (5, 3)
# ┌─────┬───────┬─────────────┐
# │ id  ┆ value ┆ value_right │
# │ --- ┆ ---   ┆ ---         │
# │ i64 ┆ i64   ┆ i64         │
# ╞═════╪═══════╪═════════════╡
# │ 1   ┆ null  ┆ 10          │
# │ 2   ┆ 20    ┆ null        │
# │ 3   ┆ null  ┆ 30          │
# │ 4   ┆ 40    ┆ null        │
# │ 5   ┆ null  ┆ 50          │
# └─────┴───────┴─────────────┘

# Take the left value if it exists; otherwise use the right value.
df_combined_first = df_aligned.select(
    "id",
    pl.coalesce("value", "value_right").alias("value"),
)

print(df_combined_first)
# shape: (5, 2)
# ┌─────┬───────┐
# │ id  ┆ value │
# │ --- ┆ ---   │
# │ i64 ┆ i64   │
# ╞═════╪═══════╡
# │ 1   ┆ 10    │
# │ 2   ┆ 20    │
# │ 3   ┆ 30    │
# │ 4   ┆ 40    │
# │ 5   ┆ 50    │
# └─────┴───────┘

##-----------------------------------##
##    Multiple columns with a loop   ##
##-----------------------------------##
'''
For many columns, build the Polars expressions programmatically.
This is often cleaner than writing each expression by hand.
'''

left_multi = pl.DataFrame({
    "id": [1, 2, 3],
    "A": [None, 2, None],
    "B": [10, None, 30],
})

right_multi = pl.DataFrame({
    "id": [1, 2, 3],
    "A": [1, None, 3],
    "B": [None, 20, None],
})

aligned_multi = left_multi.join(
    right_multi,
    on="id",
    how="full",
    suffix="_right",
    coalesce=True,
)

value_cols = ["A", "B"]

combined_multi = aligned_multi.select(
    "id",
    *[
        pl.coalesce(col, f"{col}_right").alias(col)
        for col in value_cols
    ],
)

print(combined_multi)
# shape: (3, 3)
# ┌─────┬─────┬─────┐
# │ id  ┆ A   ┆ B   │
# │ --- ┆ --- ┆ --- │
# │ i64 ┆ i64 ┆ i64 │
# ╞═════╪═════╪═════╡
# │ 1   ┆ 1   ┆ 10  │
# │ 2   ┆ 2   ┆ 20  │
# │ 3   ┆ 3   ┆ 30  │
# └─────┴─────┴─────┘


# =========================================================================================
# 4. Quick Mapping Table
# =========================================================================================
'''
Pandas                              Polars
------------------------------------------------------------------------------------------
pd.concat([df1, df2], axis=0)       pl.concat([df1, df2], how="vertical")
pd.concat([df1, df2], axis=1)       pl.concat([df1, df2], how="horizontal")
pd.concat(..., ignore_index=True)   Default behavior, because Polars has no custom row index
pd.concat(..., join="outer")        pl.concat(..., how="diagonal") for schema union row stacking
df1.append(df2)                     pl.concat([df1, df2]) or df1.vstack(df2)

pd.merge(left, right, on="key")      left.join(right, on="key")
pd.merge(..., how="inner")          left.join(right, how="inner")
pd.merge(..., how="outer")          left.join(right, how="full")
pd.merge(..., how="left")           left.join(right, how="left")
pd.merge(..., how="right")          left.join(right, how="right")
pd.merge(..., how="cross")          left.join(right, how="cross")
pd.merge(left_on=..., right_on=...)  left.join(right, left_on=..., right_on=...)
pd.merge(left_index=True, ...)       Use explicit key columns; Polars has no custom row index
pd.merge(suffixes=("_x", "_y"))      Rename before join, or use suffix="_right" for right duplicates

df.combine(other, np.maximum)        pl.max_horizontal() after aligning columns side-by-side
df.combine(other, custom_func)       Expressions, arithmetic, pl.when().then().otherwise()
df.combine_first(other)              Join/concat side-by-side, then use pl.coalesce()
'''
