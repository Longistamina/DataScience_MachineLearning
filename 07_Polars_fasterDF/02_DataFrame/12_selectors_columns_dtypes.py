'''
Column selectors in Polars.

Selectors are useful when you want to select columns by:
+ data type: numeric columns, string columns, temporal columns, nested columns, ...
+ name pattern: starts_with, ends_with, contains, regex matches, ...
+ position: first, last, by_index, all
+ set logic: union, intersection, difference, symmetric difference, complement

Recommended import:
    import polars.selectors as cs

Content flow:
1. What selectors are and when to use them
2. Select columns by data type
3. Select columns by exact dtype and nested dtype
4. Select columns by name or name pattern
5. Select columns by position
6. Combine selectors with set operations
7. Use selectors with expressions in select(), with_columns(), and group_by()
8. Avoid operator ambiguity with as_expr()
9. Debug selectors with is_selector() and expand_selector()
10. Use selectors in LazyFrame pipelines
11. Categorized list of supported selector APIs

Important distinction:
+ pl.col("name") is best when you know exact column names.
+ cs.numeric(), cs.string(), cs.starts_with(...), etc. are best when the matching
  columns should be discovered from the DataFrame schema.
'''

from __future__ import annotations

import datetime as dt
from decimal import Decimal

import polars as pl
import polars.selectors as cs

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(20)
pl.Config.set_tbl_cols(20)
pl.Config.set_float_precision(2)
pl.Config.set_tbl_width_chars(200)


#----------------------------------------------------------------------------------------------------#
#---------------------------------------- 0. Example Data -------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
The examples below are intentionally self-contained.

The DataFrame contains many different column names and dtypes so that selectors
have something meaningful to match.
'''

priority_dtype = pl.Enum(["low", "medium", "high"])

# A basic mixed-type DataFrame.
df_people = pl.DataFrame(
    {
        "id": [1, 2, 3, 4],
        "employee name": ["Ada", "Bob", "Charlie", "Dana"],
        "dept": ["IT", "HR", "IT", "Finance"],
        "salary_usd": [120_000.0, 90_000.0, 110_000.0, 130_000.0],
        "bonus_usd": [10_000, 5_000, 7_500, 12_000],
        "score_2023": [91.5, 88.0, 95.0, 89.5],
        "score_2024": [93.0, 90.0, 96.5, 92.0],
        "is_manager": [True, False, False, True],
        "hire_date": [
            dt.date(2020, 1, 15),
            dt.date(2021, 6, 1),
            dt.date(2019, 9, 20),
            dt.date(2018, 3, 10),
        ],
        "last_login": [
            dt.datetime(2024, 1, 1, 9, 0),
            dt.datetime(2024, 1, 2, 10, 30),
            dt.datetime(2024, 1, 3, 8, 45),
            dt.datetime(2024, 1, 4, 14, 15),
        ],
        "login_time": [
            dt.time(9, 0),
            dt.time(10, 30),
            dt.time(8, 45),
            dt.time(14, 15),
        ],
        "tenure": [
            dt.timedelta(days=1500),
            dt.timedelta(days=1000),
            dt.timedelta(days=1700),
            dt.timedelta(days=2100),
        ],
        "tags": [
            ["python", "sql"],
            ["excel"],
            ["python", "rust"],
            ["finance", "sql"],
        ],
        "payload": [b"a1", b"b2", b"c3", b"d4"],
        "commission": [
            Decimal("0.10"),
            Decimal("0.05"),
            Decimal("0.08"),
            Decimal("0.12"),
        ],
        "2024": [100, 200, 300, 400],
        "note text": ["top", "mid", "top", "high"],
    },
    schema_overrides={
        "commission": pl.Decimal(precision=4, scale=2),
    },
)

# Add categorical, enum, array, and struct columns.
df_people = df_people.with_columns(
    pl.col("dept").cast(pl.Categorical).alias("dept_cat"),
    pl.Series("priority", ["high", "medium", "high", "low"]).cast(priority_dtype),
    pl.Series(
        "rgb",
        [[255, 0, 0], [0, 255, 0], [0, 0, 255], [128, 128, 128]],
        dtype=pl.Array(pl.Int64, 3),
    ),
    pl.struct("salary_usd", "bonus_usd").alias("pay_info"),
)

print(df_people.select(df_people.columns[0:9])) # first 9 columns
# shape: (4, 9)
# ┌─────┬───────────────┬─────────┬────────────┬───────────┬────────────┬────────────┬────────────┬────────────┐
# │ id  ┆ employee name ┆ dept    ┆ salary_usd ┆ bonus_usd ┆ score_2023 ┆ score_2024 ┆ is_manager ┆ hire_date  │
# │ --- ┆ ---           ┆ ---     ┆ ---        ┆ ---       ┆ ---        ┆ ---        ┆ ---        ┆ ---        │
# │ i64 ┆ str           ┆ str     ┆ f64        ┆ i64       ┆ f64        ┆ f64        ┆ bool       ┆ date       │
# ╞═════╪═══════════════╪═════════╪════════════╪═══════════╪════════════╪════════════╪════════════╪════════════╡
# │ 1   ┆ Ada           ┆ IT      ┆ 120000.00  ┆ 10000     ┆ 91.50      ┆ 93.00      ┆ true       ┆ 2020-01-15 │
# │ 2   ┆ Bob           ┆ HR      ┆ 90000.00   ┆ 5000      ┆ 88.00      ┆ 90.00      ┆ false      ┆ 2021-06-01 │
# │ 3   ┆ Charlie       ┆ IT      ┆ 110000.00  ┆ 7500      ┆ 95.00      ┆ 96.50      ┆ false      ┆ 2019-09-20 │
# │ 4   ┆ Dana          ┆ Finance ┆ 130000.00  ┆ 12000     ┆ 89.50      ┆ 92.00      ┆ true       ┆ 2018-03-10 │
# └─────┴───────────────┴─────────┴────────────┴───────────┴────────────┴────────────┴────────────┴────────────┘

print(df_people.schema)
# Expected idea:
# + string columns: employee name, dept, note text
# + numeric columns: id, salary_usd, bonus_usd, score_2023, score_2024, 2024, commission
# + boolean columns: is_manager
# + temporal columns: hire_date, last_login, login_time, tenure
# + nested columns: tags, rgb, pay_info
# + categorical/enum columns: dept_cat, priority
# + binary columns: payload


#----------------------------------------------------------------------------------------------------#
#---------------------------- 1. What selectors are and when to use them ----------------------------#
#----------------------------------------------------------------------------------------------------#
'''
Selectors are not ordinary column expressions like pl.col("salary_usd").
They are schema-aware objects that expand to one or more columns.

