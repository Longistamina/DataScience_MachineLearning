'''
To select Polars DataFrame and LazyFrame based on indices,
we can use `.gather(indices)` method

1. `lf.gather(list_of_indices)`
2. `lf.gather(range(start, stop))`
3. `lf.gather(range(start, stop, step))`
4. `lf.gather_every(n, offset)`
'''

from pathlib import Path

import polars as pl

# Optional display settings for tutorial output.
pl.Config.set_tbl_cols(10)
pl.Config.set_float_precision(2)

data_dir = Path("/home").rglob("*/DataScience_MachineLearning/data")
data_dir = next(data_dir)

lf_baseball = pl.scan_csv(
    source=data_dir/"baseball.csv",
    schema_overrides={
        "Team": pl.Categorical,
        "Position": pl.Categorical,
        "PosCategory": pl.Categorical,
    },
)

# =============================================
# 1. `lf.gather(list_of_indices)`
# =============================================

print(
    lf_baseball
    .with_row_index()
    .gather([0, 10, 25, 300])
    .collect()
)
# shape: (4, 8)
# ┌───────┬─────────────────┬──────┬────────────────┬────────┬────────┬───────┬─────────────┐
# │ index ┆ Name            ┆ Team ┆ Position       ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---   ┆ ---             ┆ ---  ┆ ---            ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ u32   ┆ str             ┆ cat  ┆ cat            ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞═══════╪═════════════════╪══════╪════════════════╪════════╪════════╪═══════╪═════════════╡
# │ 0     ┆ Adam_Donachie   ┆ BAL  ┆ Catcher        ┆ 74     ┆ 180    ┆ 22.99 ┆ Catcher     │
# │ 10    ┆ Jeff_Fiorentino ┆ BAL  ┆ Outfielder     ┆ 73     ┆ 188    ┆ 23.88 ┆ Outfielder  │
# │ 25    ┆ Danys_Baez      ┆ BAL  ┆ Relief_Pitcher ┆ 75     ┆ 225    ┆ 29.47 ┆ Pitcher     │
# │ 300   ┆ Cesar_Jimenez   ┆ SEA  ┆ Relief_Pitcher ┆ 71     ┆ 180    ┆ 22.30 ┆ Pitcher     │
# └───────┴─────────────────┴──────┴────────────────┴────────┴────────┴───────┴─────────────┘

# =============================================
# 2. `lf.gather(range(start, stop))`
# =============================================

print(
    lf_baseball
    .with_row_index()
    .gather(range(5)) # means `range(0, 5)`, first 5 rows (index 0 -> 4)
    .collect()
)
# shape: (5, 8)
# ┌───────┬─────────────────┬──────┬───────────────┬────────┬────────┬───────┬─────────────┐
# │ index ┆ Name            ┆ Team ┆ Position      ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---   ┆ ---             ┆ ---  ┆ ---           ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ u32   ┆ str             ┆ cat  ┆ cat           ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞═══════╪═════════════════╪══════╪═══════════════╪════════╪════════╪═══════╪═════════════╡
# │ 0     ┆ Adam_Donachie   ┆ BAL  ┆ Catcher       ┆ 74     ┆ 180    ┆ 22.99 ┆ Catcher     │
# │ 1     ┆ Paul_Bako       ┆ BAL  ┆ Catcher       ┆ 74     ┆ 215    ┆ 34.69 ┆ Catcher     │
# │ 2     ┆ Ramon_Hernandez ┆ BAL  ┆ Catcher       ┆ 72     ┆ 210    ┆ 30.78 ┆ Catcher     │
# │ 3     ┆ Kevin_Millar    ┆ BAL  ┆ First_Baseman ┆ 72     ┆ 210    ┆ 35.43 ┆ Infielder   │
# │ 4     ┆ Chris_Gomez     ┆ BAL  ┆ First_Baseman ┆ 73     ┆ 188    ┆ 35.71 ┆ Infielder   │
# └───────┴─────────────────┴──────┴───────────────┴────────┴────────┴───────┴─────────────┘

