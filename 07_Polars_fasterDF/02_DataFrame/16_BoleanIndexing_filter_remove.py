'''
Boolean Indexing / Boolean Filtering in Polars DataFrames.

In Polars, the central ideas are:
+ df.filter(condition) keeps rows where the condition is True.
+ df.remove(condition) removes rows where the condition is True.
+ df.filter(condition).select(columns) replaces many pandas .loc[row_mask, columns] patterns.
+ c("column_name") and c.column_name create column expressions.

###############################

1. Single Condition Examples with df.filter()
   + Logic Operators: >, <, >=, <=, .is_between(), ==, !=
   + .is_in()
   + String Boolean: .str.contains(), .str.starts_with(), .str.ends_with()
   + DateTime Boolean: month-start and leap-year examples

2. Negation of Condition: ~ (tilde) operator

3. Combine Multiple Conditions:
   + & (and)
   + | (or)
   + Combine & and |

4. df.remove(condition): dropping rows that match a condition
   + df.remove(condition) is the direct "drop matching rows" pattern.
   + df.filter(~condition) is similar in many simple cases.
   + Null predicates are an important difference: remove() retains null-predicate rows,
     while filter(~condition) discards rows where the negated predicate is null.
'''

from pathlib import Path
import datetime as dt

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(12)
pl.Config.set_float_precision(2)
pl.Config.set_tbl_width_chars(120)


#-------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 0. Example Data -------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
The pandas source file uses pokemon.csv.
Here we load the same file and clean the column names so the expression examples are short.

Original examples:
+ "Type 1"  -> cleaned to "Type_1"
+ "Type 2"  -> cleaned to "Type_2"
+ "Sp. Atk" -> cleaned to "Sp_Atk"
+ "Sp. Def" -> cleaned to "Sp_Def"
'''

data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))

# Cleaned version for most examples.
lf_pokemon = (
    pl.scan_csv(data_dir / "pokemon.csv")
    .drop("#")
    .rename(lambda name: name.strip())
    .select(pl.all().name.replace(r"\s+", "_").name.replace(".", "", literal=True))
    .with_columns(
        c("Type_1", "Type_2").cast(pl.Categorical),
        c("Legendary").cast(pl.Boolean),
    )
    .pipe(lambda f: f.with_columns(
        c("Generation").cast(pl.String).cast(pl.Enum(f.collect()["Generation"].cast(pl.String).unique().sort())),
    ))                                               # Must use .collect() to realize the dataframe, to access the values for Enum casting
)

print(lf_pokemon.collect().head())
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

print(lf_pokemon.collect().schema)
# Schema({... 'Type_1': Categorical, 'Type_2': Categorical, 'Generation': Enum, 'Legendary': Boolean})


#-------------------------------------------------------------------------------------------------------------#
#------------------------------------- 1. Single Condition Examples ------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

#######################################################
## Logic Operators: >, <, >=, <=, .is_between(), ==, !=
#######################################################

#-------------
## > (greater than)
#-------------

# HP greater than 200.
print(lf_pokemon.filter(c.HP > 200).collect())
# Expected rows include Chansey and Blissey.

# Sp_Atk greater than double Attack.
print(
    lf_pokemon
    .filter(c.Sp_Atk > c.Attack * 2)
    .select("Name", "Type_1", "Attack", "Sp_Atk", "Generation", "Legendary")
    .head(8)
    .collect()
)
# Expected rows include Abra, Kadabra, Alakazam, Mega Alakazam, Magnemite, etc.

#-------------
## < (less than)
#-------------

# Speed less than 15.
print(
    lf_pokemon
    .filter(c.Speed < 15)
    .select("Name", "Type_1", "Type_2", "Speed", "Generation", "Legendary")
    .collect()
)
# Expected rows include Shuckle, Trapinch, Bonsly, Munchlax, Ferroseed.

# Defense less than half of Attack.
print(
    lf_pokemon
    .filter(c.Defense < c.Attack * 0.5)
    .select("Name", "Type_1", "Attack", "Defense", "Generation", "Legendary")
    .head()
    .collect()
)

'''
THE SAME PATTERN WORKS FOR:
+ >= greater than or equal to
+ <= less than or equal to
'''

#-------------
## .is_between()
#-------------
'''
Pandas:
    df["Speed"].between(left, right, inclusive="both")

Polars:
    c.Speed.is_between(lower_bound, upper_bound, closed="both")

