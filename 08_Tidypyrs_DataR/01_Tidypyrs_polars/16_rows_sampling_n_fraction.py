'''
Random sampling rows and values in Polars.

Content flow:
1. `tl.select(f.all().sample(n=..., seed=...))`
2. `tl.select(f.all().sample(fraction=..., seed=...))`
3. Sampling `with_replacement` / oversampling
4. Sampling within specified columns: `tp.col().sample()`
5. Sampling `over` group
6. `df.sample()` for DataFrame
'''

from pathlib import Path

import tidypyrs as tp
from tidypyrs import f

# Optional display settings for tutorial output.
tp.Config.set_tbl_rows(12)
tp.Config.set_tbl_cols(10)
tp.Config.set_float_precision(2)

data_dir = Path("/home").rglob("*/DataScience_MachineLearning/data")
data_dir = next(data_dir)

tl_baseball = tp.scan_csv(
    source=data_dir / "baseball.csv",
    schema_overrides={
        "Team": tp.Categorical,
        "Position": tp.Categorical,
        "PosCategory": tp.Categorical,
    },
)

print(tl_baseball.collect().glimpse(return_type="string"))
# Rows: 1015
# Columns: 7
# $ Name        <str> Adam_Donachie, Paul_Bako, Ramon_Hernandez, Kevin_Millar, Chris_Gomez, ...
# $ Team        <cat> BAL, BAL, BAL, BAL, BAL, ...
# $ Position    <cat> Catcher, Catcher, Catcher, First_Baseman, First_Baseman, ...
# $ Height      <i64> 74, 74, 72, 72, 73, ...
# $ Weight      <i64> 180, 215, 210, 210, 188, ...
# $ Age         <f64> 22.99, 34.69, 30.78, 35.43, 35.71, ...
# $ PosCategory <cat> Catcher, Catcher, Catcher, Infielder, Infielder, ...

# =========================================================================================
# 1. `tl.select(f.all().sample(n=..., seed=...))`
# =========================================================================================
'''
`n` argument specifies the number of rows to return.
`seed` is for reproducibility.
'''

# Sample exactly 5 rows.
print(
    tl_baseball
    .select(f.all().sample(n=5, seed=42))
    .collect()
)
# shape: (5, 7)
# ┌───────────────────┬──────┬──────────────────┬────────┬────────┬───────┬─────────────┐
# │ Name              ┆ Team ┆ Position         ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---               ┆ ---  ┆ ---              ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ str               ┆ cat  ┆ cat              ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞═══════════════════╪══════╪══════════════════╪════════╪════════╪═══════╪═════════════╡
# │ Jae_Seo           ┆ TB   ┆ Starting_Pitcher ┆ 73     ┆ 215    ┆ 29.77 ┆ Pitcher     │
# │ Humberto_Quintero ┆ HOU  ┆ Catcher          ┆ 73     ┆ 190    ┆ 27.56 ┆ Catcher     │
# │ Brian_Sanches     ┆ PHI  ┆ Relief_Pitcher   ┆ 72     ┆ 190    ┆ 28.56 ┆ Pitcher     │
# │ Kevin_Mench       ┆ MLW  ┆ Outfielder       ┆ 72     ┆ 225    ┆ 29.14 ┆ Outfielder  │
# │ John_Rodriguez    ┆ STL  ┆ Outfielder       ┆ 72     ┆ 205    ┆ 29.11 ┆ Outfielder  │
# └───────────────────┴──────┴──────────────────┴────────┴────────┴───────┴─────────────┘

# If you omit n and fraction, Polars samples 1 row by default.
print(
    tl_baseball
    .select(f.all().sample(seed=42))
    .collect()
)
# shape: (1, 7)
# ┌────────────────┬──────┬────────────┬────────┬────────┬───────┬─────────────┐
# │ Name           ┆ Team ┆ Position   ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---            ┆ ---  ┆ ---        ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ str            ┆ cat  ┆ cat        ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞════════════════╪══════╪════════════╪════════╪════════╪═══════╪═════════════╡
# │ Tony_Gwynn_Jr. ┆ MLW  ┆ Outfielder ┆ 72     ┆ 185    ┆ 24.41 ┆ Outfielder  │
# └────────────────┴──────┴────────────┴────────┴────────┴───────┴─────────────┘

# =========================================================================================
# 2. `tl.select(f.all().sample(fraction=..., seed=...))`
# =========================================================================================
'''
`fraction` argument specifies the fraction of rows to return.
'''

