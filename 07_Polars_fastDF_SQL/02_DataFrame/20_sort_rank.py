'''
Key differences from pandas:
1. Sorting rows:
   + lf.sort(by=..., descending=..., nulls_last=..., maintain_order=...)
   + sort by single column
   + sort by multiple columns and orders
   + sort by expression
   + sort with null handling

2. Sorting rows:
   + sort row-label ascending
   + sort row-label descending
   + use `.with_row_index()` to add index column then use it to sort

3. Sorting column names:
   + sort ascending
   + sort descending
   + sort with custom order

4. Ranking:
   + pandas: df["score"].rank(method="average", ascending=True, pct=False)
   + Polars Series: s.rank(method="average", descending=False)
   + Polars DataFrame: use expressions, e.g. pl.col("score").rank(...)

5. Polars rank method names:
   + "average"  : average rank for ties
   + "max"      : maximum rank for ties
   + "min"      : minimum rank for ties
   + "dense"    : compact ranks with no gaps between tie groups
   + "ordinal"  : pandas method="first" equivalent; ties get ranks by order of appearance
   + "random"   : ties get randomly ordered ranks; use seed= for reproducibility

6. Percentage rank:
   + pandas: rank(pct=True)
   + Polars: rank(...) / pl.len(), or rank(...) / pl.count("col") if nulls exist
   + For pandas-like dense percentage rank, divide dense_rank by n_unique().
'''

import polars as pl

# =========================================================================================
# 1. Sorting rows
# =========================================================================================

lf_unsort = pl.LazyFrame(
    {
        "name": ["Alice", "Alice", "Alice", "Bob", "Bob", "Charlie"],
        "subject": ["Math", "English", "Science", "Math", "English", "Math"],
        "score": [85, 90, 78, 92, 88, 95],
        "age": [20, 20, 20, 22, 22, 23],
    }
)

# In pandas this would often be an index.
# In Polars, row labels should be stored as a normal column.
lf_idx = pl.LazyFrame(
    {
        "row_label": [100, 29, 234, 1, 150],
        "Numbers": [1, 2, 3, 4, 5],
        "Letters": ["a", "b", "c", "d", "e"],
    }
)

##-----------------------------##
## lf.sort(): by single column ##
##-----------------------------##

print(
    lf_unsort
    .sort(by="score", descending=True)
    .collect()
)
# shape: (6, 4)
# ┌─────────┬─────────┬───────┬─────┐
# │ name    ┆ subject ┆ score ┆ age │
# │ ---     ┆ ---     ┆ ---   ┆ --- │
# │ str     ┆ str     ┆ i64   ┆ i64 │
# ╞═════════╪═════════╪═══════╪═════╡
# │ Charlie ┆ Math    ┆ 95    ┆ 23  │
# │ Bob     ┆ Math    ┆ 92    ┆ 22  │
# │ Alice   ┆ English ┆ 90    ┆ 20  │
# │ Bob     ┆ English ┆ 88    ┆ 22  │
# │ Alice   ┆ Math    ┆ 85    ┆ 20  │
# │ Alice   ┆ Science ┆ 78    ┆ 20  │
# └─────────┴─────────┴───────┴─────┘

##-------------------------------------------##
## lf.sort(): by multiple columns and orders ##
##-------------------------------------------##

print(
    lf_unsort
    .sort(by=["name", "score"], descending=[True, False])
    .collect()
)
# shape: (6, 4)
# ┌─────────┬─────────┬───────┬─────┐
# │ name    ┆ subject ┆ score ┆ age │
# │ ---     ┆ ---     ┆ ---   ┆ --- │
# │ str     ┆ str     ┆ i64   ┆ i64 │
# ╞═════════╪═════════╪═══════╪═════╡
# │ Charlie ┆ Math    ┆ 95    ┆ 23  │
# │ Bob     ┆ English ┆ 88    ┆ 22  │
# │ Bob     ┆ Math    ┆ 92    ┆ 22  │
# │ Alice   ┆ Science ┆ 78    ┆ 20  │
# │ Alice   ┆ Math    ┆ 85    ┆ 20  │
# │ Alice   ┆ English ┆ 90    ┆ 20  │
# └─────────┴─────────┴───────┴─────┘

##--------------------------##
## lf.sort(): by expression ##
##--------------------------##
'''
Polars can sort by an expression, not only an existing column name.
Here we sort by score per age: score / age.
'''

