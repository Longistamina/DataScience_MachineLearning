'''
Random sampling rows and values in Polars.

This file is adapted from the pandas workflow:

1. df.sample(n=..., random_state=...)
2. df.sample(frac=..., random_state=...)

Main Polars translation:

+ pandas random_state=...  -> Polars seed=...
+ pandas frac=...          -> Polars fraction=...
+ pandas replace=True      -> Polars with_replacement=True
+ pandas df.sample(...)    -> Polars df.sample(...)

Content flow:
1. DataFrame.sample(n=..., seed=...)
2. DataFrame.sample(fraction=..., seed=...)
3. Sampling with replacement / oversampling
4. Shuffling all rows
5. Expression sampling with pl.col(...).sample(...)
6. Group-wise sampling
7. LazyFrame sampling patterns
8. Quick pandas-to-Polars summary

Important:
+ In Polars, n and fraction cannot be used together.
+ If neither n nor fraction is provided, Polars samples 1 row/value by default.
+ Use seed=... for reproducible examples.
+ Use shuffle=True when you want the sampled output itself to be shuffled.
'''

from pathlib import Path
import polars as pl

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(10)
pl.Config.set_float_precision(2)


data_dir = Path("/home").rglob("*/DataScience_MachineLearning/data")
data_dir = next(data_dir)


df_baseball = pl.read_csv(
    source=data_dir / "baseball.csv",
    schema_overrides={
        "Team": pl.Categorical,
        "Position": pl.Categorical,
        "PosCategory": pl.Categorical,
    },
)

print(df_baseball.glimpse(return_type="string"))
# Rows: 1015
# Columns: 7
# $ Name        <str> Adam_Donachie, Paul_Bako, Ramon_Hernandez, Kevin_Millar, Chris_Gomez, ...
# $ Team        <cat> BAL, BAL, BAL, BAL, BAL, ...
# $ Position    <cat> Catcher, Catcher, Catcher, First_Baseman, First_Baseman, ...
# $ Height      <i64> 74, 74, 72, 72, 73, ...
# $ Weight      <i64> 180, 215, 210, 210, 188, ...
# $ Age         <f64> 22.99, 34.69, 30.78, 35.43, 35.71, ...
# $ PosCategory <cat> Catcher, Catcher, Catcher, Infielder, Infielder, ...

print(df_baseball.shape)   # (1015, 7)
print(df_baseball.schema)
# Schema({'Name': String, 'Team': Categorical, 'Position': Categorical,
#         'Height': Int64, 'Weight': Int64, 'Age': Float64, 'PosCategory': Categorical})


# =========================================================================================
# 1. df.sample(n=..., seed=...)
# =========================================================================================
'''
The n=... argument specifies the number of rows to return.

Pandas:
    df.sample(n=5, random_state=42)

Polars:
    df.sample(n=5, seed=42)

seed=... is the Polars equivalent of pandas random_state=... for reproducibility.
'''

# Sample exactly 5 rows.
df_sample_n = df_baseball.sample(n=5, seed=42)
print(df_sample_n)
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

# You can also make the output order explicitly shuffled.
df_sample_n_shuffle = df_baseball.sample(n=5, seed=42, shuffle=True)
print(df_sample_n_shuffle)
# shape: (5, 7)

'''
What does shuffle=True mean?

Sampling is already random.
The shuffle= argument controls the order of the returned sampled rows.

+ shuffle=False is the default.
+ shuffle=True makes the sampled output order shuffled.

For teaching examples, it is often clearer to use shuffle=True.
'''

# If you omit n and fraction, Polars samples 1 row by default.
df_sample_one = df_baseball.sample(seed=42)
print(df_sample_one)
# shape: (1, 7)
# ┌────────────────┬──────┬────────────┬────────┬────────┬───────┬─────────────┐
# │ Name           ┆ Team ┆ Position   ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---            ┆ ---  ┆ ---        ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ str            ┆ cat  ┆ cat        ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞════════════════╪══════╪════════════╪════════╪════════╪═══════╪═════════════╡
# │ Tony_Gwynn_Jr. ┆ MLW  ┆ Outfielder ┆ 72     ┆ 185    ┆ 24.41 ┆ Outfielder  │
# └────────────────┴──────┴────────────┴────────┴────────┴───────┴─────────────┘


# =========================================================================================
# 2. df.sample(fraction=..., seed=...)
# =========================================================================================
'''
The fraction=... argument specifies the fraction of rows to return.

Pandas:
    df.sample(frac=0.01, random_state=40)

Polars:
    df.sample(fraction=0.01, seed=40)

Important naming difference:
+ pandas uses frac=
+ Polars uses fraction=
'''