Typical use:
    df.select(cs.numeric())

This means:
    "Look at the DataFrame schema and select all columns whose dtype is numeric."

Selectors are especially useful when you do not want to hard-code all column names.
'''

print(df_people.select(cs.numeric()))
# Selects all numeric columns in the DataFrame schema.

print(df_people.select(cs.string()))
# Selects all String columns.
# Categorical and Enum are not automatically the same thing as String.

print(df_people.select(cs.temporal()))
# Selects temporal columns, such as Date, Datetime, Duration, and Time columns.


#-----------------------------------------------------------------------------------------------------#
#---------------------------------- 2. Select columns by data type -----------------------------------#
#-----------------------------------------------------------------------------------------------------#

##################
## cs.numeric() ##
##################
'''
cs.numeric() selects all numeric columns.
This includes integers, floats, and Decimal columns.
'''

print(df_people.select(cs.numeric()))
# shape: (4, 7)
# ┌─────┬────────────┬───────────┬────────────┬────────────┬──────────────┬──────┐
# │ id  ┆ salary_usd ┆ bonus_usd ┆ score_2023 ┆ score_2024 ┆ commission   ┆ 2024 │
# │ --- ┆ ---        ┆ ---       ┆ ---        ┆ ---        ┆ ---          ┆ ---  │
# │ i64 ┆ f64        ┆ i64       ┆ f64        ┆ f64        ┆ decimal[4,2] ┆ i64  │
# ╞═════╪════════════╪═══════════╪════════════╪════════════╪══════════════╪══════╡
# │ 1   ┆ 120000.00  ┆ 10000     ┆ 91.50      ┆ 93.00      ┆ 0.10         ┆ 100  │
# │ 2   ┆ 90000.00   ┆ 5000      ┆ 88.00      ┆ 90.00      ┆ 0.05         ┆ 200  │
# │ 3   ┆ 110000.00  ┆ 7500      ┆ 95.00      ┆ 96.50      ┆ 0.08         ┆ 300  │
# │ 4   ┆ 130000.00  ┆ 12000     ┆ 89.50      ┆ 92.00      ┆ 0.12         ┆ 400  │
# └─────┴────────────┴───────────┴────────────┴────────────┴──────────────┴──────┘
# columns include: id, salary_usd, bonus_usd, score_2023, score_2024, commission, 2024

##################
## cs.integer() ##
##################
'''
cs.integer() selects all integer columns, signed and unsigned.
'''

print(df_people.select(cs.integer()))
# shape: (4, 3)
# ┌─────┬───────────┬──────┐
# │ id  ┆ bonus_usd ┆ 2024 │
# │ --- ┆ ---       ┆ ---  │
# │ i64 ┆ i64       ┆ i64  │
# ╞═════╪═══════════╪══════╡
# │ 1   ┆ 10000     ┆ 100  │
# │ 2   ┆ 5000      ┆ 200  │
# │ 3   ┆ 7500      ┆ 300  │
# │ 4   ┆ 12000     ┆ 400  │
# └─────┴───────────┴──────┘
# columns include: id, bonus_usd, 2024

############################
## cs.signed_integer()    ##
## cs.unsigned_integer()  ##
############################
'''
Use signed_integer() or unsigned_integer() when you care about integer signedness.
Most small tutorial DataFrames infer signed integers by default.
'''

print(df_people.select(cs.signed_integer()))
# shape: (4, 3)
# ┌─────┬───────────┬──────┐
# │ id  ┆ bonus_usd ┆ 2024 │
# │ --- ┆ ---       ┆ ---  │
# │ i64 ┆ i64       ┆ i64  │
# ╞═════╪═══════════╪══════╡
# │ 1   ┆ 10000     ┆ 100  │
# │ 2   ┆ 5000      ┆ 200  │
# │ 3   ┆ 7500      ┆ 300  │
# │ 4   ┆ 12000     ┆ 400  │
# └─────┴───────────┴──────┘
# signed integer columns

print(df_people.select(cs.unsigned_integer()))
# usually empty here unless your schema contains unsigned integer dtypes

################
## cs.float() ##
################
'''
cs.float() selects all floating-point columns.
'''

print(df_people.select(cs.float()))
# shape: (4, 3)
# ┌────────────┬────────────┬────────────┐
# │ salary_usd ┆ score_2023 ┆ score_2024 │
# │ ---        ┆ ---        ┆ ---        │
# │ f64        ┆ f64        ┆ f64        │
# ╞════════════╪════════════╪════════════╡
# │ 120000.00  ┆ 91.50      ┆ 93.00      │
# │ 90000.00   ┆ 88.00      ┆ 90.00      │
# │ 110000.00  ┆ 95.00      ┆ 96.50      │
# │ 130000.00  ┆ 89.50      ┆ 92.00      │
# └────────────┴────────────┴────────────┘
# columns include: salary_usd, score_2023, score_2024

##################
## cs.decimal() ##
##################
'''
cs.decimal() selects Decimal columns.
Decimal is useful for exact fixed-scale values such as money or rates.
'''

print(df_people.select(cs.decimal()))
# shape: (4, 1)
# ┌──────────────┐
# │ commission   │
# │ ---          │
# │ decimal[4,2] │
# ╞══════════════╡
# │ 0.10         │
# │ 0.05         │
# │ 0.08         │
# │ 0.12         │
# └──────────────┘
# columns include: commission

##################
## cs.boolean() ##
##################
'''
cs.boolean() selects Boolean columns.
'''

print(df_people.select(cs.boolean()))
# shape: (4, 1)
# ┌────────────┐
# │ is_manager │
# │ ---        │
# │ bool       │
# ╞════════════╡
# │ true       │
# │ false      │
# │ false      │
# │ true       │
# └────────────┘
# columns include: is_manager

#################
## cs.string() ##
#################
'''
cs.string() selects String columns.