print(
    lf_unsort
    .sort(by=pl.col("score") / pl.col("age"), descending=True)
    .collect()
)
# shape: (6, 4)
# ┌─────────┬─────────┬───────┬─────┐
# │ name    ┆ subject ┆ score ┆ age │
# │ ---     ┆ ---     ┆ ---   ┆ --- │
# │ str     ┆ str     ┆ i64   ┆ i64 │
# ╞═════════╪═════════╪═══════╪═════╡
# │ Alice   ┆ English ┆ 90    ┆ 20  │
# │ Alice   ┆ Math    ┆ 85    ┆ 20  │
# │ Bob     ┆ Math    ┆ 92    ┆ 22  │
# │ Charlie ┆ Math    ┆ 95    ┆ 23  │
# │ Bob     ┆ English ┆ 88    ┆ 22  │
# │ Alice   ┆ Science ┆ 78    ┆ 20  │
# └─────────┴─────────┴───────┴─────┘
# Highest score-per-age rows appear first.

##------------------------------------##
## lf.sort(): sort with null handling ##
##------------------------------------##

lf_nulls = pl.LazyFrame(
    {
        "name": ["Alice", "Bob", "Charlie", "David", "Eva"],
        "score": [85, None, 78, 92, None],
    }
)

# By default, null ordering depends on the sort operation.
# Set nulls_last=True when you want missing values to appear at the bottom.
print(
    lf_nulls
    .sort("score", descending=True, nulls_last=True)
    .collect()
)
# shape: (5, 2)
# ┌─────────┬───────┐
# │ name    ┆ score │
# │ ---     ┆ ---   │
# │ str     ┆ i64   │
# ╞═════════╪═══════╡
# │ David   ┆ 92    │
# │ Alice   ┆ 85    │
# │ Charlie ┆ 78    │
# │ Bob     ┆ null  │
# │ Eva     ┆ null  │
# └─────────┴───────┘

##---------------------------------##
## lf.sort(): stable sort for ties ##
##---------------------------------##
'''
If rows have equal sort keys, maintain_order=True preserves their original order.
This is similar in spirit to using a stable sorting algorithm.
'''

lf_stable = pl.LazyFrame(
    {
        "student": ["A", "B", "C", "D"],
        "score": [90, 90, 85, 90],
    }
)

print(
    lf_stable
    .sort("score", descending=True, maintain_order=True)
    .collect()
)
# shape: (4, 2)
# ┌─────────┬───────┐
# │ student ┆ score │
# │ ---     ┆ ---   │
# │ str     ┆ i64   │
# ╞═════════╪═══════╡
# │ A       ┆ 90    │
# │ B       ┆ 90    │
# │ D       ┆ 90    │
# │ C       ┆ 85    │
# └─────────┴───────┘
# A, B, and D all have score 90, and they keep their original order among ties.

# =========================================================================================
# 2. Sorting row names (index)
# =========================================================================================
'''
Polars does not have index system
=> store index as an explicit column and use it to sort
'''

print(lf_idx.collect())
# shape: (5, 3)
# ┌───────────┬─────────┬─────────┐
# │ row_label ┆ Numbers ┆ Letters │
# │ ---       ┆ ---     ┆ ---     │
# │ i64       ┆ i64     ┆ str     │
# ╞═══════════╪═════════╪═════════╡
# │ 100       ┆ 1       ┆ a       │
# │ 29        ┆ 2       ┆ b       │
# │ 234       ┆ 3       ┆ c       │
# │ 1         ┆ 4       ┆ d       │
# │ 150       ┆ 5       ┆ e       │
# └───────────┴─────────┴─────────┘

##--------------------------------------------##
## sort row-label, descending=False (default) ##
##--------------------------------------------##

print(
    lf_idx
    .sort("row_label")
    .collect()
)
# shape: (5, 3)
# ┌───────────┬─────────┬─────────┐
# │ row_label ┆ Numbers ┆ Letters │
# │ ---       ┆ ---     ┆ ---     │
# │ i64       ┆ i64     ┆ str     │
# ╞═══════════╪═════════╪═════════╡
# │ 1         ┆ 4       ┆ d       │
# │ 29        ┆ 2       ┆ b       │
# │ 100       ┆ 1       ┆ a       │
# │ 150       ┆ 5       ┆ e       │
# │ 234       ┆ 3       ┆ c       │
# └───────────┴─────────┴─────────┘

##---------------------------------##
## sort row-label, descending=True ##
##---------------------------------##

