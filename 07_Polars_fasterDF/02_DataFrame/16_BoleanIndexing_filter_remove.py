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

5. pandas .loc[row_condition, columns] equivalent
   + df.filter(condition).select(columns)

6. LazyFrame filtering
   + Same expressions, but executed after .collect().
'''

from pathlib import Path
import datetime as dt
import re

import polars as pl
from polars import col as c


# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(12)
pl.Config.set_float_precision(2)
pl.Config.set_tbl_width_chars(120)

def clean_column_name(name: str) -> str:
    '''Clean names like "Type 1" -> "Type_1" and "Sp. Atk" -> "Sp_Atk".'''
    return re.sub(r"\s+", "_", name.strip()).replace(".", "")


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

# Keep a raw version too, because later we demonstrate special-character column names.
df_pkm_raw = pl.read_csv(data_dir / "pokemon.csv")

s_col_names = pl.Series(df_pkm_raw.columns)
print(
    s_col_names
    .str.strip_chars()
    .str.replace(r"\s+", "_")
    .str.replace(".", "", literal=True)
)

# Cleaned version for most examples.
df_pokemon = (
    df_pkm_raw
    .drop("#")
    .rename(lambda name: name.strip())
    .select(pl.all().name.replace(r"\s+", "_").name.replace(".", "", literal=True))
    .with_columns(
        c("Type_1").cast(pl.Categorical),
        c("Type_2").cast(pl.Categorical),
        c("Legendary").cast(pl.Boolean),
    )
    .pipe(lambda f: f.with_columns(
        c("Generation").cast(pl.String).cast(pl.Enum(f["Generation"].unique().sort().cast(pl.String).to_list())),
    ))
)

print(df_pokemon.head())
# shape: (5, 12)
# columns: Name, Type_1, Type_2, Total, HP, Attack, Defense, Sp_Atk, Sp_Def, Speed, Generation, Legendary

print(df_pokemon.schema)
# Schema({... 'Type_1': Categorical, 'Type_2': Categorical, 'Generation': Enum, 'Legendary': Boolean})


#-------------------------------------------------------------------------------------------------------------#
#------------------------------------ 1. Single Condition Examples -------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

#######################################################
## Logic Operators: >, <, >=, <=, .is_between(), ==, !=
#######################################################

#-------------
## > (greater than)
#-------------

# HP greater than 200.
print(df_pokemon.filter(c.HP > 200))
# Expected rows include Chansey and Blissey.

# Sp_Atk greater than double Attack.
print(
    df_pokemon
    .filter(c.Sp_Atk > c.Attack * 2)
    .select("Name", "Type_1", "Attack", "Sp_Atk", "Generation", "Legendary")
    .head(8)
)
# Expected rows include Abra, Kadabra, Alakazam, Mega Alakazam, Magnemite, etc.

#-------------
## < (less than)
#-------------

# Speed less than 15.
print(
    df_pokemon
    .filter(c.Speed < 15)
    .select("Name", "Type_1", "Type_2", "Speed", "Generation", "Legendary")
)
# Expected rows include Shuckle, Trapinch, Bonsly, Munchlax, Ferroseed.

# Defense less than half of Attack.
print(
    df_pokemon
    .filter(c.Defense < c.Attack * 0.5)
    .select("Name", "Type_1", "Attack", "Defense", "Generation", "Legendary")
    .head()
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
    df_pokemon
    .filter(c.Speed.is_between(5, 10))
    .select("Name", "Type_1", "Type_2", "Speed", "Generation", "Legendary")
)

# Speed between 5 and 10, excluding the right endpoint.
print(
    df_pokemon
    .filter(c.Speed.is_between(5, 10, closed="left"))
    .select("Name", "Speed")
)
# The value 10 is excluded because the right endpoint is not closed.

#-------------
## == (equal)
#-------------

# Type_1 equal to Fire.
print(
    df_pokemon
    .filter(c.Type_1 == "Fire")
    .select("Name", "Type_1", "Type_2", "Total", "Generation", "Legendary")
    .head(8)
)

# Legendary equal to True.
print(
    df_pokemon
    .filter(c.Legendary)
    .select("Name", "Type_1", "Type_2", "Total", "Generation", "Legendary")
    .head()
)

# You can also write the boolean comparison explicitly.
print(
    df_pokemon
    .filter(c.Legendary == True)
    .select("Name", "Legendary")
    .head()
)

#-------------
## != (not equal)
#-------------

# Type_2 not equal to Flying.
# Important: null comparisons evaluate to null in Polars, and filter() discards null predicates.
# Therefore this drops rows where Type_2 is null.
print(
    df_pokemon
    .filter(c.Type_2 != "Flying")
    .select("Name", "Type_1", "Type_2", "Generation")
    .head()
)

# If you want pandas-like "not Flying OR missing" behavior, explicitly keep nulls.
print(
    df_pokemon
    .filter((c.Type_2 != "Flying") | c.Type_2.is_null())
    .select("Name", "Type_1", "Type_2", "Generation")
    .head()
)

# Generation not equal to 1.
# Generation was cast to String then Enum, so compare with string labels.
print(
    df_pokemon
    .filter(c.Generation != "1")
    .select("Name", "Type_1", "Type_2", "Generation", "Legendary")
    .head()
)

##############################
##          .is_in()         ##
##############################
'''
Pandas:
    df["Type_1"].isin(["Fire", "Water"])

