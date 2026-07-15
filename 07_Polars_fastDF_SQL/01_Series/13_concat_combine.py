'''
In Polars, Series do not have custom index labels.
Concatenation simply stacks them vertically, and element-wise operations
align strictly by row position (not by index labels like pandas).

##########################################
1. pl.concat(): Concatenation of Series
2. Element-wise Merging (pl.max_horizontal, pl.when)
3. Emulating Index Alignment (Relational Joins)
'''

import polars as pl


#-----------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 1. pl.concat() --------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
'''
The pl.concat() function concatenates Series vertically.
Key Features:
+ Combines multiple Series into one
+ Inherently behaves like pandas' ignore_index=True because Polars lacks custom indices
'''

s1 = pl.Series("letters", ["a", "b"])
s2 = pl.Series("letters", ["c", "d"])

###################################
## Basic concatenation of Series ##
###################################

s_concat = pl.concat([s1, s2])
print(s_concat)
# shape: (4,)
# Series: 'letters' [str]
# [
# 	"a"
# 	"b"
# 	"c"
# 	"d"
# ]

######################################
## "keys" equivalent (Tracking origin)
######################################
'''
Polars does not support MultiIndex. If you need to track which Series
the data came from (equivalent to pandas' keys=['first', 'second']),
you should convert them to DataFrames, add an identifier column, and then concatenate.
'''

df1 = s1.to_frame().with_columns(pl.lit("first").alias("source"))
df2 = s2.to_frame().with_columns(pl.lit("second").alias("source"))

df_concat = pl.concat([df1, df2])
print(df_concat)
# shape: (4, 2)
# ┌─────────┬────────┐
# │ letters ┆ source │
# │ ---     ┆ ---    │
# │ str     ┆ str    │
# ╞═════════╪════════╡
# │ a       ┆ first  │
# │ b       ┆ first  │
# │ c       ┆ second │
# │ d       ┆ second │
# └─────────┴────────┘

#-----------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 2. Element-wise Merging -------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
'''
Pandas' .combine() aligns data by INDEX LABELS and applies a function.
Since Polars Series have no custom indices, they align strictly by POSITION (row number).
Element-wise operations between two Series are best done inside pl.select()
using horizontal functions (pl.max_horizontal, pl.sum_horizontal) or pl.when().
'''

s1 = pl.Series("s1", [330.0, 160.0])
s2 = pl.Series("s2", [345.0, 200.0])

###################################
## Basic element-wise max / min  ##
###################################

# Equivalent to pandas s1.combine(s2, func=max)
df_combined = pl.select(
    pl.max_horizontal(s1, s2).alias("max_speed")
)
print(df_combined)
# shape: (2, 1)
# ┌───────────┐
# │ max_speed │
# │ ---       │
# │ f64       │
# ╞═══════════╡
# │ 345.0     │
# │ 200.0     │
# └───────────┘

#############################################
## Combine with fill_value to handle nulls ##
#############################################
'''
If one Series has nulls (equivalent to missing index labels in pandas),
horizontal functions will ignore the null and take the valid value.
If BOTH are null, it returns null. You can use .fill_null() to emulate pandas' fill_value.
'''

s1_nulls = pl.Series("s1", [330.0, None])
s2_nulls = pl.Series("s2", [None, 200.0])

# Equivalent to pandas s1.combine(s2, func=max, fill_value=0)
df_fill = pl.select(
    pl.max_horizontal(s1_nulls, s2_nulls).fill_null(0).alias("max_with_fill")
)
print(df_fill)
# shape: (2, 1)
# ┌───────────────┐
# │ max_with_fill │
# │ ---           │
# │ f64           │
# ╞═══════════════╡
# │ 330.0         │
# │ 200.0         │
# └───────────────┘

################################
## Custom functions (pl.when) ##
################################
'''
For custom logic (e.g., func=lambda x, y: x + y if x > 300 else y),
use pl.when().then().otherwise().
'''

df_custom = pl.select(
    pl.when(s1 > 300)
    .then(s1 + s2)
    .otherwise(s2)
    .alias("custom_combine")
)
print(df_custom)
# shape: (2, 1)
# ┌────────────────┐
# │ custom_combine │
# │ ---            │
# │ f64            │
# ╞════════════════╡
# │ 675.0          │  (330 + 345 because 330 > 300)
# │ 200.0          │  (just s2 because 160 is not > 300)
# └────────────────┘


#-----------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 3. Emulating Index Alignment ------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
'''
NOTE: What if you truly need pandas-like index alignment where rows are matched by
a "key" (like 'falcon', 'eagle', 'duck') rather than row position?

In Polars, you MUST use DataFrames and Relational Joins (.join()) to achieve this.
'''

df1 = pl.DataFrame({"bird": ["falcon", "eagle"], "speed1": [330.0, 160.0]})
df2 = pl.DataFrame({"bird": ["falcon", "eagle", "duck"], "speed2": [345.0, 200.0, 30.0]})

# Full outer join to emulate pandas index alignment, then fill nulls with 0 (fill_value=0)
df_aligned = (
    df1.join(df2, on="bird", how="full", coalesce=True)
    .with_columns(
        pl.col("speed1").fill_null(0),
        pl.col("speed2").fill_null(0)
    )
    .with_columns(
        pl.max_horizontal("speed1", "speed2").alias("max_speed")
    )
)
print(df_aligned)
# shape: (3, 4)
# ┌────────┬────────┬────────┬───────────┐
# │ bird   ┆ speed1 ┆ speed2 ┆ max_speed │
# │ ---    ┆ ---    ┆ ---    ┆ ---       │
# │ str    ┆ f64    ┆ f64    ┆ f64       │
# ╞════════╪════════╪════════╪═══════════╡
# │ falcon ┆ 330.0  ┆ 345.0  ┆ 345.0     │
# │ eagle  ┆ 160.0  ┆ 200.0  ┆ 200.0     │
# │ duck   ┆ 0.0    ┆ 30.0   ┆ 30.0      │
# └────────┴────────┴────────┴───────────┘