print(
    lf_idx
    .sort("row_label", descending=True)
    .collect()
)
# shape: (5, 3)
# ┌───────────┬─────────┬─────────┐
# │ row_label ┆ Numbers ┆ Letters │
# │ ---       ┆ ---     ┆ ---     │
# │ i64       ┆ i64     ┆ str     │
# ╞═══════════╪═════════╪═════════╡
# │ 234       ┆ 3       ┆ c       │
# │ 150       ┆ 5       ┆ e       │
# │ 100       ┆ 1       ┆ a       │
# │ 29        ┆ 2       ┆ b       │
# │ 1         ┆ 4       ┆ d       │
# └───────────┴─────────┴─────────┘

##-----------------------------------------------------------------##
## Use `.with_row_index()` to add index column then use it to sort ##
##-----------------------------------------------------------------##
'''
Polars has no hidden index. If you need a visible row number, add one with with_row_index().
The created row number is a normal column.
'''

print(
    lf_unsort
    .with_row_index(name="index", offset=1)
    .sort("index", descending=True)
    .collect()
)
# shape: (6, 5)
# ┌───────┬─────────┬─────────┬───────┬─────┐
# │ index ┆ name    ┆ subject ┆ score ┆ age │
# │ ---   ┆ ---     ┆ ---     ┆ ---   ┆ --- │
# │ u32   ┆ str     ┆ str     ┆ i64   ┆ i64 │
# ╞═══════╪═════════╪═════════╪═══════╪═════╡
# │ 6     ┆ Charlie ┆ Math    ┆ 95    ┆ 23  │
# │ 5     ┆ Bob     ┆ English ┆ 88    ┆ 22  │
# │ 4     ┆ Bob     ┆ Math    ┆ 92    ┆ 22  │
# │ 3     ┆ Alice   ┆ Science ┆ 78    ┆ 20  │
# │ 2     ┆ Alice   ┆ English ┆ 90    ┆ 20  │
# │ 1     ┆ Alice   ┆ Math    ┆ 85    ┆ 20  │
# └───────┴─────────┴─────────┴───────┴─────┘

# =========================================================================================
# 3. Sorting column names
# =========================================================================================

##---------------------------##
## Ascending order (default) ##
##---------------------------##

print(
    lf_unsort
    .select(sorted(lf_unsort.collect_schema().names())) # use `sorted(df.columns)` for eager DataFrame
    .collect()
)
# shape: (6, 4)
# ┌─────┬─────────┬───────┬─────────┐
# │ age ┆ name    ┆ score ┆ subject │
# │ --- ┆ ---     ┆ ---   ┆ ---     │
# │ i64 ┆ str     ┆ i64   ┆ str     │
# ╞═════╪═════════╪═══════╪═════════╡
# │ 20  ┆ Alice   ┆ 85    ┆ Math    │
# │ 20  ┆ Alice   ┆ 90    ┆ English │
# │ 20  ┆ Alice   ┆ 78    ┆ Science │
# │ 22  ┆ Bob     ┆ 92    ┆ Math    │
# │ 22  ┆ Bob     ┆ 88    ┆ English │
# │ 23  ┆ Charlie ┆ 95    ┆ Math    │
# └─────┴─────────┴───────┴─────────┘

##------------------##
## Descending order ##
##------------------##

print(
    lf_unsort
    .select(sorted(lf_unsort.collect_schema().names(), reverse=True))
    .collect()
)
# shape: (6, 4)
# ┌─────────┬───────┬─────────┬─────┐
# │ subject ┆ score ┆ name    ┆ age │
# │ ---     ┆ ---   ┆ ---     ┆ --- │
# │ str     ┆ i64   ┆ str     ┆ i64 │
# ╞═════════╪═══════╪═════════╪═════╡
# │ Math    ┆ 85    ┆ Alice   ┆ 20  │
# │ English ┆ 90    ┆ Alice   ┆ 20  │
# │ Science ┆ 78    ┆ Alice   ┆ 20  │
# │ Math    ┆ 92    ┆ Bob     ┆ 22  │
# │ English ┆ 88    ┆ Bob     ┆ 22  │
# │ Math    ┆ 95    ┆ Charlie ┆ 23  │
# └─────────┴───────┴─────────┴─────┘

##--------------##
## Custom order ##
##--------------##

print(
    lf_unsort
    .select("score", "age", "subject", "name")
    .collect()
)
# shape: (6, 4)
# ┌───────┬─────┬─────────┬─────────┐
# │ score ┆ age ┆ subject ┆ name    │
# │ ---   ┆ --- ┆ ---     ┆ ---     │
# │ i64   ┆ i64 ┆ str     ┆ str     │
# ╞═══════╪═════╪═════════╪═════════╡
# │ 85    ┆ 20  ┆ Math    ┆ Alice   │
# │ 90    ┆ 20  ┆ English ┆ Alice   │
# │ 78    ┆ 20  ┆ Science ┆ Alice   │
# │ 92    ┆ 22  ┆ Math    ┆ Bob     │
# │ 88    ┆ 22  ┆ English ┆ Bob     │
# │ 95    ┆ 23  ┆ Math    ┆ Charlie │
# └───────┴─────┴─────────┴─────────┘

