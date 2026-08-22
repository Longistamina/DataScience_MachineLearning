'''
This file introduces Polars group-by objects and the closest Polars equivalents
for common group object inspection tasks.

Important distinction:
Polars DOES have group-by objects:
    + DataFrame.group_by(...) returns an eager GroupBy object.
    + LazyFrame.group_by(...) returns a lazy LazyGroupBy object.

However, Polars group-by objects are not designed like pandas groupby objects.
They do NOT expose pandas-style convenience attributes such as:
    + group_obj.groups
    + group_obj.indices
    + group_obj.ngroups
    + group_obj.get_group(...)

Instead, Polars usually expresses these ideas as normal DataFrame/LazyFrame
queries:
    + group names                 -> .select(...).unique()
    + row indices per group       -> .with_row_index(...).group_by(...).agg(...)
    + number of groups            -> .select(pl.col(...).n_unique())
    + iterate over groups         -> eager DataFrame.group_by(...) is iterable
    + select a specific group     -> .filter(...)

The main idea:
Polars is expression/query-first, not object-attribute-first.
'''

import polars as pl
from polars import selectors as cs
from polars import col as c
from pathlib import Path

# Optional display settings
pl.Config.set_tbl_rows(10)
pl.Config.set_tbl_cols(20)
pl.Config.set_float_precision(6)
pl.Config.set_tbl_width_chars(120)


data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))


# =========================================================================================
# 0. Setup Data
# =========================================================================================

lf_pokemon = (
    pl.scan_csv(data_dir / "pokemon.csv")
    .drop('#')
    .rename(lambda name: name.strip()) # remove trailing space characters
    .select(
        pl.all()
        .name.replace(r"\s+", "_") # replace " " or "  " (or more consecutive space characters) with just one "_"
        .name.replace(".", "", literal=True) # replace "." with empty string (remove it), literal=True to deactive regex
    )
    .with_columns(cs.string().exclude("Name").cast(pl.Categorical))
    .pipe(lambda lf: lf.with_columns(
        c.Generation.cast(pl.String).cast(pl.Enum(lf.select("Generation").collect().to_series().cast(pl.String).unique().sort())))
    )
)

print(lf_pokemon.head(5).collect())
# shape: (5, 12)
# ┌────────────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Name           ┆ Type_1 ┆ Type_2 ┆ Total ┆ HP  ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---            ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str            ┆ cat    ┆ cat    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞════════════════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Bulbasaur      ┆ Grass  ┆ Poison ┆ 318   ┆ 45  ┆ 49     ┆ 49      ┆ 65     ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ Ivysaur        ┆ Grass  ┆ Poison ┆ 405   ┆ 60  ┆ 62     ┆ 63      ┆ 80     ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ Venusaur       ┆ Grass  ┆ Poison ┆ 525   ┆ 80  ┆ 82     ┆ 83      ┆ 100    ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ VenusaurMega   ┆ Grass  ┆ Poison ┆ 625   ┆ 80  ┆ 100    ┆ 123     ┆ 122    ┆ 120    ┆ 80    ┆ 1          ┆ false     │
# │ Venusaur       ┆        ┆        ┆       ┆     ┆        ┆         ┆        ┆        ┆       ┆            ┆           │
# │ Charmander     ┆ Fire   ┆ null   ┆ 309   ┆ 39  ┆ 52     ┆ 43      ┆ 60     ┆ 50     ┆ 65    ┆ 1          ┆ false     │
# └────────────────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

print(lf_pokemon.collect_schema())
# Schema(
# {'Name': String, 'Type_1': Categorical,
# 'Type_2': Categorical,
# 'Total': Int64, 'HP': Int64, 'Attack': Int64, 'Defense': Int64, 'Sp_Atk': Int64, 'Sp_Def': Int64, 'Speed': Int64,
# 'Generation': Enum(categories=['1', '2', '3', '4', '5', '6']),
# 'Legendary': Boolean})