If you also want Categorical columns that represent strings, use:
    cs.string(include_categorical=True)
'''

print(df_people.select(cs.string()))
# shape: (4, 3)
# ┌───────────────┬─────────┬───────────┐
# │ employee name ┆ dept    ┆ note text │
# │ ---           ┆ ---     ┆ ---       │
# │ str           ┆ str     ┆ str       │
# ╞═══════════════╪═════════╪═══════════╡
# │ Ada           ┆ IT      ┆ top       │
# │ Bob           ┆ HR      ┆ mid       │
# │ Charlie       ┆ IT      ┆ top       │
# │ Dana          ┆ Finance ┆ high      │
# └───────────────┴─────────┴───────────┘
# columns include: employee name, dept, note text

print(df_people.select(cs.string(include_categorical=True)))
# shape: (4, 4)
# ┌───────────────┬─────────┬───────────┬──────────┐
# │ employee name ┆ dept    ┆ note text ┆ dept_cat │
# │ ---           ┆ ---     ┆ ---       ┆ ---      │
# │ str           ┆ str     ┆ str       ┆ cat      │
# ╞═══════════════╪═════════╪═══════════╪══════════╡
# │ Ada           ┆ IT      ┆ top       ┆ IT       │
# │ Bob           ┆ HR      ┆ mid       ┆ HR       │
# │ Charlie       ┆ IT      ┆ top       ┆ IT       │
# │ Dana          ┆ Finance ┆ high      ┆ Finance  │
# └───────────────┴─────────┴───────────┴──────────┘
# columns include string columns and categorical columns such as dept_cat

######################
## cs.categorical() ##
######################
'''
cs.categorical() selects Categorical columns.
'''

print(df_people.select(cs.categorical()))
# shape: (4, 1)
# ┌──────────┐
# │ dept_cat │
# │ ---      │
# │ cat      │
# ╞══════════╡
# │ IT       │
# │ HR       │
# │ IT       │
# │ Finance  │
# └──────────┘
# columns include: dept_cat

###############
## cs.enum() ##
###############
'''
cs.enum() selects Enum columns.
Enum columns have a fixed set of allowed categories and a defined order.
'''

print(df_people.select(cs.enum()))
# shape: (4, 1)
# ┌──────────┐
# │ priority │
# │ ---      │
# │ enum     │
# ╞══════════╡
# │ high     │
# │ medium   │
# │ high     │
# │ low      │
# └──────────┘
# columns include: priority

#################
## cs.binary() ##
#################
'''
cs.binary() selects Binary columns.
'''

print(df_people.select(cs.binary()))
# shape: (4, 1)
# ┌─────────┐
# │ payload │
# │ ---     │
# │ binary  │
# ╞═════════╡
# │ b"a1"   │
# │ b"b2"   │
# │ b"c3"   │
# │ b"d4"   │
# └─────────┘
# columns include: payload

###################
## cs.temporal() ##
###################
'''
cs.temporal() selects temporal columns, such as Date, Datetime, Duration, and Time columns.
'''

print(df_people.select(cs.temporal()))
# shape: (4, 4)
# ┌────────────┬─────────────────────┬────────────┬──────────────┐
# │ hire_date  ┆ last_login          ┆ login_time ┆ tenure       │
# │ ---        ┆ ---                 ┆ ---        ┆ ---          │
# │ date       ┆ datetime[μs]        ┆ time       ┆ duration[μs] │
# ╞════════════╪═════════════════════╪════════════╪══════════════╡
# │ 2020-01-15 ┆ 2024-01-01 09:00:00 ┆ 09:00:00   ┆ 1500d        │
# │ 2021-06-01 ┆ 2024-01-02 10:30:00 ┆ 10:30:00   ┆ 1000d        │
# │ 2019-09-20 ┆ 2024-01-03 08:45:00 ┆ 08:45:00   ┆ 1700d        │
# │ 2018-03-10 ┆ 2024-01-04 14:15:00 ┆ 14:15:00   ┆ 2100d        │
# └────────────┴─────────────────────┴────────────┴──────────────┘


#----------------------------------------------------------------------------------------------------#
#---------------------------- 3. Select columns by exact dtype and nested dtype ----------------------#
#----------------------------------------------------------------------------------------------------#

#################
## cs.by_dtype ##
#################
'''
cs.by_dtype(...) selects columns whose dtype matches the given dtype or dtypes.