# =========================================================================================
# 4. Rank
# =========================================================================================
'''
In pandas, df.rank(axis=0) can rank columns directly.
In Polars, ranking is usually an expression:

    pl.col("score").rank(method="average")

Use it inside `select(), with_columns(), group_by().agg()` or a LazyFrame pipeline.
'''

lf_unrank = pl.LazyFrame(
    {
        "name": ["Alice", "Bob", "Charlie", "David", "Eva", "Freddy", "George", "Hannah"],
        "score": [85, 92, 85, 88, 90, 66, 66, 66],
    }
)

print(lf_unrank.collect())
# shape: (8, 2)
# ┌─────────┬───────┐
# │ name    ┆ score │
# │ ---     ┆ ---   │
# │ str     ┆ i64   │
# ╞═════════╪═══════╡
# │ Alice   ┆ 85    │
# │ Bob     ┆ 92    │
# │ Charlie ┆ 85    │
# │ David   ┆ 88    │
# │ Eva     ┆ 90    │
# │ Freddy  ┆ 66    │
# │ George  ┆ 66    │
# │ Hannah  ┆ 66    │
# └─────────┴───────┘

##-------------------------##
## Expr.rank(method="max") ##
##-------------------------##

print(
    lf_unrank
    .with_columns(
        pl.col("score").rank(method="max").alias("rank_max")
    )
    .collect()
)
# shape: (8, 3)
# ┌─────────┬───────┬──────────┐
# │ name    ┆ score ┆ rank_max │
# │ ---     ┆ ---   ┆ ---      │
# │ str     ┆ i64   ┆ u32      │
# ╞═════════╪═══════╪══════════╡
# │ Alice   ┆ 85    ┆ 5        │
# │ Bob     ┆ 92    ┆ 8        │
# │ Charlie ┆ 85    ┆ 5        │
# │ David   ┆ 88    ┆ 6        │
# │ Eva     ┆ 90    ┆ 7        │
# │ Freddy  ┆ 66    ┆ 3        │
# │ George  ┆ 66    ┆ 3        │
# │ Hannah  ┆ 66    ┆ 3        │
# └─────────┴───────┴──────────┘
# score 66 group => max(1, 2, 3) = 3
# score 85 group => max(4, 5) = 5

##-------------------------##
## Expr.rank(method="min") ##
##-------------------------##

print(
    lf_unrank
    .with_columns(
        pl.col("score").rank(method="min").alias("rank_min")
    )
    .collect()
)
# shape: (8, 3)
# ┌─────────┬───────┬──────────┐
# │ name    ┆ score ┆ rank_min │
# │ ---     ┆ ---   ┆ ---      │
# │ str     ┆ i64   ┆ u32      │
# ╞═════════╪═══════╪══════════╡
# │ Alice   ┆ 85    ┆ 4        │
# │ Bob     ┆ 92    ┆ 8        │
# │ Charlie ┆ 85    ┆ 4        │
# │ David   ┆ 88    ┆ 6        │
# │ Eva     ┆ 90    ┆ 7        │
# │ Freddy  ┆ 66    ┆ 1        │
# │ George  ┆ 66    ┆ 1        │
# │ Hannah  ┆ 66    ┆ 1        │
# └─────────┴───────┴──────────┘
# score 66 group => min(1, 2, 3) = 1
# score 85 group => min(4, 5) = 4

##---------------------------##
## Expr.rank(method="dense") ##
##---------------------------##
'''
Dense ranking works like min ranking inside each tie group,
but the next different value receives the next integer rank.

Scores in ascending order:
66 -> dense rank 1
85 -> dense rank 2
88 -> dense rank 3
90 -> dense rank 4
92 -> dense rank 5
'''

print(
    lf_unrank
    .with_columns(
        pl.col("score").rank(method="dense").alias("rank_dense")
    )
    .collect()
)
# shape: (8, 3)
# ┌─────────┬───────┬────────────┐
# │ name    ┆ score ┆ rank_dense │
# │ ---     ┆ ---   ┆ ---        │
# │ str     ┆ i64   ┆ u32        │
# ╞═════════╪═══════╪════════════╡
# │ Alice   ┆ 85    ┆ 2          │
# │ Bob     ┆ 92    ┆ 5          │
# │ Charlie ┆ 85    ┆ 2          │
# │ David   ┆ 88    ┆ 3          │
# │ Eva     ┆ 90    ┆ 4          │
# │ Freddy  ┆ 66    ┆ 1          │
# │ George  ┆ 66    ┆ 1          │
# │ Hannah  ┆ 66    ┆ 1          │
# └─────────┴───────┴────────────┘
# rank_dense = [2, 5, 2, 3, 4, 1, 1, 1]