# We collect once here because several examples below inspect or iterate over
# physical groups. LazyFrame group_by is best for query pipelines, but eager
# DataFrame group_by is needed for Python-level group iteration.
df_pokemon = lf_pokemon.collect()


# =========================================================================================
# 1. Create group-by object
# =========================================================================================
'''
Polars has group-by objects, but they are mainly namespaces for grouped operations.

Eager:
    df.group_by("key")
    df.group_by(["key1", "key2"])

Lazy:
    lf.group_by("key")
    lf.group_by(["key1", "key2"])

The lazy object is useful for optimized query plans. The eager object can also be
iterated over in Python.
'''

##----------------------------------------------------##
## Eager: DataFrame.group_by("key") and multiple keys ##
##----------------------------------------------------##

grouped_single_key = df_pokemon.group_by("Type_1")
print(grouped_single_key)
# <polars.dataframe.group_by.GroupBy object at ...>

grouped_multi_keys = df_pokemon.group_by(["Type_1", "Type_2"])
print(grouped_multi_keys)
# <polars.dataframe.group_by.GroupBy object at ...>

##---------------------------------------------------##
## Lazy: LazyFrame.group_by("key") and multiple keys ##
##---------------------------------------------------##

lazy_grouped_single_key = lf_pokemon.group_by("Type_1")
print(lazy_grouped_single_key)
# <polars.lazyframe.group_by.LazyGroupBy object at ...>

lazy_grouped_multi_keys = lf_pokemon.group_by(["Type_1", "Type_2"])
print(lazy_grouped_multi_keys)
# <polars.lazyframe.group_by.LazyGroupBy object at ...>


# =========================================================================================
# 2. Group object attributes: Polars-style equivalents
# =========================================================================================
'''
Polars does not expose pandas-style attributes like:
    group_obj.groups
    group_obj.indices
    group_obj.ngroups

Instead, compute those structures explicitly as DataFrames.
This is more verbose, but it keeps the operation visible, composable, and lazy.
'''

##--------------------##
## Group names / keys ##
##--------------------##
'''
Equivalent idea:
    Get the unique group names.
'''

print(
    lf_pokemon
    .select("Type_1")
    .unique()
    .sort("Type_1")
    .collect()
)
# shape: (18, 1)
# ┌──────────┐
# │ Type_1   │
# │ ---      │
# │ cat      │
# ╞══════════╡
# │ Bug      │
# │ Dark     │
# │ Dragon   │
# │ ...      │
# └──────────┘

print(
    lf_pokemon
    .select("Type_1", "Type_2")
    .drop_nulls(["Type_1", "Type_2"])
    .unique()
    .sort("Type_1", "Type_2")
    .collect()
)
# shape: (..., 2)
# ┌────────┬──────────┐
# │ Type_1 ┆ Type_2   │
# │ ---    ┆ ---      │
# │ cat    ┆ cat      │
# ╞════════╪══════════╡
# │ Bug    ┆ Electric │
# │ Bug    ┆ Fighting │
# │ Bug    ┆ Fire     │
# │ ...    ┆ ...      │
# └────────┴──────────┘

##-----------------------##
## Row indices per group ##
##-----------------------##
'''
Equivalent idea:
    group_obj.indices

Polars does not store this as an attribute. Add a row number column, then collect
those row numbers into a list per group.
'''

print(
    lf_pokemon
    .with_row_index("row_index")
    .group_by("Type_1")
    .agg(
        c("row_index").alias("row_indices")
    )
    .sort("Type_1")
    .collect()
)
# shape: (18, 2)
# ┌──────────┬────────────────────────┐
# │ Type_1   ┆ row_indices            │
# │ ---      ┆ ---                    │
# │ cat      ┆ list[u32]              │
# ╞══════════╪════════════════════════╡
# │ Bug      ┆ [13, 14, 15, ...]      │
# │ Dark     ┆ [212, 213, 233, ...]   │
# │ Dragon   ┆ [159, 160, 161, ...]   │
# │ ...      ┆ ...                    │
# └──────────┴────────────────────────┘

