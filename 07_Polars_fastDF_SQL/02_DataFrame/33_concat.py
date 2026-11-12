'''
+ pl.concat([...], how="vertical"): stack Frames vertically, row-wise.
+ pl.concat([...], how="horizontal"/"horizontal_extend"): stack Frames horizontally, column-wise by row position.
+ pl.concat([...], how="diagonal"): stack Frames vertically while taking the union of columns.
+ pl.concat([...], how="vertical_relaxed" / "diagonal_relaxed"): allow compatible dtype coercion.
+ df.vstack(other): vertical stack two DataFrames.
+ df.hstack(other): horizontal stack columns to a DataFrame.
'''

import polars as pl

# Create sample LazyFrames
# NOTE: Polars has no custom row index, so there is no ignore_index=True parameter.
lf_origin = pl.LazyFrame({
    "A": ["A0", "A1", "A2", "A3"],
    "B": ["B0", "B1", "B2", "B3"],
    "C": ["C0", "C1", "C2", "C3"],
})

lf_ver_1 = pl.LazyFrame({
    "A": ["A4", "A5", "A6", "A7"],
    "B": ["B4", "B5", "B6", "B7"],
    "C": ["C4", "C5", "C6", "C7"],
})

lf_ver_2 = pl.LazyFrame({
    "A": ["A8", "A9", "A10", "A11"],
    "B": ["B8", "B9", "B10", "B11"],
    "C": ["C8", "C9", "C10", "C11"],
})

lf_hor_1 = pl.LazyFrame({
    "D": ["D0", "D1", "D2", "D3"],
    "E": ["E0", "E1", "E2", "E3"],
    "F": ["F0", "F1", "F2", "F3"],
})

lf_hor_2 = pl.LazyFrame({
    "G": ["G0", "G1", "G2", "G3"],
    "H": ["H0", "H1", "H2", "H3"],
    "I": ["I0", "I1", "I2", "I3"],
})

##---------------------------------##
##    pl.concat(how="vertical")    ##
##---------------------------------##
'''Concatenate LazyFrames vertically (row-wise).'''

# Original LazyFrame
print(lf_origin.collect())
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

# Concatenate lf_origin and lf_ver_1 vertically
# Equivalent to pandas pd.concat([lf_origin, lf_ver_1], axis=0, ignore_index=True)
print(
    pl.concat(
        items=[lf_origin, lf_ver_1],
        how="vertical",
    )
    .collect()
)
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

# Concatenate lf_ver_1, lf_origin, and lf_ver_2 vertically
print(
    pl.concat(
        items=[lf_ver_1, lf_origin, lf_ver_2],
        how="vertical",
    )
    .collect()
)
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
'''Concatenate LazyFrames horizontally (column-wise by row position).'''

# Equivalent to pandas pd.concat([lf_origin, lf_hor_1], axis=1)
print(
    pl.concat(
        items=[lf_origin, lf_hor_1],
        how="horizontal",
    )
    .collect()
)
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

# Concatenate three LazyFrames horizontally
print(
    pl.concat(
        items=[lf_hor_1, lf_origin, lf_hor_2],
        how="horizontal",
    )
    .collect()
)
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

# If horizontal LazyFrames have different heights, use "horizontal_extend" to pad shorter column with nulls
lf_short = pl.LazyFrame({"X": ["X0", "X1"]})
lf_long = pl.LazyFrame({"Y": ["Y0", "Y1", "Y2", "Y3"]})
print(pl.concat([lf_short, lf_long], how="horizontal_extend").collect())
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

##-----------------------------------##
##    pl.concat(how="diagonal")      ##
##-----------------------------------##
'''
how="diagonal" is a very useful Polars-specific concat mode.
It stacks LazyFrames vertically while taking the union of all column names.
Missing values are filled with null.
'''

lf_schema_1 = pl.LazyFrame({
    "A": ["A0", "A1"],
    "B": ["B0", "B1"],
})

lf_schema_2 = pl.LazyFrame({
    "A": ["A2", "A3"],
    "C": ["C2", "C3"],
})

print(
    pl.concat([lf_schema_1, lf_schema_2], how="diagonal")
    .collect()
)
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

lf_int = pl.LazyFrame({"A": [1, 2], "B": [10, 20]})
lf_float = pl.LazyFrame({"A": [3.5, 4.5], "B": [30, 40]})

print(
    pl.concat([lf_int, lf_float], how="vertical_relaxed")
    .collect()
)
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

print(
    lf_origin
    .collect()
    .vstack(lf_ver_1.collect())
)
# Same result as pl.concat([lf_origin, lf_ver_1], how="vertical")

##----------------##
##    hstack()    ##
##----------------##
'''df.hstack(other) is a direct horizontal stack method.'''

print(
    lf_origin
    .collect()
    .hstack(lf_hor_1.collect())
)
# Same result as pl.concat([lf_origin, lf_hor_1], how="horizontal")
