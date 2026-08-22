'''
Boolean Indexing / Boolean Filtering in Polars

In pandas, you often filter a Series with bracket syntax:
    s[s > 10]

In Polars, the clearer and more idiomatic Series pattern is:
    s.filter(s > 10)

For DataFrames, filtering is usually expression based:
    df.filter(pl.col("score") > 80)

Key Differences from Pandas:
1. Polars Series do NOT have custom index labels.
   Filtering keeps the matching values in their original row order.
2. Use .filter(boolean_mask) for Series filtering.
3. In Polars, pandas .between() becomes .is_between().
4. In Polars, pandas .isin() becomes .is_in().
5. Polars does not provide pandas-style .dt.is_quarter_start / .dt.is_quarter_end.
   Build these boolean masks manually with .dt.month_start(), .dt.month_end(),
   .dt.month(), and normal comparisons.
6. In Polars, False and null values in a filter predicate are discarded.

##---------------------------##

1. Series Filtering with One Condition
   + Logic Operators: >, <, >=, <=, .is_between(), ==, !=
   + .is_in()
   + String Boolean: .str.contains(), .str.starts_with(), .str.ends_with()
   + DateTime Boolean: quarter start / quarter end masks

2. Negation of Condition: ~ (tilde) operator

3. Combine Multiple Conditions:
   + & (and)
   + | (or)
   + Combine & and |

4. DataFrame Filtering with df.filter(pl.col(...))
'''

import datetime as dt
import polars as pl


# =========================================================================================
# 0. Polars .filter() Basics
# =========================================================================================
'''
Series.filter(predicate) takes a Boolean Series or list of booleans.
Rows/elements where the predicate is True are kept.
Rows/elements where the predicate is False or null are discarded.
'''

s_basic = pl.Series("values", [1, 2, 3, 4])
mask_basic = pl.Series("mask", [True, False, True, False])

print(s_basic.filter(mask_basic).to_list())
# [1, 3]

##---------------------##

# Boolean masks can contain nulls; null is treated like "not True" and is discarded.
s_null_mask = pl.Series("values", [10, 20, 30])
mask_with_null = pl.Series("mask", [True, None, False])

print(s_null_mask.filter(mask_with_null).to_list())
# [10]


# =========================================================================================
# 1. Single Condition Examples
# =========================================================================================

s1_nums = pl.Series("s1_nums", [13.75, 19.51, 17.32, 15.99, 11.56, 11.56, 10.58, 18.66, 16.01, 17.08])
s2_nums = pl.Series("s2_nums", [13.21, 13.66, 17.10, 19.00, 15.34, 12.47, 16.72, 15.62, 15.43, 18.93])

print(s1_nums)
# shape: (10,)
# Series: 's1_nums' [f64]
# [13.75, 19.51, 17.32, 15.99, 11.56, 11.56, 10.58, 18.66, 16.01, 17.08]

print(s2_nums)
# shape: (10,)
# Series: 's2_nums' [f64]
# [13.21, 13.66, 17.1, 19.0, 15.34, 12.47, 16.72, 15.62, 15.43, 18.93]

##------------------------------------------------------##
## Logic Operators: >, <, >=, <=, .is_between(), ==, != ##
##------------------------------------------------------##

# ## > (greater than)
# 
print((s1_nums > 15).to_list())
# [False, True, True, True, False, False, False, True, True, True]

print(s1_nums.filter(s1_nums > 15).to_list())  # Returns values greater than 15 (True)
# [19.51, 17.32, 15.99, 18.66, 16.01, 17.08]

print(s2_nums.filter(s2_nums > s1_nums).to_list())  # Element-wise comparison by row position
# [19.0, 15.34, 12.47, 16.72, 18.93]

# ## < (less than)
# 
print(s1_nums.filter(s1_nums < 13).to_list())  # Returns values less than 13
# [11.56, 11.56, 10.58]

print(s2_nums.filter(s2_nums < s1_nums).to_list())  # Element-wise comparison by row position
# [13.21, 13.66, 17.1, 15.62, 15.43]