print(
    lf_pokemon
    .with_row_index("row_index")
    .drop_nulls(["Type_1", "Type_2"])
    .group_by(["Type_1", "Type_2"])
    .agg(
        pl.col("row_index").alias("row_indices")
    )
    .sort("Type_1", "Type_2")
    .collect()
)
# shape: (..., 3)
# ┌────────┬──────────┬─────────────┐
# │ Type_1 ┆ Type_2   ┆ row_indices │
# │ ---    ┆ ---      ┆ ---         │
# │ cat    ┆ cat      ┆ list[u32]   │
# ╞════════╪══════════╪═════════════╡
# │ Bug    ┆ Electric ┆ [656, 657]  │
# │ Bug    ┆ Fighting ┆ [231, 232]  │
# │ Bug    ┆ Fire     ┆ [697, 698]  │
# │ ...    ┆ ...      ┆ ...         │
# └────────┴──────────┴─────────────┘

##------------------##
## Number of groups ##
##------------------##
'''
Equivalent idea:
    group_obj.ngroups

For one key, use n_unique().
For multiple keys, create a struct from the keys and count unique structs.
'''

print(
    lf_pokemon
    .select(
        pl.col("Type_1").n_unique().alias("n_groups_Type_1")
    )
    .collect()
)
# shape: (1, 1)
# ┌─────────────────┐
# │ n_groups_Type_1 │
# │ ---             │
# │ u32             │
# ╞═════════════════╡
# │ 18              │
# └─────────────────┘

print(
    lf_pokemon
    .drop_nulls(["Type_1", "Type_2"])
    .select(
        pl.struct("Type_1", "Type_2").n_unique().alias("n_groups_Type_1_Type_2")
    )
    .collect()
)
# shape: (1, 1)
# ┌────────────────────────┐
# │ n_groups_Type_1_Type_2 │
# │ ---                    │
# │ u32                    │
# ╞════════════════════════╡
# │ 136                    │
# └────────────────────────┘


# =========================================================================================
# 3. Iterate over groups within a GroupBy object
# =========================================================================================
'''
Eager DataFrame.group_by(...) objects are iterable.
LazyFrame.group_by(...) objects are not for Python-level iteration because they
represent a query plan, not materialized groups.

Important detail:
Polars returns group names as tuples, even for a single grouping key.
For example, the Fire group name appears as ('Fire',), not just 'Fire'.
'''

##--------------------------------##
## Iterate over single-key groups ##
##--------------------------------##

for i, (name, group) in enumerate(df_pokemon.group_by("Type_1", maintain_order=True)):
    print(f"Group name: {name}")
    print(group.head(3))
    print("=" * 99)

    # Printing all groups can be long, so stop early for demonstration.
    if i == 3:
        break