# Sample about 1% of the rows.
print(
    tl_baseball
    .select(f.all().sample(fraction=0.01))
    .collect()
)
# shape: around (10, 7) for a 1015-row DataFrame
# shape: (10, 7)
# ┌────────────────────┬──────┬──────────────────┬────────┬────────┬───────┬─────────────┐
# │ Name               ┆ Team ┆ Position         ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---                ┆ ---  ┆ ---              ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ str                ┆ cat  ┆ cat              ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞════════════════════╪══════╪══════════════════╪════════╪════════╪═══════╪═════════════╡
# │ Jason_Tyner        ┆ MIN  ┆ Outfielder       ┆ 73     ┆ 160    ┆ 29.85 ┆ Outfielder  │
# │ Mark_Kiger         ┆ OAK  ┆ Shortstop        ┆ 71     ┆ 180    ┆ 26.75 ┆ Infielder   │
# │ Scott_Eyre         ┆ CHC  ┆ Relief_Pitcher   ┆ 73     ┆ 210    ┆ 34.75 ┆ Pitcher     │
# │ Ervin_Santana      ┆ ANA  ┆ Starting_Pitcher ┆ 74     ┆ 160    ┆ 24.14 ┆ Pitcher     │
# │ Michael_Barrett    ┆ CHC  ┆ Catcher          ┆ 75     ┆ 210    ┆ 30.35 ┆ Catcher     │
# │ Franklin_Gutierrez ┆ CLE  ┆ Outfielder       ┆ 74     ┆ 175    ┆ 24.02 ┆ Outfielder  │
# │ Nelson_Cruz        ┆ TEX  ┆ Outfielder       ┆ 75     ┆ 175    ┆ 26.66 ┆ Outfielder  │
# │ Miguel_Olivo       ┆ FLA  ┆ Catcher          ┆ 72     ┆ 215    ┆ 28.63 ┆ Catcher     │
# │ Adam_Jones         ┆ SEA  ┆ Outfielder       ┆ 74     ┆ 200    ┆ 21.58 ┆ Outfielder  │
# │ Ramon_Ramirez      ┆ COL  ┆ Relief_Pitcher   ┆ 71     ┆ 190    ┆ 25.50 ┆ Pitcher     │
# └────────────────────┴──────┴──────────────────┴────────┴────────┴───────┴─────────────┘

'''
Cannot use n and fraction together.

The following would raise an error:

    `.sample(n=5, fraction=0.01, seed=42)`

Choose either:
+ `n=...` for an exact count
+ `fraction=...` for a proportion
'''

# =========================================================================================
# 3. Sampling `with_replacement` / oversampling
# =========================================================================================
'''
By default, Polars samples WITHOUT replacement.
This means the same row is not selected more than once.

If you want repeated rows to be possible, use:
    `with_replacement=True`
'''

# Sample more rows than the original DataFrame size.
# This requires with_replacement=True.
print(
    tl_baseball
    .select(f.all().sample(n=1200, with_replacement=True))
    .collect()
)
# (1200, 7)

# Oversample by fraction.
# For fraction > 1, use with_replacement=True.
print(
    tl_baseball
    .select(f.all().sample(fraction=1.10, with_replacement=True))
    .collect()
)
# (1116, 7) - More rows than df_baseball.

# =========================================================================================
# 4. Sampling within specified columns: `f("col").sample()`
# =========================================================================================
'''
Polars expressions also support .sample(...):

    `f("Age").sample(n=5, seed=42)`

This samples values from a column expression.

Important warning:
+ `f.all().sample(...)` samples full rows and keeps row values together.
+ `f("some_col").sample(...)` samples values from that one column expression.
+ If you sample multiple columns independently, you can break the original row relationship.

So, for normal row sampling, prefer df.sample(...).
'''

# Sample values from one column expression.
print(
    tl_baseball
    .select(
        f("Age").sample(n=5, seed=42).alias("sampled_age")
    )
    .collect()
)
# shape: (5, 1)
# column: sampled_age

# Sample with replacement from one expression.
print(
    tl_baseball
    .select(
        f("Age").sample(
            fraction=1.0,
            with_replacement=True,
            seed=1,
        ).alias("sampled_age")
    )
    .head(10)
    .collect()
)
# shape: (10, 1)

# Do NOT do this if you need original row relationships preserved.
print(
    tl_baseball
    .select(
        f("Name").sample(n=5, seed=1).alias("sampled_name"),
        f("Age").sample(n=5, seed=2).alias("sampled_age"),
    )
    .collect()
)
# The sampled_name and sampled_age columns were sampled independently.
# They should not be interpreted as original player-name/player-age pairs.

# =========================================================================================
# 5. Sampling `over` group
# =========================================================================================
'''
Sometimes you want to sample rows inside each group.

Example:
+ sample 2 players from each PosCategory
+ sample 10% of players from each PosCategory

Polars has two common approaches:

A. `.group_by().map_groups(...)`
   + intuitive
   + easy to read
   + slower because it uses a Python function per group
   + for LazyFrame, must provide schema

B. `f.all().sample().over("group", mapping_strategy="explode")`
   + more Polars-native
   + better for larger data
'''

##------------------------------##
## A. `group_by().map_groups()` ##
##------------------------------##