# ## >= (greater than or equal to)
# 
print(s1_nums.filter(s1_nums >= 15.99).to_list())
# [19.51, 17.32, 15.99, 18.66, 16.01, 17.08]

print(s2_nums.filter(s2_nums >= s1_nums).to_list())
# [19.0, 15.34, 12.47, 16.72, 18.93]

# ## <= (less than or equal to)
# 
print(s1_nums.filter(s1_nums <= 11.56).to_list())
# [11.56, 11.56, 10.58]

print(s2_nums.filter(s2_nums <= s1_nums).to_list())
# [13.21, 13.66, 17.1, 15.62, 15.43]

# ## .is_between()
# '''
Pandas: s.between(left, right, inclusive="both")
Polars: s.is_between(lower_bound, upper_bound, closed="both")

closed = "both"  : [left, right] or left <= x <= right
closed = "none"  : (left, right) or left < x < right
closed = "left"  : [left, right) or left <= x < right
closed = "right" : (left, right] or left < x <= right
'''

print(s1_nums.filter(s1_nums.is_between(10, 15.99)).to_list())
# [13.75, 15.99, 11.56, 11.56, 10.58]

print(s1_nums.filter(s1_nums.is_between(10, 15.99, closed="left")).to_list())
# [13.75, 11.56, 11.56, 10.58]
'''The value 15.99 is excluded because the right endpoint is not closed.'''

# ## == (equal to)
# 
print(s1_nums.filter(s1_nums == 11.56).to_list())
# [11.56, 11.56]

print(s2_nums.filter(s2_nums == s1_nums).to_list())
# []

# ## != (not equal to)
# 
print(s1_nums.filter(s1_nums != 11.56).to_list())
# [13.75, 19.51, 17.32, 15.99, 10.58, 18.66, 16.01, 17.08]

print(s2_nums.filter(s2_nums != s1_nums).to_list())
# [13.21, 13.66, 17.1, 19.0, 15.34, 12.47, 16.72, 15.62, 15.43, 18.93]
'''All values are returned because none of the values in s2_nums equal the corresponding row-position values in s1_nums.'''

##---------------------------##
##          .is_in()          ##
##---------------------------##

s_mammals = pl.Series("mammals", ["llama", "cow", "llama", "beetle", "llama", "hippo"])

print(s_mammals.is_in(["cow", "llama"]).to_list())
# [True, True, True, False, True, False]

print(s_mammals.filter(s_mammals.is_in(["cow", "llama"])).to_list())
# ['llama', 'cow', 'llama', 'llama']

print(s_mammals.filter(s_mammals.is_in(["llama"])).to_list())
# ['llama', 'llama', 'llama']

##------------------------------##
##        String Boolean        ##
##------------------------------##
'''
Polars uses the .str namespace for string operations.
By default, .str.contains() treats the pattern as regex.
Use literal=True when you want a plain substring search.
'''

timezones = [
    "Africa/Cairo",
    "Asia/Seoul",
    "Asia/Tokyo",
    "Australia/ACT",
    "Australia/Adelaide",
    "Australia/Brisbane",
    "Australia/Broken_Hill",
    "Australia/Darwin",
    "Australia/Eucla",
    "Etc/Zulu",
    "Europe/London",
    "Pacific/Honolulu",
    "Zulu",
    "Asia/Aqtau",
    "Asia/Aqtobe",
    "Asia/Baku",
    "Asia/Dushanbe",
    "Asia/Kathmandu",
    "Asia/Macau",
    "Asia/Singapore",
    "Asia/Thimbu",
    "Asia/Thimphu",
    "Asia/Vientiane",
]
s_timezones = pl.Series("timezone", timezones)

print(s_timezones.filter(s_timezones.str.contains("Seoul", literal=True)).to_list())
# ['Asia/Seoul']

print(s_timezones.filter(s_timezones.str.starts_with("Australia")).to_list())
# ['Australia/ACT', 'Australia/Adelaide', 'Australia/Brisbane', 'Australia/Broken_Hill', 'Australia/Darwin', 'Australia/Eucla']

print(s_timezones.filter(s_timezones.str.ends_with("lu")).to_list())
# ['Etc/Zulu', 'Pacific/Honolulu', 'Zulu']

print(s_timezones.filter(s_timezones == "Zulu").to_list())
# ['Zulu']

##-----------------------------##
##      DateTime Boolean       ##
##-----------------------------##
'''
Polars does not use pandas-style DateTimeIndex logic.
For Series, build a Boolean Series and call .filter(mask).