This is useful when you need more exact control than broad selectors such as
cs.numeric(), cs.integer(), or cs.temporal().
'''

print(df_people.select(cs.by_dtype(pl.Float64)))
# shape: (4, 3)
# ┌────────────┬────────────┬────────────┐
# │ salary_usd ┆ score_2023 ┆ score_2024 │
# │ ---        ┆ ---        ┆ ---        │
# │ f64        ┆ f64        ┆ f64        │
# ╞════════════╪════════════╪════════════╡
# │ 120000.00  ┆ 91.50      ┆ 93.00      │
# │ 90000.00   ┆ 88.00      ┆ 90.00      │
# │ 110000.00  ┆ 95.00      ┆ 96.50      │
# │ 130000.00  ┆ 89.50      ┆ 92.00      │
# └────────────┴────────────┴────────────┘

print(df_people.select(cs.by_dtype(pl.Date, pl.Datetime)))
# shape: (4, 2)
# ┌────────────┬─────────────────────┐
# │ hire_date  ┆ last_login          │
# │ ---        ┆ ---                 │
# │ date       ┆ datetime[μs]        │
# ╞════════════╪═════════════════════╡
# │ 2020-01-15 ┆ 2024-01-01 09:00:00 │
# │ 2021-06-01 ┆ 2024-01-02 10:30:00 │
# │ 2019-09-20 ┆ 2024-01-03 08:45:00 │
# │ 2018-03-10 ┆ 2024-01-04 14:15:00 │
# └────────────┴─────────────────────┘

print(df_people.select(cs.by_dtype([pl.Date, pl.Datetime])))
# A list of dtypes is also accepted.

#################
## cs.temporal ##
#################
'''
Temporal selectors:
+ cs.date()      -> Date columns
+ cs.datetime()  -> Datetime columns, optionally filtered by time unit/time zone
+ cs.time()      -> Time columns
+ cs.duration()  -> Duration columns, optionally filtered by time unit
+ cs.temporal()  -> all temporal columns
'''

print(df_people.select(cs.date()))
print(df_people.select(cs.datetime()))
print(df_people.select(cs.time()))
print(df_people.select(cs.duration()))
print(df_people.select(cs.temporal()))

#################
## cs.nested() ##
#################
'''
Nested selectors:
+ cs.list()   -> List columns
+ cs.array()  -> fixed-size Array columns
+ cs.struct() -> Struct columns
+ cs.nested() -> all nested columns
'''

print(df_people.select(cs.list()))
# columns include: tags

print(df_people.select(cs.array()))
# columns include: rgb

print(df_people.select(cs.array(width=3)))
# array columns whose fixed width is 3

print(df_people.select(cs.struct()))
# columns include: pay_info

print(df_people.select(cs.nested()))
# columns include: tags, rgb, pay_info


#----------------------------------------------------------------------------------------------------#
#------------------------------ 4. Select columns by name or name pattern ---------------------------#
#----------------------------------------------------------------------------------------------------#

################
## cs.by_name ##
################
'''
cs.by_name(...) selects columns by exact name.