print(
    lf_baseball
    .with_row_index()
    .gather(range(15, 19)) # index 15 -> 18
    .collect()
)
# shape: (4, 8)
# ┌───────┬─────────────┬──────┬──────────────────┬────────┬────────┬───────┬─────────────┐
# │ index ┆ Name        ┆ Team ┆ Position         ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---   ┆ ---         ┆ ---  ┆ ---              ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ u32   ┆ str         ┆ cat  ┆ cat              ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞═══════╪═════════════╪══════╪══════════════════╪════════╪════════╪═══════╪═════════════╡
# │ 15    ┆ Jay_Payton  ┆ BAL  ┆ Outfielder       ┆ 70     ┆ 185    ┆ 34.27 ┆ Outfielder  │
# │ 16    ┆ Erik_Bedard ┆ BAL  ┆ Starting_Pitcher ┆ 73     ┆ 189    ┆ 27.99 ┆ Pitcher     │
# │ 17    ┆ Hayden_Penn ┆ BAL  ┆ Starting_Pitcher ┆ 75     ┆ 185    ┆ 22.38 ┆ Pitcher     │
# │ 18    ┆ Adam_Loewen ┆ BAL  ┆ Starting_Pitcher ┆ 78     ┆ 219    ┆ 22.89 ┆ Pitcher     │
# └───────┴─────────────┴──────┴──────────────────┴────────┴────────┴───────┴─────────────┘

# =============================================
# 3. `lf.gather(range(start, stop, step))`
# =============================================

print(
    lf_baseball
    .with_row_index()
    .gather(range(0, 10, 2))
    .collect()
)
# shape: (5, 8)
# ┌───────┬─────────────────┬──────┬───────────────┬────────┬────────┬───────┬─────────────┐
# │ index ┆ Name            ┆ Team ┆ Position      ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---   ┆ ---             ┆ ---  ┆ ---           ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ u32   ┆ str             ┆ cat  ┆ cat           ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞═══════╪═════════════════╪══════╪═══════════════╪════════╪════════╪═══════╪═════════════╡
# │ 0     ┆ Adam_Donachie   ┆ BAL  ┆ Catcher       ┆ 74     ┆ 180    ┆ 22.99 ┆ Catcher     │
# │ 2     ┆ Ramon_Hernandez ┆ BAL  ┆ Catcher       ┆ 72     ┆ 210    ┆ 30.78 ┆ Catcher     │
# │ 4     ┆ Chris_Gomez     ┆ BAL  ┆ First_Baseman ┆ 73     ┆ 188    ┆ 35.71 ┆ Infielder   │
# │ 6     ┆ Miguel_Tejada   ┆ BAL  ┆ Shortstop     ┆ 69     ┆ 209    ┆ 30.77 ┆ Infielder   │
# │ 8     ┆ Aubrey_Huff     ┆ BAL  ┆ Third_Baseman ┆ 76     ┆ 231    ┆ 30.19 ┆ Infielder   │
# └───────┴─────────────────┴──────┴───────────────┴────────┴────────┴───────┴─────────────┘