##-----------------------------##
## Expr.rank(method="ordinal") ##
##-----------------------------##
'''
Pandas method="first" equivalent in Polars is method="ordinal".
It gives tied values distinct ranks according to their order of appearance.
'''

print(
    lf_unrank
    .with_columns(
        pl.col("score").rank(method="ordinal").alias("ordinal")
    )
    .collect()
)
# shape: (8, 3)
# ┌─────────┬───────┬──────────────┐
# │ name    ┆ score ┆ rank_ordinal │
# │ ---     ┆ ---   ┆ ---          │
# │ str     ┆ i64   ┆ u32          │
# ╞═════════╪═══════╪══════════════╡
# │ Alice   ┆ 85    ┆ 4            │
# │ Bob     ┆ 92    ┆ 8            │
# │ Charlie ┆ 85    ┆ 5            │
# │ David   ┆ 88    ┆ 6            │
# │ Eva     ┆ 90    ┆ 7            │
# │ Freddy  ┆ 66    ┆ 1            │
# │ George  ┆ 66    ┆ 2            │
# │ Hannah  ┆ 66    ┆ 3            │
# └─────────┴───────┴──────────────┘
# score 66 group appears as Freddy, George, Hannah => ranks 1, 2, 3
# score 85 group appears as Alice, Charlie         => ranks 4, 5

##----------------------------##
## Expr.rank(method="random") ##
##----------------------------##
'''
method="random" is similar to ordinal because every tied row receives a distinct rank,
but the order within ties is randomized. Use seed= for reproducible examples.
'''

print(
    lf_unrank
    .with_columns(
        pl.col("score").rank(method="random", seed=42).alias("rank_random")
    )
    .collect()
)
# shape: (8, 3)
# ┌─────────┬───────┬─────────────┐
# │ name    ┆ score ┆ rank_random │
# │ ---     ┆ ---   ┆ ---         │
# │ str     ┆ i64   ┆ u32         │
# ╞═════════╪═══════╪═════════════╡
# │ Alice   ┆ 85    ┆ 5           │
# │ Bob     ┆ 92    ┆ 8           │
# │ Charlie ┆ 85    ┆ 4           │
# │ David   ┆ 88    ┆ 6           │
# │ Eva     ┆ 90    ┆ 7           │
# │ Freddy  ┆ 66    ┆ 3           │
# │ George  ┆ 66    ┆ 2           │
# │ Hannah  ┆ 66    ┆ 1           │
# └─────────┴───────┴─────────────┘

##---------------------------##
## All rank methods together ##
##---------------------------##

print(
    lf_unrank
    .with_columns(
        pl.col("score").rank(method="average").alias("rank_average"),
        pl.col("score").rank(method="max").alias("rank_max"),
        pl.col("score").rank(method="min").alias("rank_min"),
        pl.col("score").rank(method="dense").alias("rank_dense"),
        pl.col("score").rank(method="ordinal").alias("rank_ordinal"),
    )
    .collect()
)
# shape: (8, 7)
# ┌─────────┬───────┬──────────────┬──────────┬──────────┬────────────┬──────────────┐
# │ name    ┆ score ┆ rank_average ┆ rank_max ┆ rank_min ┆ rank_dense ┆ rank_ordinal │
# │ ---     ┆ ---   ┆ ---          ┆ ---      ┆ ---      ┆ ---        ┆ ---          │
# │ str     ┆ i64   ┆ f64          ┆ u32      ┆ u32      ┆ u32        ┆ u32          │
# ╞═════════╪═══════╪══════════════╪══════════╪══════════╪════════════╪══════════════╡
# │ Alice   ┆ 85    ┆ 4.5          ┆ 5        ┆ 4        ┆ 2          ┆ 4            │
# │ Bob     ┆ 92    ┆ 8.0          ┆ 8        ┆ 8        ┆ 5          ┆ 8            │
# │ Charlie ┆ 85    ┆ 4.5          ┆ 5        ┆ 4        ┆ 2          ┆ 5            │
# │ David   ┆ 88    ┆ 6.0          ┆ 6        ┆ 6        ┆ 3          ┆ 6            │
# │ Eva     ┆ 90    ┆ 7.0          ┆ 7        ┆ 7        ┆ 4          ┆ 7            │
# │ Freddy  ┆ 66    ┆ 2.0          ┆ 3        ┆ 1        ┆ 1          ┆ 1            │
# │ George  ┆ 66    ┆ 2.0          ┆ 3        ┆ 1        ┆ 1          ┆ 2            │
# │ Hannah  ┆ 66    ┆ 2.0          ┆ 3        ┆ 1        ┆ 1          ┆ 3            │
# └─────────┴───────┴──────────────┴──────────┴──────────┴────────────┴──────────────┘

