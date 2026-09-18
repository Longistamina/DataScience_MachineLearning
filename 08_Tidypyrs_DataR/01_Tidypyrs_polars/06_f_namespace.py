'''
Tidypyrs provides the convenient `f` namespace for constructing Polars
expressions and referring to the frame currently executing a verb.

Some forms return an immediate `pl.Expr`; others return a deferred operation
that is resolved only after `select()` or `mutate()` supplies the current
DataFrame/LazyFrame.

1. `f.x` -> `pl.col("x")`
2. `f("x")` and `f("x", "y", "z")`
3. `f["x"]` and `f["x", "y", "z"]`
4. `f.all()` and the Polars expression namespace
5. `f.colnames` and automatic deferred method forwarding
6. `f.select("x")` and `f.sl("x")` for selecting from the current frame later
7. `f.pull("x")` for extracting concrete values later
8. Deferred operations in sequential mutation
9. `f` expressions with NumPy functions
'''

from pathlib import Path

import numpy as np
import tidypyrs as tp  # noqa: I001
from tidypyrs import f

tp.Config(tbl_width_chars=120, tbl_rows=5)
data_dir = next(Path("/home").glob("**/DataScience*/data"))

tl_pokemon = (
    tp.scan_csv(data_dir/"pokemon.csv")
    .select(f.all().name.to_lowercase().name.replace(r"\s+", "_").name.replace(".", "", literal=True))
    .mutate(
        f("type_1", "type_2").pipe(tp.as_categorical)
    )
)

print(tl_pokemon.collect())
# shape: (800, 13)
# ┌─────┬────────────────────┬─────────┬────────┬───┬────────┬───────┬────────────┬───────────┐
# │ #   ┆ name               ┆ type_1  ┆ type_2 ┆ … ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ --- ┆ ---                ┆ ---     ┆ ---    ┆   ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ i64 ┆ str                ┆ cat     ┆ cat    ┆   ┆ i64    ┆ i64   ┆ i64        ┆ bool      │
# ╞═════╪════════════════════╪═════════╪════════╪═══╪════════╪═══════╪════════════╪═══════════╡
# │ 1   ┆ Bulbasaur          ┆ Grass   ┆ Poison ┆ … ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ 2   ┆ Ivysaur            ┆ Grass   ┆ Poison ┆ … ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ 3   ┆ Venusaur           ┆ Grass   ┆ Poison ┆ … ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ …   ┆ …                  ┆ …       ┆ …      ┆ … ┆ …      ┆ …     ┆ …          ┆ …         │
# │ 720 ┆ HoopaHoopa Unbound ┆ Psychic ┆ Dark   ┆ … ┆ 130    ┆ 80    ┆ 6          ┆ true      │
# │ 721 ┆ Volcanion          ┆ Fire    ┆ Water  ┆ … ┆ 90     ┆ 70    ┆ 6          ┆ true      │
# └─────┴────────────────────┴─────────┴────────┴───┴────────┴───────┴────────────┴───────────┘

print(tl_pokemon.collect_schema())
# Schema({'#': Int64, 'name': String, 'type_1': Categorical, 'type_2': Categorical, 'total': Int64, 'hp': Int64, 'attack': Int64,
# 'defense': Int64, 'sp_atk': Int64, 'sp_def': Int64, 'speed': Int64, 'generation': Int64, 'legendary': Boolean})

# =========================================================================================
# 1. `f.x` -> `pl.col("x")`
# =========================================================================================

print(
    tl_pokemon.select(f.total)
    .collect()
)
# shape: (800, 1)
# ┌───────┐
# │ total │
# │ ---   │
# │ i64   │
# ╞═══════╡
# │ 318   │
# │ 405   │
# │ 525   │
# │ …     │
# │ 680   │
# │ 600   │
# └───────┘

