'''
Random sampling values from a Polars Series.

This file is the Polars Series version of the pandas Series sampling workflow:

pandas:
    s.sample(n=..., random_state=...)
    s.sample(frac=..., random_state=...)

Polars:
    s.sample(n=..., seed=...)
    s.sample(fraction=..., seed=...)

Main Polars translation:
+ pandas random_state=...  -> Polars seed=...
+ pandas frac=...          -> Polars fraction=...
+ pandas replace=True      -> Polars with_replacement=True
+ pandas Series index      -> Polars has no custom index labels

Content flow:
1. Create example Series
2. s.sample(n=..., seed=...)
3. s.sample(fraction=..., seed=...)
4. Sampling with replacement / oversampling
5. Shuffle all values with fraction=1.0 and shuffle=True
6. Series sampling vs DataFrame row sampling
7. Expression sampling with pl.col(...).sample(...)
8. What pandas Series.sample features do not translate directly
9. Quick pandas-to-Polars summary

Important:
+ n and fraction cannot be used together.
+ If neither n nor fraction is provided, Polars samples 1 value by default.
+ seed=... makes examples reproducible.
+ with_replacement=True allows the same value to be sampled more than once.
+ shuffle=True controls the order of sampled data points in the returned Series.
+ Series.sample(...) returns another Series.
'''

import polars as pl

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(8)
pl.Config.set_float_precision(2)


# =========================================================================================
# 1. Create example Series
# =========================================================================================
'''
A Polars Series is one-dimensional and has a name and dtype.

Unlike pandas, Polars Series do NOT have custom index labels.
Values are position-based: row 0, row 1, row 2, and so on.

When you sample from a Polars Series:
+ the sampled values come from that one Series
+ there are no custom index labels to preserve
+ the returned object is still a Polars Series
'''

s_players = pl.Series(
    "player",
    ["Adam", "Paul", "Ramon", "Kevin", "Chris", "Brian", "Nick", "Miguel", "Wilson", "Mark"],
)

s_age = pl.Series(
    "age",
    [22.99, 34.69, 30.78, 35.43, 35.71, 29.39, 30.77, 32.82, 26.59, 32.01],
)

s_position = pl.Series(
    "position",
    ["Catcher", "Catcher", "Catcher", "Infielder", "Infielder", "Pitcher", "Pitcher", "Infielder", "Infielder", "Outfielder"],
)

print(s_players)
# shape: (10,)
# Series: 'player' [str]
# [
#     "Adam"
#     "Paul"
#     "Ramon"
#     ...
# ]

print(s_age)
# shape: (10,)
# Series: 'age' [f64]
# [
#     22.99
#     34.69
#     30.78
#     ...
# ]

print(s_players.name)   # player
print(s_players.dtype)  # String
print(len(s_players))   # 10


# =========================================================================================
# 2. s.sample(n=..., seed=...)
# =========================================================================================
'''
The n=... argument specifies the exact number of values to return.

seed=... is the Polars equivalent of pandas random_state=... for reproducibility.

pandas:
    s.sample(n=3, random_state=42)

Polars:
    s.sample(n=3, seed=42)
'''

s_sample_n = s_players.sample(n=3, seed=42)
print(s_sample_n)
# shape: (3,)
# Series: 'player' [str]
# The exact values are reproducible for the same Polars version and seed.

# Sample numeric values from another Series.
s_age_sample = s_age.sample(n=4, seed=10)
print(s_age_sample)
# shape: (4,)
# Series: 'age' [f64]

# If you omit both n and fraction, Polars samples 1 value by default.
s_sample_one = s_players.sample(seed=42)
print(s_sample_one)
# shape: (1,)
# Series: 'player' [str]