print(
    lf_baseball
    .with_row_index()
    .gather(range(30, 60, 5))
    .collect()
)
# shape: (6, 8)
# ┌───────┬────────────────┬──────┬──────────────────┬────────┬────────┬───────┬─────────────┐
# │ index ┆ Name           ┆ Team ┆ Position         ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---   ┆ ---            ┆ ---  ┆ ---              ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ u32   ┆ str            ┆ cat  ┆ cat              ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞═══════╪════════════════╪══════╪══════════════════╪════════╪════════╪═══════╪═════════════╡
# │ 30    ┆ James_Hoey     ┆ BAL  ┆ Relief_Pitcher   ┆ 78     ┆ 200    ┆ 24.17 ┆ Pitcher     │
# │ 35    ┆ Toby_Hall      ┆ CWS  ┆ Catcher          ┆ 75     ┆ 240    ┆ 31.36 ┆ Catcher     │
# │ 40    ┆ Joe_Crede      ┆ CWS  ┆ Third_Baseman    ┆ 73     ┆ 200    ┆ 28.85 ┆ Infielder   │
# │ 45    ┆ Pablo_Ozuna    ┆ CWS  ┆ Outfielder       ┆ 70     ┆ 186    ┆ 32.51 ┆ Outfielder  │
# │ 50    ┆ Charlie_Haeger ┆ CWS  ┆ Starting_Pitcher ┆ 73     ┆ 200    ┆ 23.45 ┆ Pitcher     │
# │ 55    ┆ Javier_Vazquez ┆ CWS  ┆ Starting_Pitcher ┆ 74     ┆ 205    ┆ 30.60 ┆ Pitcher     │
# └───────┴────────────────┴──────┴──────────────────┴────────┴────────┴───────┴─────────────┘

# =============================================
# 4. `lf.gather_every(n, offset)`
# =============================================
'''
It will slice from start index to the end,
with given step.

Use this when you want to slice till the end of the frame.

Something like `df[start::step]`
'''

print(
    lf_baseball
    .with_row_index()
    .gather_every(n=3, offset=10) # Starts at index=10, gather to the end, with step=3
    .collect()
)
# shape: (335, 8)
# ┌───────┬─────────────────┬──────┬──────────────────┬────────┬────────┬───────┬─────────────┐
# │ index ┆ Name            ┆ Team ┆ Position         ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---   ┆ ---             ┆ ---  ┆ ---              ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ u32   ┆ str             ┆ cat  ┆ cat              ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞═══════╪═════════════════╪══════╪══════════════════╪════════╪════════╪═══════╪═════════════╡
# │ 10    ┆ Jeff_Fiorentino ┆ BAL  ┆ Outfielder       ┆ 73     ┆ 188    ┆ 23.88 ┆ Outfielder  │
# │ 13    ┆ Brandon_Fahey   ┆ BAL  ┆ Outfielder       ┆ 74     ┆ 160    ┆ 26.11 ┆ Outfielder  │
# │ 16    ┆ Erik_Bedard     ┆ BAL  ┆ Starting_Pitcher ┆ 73     ┆ 189    ┆ 27.99 ┆ Pitcher     │
# │ 19    ┆ Daniel_Cabrera  ┆ BAL  ┆ Starting_Pitcher ┆ 79     ┆ 230    ┆ 25.76 ┆ Pitcher     │
# │ 22    ┆ Kris_Benson     ┆ BAL  ┆ Starting_Pitcher ┆ 76     ┆ 195    ┆ 32.31 ┆ Pitcher     │
# │ …     ┆ …               ┆ …    ┆ …                ┆ …      ┆ …      ┆ …     ┆ …           │
# │ 1000  ┆ Anthony_Reyes   ┆ STL  ┆ Starting_Pitcher ┆ 74     ┆ 215    ┆ 25.37 ┆ Pitcher     │
# │ 1003  ┆ Chris_Carpenter ┆ STL  ┆ Starting_Pitcher ┆ 78     ┆ 230    ┆ 31.84 ┆ Pitcher     │
# │ 1006  ┆ Ricardo_Rincon  ┆ STL  ┆ Relief_Pitcher   ┆ 69     ┆ 190    ┆ 36.88 ┆ Pitcher     │
# │ 1009  ┆ Josh_Hancock    ┆ STL  ┆ Relief_Pitcher   ┆ 75     ┆ 205    ┆ 28.89 ┆ Pitcher     │
# │ 1012  ┆ Chris_Narveson  ┆ STL  ┆ Relief_Pitcher   ┆ 75     ┆ 205    ┆ 25.19 ┆ Pitcher     │
# └───────┴─────────────────┴──────┴──────────────────┴────────┴────────┴───────┴─────────────┘
