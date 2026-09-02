'''
Random sampling values from a pandas Series.

1. s.sample(n=..., random_state=...)
2. s.sample(frac=..., random_state=...)

Content flow:
1. Create example Series
2. s.sample(n=..., random_state=...)
3. s.sample(frac=..., random_state=...)
4. Sampling with replacement / oversampling
5. Shuffle all values with frac=1
6. Preserve or reset index labels with ignore_index=
7. Weighted sampling with weights=
8. SeriesGroupBy.sample(...)
9. Series sampling vs DataFrame row sampling
10. Quick summary

Important:
+ n and frac cannot be used together.
+ If neither n nor frac is provided, pandas samples 1 item by default.
+ random_state=... makes examples reproducible.
+ frac > 1 requires replace=True.
+ Series.sample(...) returns another Series.
'''

import pandas as pd

# =========================================================================================
# 1. Create example Series
# =========================================================================================
'''
A pandas Series is one-dimensional and can have custom index labels.

When you sample from a Series:
+ the sampled values come from that one Series
+ the original index labels are preserved by default
+ the returned object is still a Series
'''

s_players = pd.Series(
    ["Adam", "Paul", "Ramon", "Kevin", "Chris", "Brian", "Nick", "Miguel", "Wilson", "Mark"],
    index=["p01", "p02", "p03", "p04", "p05", "p06", "p07", "p08", "p09", "p10"],
    name="player",
)

s_age = pd.Series(
    [22.99, 34.69, 30.78, 35.43, 35.71, 29.39, 30.77, 32.82, 26.59, 32.01],
    index=s_players.index,
    name="age",
)

s_position = pd.Series(
    ["Catcher", "Catcher", "Catcher", "Infielder", "Infielder", "Pitcher", "Pitcher", "Infielder", "Infielder", "Outfielder"],
    index=s_players.index,
    name="position",
)

print(s_players)
# p01      Adam
# p02      Paul
# p03     Ramon
# p04     Kevin
# p05     Chris
# p06     Brian
# p07      Nick
# p08    Miguel
# p09    Wilson
# p10      Mark
# Name: player, dtype: object

print(s_age)
# p01    22.99
# p02    34.69
# p03    30.78
# p04    35.43
# p05    35.71
# p06    29.39
# p07    30.77
# p08    32.82
# p09    26.59
# p10    32.01
# Name: age, dtype: float64


# =========================================================================================
# 2. s.sample(n=..., random_state=...)
# =========================================================================================
'''
The n=... argument specifies the exact number of values to return.

random_state=... ensures reproducibility.

If the Series has index labels, those original index labels are kept by default.
'''

s_sample_n = s_players.sample(n=3, random_state=42)
print(s_sample_n)
# p09    Wilson
# p02      Paul
# p06     Brian
# Name: player, dtype: object

# Sample numeric values from another Series.
s_age_sample = s_age.sample(n=4, random_state=10)
print(s_age_sample)
# p09    26.59
# p03    30.78
# p06    29.39
# p07    30.77
# Name: age, dtype: float64

# If you omit both n and frac, pandas samples 1 item by default.
s_sample_one = s_players.sample(random_state=42)
print(s_sample_one)
# p09    Wilson
# Name: player, dtype: object


# =========================================================================================
# 3. s.sample(frac=..., random_state=...)
# =========================================================================================
'''
The frac=... argument specifies the fraction/proportion of values to return.

Examples:
+ frac=0.30 means sample 30% of the values
+ frac=1.00 means sample 100% of the values
+ frac > 1 means oversampling, and requires replace=True

Important:
+ pandas uses frac=
+ Polars uses fraction=
'''

s_sample_frac = s_players.sample(frac=0.30, random_state=40)
print(s_sample_frac)
# p05     Chris
# p04     Kevin
# p09    Wilson
# Name: player, dtype: object

print(len(s_sample_frac))
# 3

'''
Cannot use n and frac together.

The following would raise an error:

    s_players.sample(n=3, frac=0.30, random_state=42)

Choose either:
+ n=... for an exact number of values
+ frac=... for a proportion of the Series
'''


# =========================================================================================
# 4. Sampling with replacement / oversampling
# =========================================================================================
'''
By default, pandas samples WITHOUT replacement.
This means the same value/index position is not selected more than once.

Use replace=True to allow repeated selections.
This is required when n is larger than len(s), or when frac > 1.
'''

s_sample_replace_n = s_players.sample(n=12, replace=True, random_state=2)
print(s_sample_replace_n)
# p09    Wilson
# p09    Wilson
# p07      Nick
# p03     Ramon
# p09    Wilson
# p08    Miguel
# p03     Ramon
# p02      Paul
# p06     Brian
# p05     Chris
# p05     Chris
# p06     Brian
# Name: player, dtype: object