Polars:
    c.Type_1.is_in(["Fire", "Water"])
'''

print(
    df_pokemon
    .filter(c.Type_1.is_in(["Fire", "Water"]))
    .select("Name", "Type_1", "Type_2", "Generation", "Legendary")
    .tail()
)

print(
    df_pokemon
    .filter(c.Generation.is_in(["4", "6"]))
    .select("Name", "Type_1", "Type_2", "Generation", "Legendary")
    .tail()
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
    df_pokemon
    .filter(c.Name.str.contains("Mega", literal=True))
    .select("Name", "Type_1", "Type_2", "Total", "Generation", "Legendary")
    .head()
)

# Name starts with "Tor".
print(
    df_pokemon
    .filter(c.Name.str.starts_with("Tor"))
    .select("Name", "Type_1", "Type_2", "Total", "Generation", "Legendary")
)

# Name ends with "saur".
print(
    df_pokemon
    .filter(c.Name.str.ends_with("saur"))
    .select("Name", "Type_1", "Type_2", "Total", "Generation", "Legendary")
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

df_emp = pl.read_csv(
    data_dir / "emp.csv",
    try_parse_dates=True,
)

print(df_emp.schema)
# Schema({'id': Int64, 'name': String, 'salary': Float64, 'start_date': Date, 'dept': String})

# start_date is month start.
print(df_emp.filter(c.start_date == c.start_date.dt.month_start()))
# Expected row: Rick, 2012-01-01.

# start_date is in a leap year.
print(df_emp.filter(c.start_date.dt.is_leap_year()))
# Expected row: Rick, 2012-01-01.

# start_date is after 2014-01-01.
print(df_emp.filter(c.start_date > dt.date(2014, 1, 1)))


#-------------------------------------------------------------------------------------------------------------#
#---------------------------- 2. Negation of Condition: ~ (tilde) operator -----------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
Use ~ to negate a boolean expression.

Always wrap complex expressions in parentheses before applying ~.
'''

# Type_1 is NOT Fire.
print(
    df_pokemon
    .filter(~(c.Type_1 == "Fire"))
    .select("Name", "Type_1", "Type_2", "Generation", "Legendary")
    .head()
)

# Type_2 is NOT in Ground/Ghost.
# Again, null predicates are discarded by filter().
print(
    df_pokemon
    .filter(~c.Type_2.is_in(["Ground", "Ghost"]))
    .select("Name", "Type_1", "Type_2", "Generation", "Legendary")
    .head()
)

# Keep rows where Type_2 is NOT Ground/Ghost OR Type_2 is null.
print(
    df_pokemon
    .filter((~c.Type_2.is_in(["Ground", "Ghost"])) | c.Type_2.is_null())
    .select("Name", "Type_1", "Type_2", "Generation", "Legendary")
    .head()
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
    df_pokemon
    .filter((c.Type_1 == "Fire") & (c.Generation == "1"))
    .select("Name", "Type_1", "Type_2", "Total", "Generation", "Legendary")
)

# Type_2 equal to Flying AND Speed greater than 100.
print(
    df_pokemon
    .filter((c.Type_2 == "Flying") & (c.Speed > 100))
    .select("Name", "Type_1", "Type_2", "Speed", "Generation", "Legendary")
    .head(10)
)

# The same AND logic can also be written as multiple filter predicates.
# Multiple predicates are implicitly joined with &.
print(
    df_pokemon
    .filter(
        c.Type_2 == "Flying",
        c.Speed > 100,
    )
    .select("Name", "Type_2", "Speed")
    .head(10)
)

###########################
##       | (or)          ##
###########################
'''
Use | when at least one condition must be True.
'''

# HP less than 30 OR HP greater than 100.
print(
    df_pokemon
    .filter((c.HP < 30) | (c.HP > 100))
    .select("Name", "Type_1", "Type_2", "HP", "Generation", "Legendary")
    .head(12)
)

