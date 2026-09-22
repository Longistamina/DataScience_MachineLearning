'''
To select tidypyrs TibbleFrame and TibbleLazy based on indices,
we can use `.slice(indices)` method.

Tidypyrs also provides `over` parameter to support slicing over groups.

1. `tl.gather(list_of_indices, over="group")`
2. `tl.gather(range(start, stop), over="group")`
3. `tl.gather(range(start, stop, step), over="group")`
4. `tl.gather_every(start=, step=, over="group")`

NOTE: Only provide `*args` inputs or `start-step` inputs, not both.
'''

from pathlib import Path

import tidypyrs as tp

# Optional display settings for tutorial output.
tp.Config.set_tbl_cols(10)
tp.Config.set_float_precision(2)

data_dir = Path("/home").rglob("*/DataScience_MachineLearning/data")
data_dir = next(data_dir)

tl_baseball = tp.scan_csv(
    source=data_dir/"baseball.csv",
    schema_overrides={
        "Team": tp.Categorical,
        "Position": tp.Categorical,
        "PosCategory": tp.Categorical,
    },
)

# =========================================================
# 1. `tl.gather(list_of_indices, over="group")`
# =========================================================

# Normal usage
print(
    tl_baseball
    .row_index()
    .slice([0, 10, 25, 300])
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

# Use with `over`
print(
    tl_baseball
    .row_index()
    .slice([0, 10], over="Team")
    .collect()
)
# shape: (60, 8)
# ┌───────┬─────────────────┬──────┬────────────┬────────┬────────┬───────┬─────────────┐
# │ index ┆ Name            ┆ Team ┆ Position   ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---   ┆ ---             ┆ ---  ┆ ---        ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ u32   ┆ str             ┆ cat  ┆ cat        ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞═══════╪═════════════════╪══════╪════════════╪════════╪════════╪═══════╪═════════════╡
# │ 0     ┆ Adam_Donachie   ┆ BAL  ┆ Catcher    ┆ 74     ┆ 180    ┆ 22.99 ┆ Catcher     │
# │ 10    ┆ Jeff_Fiorentino ┆ BAL  ┆ Outfielder ┆ 73     ┆ 188    ┆ 23.88 ┆ Outfielder  │
# │ 34    ┆ A.J._Pierzynski ┆ CWS  ┆ Catcher    ┆ 75     ┆ 245    ┆ 30.17 ┆ Catcher     │
# │ 44    ┆ Luis_Terrero    ┆ CWS  ┆ Outfielder ┆ 74     ┆ 206    ┆ 26.78 ┆ Outfielder  │
# │ 65    ┆ Jose_Molina     ┆ ANA  ┆ Catcher    ┆ 74     ┆ 220    ┆ 31.74 ┆ Catcher     │
# │ …     ┆ …               ┆ …    ┆ …          ┆ …      ┆ …      ┆ …     ┆ …           │
# │ 924   ┆ Xavier_Nady     ┆ PIT  ┆ Outfielder ┆ 74     ┆ 205    ┆ 28.29 ┆ Outfielder  │
# │ 949   ┆ Bengie_Molina   ┆ SF   ┆ Catcher    ┆ 71     ┆ 220    ┆ 32.61 ┆ Catcher     │
# │ 959   ┆ Dave_Roberts    ┆ SF   ┆ Outfielder ┆ 70     ┆ 180    ┆ 34.75 ┆ Outfielder  │
# │ 983   ┆ Gary_Bennett    ┆ STL  ┆ Catcher    ┆ 72     ┆ 208    ┆ 34.87 ┆ Catcher     │
# │ 993   ┆ So_Taguchi      ┆ STL  ┆ Outfielder ┆ 70     ┆ 163    ┆ 37.66 ┆ Outfielder  │
# └───────┴─────────────────┴──────┴────────────┴────────┴────────┴───────┴─────────────┘

# =========================================================
# 2. `tl.gather(range(start, stop), over="group")`
# =========================================================

# Normal usage
print(
    tl_baseball
    .row_index()
    .slice(range(5)) # means `range(0, 5)`, first 5 rows (index 0 -> 4)
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

# Use with over
print(
    tl_baseball
    .row_index()
    .slice(range(2, 5), over="Position") # index 2 -> 4, over "Position" groups
    .collect()
)
# shape: (24, 8)
# ┌───────┬─────────────────┬──────┬──────────────────┬────────┬────────┬───────┬─────────────┐
# │ index ┆ Name            ┆ Team ┆ Position         ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---   ┆ ---             ┆ ---  ┆ ---              ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ u32   ┆ str             ┆ cat  ┆ cat              ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞═══════╪═════════════════╪══════╪══════════════════╪════════╪════════╪═══════╪═════════════╡
# │ 2     ┆ Ramon_Hernandez ┆ BAL  ┆ Catcher          ┆ 72     ┆ 210    ┆ 30.78 ┆ Catcher     │
# │ 34    ┆ A.J._Pierzynski ┆ CWS  ┆ Catcher          ┆ 75     ┆ 245    ┆ 30.17 ┆ Catcher     │
# │ 35    ┆ Toby_Hall       ┆ CWS  ┆ Catcher          ┆ 75     ┆ 240    ┆ 31.36 ┆ Catcher     │
# │ 36    ┆ Paul_Konerko    ┆ CWS  ┆ First_Baseman    ┆ 74     ┆ 215    ┆ 30.99 ┆ Infielder   │
# │ 68    ┆ Casey_Kotchman  ┆ ANA  ┆ First_Baseman    ┆ 75     ┆ 210    ┆ 24.02 ┆ Infielder   │
# │ …     ┆ …               ┆ …    ┆ …                ┆ …      ┆ …      ┆ …     ┆ …           │
# │ 19    ┆ Daniel_Cabrera  ┆ BAL  ┆ Starting_Pitcher ┆ 79     ┆ 230    ┆ 25.76 ┆ Pitcher     │
# │ 20    ┆ Steve_Trachsel  ┆ BAL  ┆ Starting_Pitcher ┆ 76     ┆ 205    ┆ 36.33 ┆ Pitcher     │
# │ 25    ┆ Danys_Baez      ┆ BAL  ┆ Relief_Pitcher   ┆ 75     ┆ 225    ┆ 29.47 ┆ Pitcher     │
# │ 26    ┆ Chad_Bradford   ┆ BAL  ┆ Relief_Pitcher   ┆ 77     ┆ 203    ┆ 32.46 ┆ Pitcher     │
# │ 27    ┆ Jamie_Walker    ┆ BAL  ┆ Relief_Pitcher   ┆ 74     ┆ 195    ┆ 35.67 ┆ Pitcher     │
# └───────┴─────────────────┴──────┴──────────────────┴────────┴────────┴───────┴─────────────┘

# =========================================================
# 3. `tl.gather(range(start, stop, step), over="group")`
# =========================================================

# Normal usage
print(
    tl_baseball
    .row_index()
    .slice(range(0, 10, 2))
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

# Use with `over`
print(
    tl_baseball
    .row_index()
    .slice(range(3, 15, 4), over="Team")
    .collect()
)
# shape: (90, 8)
# ┌───────┬──────────────────┬──────┬────────────────┬────────┬────────┬───────┬─────────────┐
# │ index ┆ Name             ┆ Team ┆ Position       ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---   ┆ ---              ┆ ---  ┆ ---            ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ u32   ┆ str              ┆ cat  ┆ cat            ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞═══════╪══════════════════╪══════╪════════════════╪════════╪════════╪═══════╪═════════════╡
# │ 3     ┆ Kevin_Millar     ┆ BAL  ┆ First_Baseman  ┆ 72     ┆ 210    ┆ 35.43 ┆ Infielder   │
# │ 7     ┆ Melvin_Mora      ┆ BAL  ┆ Third_Baseman  ┆ 71     ┆ 200    ┆ 35.07 ┆ Infielder   │
# │ 11    ┆ Freddie_Bynum    ┆ BAL  ┆ Outfielder     ┆ 73     ┆ 180    ┆ 26.96 ┆ Outfielder  │
# │ 37    ┆ Tadahito_Iguchi  ┆ CWS  ┆ Second_Baseman ┆ 69     ┆ 185    ┆ 32.24 ┆ Infielder   │
# │ 41    ┆ Josh_Fields      ┆ CWS  ┆ Third_Baseman  ┆ 73     ┆ 215    ┆ 24.21 ┆ Infielder   │
# │ …     ┆ …                ┆ …    ┆ …              ┆ …      ┆ …      ┆ …     ┆ …           │
# │ 956   ┆ Rich_Aurilia     ┆ SF   ┆ Third_Baseman  ┆ 73     ┆ 189    ┆ 35.49 ┆ Infielder   │
# │ 960   ┆ Jason_Ellison    ┆ SF   ┆ Outfielder     ┆ 70     ┆ 180    ┆ 28.91 ┆ Outfielder  │
# │ 986   ┆ Albert_Pujols    ┆ STL  ┆ First_Baseman  ┆ 75     ┆ 225    ┆ 27.12 ┆ Infielder   │
# │ 990   ┆ Scott_Rolen      ┆ STL  ┆ Third_Baseman  ┆ 76     ┆ 240    ┆ 31.91 ┆ Infielder   │
# │ 994   ┆ Juan_Encarnacion ┆ STL  ┆ Outfielder     ┆ 75     ┆ 215    ┆ 30.98 ┆ Outfielder  │
# └───────┴──────────────────┴──────┴────────────────┴────────┴────────┴───────┴─────────────┘

# =========================================================
# 4. `tl.gather_every(start=, step=, over="group")`
# =========================================================
'''
This mirrors `gather_every()` in polars

It will slice from start index to the end,
with given step.

Use this when you want to slice till the end of the frame.

Something like `df[start::step]`
'''

# Normal usage
print(
    tl_baseball
    .row_index()
    .slice(start=3, step=10) # Starts at index=3, slice to the end, with step=10
    .collect()
)
# shape: (102, 8)
# ┌───────┬───────────────────┬──────┬──────────────────┬────────┬────────┬───────┬─────────────┐
# │ index ┆ Name              ┆ Team ┆ Position         ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---   ┆ ---               ┆ ---  ┆ ---              ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ u32   ┆ str               ┆ cat  ┆ cat              ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞═══════╪═══════════════════╪══════╪══════════════════╪════════╪════════╪═══════╪═════════════╡
# │ 3     ┆ Kevin_Millar      ┆ BAL  ┆ First_Baseman    ┆ 72     ┆ 210    ┆ 35.43 ┆ Infielder   │
# │ 13    ┆ Brandon_Fahey     ┆ BAL  ┆ Outfielder       ┆ 74     ┆ 160    ┆ 26.11 ┆ Outfielder  │
# │ 23    ┆ Scott_Williamson  ┆ BAL  ┆ Relief_Pitcher   ┆ 72     ┆ 180    ┆ 31.03 ┆ Pitcher     │
# │ 33    ┆ Jeremy_Guthrie    ┆ BAL  ┆ Relief_Pitcher   ┆ 73     ┆ 200    ┆ 27.90 ┆ Pitcher     │
# │ 43    ┆ Brian_N._Anderson ┆ CWS  ┆ Outfielder       ┆ 74     ┆ 205    ┆ 24.97 ┆ Outfielder  │
# │ …     ┆ …                 ┆ …    ┆ …                ┆ …      ┆ …      ┆ …     ┆ …           │
# │ 973   ┆ Kevin_Correia     ┆ SF   ┆ Relief_Pitcher   ┆ 75     ┆ 200    ┆ 26.52 ┆ Pitcher     │
# │ 983   ┆ Gary_Bennett      ┆ STL  ┆ Catcher          ┆ 72     ┆ 208    ┆ 34.87 ┆ Catcher     │
# │ 993   ┆ So_Taguchi        ┆ STL  ┆ Outfielder       ┆ 70     ┆ 163    ┆ 37.66 ┆ Outfielder  │
# │ 1003  ┆ Chris_Carpenter   ┆ STL  ┆ Starting_Pitcher ┆ 78     ┆ 230    ┆ 31.84 ┆ Pitcher     │
# │ 1013  ┆ Randy_Keisler     ┆ STL  ┆ Relief_Pitcher   ┆ 75     ┆ 190    ┆ 31.01 ┆ Pitcher     │
# └───────┴───────────────────┴──────┴──────────────────┴────────┴────────┴───────┴─────────────┘

# Use with `over`
print(
    tl_baseball
    .row_index()
    .slice(start=2, step=10, over="Team") # Starts at index=2, slice to the end, with step=10, over "Team" groups
    .collect()
)
# shape: (111, 8)
# ┌───────┬────────────────────┬──────┬──────────────────┬────────┬────────┬───────┬─────────────┐
# │ index ┆ Name               ┆ Team ┆ Position         ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---   ┆ ---                ┆ ---  ┆ ---              ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ u32   ┆ str                ┆ cat  ┆ cat              ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞═══════╪════════════════════╪══════╪══════════════════╪════════╪════════╪═══════╪═════════════╡
# │ 2     ┆ Ramon_Hernandez    ┆ BAL  ┆ Catcher          ┆ 72     ┆ 210    ┆ 30.78 ┆ Catcher     │
# │ 12    ┆ Nick_Markakis      ┆ BAL  ┆ Outfielder       ┆ 74     ┆ 185    ┆ 23.29 ┆ Outfielder  │
# │ 22    ┆ Kris_Benson        ┆ BAL  ┆ Starting_Pitcher ┆ 76     ┆ 195    ┆ 32.31 ┆ Pitcher     │
# │ 32    ┆ Chris_Ray          ┆ BAL  ┆ Relief_Pitcher   ┆ 75     ┆ 200    ┆ 25.13 ┆ Pitcher     │
# │ 36    ┆ Paul_Konerko       ┆ CWS  ┆ First_Baseman    ┆ 74     ┆ 215    ┆ 30.99 ┆ Infielder   │
# │ …     ┆ …                  ┆ …    ┆ …                ┆ …      ┆ …      ┆ …     ┆ …           │
# │ 971   ┆ Barry_Zito         ┆ SF   ┆ Starting_Pitcher ┆ 76     ┆ 215    ┆ 28.80 ┆ Pitcher     │
# │ 981   ┆ Billy_Sadler       ┆ SF   ┆ Relief_Pitcher   ┆ 72     ┆ 190    ┆ 25.44 ┆ Pitcher     │
# │ 985   ┆ John_Nelson        ┆ STL  ┆ First_Baseman    ┆ 73     ┆ 190    ┆ 27.99 ┆ Infielder   │
# │ 995   ┆ Skip_Schumaker     ┆ STL  ┆ Outfielder       ┆ 70     ┆ 175    ┆ 27.07 ┆ Outfielder  │
# │ 1005  ┆ Jason_Isringhausen ┆ STL  ┆ Relief_Pitcher   ┆ 75     ┆ 230    ┆ 34.48 ┆ Pitcher     │
# └───────┴────────────────────┴──────┴──────────────────┴────────┴────────┴───────┴─────────────┘