Use require_all=False if you want to ignore missing names instead of raising an error.
This can be useful in reusable pipelines where some optional columns may or may not exist.
'''

print(df_people.select(cs.by_name("id", "dept", "salary_usd")))
# Exact column names.

print(df_people.select(cs.by_name("id", "optional_missing_col", require_all=False)))
# Selects id and silently ignores optional_missing_col.

####################
## cs.starts_with ##
####################
'''
cs.starts_with(...) selects columns whose names start with one or more prefixes.
'''

print(df_people.select(cs.starts_with("score_")))
# columns: score_2023, score_2024

print(df_people.select(cs.starts_with("salary", "bonus")))
# columns: salary_usd, bonus_usd

##################
## cs.ends_with ##
##################
'''
cs.ends_with(...) selects columns whose names end with one or more suffixes.
'''

print(df_people.select(cs.ends_with("_usd")))
# columns: salary_usd, bonus_usd

print(df_people.select(cs.ends_with("_2023", "_2024")))
# columns: score_2023, score_2024

#################
## cs.contains ##
#################
'''
cs.contains(...) selects columns whose names contain a literal substring.
This is not regex; use cs.matches(...) for regex patterns.
'''

print(df_people.select(cs.contains("score")))
# columns: score_2023, score_2024

print(df_people.select(cs.contains("date", "login")))
# columns with names containing date or login

################
## cs.matches ##
################
'''
cs.matches(...) selects columns whose names match a regular expression.

Common patterns:
+ r"^score_\\d{4}$" -> names like score_2023 and score_2024
+ r".*_usd$"       -> names ending with _usd
'''

print(df_people.select(cs.matches(r"^score_\d{4}$")))
# columns: score_2023, score_2024

print(df_people.select(cs.matches(r".*_usd$")))
# columns: salary_usd, bonus_usd

###############################################
## cs.alpha(), cs.alphanumeric(), cs.digit() ##
###############################################
'''
These selectors are about the characters in the column names:
+ cs.alpha()        -> names that contain only alphabetic characters
+ cs.alphanumeric() -> names that contain only alphabetic characters and digits
+ cs.digit()        -> names that contain only digits

These are useful for quickly checking or selecting columns based on naming rules.
'''

df_name_rules = pl.DataFrame(
    {
        "abc": [1, 2],
        "abc123": [3, 4],
        "123": [5, 6],
        "has space": [7, 8],
        "has_underscore": [9, 10],
    }
)

print(df_name_rules.select(cs.alpha()))
# columns: abc

print(df_name_rules.select(cs.alphanumeric()))
# columns: abc, abc123, 123

print(df_name_rules.select(cs.digit()))
# columns: 123

print(df_name_rules.select(cs.alpha(ignore_spaces=True)))
# columns: abc, has space


#----------------------------------------------------------------------------------------------------#
#------------------------------------ 5. Select columns by position ----------------------------------#
#----------------------------------------------------------------------------------------------------#

############
## cs.all ##
############
'''
cs.all() selects all columns.
It is similar in spirit to pl.all(), but it is a selector.
'''

print(df_people.select(cs.all()))
# all columns

##############
## cs.first ##
##############
'''
cs.first() selects the first column in the current schema/context.
'''

print(df_people.select(cs.first()))
# column: id

#############
## cs.last ##
#############
'''
cs.last() selects the last column in the current schema/context.
'''

print(df_people.select(cs.last()))
# column: pay_info

#################
## cs.by_index ##
#################
'''
cs.by_index(...) selects columns by their zero-based positions.
It also accepts range objects.
'''

print(df_people.select(cs.by_index(0, 1, 2)))
# first three columns by position

print(df_people.select(cs.by_index(range(3, 7))))
# columns at positions 3, 4, 5, 6

print(df_people.select(cs.by_index(-1)))
# last column by position


#----------------------------------------------------------------------------------------------------#
#------------------------------ 6. Combine selectors with set operations ----------------------------#
#----------------------------------------------------------------------------------------------------#
'''
Selectors support set operations:

+ A | B  -> union
+ A & B  -> intersection
+ A - B  -> difference
+ A ^ B  -> symmetric difference
+ ~A     -> complement

Important:
Selector results follow the original DataFrame schema order, not the order of the
set expression you wrote.
'''

##################
## Union: A | B ##
##################

print(df_people.select(cs.string() | cs.boolean()))
# all string columns plus boolean columns, in schema order

print(df_people.select(cs.temporal() | cs.starts_with("score_")))
# temporal columns plus score columns

#########################
## Intersection: A & B ##
#########################

print(df_people.select(cs.numeric() & cs.ends_with("_usd")))
# numeric columns whose names end with _usd: salary_usd, bonus_usd

print(df_people.select(cs.float() & cs.contains("score")))
# float columns whose names contain score: score_2023, score_2024

#######################
## Difference: A - B ##
#######################

print(df_people.select(cs.numeric() - cs.by_name("id")))
# numeric columns except id

print(df_people.select(cs.all() - cs.nested()))
# all columns except List, Array, and Struct columns

#################################
## Symmetric difference: A ^ B ##
#################################
'''
A ^ B means columns that are in A or B, but not both (exclusive OR).
'''

print(df_people.select(cs.starts_with("score") ^ cs.ends_with("_2024")))
# score_2023 is selected; score_2024 is in both sides, so it is removed

####################
## Complement: ~A ##
####################

print(df_people.select(~cs.numeric()))
# all non-numeric columns

print(df_people.select(~cs.by_name("id", "employee name")))
# all columns except id and employee name


#----------------------------------------------------------------------------------------------------#
#------------------ 7. Use selectors with expressions in select(), with_columns(), group_by() --------#
#----------------------------------------------------------------------------------------------------#

##########################
## select() expressions ##
##########################
'''
Selectors can broadcast expression methods over all matched columns.

Example: round all float columns.
'''

print(
    df_people.select(
        cs.float().round(1)
    )
)
# Every float column is rounded.

print(
    df_people.select(
        (cs.numeric() * 2).name.suffix("_x2")
    )
)
# Every numeric column is multiplied by 2 and renamed with a suffix.

################################
## with_columns() expressions ##
################################
'''
with_columns() keeps all original columns and adds/replaces transformed columns.

Example: uppercase all string columns.
'''

print(
    df_people.with_columns(
        cs.string().str.to_uppercase()
    )
)
# String columns are uppercased in place.

print(
    df_people.with_columns(
        (cs.ends_with("_usd") / 1000).name.suffix("_thousands")
    )
)
# Adds salary_usd_thousands and bonus_usd_thousands.

#######################
## group_by() + agg  ##
#######################
'''
Selectors can be used in group_by() and agg().

A common pattern:
+ group by selected categorical/string columns
+ aggregate selected numeric columns
'''

print(
    df_people.group_by(cs.by_name("dept")).agg(
        cs.ends_with("_usd").sum()
    )
)
# Sum all _usd columns by department.

print(
    df_people.group_by(cs.categorical()).agg(
        cs.numeric().mean()
    )
)
# Group by categorical columns and compute the mean of numeric columns.

##################################
## Selector.exclude(...) method ##
##################################
'''
Selector objects also have an .exclude(...) method.

This is convenient when you first select a broad group, then remove a few columns.
'''

print(df_people.select(cs.numeric().exclude("id")))
# numeric columns except id

print(df_people.select(cs.all().exclude("payload", "pay_info")))
# all columns except payload and pay_info

#####################
## cs.exclude(...) ##
#####################
'''
cs.exclude(...) is a selector-level helper for selecting everything except the
specified names, dtypes, or selectors.
'''

print(df_people.select(cs.exclude("payload", "pay_info")))
# all columns except payload and pay_info

print(df_people.select(cs.exclude(cs.nested())))
# all columns except nested columns

print(df_people.select(cs.exclude(pl.Boolean)))
# all columns except Boolean columns


#----------------------------------------------------------------------------------------------------#
#------------------------------ 8. Avoid operator ambiguity with as_expr() --------------------------#
#----------------------------------------------------------------------------------------------------#
'''
Some Python operators have different meanings for selectors and expressions.

Example:
+ ~cs.boolean() means "select all columns that are NOT Boolean".
+ ~cs.boolean().as_expr() means "take Boolean columns and negate their values".