closed = "both"  : [left, right] or left <= x <= right
closed = "none"  : (left, right) or left < x < right
closed = "left"  : [left, right) or left <= x < right
closed = "right" : (left, right] or left < x <= right
'''

# Speed between 5 and 10, inclusive.
print(
    lf_pokemon
    .filter(c.Speed.is_between(5, 10))
    .select("Name", "Type_1", "Type_2", "Speed", "Generation", "Legendary")
    .collect()
)

# Speed between 5 and 10, excluding the right endpoint.
print(
    lf_pokemon
    .filter(c.Speed.is_between(5, 10, closed="left"))
    .select("Name", "Speed")
    .collect()
)
# The value 10 is excluded because the right endpoint is not closed.

#-------------
## == (equal)
#-------------

# Type_1 equal to Fire.
print(
    lf_pokemon
    .filter(c.Type_1 == "Fire")
    .select("Name", "Type_1", "Type_2", "Total", "Generation", "Legendary")
    .head(8)
    .collect()
)

# Legendary equal to True.
print(
    lf_pokemon
    .filter(c.Legendary)
    .select("Name", "Type_1", "Type_2", "Total", "Generation", "Legendary")
    .head()
)

# You can also write the boolean comparison explicitly.
print(
    lf_pokemon
    .filter(c.Legendary) # equivalent to ``c.Legendary == True``
    .select("Name", "Legendary")
    .head()
    .collect()
)

#-------------
## != (not equal)
#-------------

# Type_2 not equal to Flying.
# Important: null comparisons evaluate to null in Polars, and filter() discards null predicates.
# Therefore this drops rows where Type_2 is null.
print(
    lf_pokemon
    .filter(c.Type_2 != "Flying")
    .select("Name", "Type_1", "Type_2", "Generation")
    .head()
    .collect()
)

# If you want pandas-like "not Flying OR missing" behavior, explicitly keep nulls.
print(
    lf_pokemon
    .filter((c.Type_2 != "Flying") | c.Type_2.is_null())
    .select("Name", "Type_1", "Type_2", "Generation")
    .head()
    .collect()
)

# Generation not equal to 1.
# Generation was cast to String then Enum, so compare with string labels.
print(
    lf_pokemon
    .filter(c.Generation != "1")
    .select("Name", "Type_1", "Type_2", "Generation", "Legendary")
    .head()
    .collect()
)

##############################
##          .is_in()        ##
##############################
'''
Pandas:
    df["Type_1"].isin(["Fire", "Water"])

Polars:
    c.Type_1.is_in(["Fire", "Water"])
'''

print(
    lf_pokemon
    .filter(c.Type_1.is_in(["Fire", "Water"]))
    .select("Name", "Type_1", "Type_2", "Generation", "Legendary")
    .tail()
    .collect()
)

print(
    lf_pokemon
    .filter(c.Generation.is_in(["4", "6"]))
    .select("Name", "Type_1", "Type_2", "Generation", "Legendary")
    .tail()
    .collect()
)

##############################
##      String Boolean      ##
##############################
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
    .filter(c.Name.str.contains("Mega", literal=True))
    .select("Name", "Type_1", "Type_2", "Total", "Generation", "Legendary")
    .head()
    .collect()
)

# Name starts with "Tor".
print(
    lf_pokemon
    .filter(c.Name.str.starts_with("Tor"))
    .select("Name", "Type_1", "Type_2", "Total", "Generation", "Legendary")
    .collect()
)

# Name ends with "saur".
print(
    lf_pokemon
    .filter(c.Name.str.ends_with("saur"))
    .select("Name", "Type_1", "Type_2", "Total", "Generation", "Legendary")
    .collect()
)

##############################
##     DateTime Boolean     ##
##############################
'''
Pandas has boolean datetime properties such as:
    df["start_date"].dt.is_month_start

Polars often uses datetime expressions instead:
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


#-------------------------------------------------------------------------------------------------------------#
#---------------------------- 2. Negation of Condition: ~ (tilde) operator -----------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
Use ~ to negate a boolean expression.

Always wrap complex expressions in parentheses before applying ~.
'''

# Type_1 is NOT Fire.
print(
    lf_pokemon
    .filter(~(c.Type_1 == "Fire"))
    .select("Name", "Type_1", "Type_2", "Generation", "Legendary")
    .head()
    .collect()
)

# Type_2 is NOT in Ground/Ghost.
# Again, null predicates are discarded by filter().
print(
    lf_pokemon
    .filter(~c.Type_2.is_in(["Ground", "Ghost"]))
    .select("Name", "Type_1", "Type_2", "Generation", "Legendary")
    .head()
    .collect()
)

# Keep rows where Type_2 is NOT Ground/Ghost OR Type_2 is null.
print(
    lf_pokemon
    .filter((~c.Type_2.is_in(["Ground", "Ghost"])) | c.Type_2.is_null())
    .select("Name", "Type_1", "Type_2", "Generation", "Legendary")
    .head()
    .collect()
)


#-------------------------------------------------------------------------------------------------------------#
#---------------------------- 3. Combine Multiple Conditions: & (and), | (or) --------------------------------#
#-------------------------------------------------------------------------------------------------------------#

###########################
##       & (and)         ##
###########################
'''
Use & when all conditions must be True.