# Attack greater than Defense OR Sp_Atk less than or equal to Sp_Def.
print(
    df_pokemon
    .filter((c.Attack > c.Defense) | (c.Sp_Atk <= c.Sp_Def))
    .select("Name", "Attack", "Defense", "Sp_Atk", "Sp_Def")
    .head()
)

###############################
##      Combine & and |      ##
###############################
'''
When combining & and |, use parentheses to make the logic explicit.
'''

# Type_1 is Fire or Water, AND Generation is greater than 4.
print(
    df_pokemon
    .filter(((c.Type_1 == "Fire") | (c.Type_1 == "Water")) & (c.Generation > "4"))
    .select("Name", "Type_1", "Type_2", "Total", "Generation", "Legendary")
    .head(10)
)

# Legendary AND (Type_1 is Psychic OR Type_2 is Dragon).
print(
    df_pokemon
    .filter(c.Legendary & ((c.Type_1 == "Psychic") | (c.Type_2 == "Dragon")))
    .select("Name", "Type_1", "Type_2", "Total", "Generation", "Legendary")
)


#-------------------------------------------------------------------------------------------------------------#
#--------------------------- 4. c("column_name") and c.column_name expressions -------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
The imported object c comes from:
    from polars import col as c

Two common styles:

1. c("column_name")
   + Works for all column names.
   + Best for names with spaces, dots, punctuation, leading digits, etc.

2. c.column_name
   + Convenient for simple names that are valid Python identifiers.
   + Good for quick interactive work.

In this file, both styles are demonstrated.
'''

#######################
## c("column_name")  ##
#######################

print(
    df_pokemon
    .filter((c("HP") < 30) | (c("HP") > 100))
    .select("Name", "HP", "Type_1", "Type_2", "Generation")
    .head()
)

print(
    df_pokemon
    .filter(c("Type_2").is_in(["Ground", "Ghost"]) & (c("HP") > 100))
    .select("Name", "Type_1", "Type_2", "HP", "Generation", "Legendary")
)

####################
## c.column_name  ##
####################

print(
    df_pokemon
    .filter((c.HP < 30) | (c.HP > 100))
    .select(c.Name, c.HP, c.Type_1, c.Type_2, c.Generation)
    .head()
)

print(
    df_pokemon
    .filter(c.Type_2.is_in(["Ground", "Ghost"]) & (c.HP > 100))
    .select(c.Name, c.Type_1, c.Type_2, c.HP, c.Generation, c.Legendary)
)

#########################################
## Special-character column names      ##
#########################################
'''
The raw pokemon file contains column names such as:
+ "Type 1"    -> contains a space
+ "Type 2"    -> contains a space
+ "Sp. Atk"   -> contains a dot and a space
+ "Sp. Def"   -> contains a dot and a space

For names like these, use c("...").
You cannot write c.Type 1 or c.Sp. Atk as attribute syntax.
'''

print(df_pkm_raw.columns)
# ['#', 'Name', 'Type 1', 'Type 2', 'Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation', 'Legendary']

print(
    df_pkm_raw
    .filter((c("Type 1") == "Fire") & (c("Sp. Atk") < 60))
    .select("Name", "Type 1", "Sp. Atk", "Generation", "Legendary")
)


#-------------------------------------------------------------------------------------------------------------#
#---------------------- 5. pandas .loc[] equivalent: filter(...).select(...) --------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
Pandas:
    df.loc[row_condition, ["Name", "Type_1", "Type_2"]]

Polars:
    df.filter(row_condition).select("Name", "Type_1", "Type_2")

filter(...) handles rows.
select(...) handles columns.
'''

# HP less than 30 OR HP greater than 100; only selected columns.
print(
    df_pokemon
    .filter((c.HP < 30) | (c.HP > 100))
    .select("Name", "Type_1", "Type_2")
    .head()
)

# Type_2 not in Ground/Ghost; only selected columns.
print(
    df_pokemon
    .filter((~c.Type_2.is_in(["Ground", "Ghost"])) | c.Type_2.is_null())
    .select("Name", "Type_2", "Generation")
    .tail()
)

# You can also transform or rename selected columns after filtering.
print(
    df_pokemon
    .filter((c.HP < 30) | (c.HP > 100))
    .select(
        c.Name,
        c.Type_1,
        c.HP.alias("hit_points"),
        (c.Attack + c.Sp_Atk).alias("combined_attack"),
    )
    .head()
)


#-------------------------------------------------------------------------------------------------------------#
#------------------------------ 6. pandas .query(...) equivalent ---------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
Polars usually does NOT use pandas-style string query expressions.
Instead, write normal expression syntax inside df.filter(...).

Pandas:
    df.query('HP > 200')