print(
    tl_pokemon.select(f.name)
    .collect()
)
# shape: (800, 1)
# ┌────────────────────┐
# │ name               │
# │ ---                │
# │ str                │
# ╞════════════════════╡
# │ Bulbasaur          │
# │ Ivysaur            │
# │ Venusaur           │
# │ …                  │
# │ HoopaHoopa Unbound │
# │ Volcanion          │
# └────────────────────┘

# =========================================================================================
# 2. `f("x")` and `f("x", "y", "z")`
# =========================================================================================

print(
    tl_pokemon
    .select(f("generation"))
    .collect()
)
# shape: (800, 1)
# ┌────────────┐
# │ generation │
# │ ---        │
# │ enum       │
# ╞════════════╡
# │ 1          │
# │ 1          │
# │ 1          │
# │ …          │
# │ 6          │
# │ 6          │
# └────────────┘

print(
    tl_pokemon
    .select(f("name", "hp", "speed"))
    .mutate(
        f("hp", "speed").mul(2).name.suffix("_doubble")
    )
    .collect()
)
# shape: (800, 5)
# ┌────────────────────┬─────┬───────┬────────────┬───────────────┐
# │ name               ┆ hp  ┆ speed ┆ hp_doubble ┆ speed_doubble │
# │ ---                ┆ --- ┆ ---   ┆ ---        ┆ ---           │
# │ str                ┆ i64 ┆ i64   ┆ i64        ┆ i64           │
# ╞════════════════════╪═════╪═══════╪════════════╪═══════════════╡
# │ Bulbasaur          ┆ 45  ┆ 45    ┆ 90         ┆ 90            │
# │ Ivysaur            ┆ 60  ┆ 60    ┆ 120        ┆ 120           │
# │ Venusaur           ┆ 80  ┆ 80    ┆ 160        ┆ 160           │
# │ …                  ┆ …   ┆ …     ┆ …          ┆ …             │
# │ HoopaHoopa Unbound ┆ 80  ┆ 80    ┆ 160        ┆ 160           │
# │ Volcanion          ┆ 80  ┆ 70    ┆ 160        ┆ 140           │
# └────────────────────┴─────┴───────┴────────────┴───────────────┘

# =========================================================================================
# 3. `f["x"]` and `f["x", "y", "z"]`
# =========================================================================================

print(
    tl_pokemon
    .select(f["legendary"])
    .collect()
)
# shape: (800, 1)
# ┌───────────┐
# │ legendary │
# │ ---       │
# │ bool      │
# ╞═══════════╡
# │ false     │
# │ false     │
# │ false     │
# │ …         │
# │ true      │
# │ true      │
# └───────────┘

print(
    tl_pokemon
    .select(f["name", "attack", "defense"])
    .mutate(
        f("attack", "defense").truediv(2).name.suffix("_half")
    )
    .collect()
)
# shape: (800, 5)
# ┌────────────────────┬────────┬─────────┬─────────────┬──────────────┐
# │ name               ┆ attack ┆ defense ┆ attack_half ┆ defense_half │
# │ ---                ┆ ---    ┆ ---     ┆ ---         ┆ ---          │
# │ str                ┆ i64    ┆ i64     ┆ f64         ┆ f64          │
# ╞════════════════════╪════════╪═════════╪═════════════╪══════════════╡
# │ Bulbasaur          ┆ 49     ┆ 49      ┆ 24.5        ┆ 24.5         │
# │ Ivysaur            ┆ 62     ┆ 63      ┆ 31.0        ┆ 31.5         │
# │ Venusaur           ┆ 82     ┆ 83      ┆ 41.0        ┆ 41.5         │
# │ …                  ┆ …      ┆ …       ┆ …           ┆ …         │
# │ HoopaHoopa Unbound ┆ 160    ┆ 60      ┆ 80.0        ┆ 30.0         │
# │ Volcanion          ┆ 110    ┆ 120     ┆ 55.0        ┆ 60.0         │
# └────────────────────┴────────┴─────────┴─────────────┴──────────────┘

