'''
Boolean Indexing / Boolean Filtering in Polars DataFrames.

In Polars, the central ideas are:
+ `lf.filter(condition)` keeps rows where the condition is True.

##---------------------------##

1. Single Condition Examples with `lf.filter()`
   + Logic Operators: >, <, >=, <=, .is_between(), ==, !=
   + .is_in()
   + String Boolean: .str.contains(), .str.starts_with(), .str.ends_with()
   + DateTime Boolean: month-start and leap-year examples

2. Negation of Condition: ~ (tilde) operator

3. Combine Multiple Conditions:
   + & (and)
   + | (or)
   + Combine & and |
'''

import datetime as dt
from pathlib import Path

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(12)
pl.Config.set_float_precision(2)
pl.Config.set_tbl_width_chars(120)

# =========================================================================================
# 0. Example Data
# =========================================================================================

data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))

# Cleaned version for most examples.
lf_pokemon = (
    pl.scan_csv(data_dir / "pokemon.csv")
    .drop("#")
    .rename(lambda name: name.strip())
    .select(pl.all().name.to_lowercase().name.replace(r"\s+", "_").name.replace(".", "", literal=True))
    .with_columns(
        c("type_1", "type_2").cast(pl.Categorical),
        c("legendary").cast(pl.Boolean),
    )
    .pipe(lambda f: f.with_columns(
        c("generation").cast(pl.String).cast(pl.Enum(f.select("generation").collect().to_series().cast(pl.String).unique().sort())),
    ))                                               # Must use .collect() to realize the dataframe, to access the values for Enum casting
)

print(lf_pokemon.collect().head())
# shape: (5, 12)
# ┌────────────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ name           ┆ type_1 ┆ type_2 ┆ total ┆ hp  ┆ attack ┆ defense ┆ sp_atk ┆ sp_def ┆ speed ┆ generation ┆ legendary │
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

print(lf_pokemon.collect().schema)
# Schema({... 'Type_1': Categorical, 'Type_2': Categorical, 'Generation': Enum, 'Legendary': Boolean})

# =========================================================================================
# 1. Single Condition Examples
# =========================================================================================

##------------------------------------------------------##
## Logic Operators: >, <, >=, <=, .is_between(), ==, != ##
##------------------------------------------------------##

### > (greater than) ###
###   pl.Expr.gt()   ###

# hp greater than 200.
print(lf_pokemon.filter(c.hp > 200).collect()) # c.hp.gt(200)
# Expected rows include Chansey and Blissey.

# sp_atk greater than double attack.
print(
    lf_pokemon
    .filter(c.sp_atk > c.attack * 2) # c.sp_atk.gt(c.attack * 2)
    .select("name", "type_1", "attack", "sp_atk", "generation", "legendary")
    .head(8)
    .collect()
)
# Expected rows include Abra, Kadabra, Alakazam, Mega Alakazam, Magnemite, etc.

### < (less than) ###
###  pl.Expr.lt() ###

# Speed less than 15.
print(
    lf_pokemon
    .filter(c.Speed < 15)
    .select("name", "type_1", "type_2", "speed", "generation", "legendary")
    .collect()
)
# Expected rows include Shuckle, Trapinch, Bonsly, Munchlax, Ferroseed.

# defense less than half of attack.
print(
    lf_pokemon
    .filter(c.defense < c.attack * 0.5)
    .select("name", "type_1", "attack", "defense", "generation", "legendary")
    .head()
    .collect()
)

'''
THE SAME PATTERN WORKS FOR:
+ >=, pl.Expr.ge(): greater than or equal to
+ <=, pl.Expr.le(): less than or equal to
'''

### .is_between() ###
'''
Polars:
    c.Speed.is_between(lower_bound, upper_bound, closed="both")

closed = "both"  : [left, right] or left <= x <= right
closed = "none"  : (left, right) or left < x < right
closed = "left"  : [left, right) or left <= x < right
closed = "right" : (left, right] or left < x <= right
'''