# Group name: ('Grass',)
# shape: (3, 12)
# ┌───────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Name      ┆ Type_1 ┆ Type_2 ┆ Total ┆ HP  ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---       ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str       ┆ cat    ┆ cat    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞═══════════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Bulbasaur ┆ Grass  ┆ Poison ┆ 318   ┆ 45  ┆ 49     ┆ 49      ┆ 65     ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ Ivysaur   ┆ Grass  ┆ Poison ┆ 405   ┆ 60  ┆ 62     ┆ 63      ┆ 80     ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ Venusaur  ┆ Grass  ┆ Poison ┆ 525   ┆ 80  ┆ 82     ┆ 83      ┆ 100    ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# └───────────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘
# ===================================================================================================
# Group name: ('Fire',)
# shape: (3, 12)
# ┌────────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Name       ┆ Type_1 ┆ Type_2 ┆ Total ┆ HP  ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---        ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str        ┆ cat    ┆ cat    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞════════════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Charmander ┆ Fire   ┆ null   ┆ 309   ┆ 39  ┆ 52     ┆ 43      ┆ 60     ┆ 50     ┆ 65    ┆ 1          ┆ false     │
# │ Charmeleon ┆ Fire   ┆ null   ┆ 405   ┆ 58  ┆ 64     ┆ 58      ┆ 80     ┆ 65     ┆ 80    ┆ 1          ┆ false     │
# │ Charizard  ┆ Fire   ┆ Flying ┆ 534   ┆ 78  ┆ 84     ┆ 78      ┆ 109    ┆ 85     ┆ 100   ┆ 1          ┆ false     │
# └────────────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘
# ===================================================================================================
# Group name: ('Water',)
# shape: (3, 12)
# ┌───────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Name      ┆ Type_1 ┆ Type_2 ┆ Total ┆ HP  ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---       ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str       ┆ cat    ┆ cat    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞═══════════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Squirtle  ┆ Water  ┆ null   ┆ 314   ┆ 44  ┆ 48     ┆ 65      ┆ 50     ┆ 64     ┆ 43    ┆ 1          ┆ false     │
# │ Wartortle ┆ Water  ┆ null   ┆ 405   ┆ 59  ┆ 63     ┆ 80      ┆ 65     ┆ 80     ┆ 58    ┆ 1          ┆ false     │
# │ Blastoise ┆ Water  ┆ null   ┆ 530   ┆ 79  ┆ 83     ┆ 100     ┆ 85     ┆ 105    ┆ 78    ┆ 1          ┆ false     │
# └───────────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

##-------------------------------##
## Iterate over multi-key groups ##
##-------------------------------##

for i, (name, group) in enumerate(
    df_pokemon
    .drop_nulls(["Type_1", "Type_2"])
    .group_by(["Type_1", "Type_2"], maintain_order=True)
):
    print(f"Group name: {name}")
    print(group.head(3))
    print("=" * 99)

    # Printing all groups can be long, so stop early for demonstration.
    if i == 3:
        break

# Group name: ('Grass', 'Poison')
# shape: (3, 12)
# ┌───────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Name      ┆ Type_1 ┆ Type_2 ┆ Total ┆ HP  ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---       ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str       ┆ cat    ┆ cat    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞═══════════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Bulbasaur ┆ Grass  ┆ Poison ┆ 318   ┆ 45  ┆ 49     ┆ 49      ┆ 65     ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ Ivysaur   ┆ Grass  ┆ Poison ┆ 405   ┆ 60  ┆ 62     ┆ 63      ┆ 80     ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ Venusaur  ┆ Grass  ┆ Poison ┆ 525   ┆ 80  ┆ 82     ┆ 83      ┆ 100    ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# └───────────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘
# ===================================================================================================
# Group name: ('Fire', 'Flying')
# shape: (3, 12)
# ┌────────────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Name           ┆ Type_1 ┆ Type_2 ┆ Total ┆ HP  ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---            ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str            ┆ cat    ┆ cat    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞════════════════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Charizard      ┆ Fire   ┆ Flying ┆ 534   ┆ 78  ┆ 84     ┆ 78      ┆ 109    ┆ 85     ┆ 100   ┆ 1          ┆ false     │
# │ CharizardMega  ┆ Fire   ┆ Flying ┆ 634   ┆ 78  ┆ 104    ┆ 78      ┆ 159    ┆ 115    ┆ 100   ┆ 1          ┆ false     │
# │ Charizard Y    ┆        ┆        ┆       ┆     ┆        ┆         ┆        ┆        ┆       ┆            ┆           │
# │ Moltres        ┆ Fire   ┆ Flying ┆ 580   ┆ 90  ┆ 100    ┆ 90      ┆ 125    ┆ 85     ┆ 90    ┆ 1          ┆ true      │
# └────────────────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

##---------------------------------------------------##
## Polars-native alternative: first n rows per group ##
##---------------------------------------------------##
'''
If the goal is just to inspect the first rows of each group, prefer GroupBy.head()
instead of Python-level iteration.
'''