##--------------------------##
## Rank UNIQUE values only  ##
##--------------------------##

lf_unique = pl.LazyFrame(
    {
        "name": ["Alice", "Bob", "Charlie", "David", "Eva", "Freddy", "George", "Hannah"],
        "score": [85, 92, 86, 88, 90, 54, 25, 42],
    }
)

print(lf_unique.collect())
# shape: (8, 2)
# ┌─────────┬───────┐
# │ name    ┆ score │
# │ ---     ┆ ---   │
# │ str     ┆ i64   │
# ╞═════════╪═══════╡
# │ Alice   ┆ 85    │
# │ Bob     ┆ 92    │
# │ Charlie ┆ 86    │
# │ David   ┆ 88    │
# │ Eva     ┆ 90    │
# │ Freddy  ┆ 54    │
# │ George  ┆ 25    │
# │ Hannah  ┆ 42    │
# └─────────┴───────┘

print(
    lf_unique
    .with_columns(
        pl.col("score").rank(method="average").alias("rank_average"),
        pl.col("score").rank(method="max").alias("rank_max"),
        pl.col("score").rank(method="min").alias("rank_min"),
        pl.col("score").rank(method="dense").alias("rank_dense"),
        pl.col("score").rank(method="ordinal").alias("rank_ordinal"),
    )
    .collect()
)
# shape: (8, 7)
# ┌─────────┬───────┬──────────────┬──────────┬──────────┬────────────┬──────────────┐
# │ name    ┆ score ┆ rank_average ┆ rank_max ┆ rank_min ┆ rank_dense ┆ rank_ordinal │
# │ ---     ┆ ---   ┆ ---          ┆ ---      ┆ ---      ┆ ---        ┆ ---          │
# │ str     ┆ i64   ┆ f64          ┆ u32      ┆ u32      ┆ u32        ┆ u32          │
# ╞═════════╪═══════╪══════════════╪══════════╪══════════╪════════════╪══════════════╡
# │ Alice   ┆ 85    ┆ 4.0          ┆ 4        ┆ 4        ┆ 4          ┆ 4            │
# │ Bob     ┆ 92    ┆ 8.0          ┆ 8        ┆ 8        ┆ 8          ┆ 8            │
# │ Charlie ┆ 86    ┆ 5.0          ┆ 5        ┆ 5        ┆ 5          ┆ 5            │
# │ David   ┆ 88    ┆ 6.0          ┆ 6        ┆ 6        ┆ 6          ┆ 6            │
# │ Eva     ┆ 90    ┆ 7.0          ┆ 7        ┆ 7        ┆ 7          ┆ 7            │
# │ Freddy  ┆ 54    ┆ 3.0          ┆ 3        ┆ 3        ┆ 3          ┆ 3            │
# │ George  ┆ 25    ┆ 1.0          ┆ 1        ┆ 1        ┆ 1          ┆ 1            │
# │ Hannah  ┆ 42    ┆ 2.0          ┆ 2        ┆ 2        ┆ 2          ┆ 2            │
# └─────────┴───────┴──────────────┴──────────┴──────────┴────────────┴──────────────┘
# When all values are unique, all standard rank methods give the same rank values.
# The only visible difference may be dtype: average returns f64, while others usually return u32.

##------------------##
## Percentage ranks ##
##------------------##
'''
Polars rank() does not have pct=True.
Compute percentage ranks manually:

    rank / pl.len()

If the column contains nulls and you want to divide by the number of non-null values,
use:

    rank / pl.count("score")
'''