# =========================================================================================
# 4. `f.all()` and the Polars expression namespace
# =========================================================================================
'''
`f.all()` is equivalent to `pl.all()`. Because it immediately returns a normal
Polars expression, all expression namespaces remain available. The example
below transforms every column name without listing the columns individually.
'''

print(
    tl_pokemon
    .select(
        f.all()
        .name.to_uppercase()
        .name.replace("_", " ", literal=True)
    )
    .slice_head(3)
    .collect()
)
# shape: (3, 13)
# ┌─────┬───────────┬────────┬────────┬───┬────────┬───────┬────────────┬───────────┐
# │ #   ┆ NAME      ┆ TYPE 1 ┆ TYPE 2 ┆ … ┆ SP DEF ┆ SPEED ┆ GENERATION ┆ LEGENDARY │
# │ --- ┆ ---       ┆ ---    ┆ ---    ┆   ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ i64 ┆ str       ┆ cat    ┆ cat    ┆   ┆ i64    ┆ i64   ┆ i64        ┆ bool      │
# ╞═════╪═══════════╪════════╪════════╪═══╪════════╪═══════╪════════════╪═══════════╡
# │ 1   ┆ Bulbasaur ┆ Grass  ┆ Poison ┆ … ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ 2   ┆ Ivysaur   ┆ Grass  ┆ Poison ┆ … ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ 3   ┆ Venusaur  ┆ Grass  ┆ Poison ┆ … ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# └─────┴───────────┴────────┴────────┴───┴────────┴───────┴────────────┴───────────┘

# =========================================================================================
# 5. `f.colnames` and automatic deferred method forwarding
# =========================================================================================
'''
Unlike `f.all()`, `f.colnames` needs to know the current frame. It therefore
resolves later to a Polars Series containing the column names.

Indexing, attribute access, and method calls are automatically forwarded to
that future Series. Tidypyrs does not need to implement `sort()`, `filter()`,
`head()`, and other Series methods separately.
'''

# Select alternating columns. `[::2]` is applied after `f.colnames` resolves.
print(
    tl_pokemon
    .select(f.colnames[::2])
    .slice_head(3)
    .collect()
)
# shape: (3, 7)
# ┌─────┬────────┬───────┬────────┬────────┬───────┬───────────┐
# │ #   ┆ type_1 ┆ total ┆ attack ┆ sp_atk ┆ speed ┆ legendary │
# │ --- ┆ ---    ┆ ---   ┆ ---    ┆ ---    ┆ ---   ┆ ---       │
# │ i64 ┆ cat    ┆ i64   ┆ i64    ┆ i64    ┆ i64   ┆ bool      │
# ╞═════╪════════╪═══════╪════════╪════════╪═══════╪═══════════╡
# │ 1   ┆ Grass  ┆ 318   ┆ 49     ┆ 65     ┆ 45    ┆ false     │
# │ 2   ┆ Grass  ┆ 405   ┆ 62     ┆ 80     ┆ 60    ┆ false     │
# │ 3   ┆ Grass  ┆ 525   ┆ 82     ┆ 100    ┆ 80    ┆ false     │
# └─────┴────────┴───────┴────────┴────────┴───────┴───────────┘