# =========================================================================================
# 3. s.sample(fraction=..., seed=...)
# =========================================================================================
'''
The fraction=... argument specifies the fraction/proportion of values to return.

Examples:
+ fraction=0.30 means sample 30% of the values
+ fraction=1.00 means sample 100% of the values
+ fraction > 1 means oversampling, and requires with_replacement=True

Important naming difference:
+ pandas uses frac=
+ Polars uses fraction=
'''

s_sample_fraction = s_players.sample(fraction=0.30, seed=40)
print(s_sample_fraction)
# shape: (3,)
# Series: 'player' [str]

print(len(s_sample_fraction))
# 3

'''
Cannot use n and fraction together.

The following would raise an error:

    s_players.sample(n=3, fraction=0.30, seed=42)

Choose either:
+ n=... for an exact number of values
+ fraction=... for a proportion of the Series
'''


# =========================================================================================
# 4. Sampling with replacement / oversampling
# =========================================================================================
'''
By default, Polars samples WITHOUT replacement.
This means the same position/value is not selected more than once.

Use with_replacement=True to allow repeated selections.
This is required when n is larger than len(s), or when fraction > 1.

pandas:
    s.sample(n=12, replace=True, random_state=42)

Polars:
    s.sample(n=12, with_replacement=True, seed=42)
'''

s_sample_replace_n = s_players.sample(
    n=12,
    with_replacement=True,
    seed=2,
)
print(s_sample_replace_n)
# shape: (12,)
# Series: 'player' [str]
# Repeated values are possible.

# Oversample 150% of the Series length.
s_sample_replace_fraction = s_players.sample(
    fraction=1.50,
    with_replacement=True,
    seed=1,
)
print(s_sample_replace_fraction)
# shape: (15,)
# Series: 'player' [str]

print(len(s_sample_replace_fraction))
# 15


# =========================================================================================
# 5. Shuffle all values with fraction=1.0 and shuffle=True
# =========================================================================================
'''
A common pandas Series pattern is:

    s.sample(frac=1)

For Polars, use:

    s.sample(fraction=1.0, shuffle=True)

This returns every value, but in random order.

Why shuffle=True?
+ Sampling is random, but shuffle=True explicitly shuffles the order of sampled data points.
+ For teaching examples, shuffle=True makes the intention very clear.
'''

s_shuffled = s_players.sample(fraction=1.0, shuffle=True)
print(s_shuffled)
# shape: (10,)
# Series: 'player' [str]
# All values, shuffled.

# Example: split a Series after shuffling.
s_train = s_shuffled.slice(0, 8)
s_test = s_shuffled.slice(8)

print(s_train)
# shape: (8,)

print(s_test)
# shape: (2,)

'''
Alternative:
Polars Series also has .shuffle(seed=...), which is convenient when your only goal is shuffling.

    s_players.shuffle(seed=7)

But this lesson focuses on .sample(...), because it translates directly from pandas sampling.
'''


# =========================================================================================
# 7. Expression sampling with pl.col(...).sample(...)
# =========================================================================================
'''
Polars expressions also support .sample(...):

    pl.col("age").sample(n=4, seed=10)

This is useful inside DataFrame.select(...) or LazyFrame.select(...).

Important:
+ pl.col("age").sample(...) samples values from that one column expression.
+ df.sample(...) samples full rows.
'''

df_players = pl.DataFrame(
    {
        "player": s_players,
        "age": s_age,
        "position": s_position,
    }
)
print(df_players)
# shape: (10, 3)
# ┌────────┬───────┬────────────┐
# │ player ┆ age   ┆ position   │
# │ ---    ┆ ---   ┆ ---        │
# │ str    ┆ f64   ┆ str        │
# ╞════════╪═══════╪════════════╡
# │ Adam   ┆ 22.99 ┆ Catcher    │
# │ Paul   ┆ 34.69 ┆ Catcher    │
# │ Ramon  ┆ 30.78 ┆ Catcher    │
# │ Kevin  ┆ 35.43 ┆ Infielder  │
# │ Chris  ┆ 35.71 ┆ Infielder  │
# │ Brian  ┆ 29.39 ┆ Pitcher    │
# │ Nick   ┆ 30.77 ┆ Pitcher    │
# │ Miguel ┆ 32.82 ┆ Infielder  │
# │ Wilson ┆ 26.59 ┆ Infielder  │
# │ Mark   ┆ 32.01 ┆ Outfielder │
# └────────┴───────┴────────────┘