There is no direct pandas-style .dt.is_quarter_start / .dt.is_quarter_end.
The examples below create these masks manually.
'''

s_datetime = pl.Series(
    "date",
    [
        dt.date(2023, 1, 1),
        dt.date(2023, 1, 31),
        dt.date(2023, 2, 28),
        dt.date(2023, 3, 31),
        dt.date(2023, 4, 30),
        dt.date(2023, 5, 31),
        dt.date(2023, 6, 30),
    ],
)

print(s_datetime.dt.strftime("%Y-%m-%d").to_list())
# ['2023-01-01', '2023-01-31', '2023-02-28', '2023-03-31', '2023-04-30', '2023-05-31', '2023-06-30']

# Quarter start: month is Jan/Apr/Jul/Oct AND date is the first day of that month.
mask_quarter_start = s_datetime.dt.month().is_in([1, 4, 7, 10]) & (s_datetime == s_datetime.dt.month_start())
print(s_datetime.filter(mask_quarter_start).dt.strftime("%Y-%m-%d").to_list())
# ['2023-01-01']

# Quarter end: month is Mar/Jun/Sep/Dec AND date is the last day of that month.
mask_quarter_end = s_datetime.dt.month().is_in([3, 6, 9, 12]) & (s_datetime == s_datetime.dt.month_end())
print(s_datetime.filter(mask_quarter_end).dt.strftime("%Y-%m-%d").to_list())
# ['2023-03-31', '2023-06-30']


# =========================================================================================
# 2. Negation of Condition: ~ (tilde) operator
# =========================================================================================

'''
The tilde (~) operator negates a boolean condition in Polars.
True becomes False, and False becomes True.