# Sample about 1% of the rows.
df_sample_fraction = df_baseball.sample(fraction=0.01, seed=40, shuffle=True)
print(df_sample_fraction)
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

# Confirm the number of sampled rows.
print(df_sample_fraction.height)
# 10 - Around 1% of 1015 rows.

# Sample 25% of the rows.
df_sample_25_percent = df_baseball.sample(fraction=0.25, seed=123, shuffle=True)
print(df_sample_25_percent.shape)
# Around (253, 7)

'''
Cannot use n and fraction together.

The following would raise an error:

    df_baseball.sample(n=5, fraction=0.01, seed=42)

Choose either:
+ n=... for an exact count
+ fraction=... for a proportion
'''


# =========================================================================================
# 3. Sampling with replacement / oversampling
# =========================================================================================
'''
By default, Polars samples WITHOUT replacement.
This means the same row is not selected more than once.

If you want repeated rows to be possible, use:
    with_replacement=True

Pandas:
    df.sample(n=1200, replace=True, random_state=42)

Polars:
    df.sample(n=1200, with_replacement=True, seed=42)
'''

# Sample more rows than the original DataFrame size.
# This requires with_replacement=True.
df_sample_replacement_n = df_baseball.sample(
    n=1200,
    with_replacement=True,
    seed=42,
    shuffle=True,
)
print(df_sample_replacement_n.shape)
# (1200, 7)

# Oversample by fraction.
# For fraction > 1, use with_replacement=True.
df_sample_replacement_fraction = df_baseball.sample(
    fraction=1.10,
    with_replacement=True,
    seed=42,
    shuffle=True,
)
print(df_sample_replacement_fraction.shape)
# (1116, 7) - More rows than df_baseball.


# =========================================================================================
# 4. Shuffling all rows
# =========================================================================================
'''
A very common pandas pattern is shuffling all rows:

Pandas:
    df.sample(frac=1)

Polars:
    df.sample(fraction=1.0, shuffle=True)

This returns all rows but in random order.
'''

# Shuffle all rows.
df_shuffled = df_baseball.sample(fraction=1.0, shuffle=True)
print(df_shuffled.head(5))
# shape: (5, 7)
# First 5 rows after shuffling.

##----------------------------------------------------------##

# Example: simple train/test split after shuffling.
split_at = int(df_baseball.height * 0.80)

train = df_shuffled.slice(0, split_at)
test = df_shuffled.slice(split_at)

print(train.shape)
# Around (812, 7)

print(test.shape)
# Around (203, 7)


# =========================================================================================
# 5. Expression sampling with pl.col().sample()
# =========================================================================================

'''
Polars expressions also support .sample(...):

    pl.col("Age").sample(n=5, seed=42)

This samples values from a column expression.

Important warning:
+ df.sample(...) samples full rows and keeps row values together.
+ pl.col("some_col").sample(...) samples values from that one column expression.
+ If you sample multiple columns independently, you can break the original row relationship.

So, for normal row sampling, prefer df.sample(...).
'''

# Sample values from one column expression.
df_age_expr_sample = df_baseball.select(
    pl.col("Age").sample(n=5, seed=42).alias("sampled_age")
)
print(df_age_expr_sample)
# shape: (5, 1)
# column: sampled_age

# Sample with replacement from one expression.
df_age_expr_sample_replace = df_baseball.select(
    pl.col("Age").sample(
        fraction=1.0,
        with_replacement=True,
        seed=1,
    ).alias("sampled_age")
)
print(df_age_expr_sample_replace.head(10))
# shape: (10, 1)

# Do NOT do this if you need original row relationships preserved.
df_independent_column_samples = df_baseball.select(
    pl.col("Name").sample(n=5, seed=1).alias("sampled_name"),
    pl.col("Age").sample(n=5, seed=2).alias("sampled_age"),
)
print(df_independent_column_samples)
# The sampled_name and sampled_age columns were sampled independently.
# They should not be interpreted as original player-name/player-age pairs.


# =========================================================================================
# 7. Group-wise sampling
# =========================================================================================
'''
Sometimes you want to sample rows inside each group.

Example:
+ sample 2 players from each PosCategory
+ sample 10% of players from each PosCategory

Polars has two common approaches:

1. map_groups(...)
   + intuitive
   + easy to read
   + slower because it uses a Python function per group

2. expression-based random rank per group
   + more Polars-native
   + better for larger data
'''

##-------------------------------------##
## Approach A: group_by().map_groups() ##
##-------------------------------------##