# Sort the future column-name Series, then select columns in that order.
print(
    tl_pokemon
    .select(f.colnames.sort())
    .slice_head(3)
    .collect()
)
# shape: (3, 13)
# ┌─────┬────────┬─────────┬────────────┬───┬───────┬───────┬────────┬────────┐
# │ #   ┆ attack ┆ defense ┆ generation ┆ … ┆ speed ┆ total ┆ type_1 ┆ type_2 │
# │ --- ┆ ---    ┆ ---     ┆ ---        ┆   ┆ ---   ┆ ---   ┆ ---    ┆ ---    │
# │ i64 ┆ i64    ┆ i64     ┆ i64        ┆   ┆ i64   ┆ i64   ┆ cat    ┆ cat    │
# ╞═════╪════════╪═════════╪════════════╪═══╪═══════╪═══════╪════════╪════════╡
# │ 1   ┆ 49     ┆ 49      ┆ 1          ┆ … ┆ 45    ┆ 318   ┆ Grass  ┆ Poison │
# │ 2   ┆ 62     ┆ 63      ┆ 1          ┆ … ┆ 60    ┆ 405   ┆ Grass  ┆ Poison │
# │ 3   ┆ 82     ┆ 83      ┆ 1          ┆ … ┆ 80    ┆ 525   ┆ Grass  ┆ Poison │
# └─────┴────────┴─────────┴────────────┴───┴───────┴───────┴────────┴────────┘

# Deferred operations can be chained. Both the Series being filtered and the
# Boolean mask are resolved against the same current frame.
print(
    tl_pokemon
    .select(
        f.colnames.filter(f.colnames.str.contains(r"^(name|type|generation)"))
    )
    .slice_head(3)
    .collect()
)
# shape: (3, 4)
# ┌───────────┬────────┬────────┬────────────┐
# │ name      ┆ type_1 ┆ type_2 ┆ generation │
# │ ---       ┆ ---    ┆ ---    ┆ ---        │
# │ str       ┆ cat    ┆ cat    ┆ i64        │
# ╞═══════════╪════════╪════════╪════════════╡
# │ Bulbasaur ┆ Grass  ┆ Poison ┆ 1          │
# │ Ivysaur   ┆ Grass  ┆ Poison ┆ 1          │
# │ Venusaur  ┆ Grass  ┆ Poison ┆ 1          │
# └───────────┴────────┴────────┴────────────┘

# =========================================================================================
# 6. `f.select("x")` and `f.sl("x")` for selecting from the current frame later
# =========================================================================================
'''
`f.select()` describes a selection from the frame that will be executing the
verb. It returns a deferred one-column frame here because no current frame is
available while Python is evaluating the arguments to `mutate()`.

`tp.as_enum()` and its alias `tp.as_ordered()` are defer-aware. They can accept
that future one-column frame, infer its observed categories, and return an Enum
expression when `mutate()` eventually supplies the frame.

Inferring categories from a LazyFrame requires an internal collection. Supply
explicit categories when preserving full laziness is more important.

-----------------------------------------------------------------------------

`f.sl()` is the short form of `f.select()`
'''

##------------##
## f.select() ##
##------------##

# with `tp.as_enum`
print(
    tl_pokemon
    .mutate(
        generation_enum = tp.as_enum(f.select("generation"))
    )
    .select(f("name", "generation", "generation_enum"))
    .collect()
)
# shape: (800, 3)
# ┌────────────────────┬────────────┬─────────────────┐
# │ name               ┆ generation ┆ generation_enum │
# │ ---                ┆ ---        ┆ ---             │
# │ str                ┆ i64        ┆ enum            │
# ╞════════════════════╪════════════╪═════════════════╡
# │ Bulbasaur          ┆ 1          ┆ 1               │
# │ Ivysaur            ┆ 1          ┆ 1               │
# │ Venusaur           ┆ 1          ┆ 1               │
# │ …                  ┆ …          ┆ …               │
# │ HoopaHoopa Unbound ┆ 6          ┆ 6               │
# │ Volcanion          ┆ 6          ┆ 6               │
# └────────────────────┴────────────┴─────────────────┘