# With UNIQUE values
print(
    lf_unique
    .with_columns(
        (pl.col("score").rank(method="average") / pl.len()).alias("rank_pct")
    )
    .collect()
)
# shape: (8, 3)
# ┌─────────┬───────┬──────────┐
# │ name    ┆ score ┆ rank_pct │
# │ ---     ┆ ---   ┆ ---      │
# │ str     ┆ i64   ┆ f64      │
# ╞═════════╪═══════╪══════════╡
# │ Alice   ┆ 85    ┆ 0.5      │
# │ Bob     ┆ 92    ┆ 1.0      │
# │ Charlie ┆ 86    ┆ 0.625    │
# │ David   ┆ 88    ┆ 0.75     │
# │ Eva     ┆ 90    ┆ 0.875    │
# │ Freddy  ┆ 54    ┆ 0.375    │
# │ George  ┆ 25    ┆ 0.125    │
# │ Hannah  ┆ 42    ┆ 0.25     │
# └─────────┴───────┴──────────┘
# rank_pct = rank / 8
# Alice score 85 => rank 4 => 4 / 8 = 0.5
# Bob score 92   => rank 8 => 8 / 8 = 1.0

# With DUPLICATE values
print(
    lf_unrank
    .with_columns(
        (pl.col("score").rank(method="average") / pl.len()).alias("rank_average_pct"),
        (pl.col("score").rank(method="min") / pl.len()).alias("rank_min_pct"),
        (pl.col("score").rank(method="max") / pl.len()).alias("rank_max_pct"),
        (pl.col("score").rank(method="dense") / pl.col("score").n_unique()).alias("rank_dense_pct"),
        (pl.col("score").rank(method="ordinal") / pl.len()).alias("rank_ordinal_pct"),
    )
    .collect()
)
# shape: (8, 7)
# ┌─────────┬───────┬────────────────┬──────────────┬──────────────┬────────────────┬────────────────┐
# │ name    ┆ score ┆ rank_average_p ┆ rank_min_pct ┆ rank_max_pct ┆ rank_dense_pct ┆ rank_ordinal_p │
# │ ---     ┆ ---   ┆ ct             ┆ ---          ┆ ---          ┆ ---            ┆ ct             │
# │ str     ┆ i64   ┆ ---            ┆ f64          ┆ f64          ┆ f64            ┆ ---            │
# │         ┆       ┆ f64            ┆              ┆              ┆                ┆ f64            │
# ╞═════════╪═══════╪════════════════╪══════════════╪══════════════╪════════════════╪════════════════╡
# │ Alice   ┆ 85    ┆ 0.5625         ┆ 0.5          ┆ 0.625        ┆ 0.4            ┆ 0.5            │
# │ Bob     ┆ 92    ┆ 1.0            ┆ 1.0          ┆ 1.0          ┆ 1.0            ┆ 1.0            │
# │ Charlie ┆ 85    ┆ 0.5625         ┆ 0.5          ┆ 0.625        ┆ 0.4            ┆ 0.625          │
# │ David   ┆ 88    ┆ 0.75           ┆ 0.75         ┆ 0.75         ┆ 0.6            ┆ 0.75           │
# │ Eva     ┆ 90    ┆ 0.875          ┆ 0.875        ┆ 0.875        ┆ 0.8            ┆ 0.875          │
# │ Freddy  ┆ 66    ┆ 0.25           ┆ 0.125        ┆ 0.375        ┆ 0.2            ┆ 0.125          │
# │ George  ┆ 66    ┆ 0.25           ┆ 0.125        ┆ 0.375        ┆ 0.2            ┆ 0.25           │
# │ Hannah  ┆ 66    ┆ 0.25           ┆ 0.125        ┆ 0.375        ┆ 0.2            ┆ 0.375          │
# └─────────┴───────┴────────────────┴──────────────┴──────────────┴────────────────┴────────────────┘
# AVERAGE for score 66: rank 2.0 / 8 = 0.25
# MIN for score 66:     rank 1   / 8 = 0.125
# MAX for score 66:     rank 3   / 8 = 0.375
# DENSE for score 66:   rank 1   / 5 distinct scores = 0.2
# ORDINAL for score 66: Freddy=1/8, George=2/8, Hannah=3/8

# Percentage ranks with null values
print(
    lf_nulls
    .with_columns(
        (pl.col("score").rank(method="average") / pl.len()).alias("pct_all_rows"),
        (pl.col("score").rank(method="average") / pl.count("score")).alias("pct_non_null"),
    )
    .collect()
)
# shape: (5, 4)
# ┌─────────┬───────┬──────────────┬──────────────┐
# │ name    ┆ score ┆ pct_all_rows ┆ pct_non_null │
# │ ---     ┆ ---   ┆ ---          ┆ ---          │
# │ str     ┆ i64   ┆ f64          ┆ f64          │
# ╞═════════╪═══════╪══════════════╪══════════════╡
# │ Alice   ┆ 85    ┆ 0.4          ┆ 0.666667     │
# │ Bob     ┆ null  ┆ null         ┆ null         │
# │ Charlie ┆ 78    ┆ 0.2          ┆ 0.333333     │
# │ David   ┆ 92    ┆ 0.6          ┆ 1.0          │
# │ Eva     ┆ null  ┆ null         ┆ null         │
# └─────────┴───────┴──────────────┴──────────────┘
# Polars preserves null ranks as null.
# pct_all_rows divides by 5 rows.
# pct_non_null divides by 3 non-null scores.