Use .as_expr() when you want expression behavior instead of selector-set behavior.
'''

df_flags = pl.DataFrame(
    {
        "name": ["Ada", "Bob", "Charlie"],
        "has_badge": [True, False, True],
        "has_laptop": [True, True, False],
        "score": [91, 88, 95],
    }
)

# Selector complement: select non-Boolean columns.
print(df_flags.select(~cs.boolean()))
# shape: (3, 2)
# ┌─────────┬───────┐
# │ name    ┆ score │
# │ ---     ┆ ---   │
# │ str     ┆ i64   │
# ╞═════════╪═══════╡
# │ Ada     ┆ 91    │
# │ Bob     ┆ 88    │
# │ Charlie ┆ 95    │
# └─────────┴───────┘

# Expression negation: keep Boolean columns and invert their values.
print(df_flags.select((~cs.boolean().as_expr()).name.prefix("not_")))
# shape: (3, 2)
# ┌───────────────┬────────────────┐
# │ not_has_badge ┆ not_has_laptop │
# │ ---           ┆ ---            │
# │ bool          ┆ bool           │
# ╞═══════════════╪════════════════╡
# │ false         ┆ false          │
# │ true          ┆ false          │
# │ false         ┆ true           │
# └───────────────┴────────────────┘

################################

# Another example: use OR on selector sets vs OR on expression values.
print(df_flags.select(cs.starts_with("has_") | cs.by_name("score")))
# selector union: has_badge, has_laptop, score

print(
    df_flags.select(
        (cs.starts_with("has_").as_expr() | (pl.col("score") > 90)).name.suffix("_or_high_score")
    )
)
# expression OR: Boolean logic applied to the values.


#----------------------------------------------------------------------------------------------------#
#--------------------------- 9. Debug selectors with utilities --------------------------------------#
#----------------------------------------------------------------------------------------------------#

####################
## cs.is_selector ##
####################
'''
cs.is_selector(obj) checks whether an object is a selector.
This is useful when code starts mixing selectors and normal expressions.
'''

selector_numeric_no_id = cs.numeric() - cs.by_name("id")
print(cs.is_selector(selector_numeric_no_id))
# True

expr_numeric_no_id = selector_numeric_no_id.as_expr()
print(cs.is_selector(expr_numeric_no_id))
# False

########################
## cs.expand_selector ##
########################
'''
cs.expand_selector(target, selector) shows which columns a selector expands to
for a particular DataFrame, LazyFrame, or schema.

This is one of the best ways to debug selector logic.
'''

print(cs.expand_selector(df_people, cs.numeric()))
# ('id', 'salary_usd', 'bonus_usd', 'score_2023', 'score_2024', 'commission', '2024')
# tuple of numeric column names

print(cs.expand_selector(df_people, cs.numeric() & cs.ends_with("_usd")))
# ('salary_usd', 'bonus_usd')

print(cs.expand_selector(df_people, cs.all() - cs.nested()))
# all non-nested column names


#----------------------------------------------------------------------------------------------------#
#---------------------------------- 10. Selectors in LazyFrame --------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
Selectors work naturally in LazyFrame pipelines because they resolve against the
LazyFrame schema.

Like other lazy operations, nothing is executed until collect().
'''

lf_people = df_people.lazy()

lazy_query = (
    lf_people
    .select(
        cs.by_name("dept"),
        cs.ends_with("_usd"),
        cs.starts_with("score_"),
    )
    .with_columns(
        (cs.ends_with("_usd") / 1000).name.suffix("_k")
    )
)

print(lazy_query.collect())
# shape: (4, 7)
# ┌─────────┬────────────┬───────────┬────────────┬────────────┬──────────────┬─────────────┐
# │ dept    ┆ salary_usd ┆ bonus_usd ┆ score_2023 ┆ score_2024 ┆ salary_usd_k ┆ bonus_usd_k │
# │ ---     ┆ ---        ┆ ---       ┆ ---        ┆ ---        ┆ ---          ┆ ---         │
# │ str     ┆ f64        ┆ i64       ┆ f64        ┆ f64        ┆ f64          ┆ f64         │
# ╞═════════╪════════════╪═══════════╪════════════╪════════════╪══════════════╪═════════════╡
# │ IT      ┆ 120000.00  ┆ 10000     ┆ 91.50      ┆ 93.00      ┆ 120.00       ┆ 10.00       │
# │ HR      ┆ 90000.00   ┆ 5000      ┆ 88.00      ┆ 90.00      ┆ 90.00        ┆ 5.00        │
# │ IT      ┆ 110000.00  ┆ 7500      ┆ 95.00      ┆ 96.50      ┆ 110.00       ┆ 7.50        │
# │ Finance ┆ 130000.00  ┆ 12000     ┆ 89.50      ┆ 92.00      ┆ 130.00       ┆ 12.00       │
# └─────────┴────────────┴───────────┴────────────┴────────────┴──────────────┴─────────────┘