# with `tp.as_ordered`
print(
    tl_pokemon
    .mutate(
        generation_ordered = tp.as_ordered(f.select("generation"), reverse=True)
    )
    .select(f("name", "generation", "generation_ordered"))
    .collect()
)
# shape: (800, 3)
# ┌────────────────────┬────────────┬────────────────────┐
# │ name               ┆ generation ┆ generation_ordered │
# │ ---                ┆ ---        ┆ ---                │
# │ str                ┆ i64        ┆ enum               │
# ╞════════════════════╪════════════╪════════════════════╡
# │ Bulbasaur          ┆ 1          ┆ 1                  │
# │ Ivysaur            ┆ 1          ┆ 1                  │
# │ Venusaur           ┆ 1          ┆ 1                  │
# │ …                  ┆ …          ┆ …                  │
# │ HoopaHoopa Unbound ┆ 6          ┆ 6                  │
# │ Volcanion          ┆ 6          ┆ 6                  │
# └────────────────────┴────────────┴────────────────────┘

##--------##
## f.sl() ##
##--------##

# with `tp.as_enum`
print(
    tl_pokemon
    .mutate(
        generation_enum = tp.as_enum(f.sl("generation"))
    )
    .select(f("name", "generation", "generation_enum"))
    .collect()
)

# with `tp.as_ordered`
print(
    tl_pokemon
    .mutate(
        generation_ordered = tp.as_ordered(f.sl("generation"), reverse=True)
    )
    .select(f("name", "generation", "generation_ordered"))
    .collect()
)

# =========================================================================================
# 7. `f.pull("x")` for extracting concrete values later
# =========================================================================================
'''
`f.pull()` defers extracting one column as a concrete Polars Series. This is
useful whenever a function needs actual values rather than a column expression.

Here it supplies observed categories to `tp.as_enum()` and `tp.as_ordered()`.
Like `f.colnames`, its future Series supports automatic deferred method calls,
so category preparation can be chained directly onto `f.pull()`.
'''

##------------------------------------------##
## f("col").pipe(tp.as_enum, f.pull("col")) ##
##------------------------------------------##

# with `tp.as_enum`
print(
    tl_pokemon
    .mutate(
        f("generation").pipe(tp.as_enum, f.pull("generation")).alias("generation_enum")
    )
    .select(f("name", "generation", "generation_enum"))
    .collect()
)
# shape: (800, 3)
# ┌────────────────────┬────────────┬─────────────────┐
# │ name               ┆ generation ┆ generation_enum │
# │ ---                ┆ ---        ┆ ---             │
# │ str                ┆ i64        ┆ enum            │
# ╞════════════════════╪════════════╪═════════════════╡
# │ Bulbasaur          ┆ 1          ┆ 1               │
# │ Ivysaur            ┆ 1          ┆ 1               │
# │ Venusaur           ┆ 1          ┆ 1               │
# │ …                  ┆ …          ┆ …               │
# │ HoopaHoopa Unbound ┆ 6          ┆ 6               │
# │ Volcanion          ┆ 6          ┆ 6               │
# └────────────────────┴────────────┴─────────────────┘

# with `tp.as_ordered`
print(
    tl_pokemon
    .mutate(
        f("generation").pipe(tp.as_ordered, f.pull("generation"), reverse=True).alias("generation_ordered")
    )
    .select(f("name", "generation", "generation_ordered"))
    .collect()
)
# shape: (800, 3)
# ┌────────────────────┬────────────┬────────────────────┐
# │ name               ┆ generation ┆ generation_ordered │
# │ ---                ┆ ---        ┆ ---                │
# │ str                ┆ i64        ┆ enum               │
# ╞════════════════════╪════════════╪════════════════════╡
# │ Bulbasaur          ┆ 1          ┆ 1                  │
# │ Ivysaur            ┆ 1          ┆ 1                  │
# │ Venusaur           ┆ 1          ┆ 1                  │
# │ …                  ┆ …          ┆ …                  │
# │ HoopaHoopa Unbound ┆ 6          ┆ 6                  │
# │ Volcanion          ┆ 6          ┆ 6                  │
# └────────────────────┴────────────┴────────────────────┘

##----------------------------------------------------------------##
## automatic forwarding on the future Series returned by f.pull() ##
##----------------------------------------------------------------##