# Simple and readable: sample 2 rows from each PosCategory.
df_group_sample_map = (
    df_baseball
    .group_by("PosCategory")
    .map_groups(lambda group_df: group_df.sample(n=2, seed=42, shuffle=True))
)
print(df_group_sample_map)
# shape: number_of_groups * 2 rows

##-------------------------------------------##
## Approach B: random rank inside each group ##
##-------------------------------------------##
'''
This expression creates a random row rank inside each PosCategory group:

    pl.int_range(pl.len()).shuffle(seed=42).over("PosCategory")

Then we keep rows whose random rank is less than 2.
This gives 2 random rows per PosCategory without a Python UDF.
'''

df_group_sample_expr = df_baseball.filter(
    pl.int_range(pl.len()).shuffle(seed=42).over("PosCategory") < 2
)
print(df_group_sample_expr)
# shape: number_of_groups * 2 rows

# Sample approximately 10% from each PosCategory.
df_group_sample_fraction = df_baseball.filter(
    pl.int_range(pl.len()).shuffle(seed=40).over("PosCategory")
    < (pl.len().over("PosCategory") * 0.10).ceil()
)
print(df_group_sample_fraction)
# Around 10% of each PosCategory group.


# =========================================================================================
# 8. LazyFrame sampling patterns
# =========================================================================================
'''
Current Polars has DataFrame.sample(), Series.sample(), and Expr.sample().
LazyFrame does not have the same direct lf.sample(...) row-sampling method.

Common options:

1. Collect first, then sample eagerly:

       lf.collect().sample(n=5, seed=42)

   This is easy, but it materializes the LazyFrame first.

2. Stay lazy by creating a random row-rank expression and filtering it:

       lf.with_columns(
           pl.int_range(pl.len()).shuffle(seed=42).alias("__random_rank")
       ).filter(
           pl.col("__random_rank") < 5
       ).drop("__random_rank")

   This keeps the code in LazyFrame form until collect().
'''

lf_baseball = df_baseball.lazy()

# Easy method: collect first, then sample eagerly.
df_lazy_collected_sample = lf_baseball.collect().sample(n=5, seed=42, shuffle=True)
print(df_lazy_collected_sample)
# shape: (5, 7)

# Lazy row sampling by n using a temporary random rank column.
lf_sample_n = (
    lf_baseball
    .with_columns(
        pl.int_range(pl.len()).shuffle(seed=42).alias("__random_rank")
    )
    .filter(pl.col("__random_rank") < 5)
    .drop("__random_rank")
)
print(lf_sample_n.collect())
# shape: (5, 7)

# Lazy row sampling by approximate fraction.
# Here we keep rows whose random rank is below 1% of the total row count.
lf_sample_fraction = (
    lf_baseball
    .with_columns(
        pl.int_range(pl.len()).shuffle(seed=40).alias("__random_rank")
    )
    .filter(pl.col("__random_rank") < (pl.len() * 0.01).ceil())
    .drop("__random_rank")
)
print(lf_sample_fraction.collect())
# Around 1% of the rows.

# Lazy group-wise sample: 2 rows per PosCategory.
lf_group_sample = lf_baseball.filter(
    pl.int_range(pl.len()).shuffle(seed=42).over("PosCategory") < 2
)
print(lf_group_sample.collect())
# shape: number_of_groups * 2 rows


# =========================================================================================
# 9. Quick pandas-to-Polars summary
# =========================================================================================
'''
Pandas vs Polars sampling summary

1. Sample n rows

   pandas:
       df.sample(n=5, random_state=42)

   Polars:
       df.sample(n=5, seed=42)

2. Sample a fraction of rows

   pandas:
       df.sample(frac=0.01, random_state=42)

   Polars:
       df.sample(fraction=0.01, seed=42)

3. Sample with replacement

   pandas:
       df.sample(n=1200, replace=True, random_state=42)

   Polars:
       df.sample(n=1200, with_replacement=True, seed=42)

4. Shuffle all rows

   pandas:
       df.sample(frac=1, random_state=42)

   Polars:
       df.sample(fraction=1.0, shuffle=True, seed=42)

5. Series sampling

   pandas:
       s.sample(n=5, random_state=42)

   Polars:
       s.sample(n=5, seed=42)

6. Expression sampling

   Polars only:
       df.select(pl.col("Age").sample(n=5, seed=42))

   Remember:
       This samples column values, not whole DataFrame rows.

7. Group-wise row sampling

   Simple but slower:
       df.group_by("group").map_groups(lambda g: g.sample(n=2, seed=42))

   More Polars-native:
       df.filter(pl.int_range(pl.len()).shuffle(seed=42).over("group") < 2)
'''