For readability, always wrap complex conditions in parentheses before applying ~.
'''

print((s1_nums > 15).to_list())
# [False, True, True, True, False, False, False, True, True, True]

print((~(s1_nums > 15)).to_list())
# [True, False, False, False, True, True, True, False, False, False]

print(s1_nums.filter(~(s1_nums > 15)).to_list())
# [13.75, 11.56, 11.56, 10.58]

print(s_mammals.filter(~s_mammals.is_in(["cow", "llama"])).to_list())
# ['beetle', 'hippo']

print(s_datetime.filter(~mask_quarter_end).dt.strftime("%Y-%m-%d").to_list())
# ['2023-01-01', '2023-01-31', '2023-02-28', '2023-04-30', '2023-05-31']


# =========================================================================================
# 3. Combine Multiple Conditions
# =========================================================================================

##-----------------------##
##       & (and)         ##
##-----------------------##
'''True only when ALL conditions are True.'''

print(s1_nums.filter((s1_nums > 12) & (s1_nums.round(0) % 2 == 0)).to_list())
# [13.75, 19.51, 15.99, 16.01]

print(s1_nums.filter(~((s1_nums > 12) & (s1_nums.round(0) % 2 == 0))).to_list())
# [17.32, 11.56, 11.56, 10.58, 18.66, 17.08]

# Polars .str.ends_with() does not take a tuple like pandas.
# Use two .ends_with() conditions OR a regex pattern with .str.contains().
mask_asia_ending_e_or_u = s_timezones.str.contains("Asia", literal=True) & (
    s_timezones.str.ends_with("e") | s_timezones.str.ends_with("u")
)
print(s_timezones.filter(mask_asia_ending_e_or_u).to_list())
# ['Asia/Aqtau', 'Asia/Aqtobe', 'Asia/Baku', 'Asia/Dushanbe', 'Asia/Kathmandu', 'Asia/Macau', 'Asia/Singapore', 'Asia/Thimbu', 'Asia/Thimphu', 'Asia/Vientiane']

##-----------------------##
##       | (or)          ##
##-----------------------##
'''False only when ALL conditions are False.'''

print(s1_nums.filter((s1_nums < 12) | (s1_nums > 18)).to_list())
# [19.51, 11.56, 11.56, 10.58, 18.66]

print(s1_nums.filter(~((s1_nums < 12) | (s1_nums > 18))).to_list())
# [13.75, 17.32, 15.99, 16.01, 17.08]

mask_korea_or_japan = (
    s_timezones.str.contains("Kyoto", literal=True)
    | s_timezones.str.contains("Tokyo", literal=True)
    | s_timezones.str.contains("Seoul", literal=True)
)
print(s_timezones.filter(mask_korea_or_japan).to_list())
# ['Asia/Seoul', 'Asia/Tokyo']

##---------------------------##
##      Combine & and |      ##
##---------------------------##

print(s1_nums.filter(((s1_nums < 12) | (s1_nums > 18)) & (s1_nums.round(0) % 2 == 0)).to_list())
# [19.51, 11.56, 11.56]

print(s1_nums.filter(~(((s1_nums < 12) | (s1_nums > 18)) & (s1_nums.round(0) % 2 == 0))).to_list())
# [13.75, 17.32, 15.99, 10.58, 18.66, 16.01, 17.08]

mask_asia_ending_e_or_u_or_tokyo = mask_asia_ending_e_or_u | s_timezones.str.contains("Tokyo", literal=True)
print(s_timezones.filter(mask_asia_ending_e_or_u_or_tokyo).to_list())
# ['Asia/Tokyo', 'Asia/Aqtau', 'Asia/Aqtobe', 'Asia/Baku', 'Asia/Dushanbe', 'Asia/Kathmandu', 'Asia/Macau', 'Asia/Singapore', 'Asia/Thimbu', 'Asia/Thimphu', 'Asia/Vientiane']
'''
Though "Tokyo" does not end with "e" or "u" (first condition),
it satisfies the second condition, so it is returned.
'''


# =========================================================================================
# 4. DataFrame Filtering with .filter()
# =========================================================================================
'''
Most real Polars workflows filter DataFrames with expressions:

    df.filter(pl.col("column") > value)