Important:
+ Use parentheses around each condition.
+ Python's and/or keywords do NOT work with Polars expressions.
'''

# Type_1 equal to Fire AND Generation equal to 1.
print(
    lf_pokemon
    .filter((c.Type_1 == "Fire") & (c.Generation == "1"))
    .select("Name", "Type_1", "Type_2", "Total", "Generation", "Legendary")
    .collect()
)

# Type_2 equal to Flying AND Speed greater than 100.
print(
    lf_pokemon
    .filter((c.Type_2 == "Flying") & (c.Speed > 100))
    .select("Name", "Type_1", "Type_2", "Speed", "Generation", "Legendary")
    .head(10)
    .collect()
)

# The same AND logic can also be written as multiple filter predicates.
# Multiple predicates are implicitly joined with &.
print(
    lf_pokemon
    .filter(
        c.Type_2 == "Flying",
        c.Speed > 100,
    )
    .select("Name", "Type_2", "Speed")
    .head(10)
    .collect()
)

###########################
##       | (or)          ##
###########################
'''
Use | when at least one condition must be True.
'''

# HP less than 30 OR HP greater than 100.
print(
    lf_pokemon
    .filter((c.HP < 30) | (c.HP > 100))
    .select("Name", "Type_1", "Type_2", "HP", "Generation", "Legendary")
    .head(12)
    .collect()
)

# Attack greater than Defense OR Sp_Atk less than or equal to Sp_Def.
print(
    lf_pokemon
    .filter((c.Attack > c.Defense) | (c.Sp_Atk <= c.Sp_Def))
    .select("Name", "Attack", "Defense", "Sp_Atk", "Sp_Def")
    .head()
    .collect()
)

###############################
##      Combine & and |      ##
###############################
'''
When combining & and |, use parentheses to make the logic explicit.
'''

# Type_1 is Fire or Water, AND Generation is greater than 4.
print(
    lf_pokemon
    .filter(((c.Type_1 == "Fire") | (c.Type_1 == "Water")) & (c.Generation > "4"))
    .select("Name", "Type_1", "Type_2", "Total", "Generation", "Legendary")
    .head(10)
    .collect()
)

# Legendary AND (Type_1 is Psychic OR Type_2 is Dragon).
print(
    lf_pokemon
    .filter(c.Legendary & ((c.Type_1 == "Psychic") | (c.Type_2 == "Dragon")))
    .select("Name", "Type_1", "Type_2", "Total", "Generation", "Legendary")
    .collect()
)


#-------------------------------------------------------------------------------------------------------------#
#------------------------------- 4. df.remove(condition): drop matching rows ---------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
df.filter(condition)
    Keeps rows where condition is True.

df.remove(condition)
    Drops rows where condition is True.

In many simple non-null cases:
    df.remove(condition)
looks like:
    df.filter(~condition)

But they are NOT exactly identical when the predicate can be null:
+ filter(~condition) keeps only rows where ~condition is True.
+ remove(condition) drops rows where condition is True, and retains rows where condition is False or null.
'''

# Remove Fire-type rows.
print(
    lf_pokemon
    .remove(c.Type_1 == "Fire")
    .select("Name", "Type_1", "Type_2", "Generation")
    .head()
    .collect()
)

# Similar result for this non-null column.
print(
    lf_pokemon
    .filter(~(c.Type_1 == "Fire"))
    .select("Name", "Type_1", "Type_2", "Generation")
    .head()
    .collect()
)

# Remove rows that match any of these conditions.
print(
    lf_pokemon
    .remove((c.HP < 30) | (c.HP > 100))
    .select("Name", "HP", "Type_1", "Type_2", "Generation")
    .head()
    .collect()
)

# Remove rows matching multiple predicates.
# Multiple predicates are combined with &.
print(
    lf_pokemon
    .remove(
        c.Type_2 == "Flying",
        c.Speed > 100,
    )
    .select("Name", "Type_2", "Speed", "Generation")
    .head()
    .collect()
)

###############################
## Null behavior difference  ##
###############################

lf_null_demo = pl.LazyFrame(
    {
        "name": ["a", "b", "c", "d"],
        "score": [1, 2, None, 4],
    }
)

print(lf_null_demo.collect())
# shape: (4, 2)
# ┌──────┬───────┐
# │ name ┆ score │
# │ ---  ┆ ---   │
# │ str  ┆ i64   │
# ╞══════╪═══════╡
# │ a    ┆ 1     │
# │ b    ┆ 2     │
# │ c    ┆ null  │
# │ d    ┆ 4     │
# └──────┴───────┘

# Keep rows where NOT(score > 2).
# The null row is discarded because ~(null) is still null, and filter() only keeps True.
print(lf_null_demo.filter(~(c.score > 2)).collect())
# shape: (2, 2)
# ┌──────┬───────┐
# │ name ┆ score │
# │ ---  ┆ ---   │
# │ str  ┆ i64   │
# ╞══════╪═══════╡
# │ a    ┆ 1     │
# │ b    ┆ 2     │
# └──────┴───────┘

# Drop rows where score > 2.
# The null row is retained because remove() only removes rows where the predicate is True.
print(lf_null_demo.remove(c.score > 2).collect())
# shape: (3, 2)
# ┌──────┬───────┐
# │ name ┆ score │
# │ ---  ┆ ---   │
# │ str  ┆ i64   │
# ╞══════╪═══════╡
# │ a    ┆ 1     │
# │ b    ┆ 2     │
# │ c    ┆ null  │
# └──────┴───────┘