# speed between 5 and 10, inclusive.
print(
    lf_pokemon
    .filter(c.speed.is_between(5, 10))
    .select("name", "type_1", "type_2", "speed", "generation", "legendary")
    .collect()
)

# speed between 5 and 10, excluding the right endpoint.
print(
    lf_pokemon
    .filter(c.speed.is_between(5, 10, closed="left"))
    .select("name", "speed")
    .collect()
)
# The value 10 is excluded because the right endpoint is not closed.

###  == (equal)  ###
### pl.Expr.eq() ###

# type_1 equal to fire.
print(
    lf_pokemon
    .filter(c.type_1 == "fire")
    .select("name", "type_1", "type_2", "total", "generation", "legendary")
    .head(8)
    .collect()
)

# legendary equal to true.
print(
    lf_pokemon
    .filter(c.legendary) # equivalent to ``c.Legendary == True``
    .select("name", "type_1", "type_2", "total", "generation", "legendary")
    .head()
)

### != (not equal) ###
###  pl.Expr.ne()  ###

# type_2 not equal to flying.
# Important: null comparisons evaluate to null in Polars, and filter() discards null predicates.
# therefore this drops rows where type_2 is null.
print(
    lf_pokemon
    .filter(c.type_2 != "flying")
    .select("name", "type_1", "type_2", "generation")
    .head()
    .collect()
)

# If you want pandas-like "not Flying OR missing" behavior, explicitly keep nulls.
print(
    lf_pokemon
    .filter((c.type_2 != "flying") | c.type_2.is_null())
    .select("name", "type_1", "type_2", "generation")
    .head()
    .collect()
)

# generation not equal to 1.
# generation was cast to string then enum, so compare with string labels.
print(
    lf_pokemon
    .filter(c.generation != "1")
    .select("name", "type_1", "type_2", "generation", "legendary")
    .head()
    .collect()
)

##--------------------------##
##          .is_in()        ##
##--------------------------##
'''
Polars:
    c.Type_1.is_in(["Fire", "Water"])
'''

print(
    lf_pokemon
    .filter(c.type_1.is_in(["Fire", "Water"]))
    .select("name", "type_1", "type_2", "generation", "legendary")
    .tail()
    .collect()
)

print(
    lf_pokemon
    .filter(c.generation.is_in(["4", "6"]))
    .select("name", "type_1", "type_2", "generation", "legendary")
    .tail()
    .collect()
)

##--------------------------##
##      String Boolean      ##
##--------------------------##
'''
Polars uses the .str namespace for string operations.

Important:
+ .str.contains(pattern) treats pattern as a regular expression by default.
+ Use literal=True for a plain substring search.
+ Pandas .str.startswith() becomes Polars .str.starts_with().
+ Pandas .str.endswith() becomes Polars .str.ends_with().
'''

# Name contains "Mega".
print(
    lf_pokemon
    .filter(c.name.str.contains("Mega", literal=True))
    .select("name", "type_1", "type_2", "total", "generation", "legendary")
    .head()
    .collect()
)

# Name starts with "Tor".
print(
    lf_pokemon
    .filter(c.name.str.starts_with("Tor"))
    .select("name", "type_1", "type_2", "total", "generation", "legendary")
    .collect()
)

# Name ends with "saur".
print(
    lf_pokemon
    .filter(c.name.str.ends_with("saur"))
    .select("name", "type_1", "type_2", "total", "generation", "legendary")
    .collect()
)

##--------------------------##
##     DateTime Boolean     ##
##--------------------------##
'''
    c.start_date == c.start_date.dt.month_start()

Some temporal boolean methods, such as .dt.is_leap_year(), are available directly.
'''

lf_emp = pl.scan_csv(
    data_dir / "emp.csv",
    try_parse_dates=True,
)

print(lf_emp.collect().schema)
# Schema({'id': Int64, 'name': String, 'salary': Float64, 'start_date': Date, 'dept': String})