##------------------##
## Descending ranks ##
##------------------##

print(
    lf_unrank
    .with_columns(
        pl.col("score").rank(method="dense", descending=True).alias("rank_highest_score_1")
    )
    .collect()
)
# shape: (8, 3)
# ┌─────────┬───────┬──────────────────────┐
# │ name    ┆ score ┆ rank_highest_score_1 │
# │ ---     ┆ ---   ┆ ---                  │
# │ str     ┆ i64   ┆ u32                  │
# ╞═════════╪═══════╪══════════════════════╡
# │ Alice   ┆ 85    ┆ 4                    │
# │ Bob     ┆ 92    ┆ 1                    │
# │ Charlie ┆ 85    ┆ 4                    │
# │ David   ┆ 88    ┆ 3                    │
# │ Eva     ┆ 90    ┆ 2                    │
# │ Freddy  ┆ 66    ┆ 5                    │
# │ George  ┆ 66    ┆ 5                    │
# │ Hannah  ┆ 66    ┆ 5                    │
# └─────────┴───────┴──────────────────────┘
# score 92 -> rank 1
# score 90 -> rank 2
# score 88 -> rank 3
# score 85 -> rank 4
# score 66 -> rank 5

##------------------##
## Group-wise ranks ##
##------------------##
'''
Use .over("group_column") for rankings within groups.
This is similar to pandas groupby(...)["score"].rank(...).
'''

lf_scores = pl.LazyFrame(
    {
        "name": ["Alice", "Bob", "Charlie", "David", "Eva", "Freddy"],
        "subject": ["Math", "Math", "Math", "English", "English", "English"],
        "score": [85, 92, 85, 88, 90, 88],
    }
)

print(
    lf_scores
    .with_columns(
        pl.col("score").rank(method="dense", descending=True).over("subject").alias("rank_in_subject")
    )
    .collect()
)
# shape: (6, 4)
# ┌─────────┬─────────┬───────┬─────────────────┐
# │ name    ┆ subject ┆ score ┆ rank_in_subject │
# │ ---     ┆ ---     ┆ ---   ┆ ---             │
# │ str     ┆ str     ┆ i64   ┆ u32             │
# ╞═════════╪═════════╪═══════╪═════════════════╡
# │ Alice   ┆ Math    ┆ 85    ┆ 2               │
# │ Bob     ┆ Math    ┆ 92    ┆ 1               │
# │ Charlie ┆ Math    ┆ 85    ┆ 2               │
# │ David   ┆ English ┆ 88    ┆ 2               │
# │ Eva     ┆ English ┆ 90    ┆ 1               │
# │ Freddy  ┆ English ┆ 88    ┆ 2               │
# └─────────┴─────────┴───────┴─────────────────┘
# Math:    Bob 92 -> 1, Alice/Charlie 85 -> 2
# English: Eva 90 -> 1, David/Freddy 88 -> 2

##-----------------------##
## Rank multiple columns ##
##-----------------------##
'''
If you have several numeric columns and want to rank each column independently,
use expression expansion with pl.col([...]).rank().
'''

lf_multi_scores = pl.LazyFrame(
    {
        "student": ["Alice", "Bob", "Charlie"],
        "math": [85, 92, 85],
        "english": [90, 88, 95],
    }
)

print(
    lf_multi_scores
    .with_columns(
        pl.col(["math", "english"]).rank(method="average").name.suffix("_rank")
    )
    .collect()
)
# shape: (3, 5)
# ┌─────────┬──────┬─────────┬───────────┬──────────────┐
# │ student ┆ math ┆ english ┆ math_rank ┆ english_rank │
# │ ---     ┆ ---  ┆ ---     ┆ ---       ┆ ---          │
# │ str     ┆ i64  ┆ i64     ┆ f64       ┆ f64          │
# ╞═════════╪══════╪═════════╪═══════════╪══════════════╡
# │ Alice   ┆ 85   ┆ 90      ┆ 1.5       ┆ 2.0          │
# │ Bob     ┆ 92   ┆ 88      ┆ 3.0       ┆ 1.0          │
# │ Charlie ┆ 85   ┆ 95      ┆ 1.5       ┆ 3.0          │
# └─────────┴──────┴─────────┴───────────┴──────────────┘
# Adds math_rank and english_rank.