# Sample values from one column expression.
df_age_expr_sample = df_players.select(
    pl.col("age").sample(n=4, seed=10).alias("sampled_age")
)
print(df_age_expr_sample)
# shape: (4, 1)
# column: sampled_age

# Sample a fraction from one expression.
df_player_expr_sample = df_players.select(
    pl.col("player").sample(fraction=0.30, seed=40).alias("sampled_player")
)
print(df_player_expr_sample)
# shape: (3, 1)
# column: sampled_player

# Do NOT do this if you need original row relationships preserved.
df_independent_column_samples = df_players.select(
    pl.col("player").sample(n=3, seed=1).alias("sampled_player"),
    pl.col("age").sample(n=3, seed=2).alias("sampled_age"),
)
print(df_independent_column_samples)
# The sampled_player and sampled_age columns were sampled independently.


# =========================================================================================
# 8. What pandas Series.sample features do not translate directly
# =========================================================================================
'''
Some pandas Series.sample(...) features do not have a direct Series-level Polars equivalent.

1. pandas ignore_index=True

   pandas has custom index labels, so ignore_index=True resets them.
   Polars Series has no custom index labels, so there is no equivalent parameter.

2. pandas weights=...

   pandas Series.sample(...) supports weighted sampling.
   Polars Series.sample(...) does not have a weights= parameter.

3. pandas SeriesGroupBy.sample(...)

   pandas can directly sample values within Series groups.
   In Polars, group-wise row sampling is usually done on a DataFrame using expressions,
   because Polars has no separate custom index-aligned SeriesGroupBy object in the pandas sense.
'''

# Example of group-wise row sampling in Polars DataFrame style.
# Sample 1 full row from each position group.
df_group_sample = df_players.filter(
    pl.int_range(pl.len()).shuffle(seed=42).over("position") < 1
)
print(df_group_sample)
# shape: one row per position group

'''
The group-wise example above samples rows, not just standalone Series values.
That is usually the safer Polars workflow because row relationships are preserved.
'''


# =========================================================================================
# 9. Quick pandas-to-Polars summary
# =========================================================================================
'''
pandas Series vs Polars Series sampling summary

1. Sample exact number of values

   pandas:
       s.sample(n=3, random_state=42)

   Polars:
       s.sample(n=3, seed=42)

2. Sample a fraction of values

   pandas:
       s.sample(frac=0.30, random_state=42)

   Polars:
       s.sample(fraction=0.30, seed=42)

3. Sample with replacement

   pandas:
       s.sample(n=12, replace=True, random_state=42)

   Polars:
       s.sample(n=12, with_replacement=True, seed=42)

4. Oversample by fraction

   pandas:
       s.sample(frac=1.50, replace=True, random_state=42)

   Polars:
       s.sample(fraction=1.50, with_replacement=True, seed=42)

5. Shuffle all values

   pandas:
       s.sample(frac=1.0, random_state=42)

   Polars:
       s.sample(fraction=1.0, shuffle=True, seed=42)

6. Reset sampled index

   pandas:
       s.sample(n=3, random_state=42, ignore_index=True)

   Polars:
       No equivalent needed because Polars has no custom index labels.

7. Weighted sampling

   pandas:
       s.sample(n=3, weights=weights, random_state=42)

   Polars:
       Series.sample(...) has no weights= parameter.
       Use a custom workflow if weighted sampling is required.

8. Expression sampling

   Polars only:
       df.select(pl.col("age").sample(n=3, seed=42))

   Remember:
       This samples column values, not full DataFrame rows.
'''