# start_date is month start.
print(lf_emp.filter(c.start_date == c.start_date.dt.month_start()).collect())
# Expected row: Rick, 2012-01-01.

# start_date is in a leap year.
print(lf_emp.filter(c.start_date.dt.is_leap_year()).collect())
# Expected row: Rick, 2012-01-01.

# start_date is after 2014-01-01.
print(lf_emp.filter(c.start_date > dt.date(2014, 1, 1)).collect())

# =========================================================================================
# 2. Negation of Condition: ~ (tilde) operator
# =========================================================================================
'''
Use ~ to negate a boolean expression.

Always wrap complex expressions in parentheses before applying ~.
'''

# type_1 is NOT Fire.
print(
    lf_pokemon
    .filter(~(c.type_1 == "Fire"))
    .select("name", "type_1", "type_2", "generation", "legendary")
    .head()
    .collect()
)

# type_2 is NOT in Ground/Ghost.
# Again, null predicates are discarded by filter().
print(
    lf_pokemon
    .filter(~c.type_2.is_in(["Ground", "Ghost"]))
    .select("name", "type_1", "type_2", "generation", "legendary")
    .head()
    .collect()
)

# Keep rows where Type_2 is NOT Ground/Ghost OR Type_2 is null.
print(
    lf_pokemon
    .filter((~c.type_2.is_in(["Ground", "Ghost"])) | c.type_2.is_null())
    .select("name", "type_1", "type_2", "generation", "legendary")
    .head()
    .collect()
)

# =========================================================================================
# 3. Combine Multiple Conditions: & (and), | (or)
# =========================================================================================

##-----------------------##
##       & (and)         ##
##-----------------------##
'''
Use & when all conditions must be True.

Important:
+ Use parentheses around each condition.
+ Python's and/or keywords do NOT work with Polars expressions.
'''

# type_1 equal to Fire AND generation equal to 1.
print(
    lf_pokemon
    .filter((c.type_1 == "Fire") & (c.generation == "1"))
    .select("name", "type_1", "type_2", "total", "generation", "legendary")
    .collect()
)

# Type_2 equal to Flying AND Speed greater than 100.
print(
    lf_pokemon
    .filter((c.type_2 == "Flying") & (c.speed > 100))
    .select("name", "type_1", "type_2", "speed", "generation", "legendary")
    .head(10)
    .collect()
)

# The same AND logic can also be written as multiple filter predicates.
# Multiple predicates are implicitly joined with &.
print(
    lf_pokemon
    .filter(
        c.type_2 == "Flying",
        c.speed > 100,
    )
    .select("name", "type_2", "speed")
    .head(10)
    .collect()
)

##-----------------------##
##       | (or)          ##
##-----------------------##
'''
Use | when at least one condition must be True.
'''

# hp less than 30 OR hp greater than 100.
print(
    lf_pokemon
    .filter((c.hp < 30) | (c.hp > 100))
    .select("name", "type_1", "type_2", "hp", "generation", "legendary")
    .head(12)
    .collect()
)

# attack greater than defense OR sp_atk less than or equal to sp_def.
print(
    lf_pokemon
    .filter((c.attack > c.defense) | (c.sp_atk <= c.sp_def))
    .select("name", "attack", "defense", "sp_atk", "sp_def")
    .head()
    .collect()
)

##---------------------------##
##      Combine & and |      ##
##---------------------------##
'''
When combining & and |, use parentheses to make the logic explicit.
'''

# type_1 is Fire or Water, AND generation is greater than 4.
print(
    lf_pokemon
    .filter(((c.type_1 == "Fire") | (c.type_1 == "Water")) & (c.generation > "4"))
    .select("name", "type_1", "type_2", "total", "generation", "legendary")
    .head(10)
    .collect()
)

# legendary AND (type_1 is Psychic OR type_2 is Dragon).
print(
    lf_pokemon
    .filter(c.legendary & ((c.type_1 == "Psychic") | (c.type_2 == "Dragon")))
    .select("name", "type_1", "type_2", "total", "generation", "legendary")
    .collect()
)
