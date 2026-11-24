'''
tp.bind_rows -> pl.concat(how='diagonal_relaxed')
tp.bind_cols -> pl.concat(how='horizontal_extend')
'''

import tidypyrs as tp

# Create sample TibbleLazies
tl_origin = tp.TibbleLazy({
    "A": ["A0", "A1", "A2", "A3"],
    "B": ["B0", "B1", "B2", "B3"],
    "C": ["C0", "C1", "C2", "C3"],
})

tl_ver_1 = tp.TibbleLazy({
    "A": ["A4", "A5", "A6", "A7"],
    "B": ["B4", "B5", "B6", "B7"],
    "C": ["C4", "C5", "C6", "C7"],
})

tl_ver_2 = tp.TibbleLazy({
    "A": ["A8", "A9", "A10", "A11"],
    "B": ["B8", "B9", "B10", "B11"],
    "C": ["C8", "C9", "C10", "C11"],
})

tl_hor_1 = tp.TibbleLazy({
    "D": ["D0", "D1", "D2", "D3"],
    "E": ["E0", "E1", "E2", "E3"],
    "F": ["F0", "F1", "F2", "F3"],
})

tl_hor_2 = tp.TibbleLazy({
    "G": ["G0", "G1", "G2", "G3"],
    "H": ["H0", "H1", "H2", "H3"],
    "I": ["I0", "I1", "I2", "I3"],
})

##-------------------------------------##
## tl0.bind_rows([tl1, tl2, tl3, ...]) ##
##-------------------------------------##

print(
    tl_origin
    .bind_rows(tl_ver_1)
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

print(
    tl_origin
    .bind_rows(tl_ver_2, tl_ver_1)
    .collect()
)
# shape: (12, 3)
# ┌─────┬─────┬─────┐
# │ A   ┆ B   ┆ C   │
# │ --- ┆ --- ┆ --- │
# │ str ┆ str ┆ str │
# ╞═════╪═════╪═════╡
# │ A0  ┆ B0  ┆ C0  │
# │ A1  ┆ B1  ┆ C1  │
# │ A2  ┆ B2  ┆ C2  │
# │ A3  ┆ B3  ┆ C3  │
# │ A8  ┆ B8  ┆ C8  │
# │ …   ┆ …   ┆ …   │
# │ A11 ┆ B11 ┆ C11 │
# │ A4  ┆ B4  ┆ C4  │
# │ A5  ┆ B5  ┆ C5  │
# │ A6  ┆ B6  ┆ C6  │
# │ A7  ┆ B7  ┆ C7  │
# └─────┴─────┴─────┘

# Different type still works (coerce to a common super-type)
tl_int = tp.TibbleLazy({"A": [1, 2], "B": [10, 20]})
tl_float = tp.TibbleLazy({"A": [3.5, 4.5], "B": [30, 40]})
print(
    tl_int
    .bind_rows(tl_float)
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

##-------------------------------------##
## tl0.bind_cols([tl1, tl2, tl3, ...]) ##
##-------------------------------------##

print(
    tl_origin
    .bind_cols(tl_hor_1)
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

print(
    tl_origin
    .bind_cols(tl_hor_2, tl_hor_1)
    .collect()
)
# shape: (4, 9)
# ┌─────┬─────┬─────┬─────┬───┬─────┬─────┬─────┬─────┐
# │ A   ┆ B   ┆ C   ┆ G   ┆ … ┆ I   ┆ D   ┆ E   ┆ F   │
# │ --- ┆ --- ┆ --- ┆ --- ┆   ┆ --- ┆ --- ┆ --- ┆ --- │
# │ str ┆ str ┆ str ┆ str ┆   ┆ str ┆ str ┆ str ┆ str │
# ╞═════╪═════╪═════╪═════╪═══╪═════╪═════╪═════╪═════╡
# │ A0  ┆ B0  ┆ C0  ┆ G0  ┆ … ┆ I0  ┆ D0  ┆ E0  ┆ F0  │
# │ A1  ┆ B1  ┆ C1  ┆ G1  ┆ … ┆ I1  ┆ D1  ┆ E1  ┆ F1  │
# │ A2  ┆ B2  ┆ C2  ┆ G2  ┆ … ┆ I2  ┆ D2  ┆ E2  ┆ F2  │
# │ A3  ┆ B3  ┆ C3  ┆ G3  ┆ … ┆ I3  ┆ D3  ┆ E3  ┆ F3  │
# └─────┴─────┴─────┴─────┴───┴─────┴─────┴─────┴─────┘

# If horizontal Frames have different heights, automatically pads shorter column with nulls
tl_short = tp.TibbleLazy({"X": ["X0", "X1"]})
tl_long = tp.TibbleLazy({"Y": ["Y0", "Y1", "Y2", "Y3"]})
print(
    tl_short
    .bind_cols(tl_long)
    .collect()
)
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