# Simple and readable: sample 2 rows from each PosCategory.
print(
    tl_baseball
    .group_by("PosCategory")
    .map_groups(
        lambda group_df: group_df.sample(n=2, seed=42, shuffle=True),
        schema=f.schema
    )
    .collect()
)
# shape: (8, 7)
# ┌────────────────┬──────┬────────────────┬────────┬────────┬───────┬─────────────┐
# │ Name           ┆ Team ┆ Position       ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---            ┆ ---  ┆ ---            ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ str            ┆ cat  ┆ cat            ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞════════════════╪══════╪════════════════╪════════╪════════╪═══════╪═════════════╡
# │ Prince_Fielder ┆ MLW  ┆ First_Baseman  ┆ 72     ┆ 260    ┆ 22.81 ┆ Infielder   │
# │ Jorge_Cantu    ┆ TB   ┆ Second_Baseman ┆ 73     ┆ 184    ┆ 25.08 ┆ Infielder   │
# │ Brian_Shouse   ┆ MLW  ┆ Relief_Pitcher ┆ 71     ┆ 190    ┆ 38.43 ┆ Pitcher     │
# │ Ruddy_Lugo     ┆ TB   ┆ Relief_Pitcher ┆ 70     ┆ 205    ┆ 26.77 ┆ Pitcher     │
# │ Chris_Coste    ┆ PHI  ┆ Catcher        ┆ 73     ┆ 200    ┆ 34.07 ┆ Catcher     │
# │ Shawn_Riggans  ┆ TB   ┆ Catcher        ┆ 74     ┆ 190    ┆ 26.60 ┆ Catcher     │
# │ Gabe_Gross     ┆ MLW  ┆ Outfielder     ┆ 75     ┆ 209    ┆ 27.36 ┆ Outfielder  │
# │ Carl_Crawford  ┆ TB   ┆ Outfielder     ┆ 74     ┆ 219    ┆ 25.57 ┆ Outfielder  │
# └────────────────┴──────┴────────────────┴────────┴────────┴───────┴─────────────┘

##------------------------------------------------------------------##
## B. `f.all().sample().over("group", mapping_strategy="explode")` ##
##------------------------------------------------------------------##

print(
    tl_baseball
    .select(
        f.all().sample(fraction=0.1).over("Team", mapping_strategy="explode")
    )
    .collect()
)
# shape: (89, 7)
# ┌────────────────┬──────┬──────────────────┬────────┬────────┬───────┬─────────────┐
# │ Name           ┆ Team ┆ Position         ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---            ┆ ---  ┆ ---              ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ str            ┆ cat  ┆ cat              ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞════════════════╪══════╪══════════════════╪════════╪════════╪═══════╪═════════════╡
# │ Adam_Loewen    ┆ BAL  ┆ Relief_Pitcher   ┆ 73     ┆ 189    ┆ 25.89 ┆ Outfielder  │
# │ Kris_Benson    ┆ BAL  ┆ Starting_Pitcher ┆ 71     ┆ 230    ┆ 22.89 ┆ Pitcher     │
# │ Hayden_Penn    ┆ BAL  ┆ Relief_Pitcher   ┆ 69     ┆ 180    ┆ 36.33 ┆ Outfielder  │
# │ Juan_Uribe     ┆ CWS  ┆ Catcher          ┆ 77     ┆ 200    ┆ 31.36 ┆ Infielder   │
# │ Ryan_Sweeney   ┆ CWS  ┆ Relief_Pitcher   ┆ 78     ┆ 195    ┆ 24.09 ┆ Infielder   │
# │ Charlie_Haeger ┆ CWS  ┆ Catcher          ┆ 77     ┆ 190    ┆ 26.78 ┆ Infielder   │
# │ …              ┆ …    ┆ …                ┆ …      ┆ …      ┆ …     ┆ …           │
# │ Scott_Munter   ┆ SF   ┆ Starting_Pitcher ┆ 74     ┆ 205    ┆ 22.41 ┆ Pitcher     │
# │ Matt_Cain      ┆ SF   ┆ Relief_Pitcher   ┆ 74     ┆ 210    ┆ 28.86 ┆ Infielder   │
# │ Steve_Kline    ┆ SF   ┆ Outfielder       ┆ 70     ┆ 197    ┆ 35.25 ┆ Pitcher     │
# │ Scott_Rolen    ┆ STL  ┆ Relief_Pitcher   ┆ 75     ┆ 205    ┆ 31.01 ┆ Outfielder  │
# │ Randy_Keisler  ┆ STL  ┆ Relief_Pitcher   ┆ 75     ┆ 212    ┆ 31.14 ┆ Infielder   │
# │ Albert_Pujols  ┆ STL  ┆ Outfielder       ┆ 79     ┆ 240    ┆ 25.19 ┆ Outfielder  │
# └────────────────┴──────┴──────────────────┴────────┴────────┴───────┴─────────────┘