print(lazy_query.explain())
# WITH_COLUMNS:
# [[(col("salary_usd")) / (1000.00)].alias("salary_usd_k"), [(col("bonus_usd")) / (1000)].alias("bonus_usd_k")]
#  DF ["id", "employee name", "dept", "salary_usd", ...]; PROJECT["dept", "salary_usd", "bonus_usd", "score_2023", ...] 5/21 COLUMNS
# Shows the lazy query plan.


#----------------------------------------------------------------------------------------------------#
#------------------------------ 11. Categorized selector API list -----------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
Below is a categorized map of the selector APIs documented in Polars.
This final section is a reference list, not a full demo of every function.

A. Base selector object and methods
-----------------------------------
+ cs.Selector()
    Base selector expression/proxy.

+ selector.as_expr()
    Materialize a selector as a normal expression.
    Useful when operators such as ~, |, &, and - should operate on values rather
    than on selector sets.

+ selector.exclude(columns, *more_columns)
    Exclude columns from a broad selector such as cs.all(), cs.numeric(), etc.


B. Positional selectors
-----------------------
+ cs.all()
    Select all columns.

+ cs.first(strict=True)
    Select the first column in the current scope.

+ cs.last(strict=True)
    Select the last column in the current scope.

+ cs.by_index(*indices, require_all=True)
    Select columns by zero-based position, negative position, or range object.


C. Name and pattern selectors
-----------------------------
+ cs.by_name(*names, require_all=True)
    Select columns by exact names.

+ cs.starts_with(*prefix)
    Select columns whose names start with the given prefix or prefixes.

+ cs.ends_with(*suffix)
    Select columns whose names end with the given suffix or suffixes.

+ cs.contains(*substring)
    Select columns whose names contain the given literal substring or substrings.

+ cs.matches(pattern)
    Select columns whose names match a regular expression.

+ cs.alpha(ascii_only=False, ignore_spaces=False)
    Select columns with alphabetic names.

+ cs.alphanumeric(ascii_only=False, ignore_spaces=False)
    Select columns with alphanumeric names.

+ cs.digit(ascii_only=False)
    Select columns whose names consist only of digits.


D. Data type selectors
----------------------
+ cs.by_dtype(*dtypes)
    Select columns matching exact Polars dtypes.

+ cs.numeric()
    Select all numeric columns: integer, float, and Decimal.

+ cs.integer()
    Select all integer columns, signed and unsigned.

+ cs.signed_integer()
    Select signed integer columns.

+ cs.unsigned_integer()
    Select unsigned integer columns.

+ cs.float()
    Select floating-point columns.

+ cs.decimal()
    Select Decimal columns.

+ cs.boolean()
    Select Boolean columns.

+ cs.string(include_categorical=False)
    Select String columns; optionally include Categorical columns.

+ cs.categorical()
    Select Categorical columns.

+ cs.enum()
    Select Enum columns.

+ cs.binary()
    Select Binary columns.


E. Temporal selectors
---------------------
+ cs.date()
    Select Date columns.

+ cs.datetime(time_unit=None, time_zone=None)
    Select Datetime columns, optionally filtering by time unit or time zone.

+ cs.time()
    Select Time columns.

+ cs.duration(time_unit=None)
    Select Duration columns, optionally filtering by time unit.

+ cs.temporal()
    Select all temporal columns.


F. Nested selectors
-------------------
+ cs.list(inner=None)
    Select List columns; optionally match inner dtype/selector.

+ cs.array(inner=None, width=None)
    Select fixed-size Array columns; optionally match inner dtype/selector and width.

+ cs.struct()
    Select Struct columns.

+ cs.nested()
    Select nested columns, such as List, Array, and Struct.


G. Selector utility functions
-----------------------------
+ cs.exclude(columns, *more_columns)
    Select all columns except those matching given names, dtypes, or selectors.

+ cs.expand_selector(target, selector, strict=True)
    Resolve a selector to the tuple of matching column names for a target frame/schema.

+ cs.is_selector(obj)
    Return True if obj is a selector, otherwise False.


H. Selector set operations
--------------------------
+ A | B
    Union: columns matched by either A or B.

+ A & B
    Intersection: columns matched by both A and B.

+ A - B
    Difference: columns matched by A but not B.

+ A ^ B
    Symmetric difference: columns matched by A or B, but not both.

+ ~A
    Complement: columns not matched by A.

Remember:
Selector set operations preserve the DataFrame schema order of selected columns.
'''