print(
    tl_pokemon
    .mutate(
        generation_enum=tp.as_enum(
            f.generation,
            categories=f.pull("generation").unique().sort(),
        )
    )
    .select(f("name", "generation", "generation_enum"))
    .slice_head(3)
    .collect()
)
# shape: (3, 3)
# ┌───────────┬────────────┬─────────────────┐
# │ name      ┆ generation ┆ generation_enum │
# │ ---       ┆ ---        ┆ ---             │
# │ str       ┆ i64        ┆ enum            │
# ╞═══════════╪════════════╪═════════════════╡
# │ Bulbasaur ┆ 1          ┆ 1               │
# │ Ivysaur   ┆ 1          ┆ 1               │
# │ Venusaur  ┆ 1          ┆ 1               │
# └───────────┴────────────┴─────────────────┘

##---------------------------------------------------##
## mutate(new_col = tp.as_enum("col", f.pull("col")) ##
##---------------------------------------------------##

# with `tp.as_enum`
print(
    tl_pokemon
    .mutate(
        generation_enum = tp.as_enum("generation", f.pull("generation"))
    )
    .select(f("name", "generation", "generation_enum"))
    .collect()
)
# shape: (800, 3)
# ┌────────────────────┬────────────┬─────────────────┐
# │ name               ┆ generation ┆ generation_enum │
# │ ---                ┆ ---        ┆ ---             │
# │ str                ┆ i64        ┆ enum            │
# ╞════════════════════╪════════════╪═════════════════╡
# │ Bulbasaur          ┆ 1          ┆ 1               │
# │ Ivysaur            ┆ 1          ┆ 1               │
# │ Venusaur           ┆ 1          ┆ 1               │
# │ …                  ┆ …          ┆ …               │
# │ HoopaHoopa Unbound ┆ 6          ┆ 6               │
# │ Volcanion          ┆ 6          ┆ 6               │
# └────────────────────┴────────────┴─────────────────┘

# with `tp.as_ordered`
print(
    tl_pokemon
    .mutate(
        generation_ordered = tp.as_ordered("generation", f.pull("generation"), reverse=True)
    )
    .select(f("name", "generation", "generation_ordered"))
    .collect()
)
# shape: (800, 3)
# ┌────────────────────┬────────────┬────────────────────┐
# │ name               ┆ generation ┆ generation_ordered │
# │ ---                ┆ ---        ┆ ---                │
# │ str                ┆ i64        ┆ enum               │
# ╞════════════════════╪════════════╪════════════════════╡
# │ Bulbasaur          ┆ 1          ┆ 1                  │
# │ Ivysaur            ┆ 1          ┆ 1                  │
# │ Venusaur           ┆ 1          ┆ 1                  │
# │ …                 ┆ …          ┆ …                 │
# │ HoopaHoopa Unbound ┆ 6          ┆ 6                  │
# │ Volcanion          ┆ 6          ┆ 6                  │
# └────────────────────┴────────────┴────────────────────┘

# =========================================================================================
# 8. Deferred operations in sequential mutation
# =========================================================================================
'''
By default, `mutate(parallel=True)` resolves every expression against the
original input frame. This is efficient for independent expressions.

Use `parallel=False` when a later expression refers to a column created by an
earlier expression in the same `mutate()` call. Expressions are then resolved
and added from left to right.

The named argument `ordered=...` also demonstrates automatic deferred
`.alias("ordered")` handling. The generic `_Deferred` forwarding machinery
records that future method call; no dedicated `_Deferred.alias()` is needed.
'''