Use pl.col("column") to refer to a column.
Use &, |, and ~ to combine or negate conditions.
Always wrap each condition in parentheses when combining with & or |.
'''

df_scores = pl.DataFrame(
    {
        "name": ["Ada", "Ben", "Cara", "Dan", "Eli", "Fay"],
        "city": ["Seoul", "Tokyo", "Seoul", "Busan", "Tokyo", "Seoul"],
        "score": [91, 78, 85, 62, 88, 70],
        "passed": [True, True, True, False, True, False],
    }
)

##------------------------##
## Basic DataFrame filter ##
##------------------------##

print(df_scores.filter(pl.col("score") > 80).to_dicts())
# [{'name': 'Ada', 'city': 'Seoul', 'score': 91, 'passed': True}, {'name': 'Cara', 'city': 'Seoul', 'score': 85, 'passed': True}, {'name': 'Eli', 'city': 'Tokyo', 'score': 88, 'passed': True}]

print(df_scores.filter(pl.col("city") == "Seoul").to_dicts())
# [{'name': 'Ada', 'city': 'Seoul', 'score': 91, 'passed': True}, {'name': 'Cara', 'city': 'Seoul', 'score': 85, 'passed': True}, {'name': 'Fay', 'city': 'Seoul', 'score': 70, 'passed': False}]

##----------------------------##
## .is_between() in DataFrame ##
##----------------------------##

print(df_scores.filter(pl.col("score").is_between(70, 88)).to_dicts())
# [{'name': 'Ben', 'city': 'Tokyo', 'score': 78, 'passed': True}, {'name': 'Cara', 'city': 'Seoul', 'score': 85, 'passed': True}, {'name': 'Eli', 'city': 'Tokyo', 'score': 88, 'passed': True}, {'name': 'Fay', 'city': 'Seoul', 'score': 70, 'passed': False}]

print(df_scores.filter(pl.col("score").is_between(70, 88, closed="left")).to_dicts())
# [{'name': 'Ben', 'city': 'Tokyo', 'score': 78, 'passed': True}, {'name': 'Cara', 'city': 'Seoul', 'score': 85, 'passed': True}, {'name': 'Fay', 'city': 'Seoul', 'score': 70, 'passed': False}]

##-----------------------##
## .is_in() in DataFrame ##
##-----------------------##

print(df_scores.filter(pl.col("city").is_in(["Seoul", "Busan"])).to_dicts())
# [{'name': 'Ada', 'city': 'Seoul', 'score': 91, 'passed': True}, {'name': 'Cara', 'city': 'Seoul', 'score': 85, 'passed': True}, {'name': 'Dan', 'city': 'Busan', 'score': 62, 'passed': False}, {'name': 'Fay', 'city': 'Seoul', 'score': 70, 'passed': False}]

##--------------------------##
## Multiple DataFrame masks ##
##--------------------------##

# AND: Seoul students who passed
print(df_scores.filter((pl.col("city") == "Seoul") & pl.col("passed")).to_dicts()) # not recommend (pl.col("passed") == True)
# [{'name': 'Ada', 'city': 'Seoul', 'score': 91, 'passed': True}, {'name': 'Cara', 'city': 'Seoul', 'score': 85, 'passed': True}]

# OR: low score OR Tokyo city
print(df_scores.filter((pl.col("score") < 75) | (pl.col("city") == "Tokyo")).to_dicts())
# [{'name': 'Ben', 'city': 'Tokyo', 'score': 78, 'passed': True}, {'name': 'Dan', 'city': 'Busan', 'score': 62, 'passed': False}, {'name': 'Eli', 'city': 'Tokyo', 'score': 88, 'passed': True}, {'name': 'Fay', 'city': 'Seoul', 'score': 70, 'passed': False}]

# Negation: everyone NOT in Seoul
print(df_scores.filter(~(pl.col("city") == "Seoul")).to_dicts())
# [{'name': 'Ben', 'city': 'Tokyo', 'score': 78, 'passed': True}, {'name': 'Dan', 'city': 'Busan', 'score': 62, 'passed': False}, {'name': 'Eli', 'city': 'Tokyo', 'score': 88, 'passed': True}]

##-----------------------------------##
## Multiple predicates as *arguments ##
##-----------------------------------##
'''
DataFrame.filter() can receive multiple predicates.
Multiple predicates are implicitly combined with AND.
'''

print(
    df_scores.filter(
        pl.col("score") >= 80,
        pl.col("city").is_in(["Seoul", "Tokyo"]),
    ).to_dicts()
)
# [{'name': 'Ada', 'city': 'Seoul', 'score': 91, 'passed': True}, {'name': 'Cara', 'city': 'Seoul', 'score': 85, 'passed': True}, {'name': 'Eli', 'city': 'Tokyo', 'score': 88, 'passed': True}]

##------------------------------------##
## Keyword constraints in df.filter() ##
##------------------------------------##
'''
Polars also supports keyword constraints in DataFrame.filter().
For example, df.filter(city="Seoul") behaves like:
    df.filter(pl.col("city") == "Seoul")
'''

print(df_scores.filter(city="Seoul").to_dicts())
# [{'name': 'Ada', 'city': 'Seoul', 'score': 91, 'passed': True}, {'name': 'Cara', 'city': 'Seoul', 'score': 85, 'passed': True}, {'name': 'Fay', 'city': 'Seoul', 'score': 70, 'passed': False}]