print(
    df_pokemon
    .group_by("Type_1", maintain_order=True)
    .head(3)
)
# shape: (54, 12)
# ┌────────┬────────────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Type_1 ┆ Name           ┆ Type_2 ┆ Total ┆ HP  ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---    ┆ ---            ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ cat    ┆ str            ┆ cat    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞════════╪════════════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Grass  ┆ Bulbasaur      ┆ Poison ┆ 318   ┆ 45  ┆ 49     ┆ 49      ┆ 65     ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ Grass  ┆ Ivysaur        ┆ Poison ┆ 405   ┆ 60  ┆ 62     ┆ 63      ┆ 80     ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ Grass  ┆ Venusaur       ┆ Poison ┆ 525   ┆ 80  ┆ 82     ┆ 83      ┆ 100    ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ Fire   ┆ Charmander     ┆ null   ┆ 309   ┆ 39  ┆ 52     ┆ 43      ┆ 60     ┆ 50     ┆ 65    ┆ 1          ┆ false     │
# │ Fire   ┆ Charmeleon     ┆ null   ┆ 405   ┆ 58  ┆ 64     ┆ 58      ┆ 80     ┆ 65     ┆ 80    ┆ 1          ┆ false     │
# │ …      ┆ …              ┆ …      ┆ …     ┆ …   ┆ …      ┆ …       ┆ …      ┆ …      ┆ …     ┆ …          ┆ …         │
# │ Steel  ┆ SteelixMega    ┆ Ground ┆ 610   ┆ 75  ┆ 125    ┆ 230     ┆ 55     ┆ 95     ┆ 30    ┆ 2          ┆ false     │
# │        ┆ Steelix        ┆        ┆       ┆     ┆        ┆         ┆        ┆        ┆       ┆            ┆           │
# │ Steel  ┆ Skarmory       ┆ Flying ┆ 465   ┆ 65  ┆ 80     ┆ 140     ┆ 40     ┆ 70     ┆ 70    ┆ 2          ┆ false     │
# │ Flying ┆ TornadusIncarn ┆ null   ┆ 580   ┆ 79  ┆ 115    ┆ 70      ┆ 125    ┆ 80     ┆ 111   ┆ 5          ┆ true      │
# │        ┆ ate Forme      ┆        ┆       ┆     ┆        ┆         ┆        ┆        ┆       ┆            ┆           │
# │ Flying ┆ TornadusTheria ┆ null   ┆ 580   ┆ 79  ┆ 100    ┆ 80      ┆ 110    ┆ 90     ┆ 121   ┆ 5          ┆ true      │
# │        ┆ n Forme        ┆        ┆       ┆     ┆        ┆         ┆        ┆        ┆       ┆            ┆           │
# │ Flying ┆ Noibat         ┆ Dragon ┆ 245   ┆ 40  ┆ 30     ┆ 35      ┆ 45     ┆ 40     ┆ 55    ┆ 6          ┆ false     │
# └────────┴────────────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘


# =========================================================================================
# 4. Select specific groups: filter instead
# =========================================================================================
'''
Polars does not use group_obj.get_group(...).

The idiomatic replacement is filtering:
    df.filter(pl.col("key") == value)

This works in both eager and lazy mode.
'''

##------------------------##
## Single group condition ##
##------------------------##