print(
    tl_pokemon
    .select(f("name", "generation"))
    .mutate(
        copied_generation=f.generation,
        ordered=tp.as_ordered(f.select("copied_generation")),
        parallel=False,
    )
    .slice_head(3)
    .collect()
)
# shape: (3, 4)
# ┌───────────┬────────────┬───────────────────┬─────────┐
# │ name      ┆ generation ┆ copied_generation ┆ ordered │
# │ ---       ┆ ---        ┆ ---               ┆ ---     │
# │ str       ┆ i64        ┆ i64               ┆ enum    │
# ╞═══════════╪════════════╪═══════════════════╪═════════╡
# │ Bulbasaur ┆ 1          ┆ 1                 ┆ 1       │
# │ Ivysaur   ┆ 1          ┆ 1                 ┆ 1       │
# │ Venusaur  ┆ 1          ┆ 1                 ┆ 1       │
# └───────────┴────────────┴───────────────────┴─────────┘

# This would fail with `parallel=True`: `copied_generation` would not yet
# exist when `f.select("copied_generation")` is resolved.

# =========================================================================================
# 9. `f` expressions with NumPy functions
# =========================================================================================

print(
    tl_pokemon
    .select(f("name", "speed"))
    .mutate(
        speed_log = np.log(f("speed")),
        speed_log10 = np.log10(f("speed")),
    )
    .collect()
)
# shape: (800, 4)
# ┌────────────────────┬───────┬───────────┬─────────────┐
# │ name               ┆ speed ┆ speed_log ┆ speed_log10 │
# │ ---                ┆ ---   ┆ ---       ┆ ---         │
# │ str                ┆ i64   ┆ f64       ┆ f64         │
# ╞════════════════════╪═══════╪═══════════╪═════════════╡
# │ Bulbasaur          ┆ 45    ┆ 3.806662  ┆ 1.653213    │
# │ Ivysaur            ┆ 60    ┆ 4.094345  ┆ 1.778151    │
# │ Venusaur           ┆ 80    ┆ 4.382027  ┆ 1.90309     │
# │ …                  ┆ …     ┆ …         ┆ …           │
# │ HoopaHoopa Unbound ┆ 80    ┆ 4.382027  ┆ 1.90309     │
# │ Volcanion          ┆ 70    ┆ 4.248495  ┆ 1.845098    │
# └────────────────────┴───────┴───────────┴─────────────┘

print(
    tl_pokemon
    .select(f("name", "total"))
    .mutate(
        f("total").pipe(np.sin).alias("total_sin"),
        f("total").pipe(np.cos).alias("total_cos"),
    )
    .collect()
)
# shape: (800, 4)
# ┌────────────────────┬───────┬───────────┬───────────┐
# │ name               ┆ total ┆ total_sin ┆ total_cos │
# │ ---                ┆ ---   ┆ ---       ┆ ---       │
# │ str                ┆ i64   ┆ f64       ┆ f64       │
# ╞════════════════════╪═══════╪═══════════╪═══════════╡
# │ Bulbasaur          ┆ 318   ┆ -0.643561 ┆ -0.765395 │
# │ Ivysaur            ┆ 405   ┆ 0.262346  ┆ -0.964974 │
# │ Venusaur           ┆ 525   ┆ -0.346678 ┆ -0.937984 │
# │ …                  ┆ …     ┆ …         ┆ …         │
# │ HoopaHoopa Unbound ┆ 680   ┆ 0.988041  ┆ 0.154192  │
# │ Volcanion          ┆ 600   ┆ 0.044182  ┆ -0.999023 │
# └────────────────────┴───────┴───────────┴───────────┘

print(
    tl_pokemon
    .select(
        f("total").map_batches(lambda s: np.mean(s.to_numpy()), return_dtype=tp.Float64, returns_scalar=True).alias("total_mean"),
        f("hp").map_batches(lambda s: np.max(s.to_numpy()), return_dtype=tp.Float64, returns_scalar=True).alias("hp_max")
    )
    .collect()
)
# shape: (1, 2)
# ┌────────────┬────────┐
# │ total_mean ┆ hp_max │
# │ ---        ┆ ---    │
# │ f64        ┆ f64    │
# ╞════════════╪════════╡
# │ 435.1025   ┆ 255.0  │
# └────────────┴────────┘