# Oversample 150% of the Series length.
s_sample_replace_frac = s_players.sample(frac=1.50, replace=True, random_state=1)
print(s_sample_replace_frac)
# p06     Brian
# p09    Wilson
# p10      Mark
# p06     Brian
# p01      Adam
# p01      Adam
# p02      Paul
# p08    Miguel
# p07      Nick
# p10      Mark
# p03     Ramon
# p05     Chris
# p06     Brian
# p03     Ramon
# p05     Chris
# Name: player, dtype: object

print(len(s_sample_replace_frac))
# 15


# =========================================================================================
# 5. Shuffle all values with frac=1
# =========================================================================================
'''
Shuffle element order in a series:

    s.sample(frac=1)

This returns every value exactly once, but in random order.
'''

s_shuffled = s_players.sample(frac=1.0)
print(s_shuffled)
# p09    Wilson
# p06     Brian
# p01      Adam
# p03     Ramon
# p02      Paul
# p10      Mark
# p08    Miguel
# p04     Kevin
# p07      Nick
# p05     Chris
# Name: player, dtype: object

# Example: split a Series after shuffling.
s_train = s_shuffled.iloc[:8]
s_test = s_shuffled.iloc[8:]

print(s_train)
# first 8 shuffled values

print(s_test)
# last 2 shuffled values


# =========================================================================================
# 6. Preserve or reset index labels with ignore_index=
# =========================================================================================
'''
By default, Series.sample(...) preserves the original index labels.

Use ignore_index=True to reset the sampled Series index to:
    0, 1, 2, ...

This is useful when the original labels no longer matter after sampling.
'''

s_sample_keep_index = s_players.sample(n=4, random_state=42)
print(s_sample_keep_index)
# p09    Wilson
# p02      Paul
# p06     Brian
# p01      Adam
# Name: player, dtype: object

s_sample_reset_index = s_players.sample(n=4, random_state=42, ignore_index=True)
print(s_sample_reset_index)
# 0    Wilson
# 1      Paul
# 2     Brian
# 3      Adam
# Name: player, dtype: object


# =========================================================================================
# 7. Weighted sampling with weights=
# =========================================================================================
'''
weights=... controls the probability of each value being sampled.

Higher weight = more likely to be sampled.

The weights can be:
+ a list/array with the same length as the Series
+ a Series aligned by index labels

If weights do not sum to 1, pandas normalizes them internally.
'''

sampling_weights = pd.Series(
    [1, 1, 1, 1, 1, 1, 1, 1, 10, 10],
    index=s_players.index,
    name="sampling_weight",
)

print(sampling_weights)
# p01     1
# p02     1
# p03     1
# p04     1
# p05     1
# p06     1
# p07     1
# p08     1
# p09    10
# p10    10
# Name: sampling_weight, dtype: int64

s_weighted = s_players.sample(n=5, weights=sampling_weights, random_state=42)
print(s_weighted)
# p09    Wilson
# p10      Mark
# p05     Chris
# p02      Paul
# p01      Adam
# Name: player, dtype: object

'''
Note:
If replace=False, pandas does not allow an impossible or biased weighted sample.
For example, asking for too many values when one item has nearly all the weight can raise an error.
'''


# =========================================================================================
# 8. SeriesGroupBy.sample(...)
# =========================================================================================
'''
A pandas Series can also be sampled within groups.

Example:
+ s_players contains player names
+ s_position contains the group label for each player
+ s_players.groupby(s_position).sample(n=1) samples 1 player name from each position group
'''

s_group_sample = s_players.groupby(s_position).sample(n=1, random_state=42)
print(s_group_sample)
# p01     Adam
# p05    Chris
# p10     Mark
# p06    Brian
# Name: player, dtype: object

# Sample 50% from each group.
s_group_sample_frac = s_players.groupby(s_position).sample(frac=0.50, random_state=42)
print(s_group_sample_frac)
# One half of each group, rounded according to pandas group sampling behavior.


# =========================================================================================
# 10. Quick summary
# =========================================================================================

'''
pandas Series sampling summary

1. Sample exact number of values

   s.sample(n=3, random_state=42)

2. Sample a fraction of values

   s.sample(frac=0.30, random_state=42)

3. Sample with replacement

   s.sample(n=12, replace=True, random_state=42)

4. Oversample by fraction

   s.sample(frac=1.50, replace=True, random_state=42)

5. Shuffle all values

   s.sample(frac=1.0, random_state=42)

6. Reset sampled index

   s.sample(n=3, random_state=42, ignore_index=True)

7. Weighted sampling

   s.sample(n=3, weights=weights, random_state=42)

8. Group-wise Series sampling

   s.groupby(group_labels).sample(n=1, random_state=42)

Key parameter names:
+ n=              exact number of values
+ frac=           fraction/proportion of values
+ replace=        allow repeated values/index positions
+ random_state=   reproducible random seed
+ weights=        non-uniform sampling probabilities
+ ignore_index=   reset index labels in the returned Series
'''