print(
    df_pokemon
    .filter(pl.col("Type_1") == "Fire")
    .head()
)
# shape: (5, 12)
# ┌──────────────────────────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Name                         ┆ Type_1 ┆ Type_2 ┆ Total ┆ HP  ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---                          ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str                          ┆ cat    ┆ cat    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ cat        ┆ bool      │
# ╞══════════════════════════════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Charmander                   ┆ Fire   ┆ null   ┆ 309   ┆ 39  ┆ 52     ┆ 43      ┆ 60     ┆ 50     ┆ 65    ┆ 1          ┆ false     │
# │ Charmeleon                   ┆ Fire   ┆ null   ┆ 405   ┆ 58  ┆ 64     ┆ 58      ┆ 80     ┆ 65     ┆ 80    ┆ 1          ┆ false     │
# │ Charizard                    ┆ Fire   ┆ Flying ┆ 534   ┆ 78  ┆ 84     ┆ 78      ┆ 109    ┆ 85     ┆ 100   ┆ 1          ┆ false     │
# │ CharizardMega Charizard X    ┆ Fire   ┆ Dragon ┆ 634   ┆ 78  ┆ 130    ┆ 111     ┆ 130    ┆ 85     ┆ 100   ┆ 1          ┆ false     │
# │ CharizardMega Charizard Y    ┆ Fire   ┆ Flying ┆ 634   ┆ 78  ┆ 104    ┆ 78      ┆ 159    ┆ 115    ┆ 100   ┆ 1          ┆ false     │
# └──────────────────────────────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

##---------------------##
## Multiple group keys ##
##----------------------##

print(
    df_pokemon
    .filter((pl.col("Type_1") == "Water") & (pl.col("Type_2") == "Flying"))
    .head()
)
# shape: (5, 12)
# ┌──────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Name     ┆ Type_1 ┆ Type_2 ┆ Total ┆ HP  ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---      ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str      ┆ cat    ┆ cat    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ cat        ┆ bool      │
# ╞══════════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Gyarados ┆ Water  ┆ Flying ┆ 540   ┆ 95  ┆ 125    ┆ 79      ┆ 60     ┆ 100    ┆ 81    ┆ 1          ┆ false     │
# │ Mantine  ┆ Water  ┆ Flying ┆ 465   ┆ 65  ┆ 40     ┆ 70      ┆ 80     ┆ 140    ┆ 70    ┆ 2          ┆ false     │
# │ Wingull  ┆ Water  ┆ Flying ┆ 270   ┆ 40  ┆ 30     ┆ 30      ┆ 55     ┆ 30     ┆ 85    ┆ 3          ┆ false     │
# │ Pelipper ┆ Water  ┆ Flying ┆ 430   ┆ 60  ┆ 50     ┆ 100     ┆ 85     ┆ 70     ┆ 65    ┆ 3          ┆ false     │
# │ Mantyke  ┆ Water  ┆ Flying ┆ 345   ┆ 45  ┆ 20     ┆ 50      ┆ 60     ┆ 120    ┆ 50    ┆ 4          ┆ false     │
# └──────────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

##----------------------------------------------##
## Same idea in lazy mode: filter, then collect ##
##----------------------------------------------##

print(
    lf_pokemon
    .filter(pl.col("Type_1") == "Fire")
    .head()
    .collect()
)

print(
    lf_pokemon
    .filter(
        (pl.col("Type_1") == "Water") &
        (pl.col("Type_2") == "Flying")
    )
    .head()
    .collect()
)


# =========================================================================================
# 5. Summary: pandas idea vs Polars
# =========================================================================================
'''
Summary:

1. Create group-by object
   Polars has this:
       df.group_by("Type_1")
       lf.group_by("Type_1")

2. Inspect groups / indices / number of groups
   Polars does not expose these as object attributes.
   Compute them explicitly:
       group names         -> .unique()
       row indices         -> .with_row_index().group_by(...).agg(pl.col("row_index"))
       number of groups    -> .n_unique()

3. Iterate over groups
   Eager DataFrame.group_by(...) is iterable.
   LazyFrame.group_by(...) is not meant for Python-level iteration.

4. Select a specific group
   Polars does not use get_group(...).
   Use .filter(...) instead.

Rule of thumb:
If you want to inspect small physical groups interactively, eager GroupBy iteration
is available. If you want scalable data processing, use LazyFrame expressions,
filters, and aggregations instead of relying on group object internals.
'''