Polars:
    df.filter(c.HP > 200)

Pandas external variables:
    df.query('Attack >= @atk_threshold')

Polars external variables:
    df.filter(c.Attack >= atk_threshold)
'''

############################################
## df.query("condition_expression") style ##
############################################

print(
    df_pokemon
    .filter(c.HP > 200)
    .select("Name", "Type_1", "Type_2", "HP", "Generation", "Legendary")
)

print(
    df_pokemon
    .filter((c.Sp_Atk > c.Attack * 2) & (c.Type_1 == "Psychic"))
    .select("Name", "Type_1", "Sp_Atk", "Attack", "Generation", "Legendary")
    .tail()
)

print(
    df_pokemon
    .filter((c.Speed < 15) | (c.Speed > 150))
    .select("Name", "Type_1", "Type_2", "Speed", "Generation", "Legendary")
)

############################################
## String methods inside filter()          ##
############################################

print(
    df_pokemon
    .filter(c.Name.str.contains("Mega", literal=True))
    .select("Name", "Type_1", "Type_2", "Total", "Generation", "Legendary")
    .head(5)
)

############################################
## Negated query-style condition           ##
############################################

print(
    df_pokemon
    .filter(~(c.Type_2 == "Flying"))
    .select("Name", "Type_1", "Type_2", "Total", "Generation", "Legendary")
    .head()
)

############################################
## Special-character column names          ##
############################################

print(
    df_pkm_raw
    .filter((c("Type 1") == "Fire") & (c("Sp. Atk") < 60))
    .select("Name", "Type 1", "Sp. Atk")
)

############################################
## Python variables                         ##
############################################

atk_threshold = 180
selected_types = ["Fire", "Water"]

print(
    df_pokemon
    .filter(c.Attack >= atk_threshold)
    .select("Name", "Attack", "Legendary")
)

print(
    df_pokemon
    .filter(c.Type_1.is_in(selected_types) & (c.Generation >= "5"))
    .select("Name", "Type_1", "Generation", "Legendary")
    .head()
)


#-------------------------------------------------------------------------------------------------------------#
#------------------------------- 7. df.remove(condition): drop matching rows ---------------------------------#
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
    df_pokemon
    .remove(c.Type_1 == "Fire")
    .select("Name", "Type_1", "Type_2", "Generation")
    .head()
)

# Similar result for this non-null column.
print(
    df_pokemon
    .filter(~(c.Type_1 == "Fire"))
    .select("Name", "Type_1", "Type_2", "Generation")
    .head()
)

# Remove rows that match any of these conditions.
print(
    df_pokemon
    .remove((c.HP < 30) | (c.HP > 100))
    .select("Name", "HP", "Type_1", "Type_2", "Generation")
    .head()
)

# Remove rows matching multiple predicates.
# Multiple predicates are combined with &.
print(
    df_pokemon
    .remove(
        c.Type_2 == "Flying",
        c.Speed > 100,
    )
    .select("Name", "Type_2", "Speed", "Generation")
    .head()
)

###############################
## Null behavior difference  ##
###############################

df_null_demo = pl.DataFrame(
    {
        "name": ["a", "b", "c", "d"],
        "score": [1, 2, None, 4],
    }
)

print(df_null_demo)
# shape: (4, 2)
# score row c is null.

# Keep rows where NOT(score > 2).
# The null row is discarded because ~(null) is still null, and filter() only keeps True.
print(df_null_demo.filter(~(c.score > 2)))
# Keeps rows a and b.

# Drop rows where score > 2.
# The null row is retained because remove() only removes rows where the predicate is True.
print(df_null_demo.remove(c.score > 2))
# Keeps rows a, b, and c.

'''
Compatibility note:
If you use an older Polars version without DataFrame.remove(), write the explicit filter version:
    df.filter(~condition)

Just remember that null-predicate behavior can differ, as shown above.
'''


#-------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 8. LazyFrame filtering ------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
LazyFrame uses the same expression syntax.
The query is planned first and executed only when .collect() is called.

This is useful when reading from scan_csv(), scan_parquet(), scan_ndjson(), etc.
'''

lf_pokemon = df_pokemon.lazy()

result = (
    lf_pokemon
    .filter((c.Type_1 == "Fire") & (c.Generation == "1"))
    .select("Name", "Type_1", "Type_2", "HP", "Attack", "Generation")
    .collect()
)

print(result)
# Same result shape as the eager filter/select pipeline.

# A lazy "remove" style can be written as a negated filter.
result = (
    lf_pokemon
    .filter(~((c.HP < 30) | (c.HP > 100)))
    .select("Name", "HP", "Type_1", "Generation")
    .collect()
)

print(result.head())
