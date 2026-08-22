# FILE VERSION: 05_where_filter_predicates_v1
'''
Polars SQL: WHERE filters and predicate expressions.

This file focuses on the SQL WHERE clause and common predicates.
It is the SQL adaptation of native Polars filtering patterns such as:

    lf.filter(condition)
    df.filter(condition)

Main ideas:
1. WHERE keeps rows where the predicate evaluates to TRUE.
2. Rows where the predicate is FALSE or NULL are not kept.
3. SQL uses AND / OR / NOT for boolean composition.
4. Use parentheses when mixing AND and OR.
5. SQL comparison predicates map naturally to native Polars comparison expressions.
6. IN and BETWEEN are concise SQL equivalents of .is_in(...) and .is_between(...).
7. LIKE / ILIKE / RLIKE are string-pattern predicates.
8. IS NULL / IS NOT NULL should be used for missing values, not = NULL.
9. IS DISTINCT FROM / IS NOT DISTINCT FROM are NULL-safe equality predicates.
10. Boolean columns can be filtered directly or with IS TRUE / IS FALSE.

Important Polars SQL differences from native Polars:
+ Native Polars uses Python operators: &, |, and ~.
+ SQL uses AND, OR, and NOT.
+ Native Polars uses == for equality.
+ SQL normally uses = for equality, though Polars SQL also supports ==.
+ Native Polars uses .is_null(), .is_not_null(), .is_in(), .is_between().
+ SQL uses IS NULL, IS NOT NULL, IN, and BETWEEN.
+ In both SQL WHERE and native Polars filter(), only TRUE rows are kept.
  NULL predicates behave like unknown and are not kept.

Docs checked while writing this file:
+ https://docs.pola.rs/user-guide/sql/select/
+ https://docs.pola.rs/api/python/stable/reference/sql/index.html
+ https://docs.pola.rs/api/python/stable/reference/sql/operators/index.html
+ https://docs.pola.rs/api/python/stable/reference/lazyframe/api/polars.LazyFrame.filter.html
'''

import datetime as dt

import polars as pl
from polars import col as c
from polars.testing import assert_frame_equal

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(12)
pl.Config.set_tbl_width_chars(120)
pl.Config.set_float_precision(2)


# =========================================================================================
# 0. Setup Data
# =========================================================================================
'''
The examples use a small employee table.

The column names are intentionally SQL-friendly in this file because the focus is
filtering, not quoted identifiers. Quoted identifiers were covered in file 04.

Columns:
+ employee_id            integer id
+ name                   employee name
+ dept                   department
+ city                   city name, with one null
+ salary_usd             numeric column, with one null
+ bonus_usd              numeric column, with several nulls
+ score_2024             numeric score
+ is_manager             boolean column, with one null
+ hire_date              date column
+ manager_id             nullable integer, for NULL-safe comparison examples
+ backup_manager_id      nullable integer, for NULL-safe comparison examples
'''

df_emp = pl.DataFrame(
    {
        "employee_id": [1, 2, 3, 4, 5, 6, 7, 8],
        "name": ["Ada", "Bob", "Charlie", "Dana", "Evan", "Fay", "Grace", "Hana"],
        "dept": ["IT", "HR", "IT", "Finance", "IT", "Finance", "HR", "IT"],
        "city": ["London", "Paris", "London", "Berlin", "Lisbon", None, "Paris", "Hanoi"],
        "salary_usd": [120_000.0, 90_000.0, 110_000.0, 130_000.0, 105_000.0, None, 88_000.0, 99_000.0],
        "bonus_usd": [10_000.0, 5_000.0, 7_500.0, 12_000.0, None, 8_000.0, None, 4_000.0],
        "score_2024": [93.0, 88.0, 96.5, 92.0, 89.5, 91.0, 84.0, 90.0],
        "is_manager": [True, False, False, True, False, True, None, False],
        "hire_date": [
            dt.date(2020, 1, 15),
            dt.date(2021, 6, 1),
            dt.date(2019, 9, 20),
            dt.date(2018, 3, 10),
            dt.date(2022, 7, 8),
            dt.date(2017, 11, 30),
            dt.date(2023, 2, 14),
            dt.date(2024, 4, 5),
        ],
        "manager_id": [None, 1, 1, None, 3, 3, None, 2],
        "backup_manager_id": [None, 1, None, 4, 3, 2, None, 2],
    },
    schema_overrides={"dept": pl.Categorical}
)

lf_emp = df_emp.lazy()

print(df_emp)
print(df_emp.schema)


# =========================================================================================
# 1. Basic WHERE filter
# =========================================================================================
'''
WHERE filters rows.

Native Polars equivalent:
    lf.filter(c("salary_usd") >= 100_000)

Rows where salary_usd is null are not kept, because the comparison evaluates to
NULL/unknown, not TRUE.
'''

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        dept,
        salary_usd
    FROM self
    WHERE salary_usd >= 100000
    """
)
print(out_sql.collect())
# shape: (4, 4)
# ┌─────────────┬─────────┬─────────┬────────────┐
# │ employee_id ┆ name    ┆ dept    ┆ salary_usd │
# │ ---         ┆ ---     ┆ ---     ┆ ---        │
# │ i64         ┆ str     ┆ cat     ┆ f64        │
# ╞═════════════╪═════════╪═════════╪════════════╡
# │ 1           ┆ Ada     ┆ IT      ┆ 120000.00  │
# │ 3           ┆ Charlie ┆ IT      ┆ 110000.00  │
# │ 4           ┆ Dana    ┆ Finance ┆ 130000.00  │
# │ 5           ┆ Evan    ┆ IT      ┆ 105000.00  │
# └─────────────┴─────────┴─────────┴────────────┘

out_native = lf_emp.filter(
    c("salary_usd") >= 100_000
).select(
    "employee_id",
    "name",
    "dept",
    "salary_usd",
)

assert_frame_equal(out_sql.collect(), out_native.collect())


# =========================================================================================
# 2. Comparison operators
# =========================================================================================
'''
Common SQL comparison operators:

    =       equal
    !=      not equal
    <>      not equal, SQL-standard style
    >       greater than
    >=      greater than or equal
    <       less than
    <=      less than or equal

Polars SQL also supports == for equality, but = is the normal SQL spelling.
'''

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        dept,
        score_2024
    FROM self
    WHERE dept = 'IT' AND score_2024 > 90
    """
)
print(out_sql.collect())
# shape: (2, 4)
# ┌─────────────┬─────────┬──────┬────────────┐
# │ employee_id ┆ name    ┆ dept ┆ score_2024 │
# │ ---         ┆ ---     ┆ ---  ┆ ---        │
# │ i64         ┆ str     ┆ cat  ┆ f64        │
# ╞═════════════╪═════════╪══════╪════════════╡
# │ 1           ┆ Ada     ┆ IT   ┆ 93.00      │
# │ 3           ┆ Charlie ┆ IT   ┆ 96.50      │
# └─────────────┴─────────┴──────┴────────────┘


out_native = lf_emp.filter(
    (c("dept") == "IT") & (c("score_2024") > 90)
).select(
    "employee_id",
    "name",
    "dept",
    "score_2024",
)

assert_frame_equal(out_sql.collect(), out_native.collect())


# =========================================================================================
# 3. AND / OR / NOT
# =========================================================================================
'''
SQL uses AND, OR, and NOT to combine predicates.

Native Polars uses:
    &   for AND
    |   for OR
    ~   for NOT

Always use parentheses in native Polars because Python operator precedence can be
surprising. Parentheses are also recommended in SQL when mixing AND and OR.
'''

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        dept,
        salary_usd,
        score_2024,
        bonus_usd
    FROM self
    WHERE
        (score_2024 >= 90 OR bonus_usd IS NULL)
        AND NOT (dept = 'HR')
    """
)
print(out_sql.collect())
# shape: (6, 6)
# ┌─────────────┬─────────┬─────────┬────────────┬────────────┬───────────┐
# │ employee_id ┆ name    ┆ dept    ┆ salary_usd ┆ score_2024 ┆ bonus_usd │
# │ ---         ┆ ---     ┆ ---     ┆ ---        ┆ ---        ┆ ---       │
# │ i64         ┆ str     ┆ cat     ┆ f64        ┆ f64        ┆ f64       │
# ╞═════════════╪═════════╪═════════╪════════════╪════════════╪═══════════╡
# │ 1           ┆ Ada     ┆ IT      ┆ 120000.00  ┆ 93.00      ┆ 10000.00  │
# │ 3           ┆ Charlie ┆ IT      ┆ 110000.00  ┆ 96.50      ┆ 7500.00   │
# │ 4           ┆ Dana    ┆ Finance ┆ 130000.00  ┆ 92.00      ┆ 12000.00  │
# │ 5           ┆ Evan    ┆ IT      ┆ 105000.00  ┆ 89.50      ┆ null      │
# │ 6           ┆ Fay     ┆ Finance ┆ null       ┆ 91.00      ┆ 8000.00   │
# │ 8           ┆ Hana    ┆ IT      ┆ 99000.00   ┆ 90.00      ┆ 4000.00   │
# └─────────────┴─────────┴─────────┴────────────┴────────────┴───────────┘

out_native = lf_emp.filter(
    ((c("score_2024") >= 90) | c("bonus_usd").is_null())
    & ~(c("dept") == "HR")
).select(
    "employee_id",
    "name",
    "dept",
    "salary_usd",
    "score_2024",
    "bonus_usd",
)

assert_frame_equal(out_sql.collect(), out_native.collect())


# =========================================================================================
# 4. Boolean columns in WHERE
# =========================================================================================
'''
A boolean column can be used directly in WHERE.

    WHERE is_manager

means:

    keep rows where is_manager is TRUE

Rows where is_manager is FALSE or NULL are not kept.

You can also write:
    WHERE is_manager IS TRUE
    WHERE is_manager IS FALSE
'''

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        is_manager
    FROM self
    WHERE is_manager
    """
)
print(out_sql.collect())
# shape: (3, 3)
# ┌─────────────┬──────┬────────────┐
# │ employee_id ┆ name ┆ is_manager │
# │ ---         ┆ ---  ┆ ---        │
# │ i64         ┆ str  ┆ bool       │
# ╞═════════════╪══════╪════════════╡
# │ 1           ┆ Ada  ┆ true       │
# │ 4           ┆ Dana ┆ true       │
# │ 6           ┆ Fay  ┆ true       │
# └─────────────┴──────┴────────────┘

out_native = lf_emp.filter(
    c("is_manager")
).select(
    "employee_id",
    "name",
    "is_manager",
)

assert_frame_equal(out_sql.collect(), out_native.collect())

##------##
## Explicit TRUE version.
##------##

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        is_manager
    FROM self
    WHERE is_manager IS TRUE
    """
)

print(out_sql.collect())

out_native = lf_emp.filter(
    c("is_manager") == True
).select(
    "employee_id",
    "name",
    "is_manager",
)

assert_frame_equal(out_sql.collect(), out_native.collect())

##------##
## Explicit FALSE version.
##------##

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        is_manager
    FROM self
    WHERE is_manager IS FALSE
    """
)

print(out_sql.collect())

out_native = lf_emp.filter(
    c("is_manager") == False
).select(
    "employee_id",
    "name",
    "is_manager",
)

assert_frame_equal(out_sql.collect(), out_native.collect())


# =========================================================================================
# 5. IN and NOT IN
# =========================================================================================
'''
IN checks membership in a list of literal values.

Native Polars equivalent:
    c("dept").is_in([...])

NOT IN is equivalent to negating .is_in(...).
'''

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        dept,
        city
    FROM self
    WHERE dept IN ('IT', 'Finance')
    """
)
print(out_sql.collect())
# shape: (6, 4)
# ┌─────────────┬─────────┬─────────┬────────┐
# │ employee_id ┆ name    ┆ dept    ┆ city   │
# │ ---         ┆ ---     ┆ ---     ┆ ---    │
# │ i64         ┆ str     ┆ cat     ┆ cat    │
# ╞═════════════╪═════════╪═════════╪════════╡
# │ 1           ┆ Ada     ┆ IT      ┆ London │
# │ 3           ┆ Charlie ┆ IT      ┆ London │
# │ 4           ┆ Dana    ┆ Finance ┆ Berlin │
# │ 5           ┆ Evan    ┆ IT      ┆ Lisbon │
# │ 6           ┆ Fay     ┆ Finance ┆ null   │
# │ 8           ┆ Hana    ┆ IT      ┆ Hanoi  │
# └─────────────┴─────────┴─────────┴────────┘

out_native = lf_emp.filter(
    c("dept").is_in(["IT", "Finance"])
).select(
    "employee_id",
    "name",
    "dept",
    "city",
)

assert_frame_equal(out_sql.collect(), out_native.collect())

##----------------------##

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        dept
    FROM self
    WHERE dept NOT IN ('HR')
    """
)
print(out_sql.collect())
# shape: (6, 3)
# ┌─────────────┬─────────┬─────────┐
# │ employee_id ┆ name    ┆ dept    │
# │ ---         ┆ ---     ┆ ---     │
# │ i64         ┆ str     ┆ cat     │
# ╞═════════════╪═════════╪═════════╡
# │ 1           ┆ Ada     ┆ IT      │
# │ 3           ┆ Charlie ┆ IT      │
# │ 4           ┆ Dana    ┆ Finance │
# │ 5           ┆ Evan    ┆ IT      │
# │ 6           ┆ Fay     ┆ Finance │
# │ 8           ┆ Hana    ┆ IT      │
# └─────────────┴─────────┴─────────┘

out_native = lf_emp.filter(
    ~c("dept").is_in(["HR"])
).select(
    "employee_id",
    "name",
    "dept",
)

assert_frame_equal(out_sql.collect(), out_native.collect())


# =========================================================================================
# 6. BETWEEN and NOT BETWEEN
# =========================================================================================
'''
BETWEEN is inclusive in SQL:

    score_2024 BETWEEN 90 AND 95

means:

    score_2024 >= 90 AND score_2024 <= 95

Native Polars equivalent:
    c("score_2024").is_between(90, 95)

The default native Polars interval is also closed on both sides.
'''

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        score_2024
    FROM self
    WHERE score_2024 BETWEEN 90 AND 95
    """
)
print(out_sql.collect())
# shape: (4, 3)
# ┌─────────────┬──────┬────────────┐
# │ employee_id ┆ name ┆ score_2024 │
# │ ---         ┆ ---  ┆ ---        │
# │ i64         ┆ str  ┆ f64        │
# ╞═════════════╪══════╪════════════╡
# │ 1           ┆ Ada  ┆ 93.00      │
# │ 4           ┆ Dana ┆ 92.00      │
# │ 6           ┆ Fay  ┆ 91.00      │
# │ 8           ┆ Hana ┆ 90.00      │
# └─────────────┴──────┴────────────┘

out_native = lf_emp.filter(
    c("score_2024").is_between(90, 95)
).select(
    "employee_id",
    "name",
    "score_2024",
)

assert_frame_equal(out_sql.collect(), out_native.collect())

##-------------------##

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        score_2024
    FROM self
    WHERE score_2024 NOT BETWEEN 90 AND 95
    """
)
print(out_sql.collect())
# shape: (4, 3)
# ┌─────────────┬─────────┬────────────┐
# │ employee_id ┆ name    ┆ score_2024 │
# │ ---         ┆ ---     ┆ ---        │
# │ i64         ┆ str     ┆ f64        │
# ╞═════════════╪═════════╪════════════╡
# │ 2           ┆ Bob     ┆ 88.00      │
# │ 3           ┆ Charlie ┆ 96.50      │
# │ 5           ┆ Evan    ┆ 89.50      │
# │ 7           ┆ Grace   ┆ 84.00      │
# └─────────────┴─────────┴────────────┘

out_native = lf_emp.filter(
    ~c("score_2024").is_between(90, 95)
).select(
    "employee_id",
    "name",
    "score_2024",
)

assert_frame_equal(out_sql.collect(), out_native.collect())


# =========================================================================================
# 7. LIKE and ILIKE
# =========================================================================================
'''
LIKE filters strings using SQL wildcard patterns:

    %   zero or more characters
    _   exactly one character

ILIKE is the case-insensitive version.

Native Polars equivalents often use:
    .str.starts_with(...)
    .str.ends_with(...)
    .str.contains(...)

Use LIKE/ILIKE for SQL-style pattern matching. More general string functions are
covered in a later SQL functions file.
'''

# Names starting with A.
out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name
    FROM self
    WHERE name LIKE 'A%'
    """
)
print(out_sql.collect())
# shape: (1, 2)
# ┌─────────────┬──────┐
# │ employee_id ┆ name │
# │ ---         ┆ ---  │
# │ i64         ┆ str  │
# ╞═════════════╪══════╡
# │ 1           ┆ Ada  │
# └─────────────┴──────┘

out_native = lf_emp.filter(
    c("name").str.starts_with("A")
).select(
    "employee_id",
    "name",
)

assert_frame_equal(out_sql.collect(), out_native.collect())

##---------------------##

# Names that contain "an", case-insensitive.
out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name
    FROM self
    WHERE name ILIKE '%AN%'
    """
)
print(out_sql.collect())
# shape: (3, 2)
# ┌─────────────┬──────┐
# │ employee_id ┆ name │
# │ ---         ┆ ---  │
# │ i64         ┆ str  │
# ╞═════════════╪══════╡
# │ 4           ┆ Dana │
# │ 5           ┆ Evan │
# │ 8           ┆ Hana │
# └─────────────┴──────┘

out_native = lf_emp.filter(
    c("name").str.contains("(?i)an")
).select(
    "employee_id",
    "name",
)

assert_frame_equal(out_sql.collect(), out_native.collect())

##------------------------##

# Cities whose second letter is "a".
# The pattern '_a%' means: one character, then a, then anything.
out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        city
    FROM self
    WHERE city LIKE '_a%'
    """
)
print(out_sql.collect())
# shape: (3, 3)
# ┌─────────────┬───────┬───────┐
# │ employee_id ┆ name  ┆ city  │
# │ ---         ┆ ---   ┆ ---   │
# │ i64         ┆ str   ┆ str   │
# ╞═════════════╪═══════╪═══════╡
# │ 2           ┆ Bob   ┆ Paris │
# │ 7           ┆ Grace ┆ Paris │
# │ 8           ┆ Hana  ┆ Hanoi │
# └─────────────┴───────┴───────┘

out_native = lf_emp.filter(
    c("city").str.contains(r"^.a")
).select(
    "employee_id",
    "name",
    "city",
)

assert_frame_equal(out_sql.collect(), out_native.collect())


# =========================================================================================
# 8. Regex predicates
# =========================================================================================
'''
Polars SQL also supports regex-style predicates such as RLIKE / REGEXP and
PostgreSQL-style operators such as ~.

This is close to native Polars .str.contains(regex).

Keep SQL LIKE and regex separate in your head:
+ LIKE uses SQL wildcards such as % and _.
+ RLIKE / REGEXP uses regular expressions.
'''

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name
    FROM self
    WHERE name RLIKE '^D|e$'
    """
)
print(out_sql.collect())
# shape: (3, 2)
# ┌─────────────┬─────────┐
# │ employee_id ┆ name    │
# │ ---         ┆ ---     │
# │ i64         ┆ str     │
# ╞═════════════╪═════════╡
# │ 3           ┆ Charlie │
# │ 4           ┆ Dana    │
# │ 7           ┆ Grace   │
# └─────────────┴─────────┘

out_native = lf_emp.filter(
    c("name").str.contains(r"^D|e$")
).select(
    "employee_id",
    "name",
)

assert_frame_equal(out_sql.collect(), out_native.collect())

##------------------------##

# Equivalent PostgreSQL-style regex operator.
out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name
    FROM self
    WHERE name ~ '^D|e$'
    """
)
print(out_sql.collect())

assert_frame_equal(out_sql.collect(), out_native.collect())


# =========================================================================================
# 9. IS NULL and IS NOT NULL
# =========================================================================================
'''
Use IS NULL / IS NOT NULL for missing values.

Do NOT write:
    WHERE bonus_usd = NULL

In SQL, NULL means unknown/missing. Equality comparisons against NULL are not the
right tool for missing-value detection.

Native Polars equivalents:
    c("bonus_usd").is_null()
    c("bonus_usd").is_not_null()
'''

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        bonus_usd
    FROM self
    WHERE bonus_usd IS NULL
    """
)
print(out_sql.collect())
# shape: (2, 3)
# ┌─────────────┬───────┬───────────┐
# │ employee_id ┆ name  ┆ bonus_usd │
# │ ---         ┆ ---   ┆ ---       │
# │ i64         ┆ str   ┆ f64       │
# ╞═════════════╪═══════╪═══════════╡
# │ 5           ┆ Evan  ┆ null      │
# │ 7           ┆ Grace ┆ null      │
# └─────────────┴───────┴───────────┘

out_native = lf_emp.filter(
    c("bonus_usd").is_null()
).select(
    "employee_id",
    "name",
    "bonus_usd",
)

assert_frame_equal(out_sql.collect(), out_native.collect())

##---------------------------------##

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        bonus_usd
    FROM self
    WHERE bonus_usd IS NOT NULL
    """
)
print(out_sql.collect())
# shape: (6, 3)
# ┌─────────────┬─────────┬───────────┐
# │ employee_id ┆ name    ┆ bonus_usd │
# │ ---         ┆ ---     ┆ ---       │
# │ i64         ┆ str     ┆ f64       │
# ╞═════════════╪═════════╪═══════════╡
# │ 1           ┆ Ada     ┆ 10000.00  │
# │ 2           ┆ Bob     ┆ 5000.00   │
# │ 3           ┆ Charlie ┆ 7500.00   │
# │ 4           ┆ Dana    ┆ 12000.00  │
# │ 6           ┆ Fay     ┆ 8000.00   │
# │ 8           ┆ Hana    ┆ 4000.00   │
# └─────────────┴─────────┴───────────┘

out_native = lf_emp.filter(
    c("bonus_usd").is_not_null()
).select(
    "employee_id",
    "name",
    "bonus_usd",
)

assert_frame_equal(out_sql.collect(), out_native.collect())


# =========================================================================================
# 10. NULL behavior in normal comparisons
# =========================================================================================
'''
Normal comparisons with NULL produce NULL/unknown.

Example:
    salary_usd > 100000

For rows where salary_usd is NULL, the predicate is NULL, not TRUE.
SQL WHERE keeps only TRUE rows, so those rows are filtered out.

Native Polars filter() behaves similarly: rows where the predicate is null are
not kept.
'''

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        salary_usd,
        salary_usd > 100000 AS high_salary_predicate
    FROM self
    WHERE salary_usd > 100000
    """
)
print(out_sql.collect())
# shape: (4, 4)
# ┌─────────────┬─────────┬────────────┬───────────────────────┐
# │ employee_id ┆ name    ┆ salary_usd ┆ high_salary_predicate │
# │ ---         ┆ ---     ┆ ---        ┆ ---                   │
# │ i64         ┆ str     ┆ f64        ┆ bool                  │
# ╞═════════════╪═════════╪════════════╪═══════════════════════╡
# │ 1           ┆ Ada     ┆ 120000.00  ┆ true                  │
# │ 3           ┆ Charlie ┆ 110000.00  ┆ true                  │
# │ 4           ┆ Dana    ┆ 130000.00  ┆ true                  │
# │ 5           ┆ Evan    ┆ 105000.00  ┆ true                  │
# └─────────────┴─────────┴────────────┴───────────────────────┘
'''null values are all filtered out'''

out_native = lf_emp.with_columns(
    (c("salary_usd") > 100_000).alias("high_salary_predicate")
).filter(
    c("salary_usd") > 100_000
).select(
    "employee_id",
    "name",
    "salary_usd",
    "high_salary_predicate",
)

assert_frame_equal(out_sql.collect(), out_native.collect())

##---------------------------------##

# If you want to keep rows where salary is high OR missing, say that explicitly.
out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        salary_usd
    FROM self
    WHERE salary_usd > 100000 OR salary_usd IS NULL
    """
)
print(out_sql.collect())
# shape: (5, 3)
# ┌─────────────┬─────────┬────────────┐
# │ employee_id ┆ name    ┆ salary_usd │
# │ ---         ┆ ---     ┆ ---        │
# │ i64         ┆ str     ┆ f64        │
# ╞═════════════╪═════════╪════════════╡
# │ 1           ┆ Ada     ┆ 120000.00  │
# │ 3           ┆ Charlie ┆ 110000.00  │
# │ 4           ┆ Dana    ┆ 130000.00  │
# │ 5           ┆ Evan    ┆ 105000.00  │
# │ 6           ┆ Fay     ┆ null       │
# └─────────────┴─────────┴────────────┘

out_native = lf_emp.filter(
    (c("salary_usd") > 100_000) | c("salary_usd").is_null()
).select(
    "employee_id",
    "name",
    "salary_usd",
)

assert_frame_equal(out_sql.collect(), out_native.collect())


# =========================================================================================
# 11. NULL-safe equality: IS DISTINCT FROM
# =========================================================================================
'''
Normal equality does not treat two NULL values as equal.

SQL has NULL-safe comparison operators:

    a IS DISTINCT FROM b
    a IS NOT DISTINCT FROM b
    a <=> b                         # shorthand for IS NOT DISTINCT FROM

These are useful when matching nullable columns.

Native Polars can express the same logic manually:
    equal_non_null OR both_null
'''

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        manager_id,
        backup_manager_id
    FROM self
    WHERE manager_id IS NOT DISTINCT FROM backup_manager_id
    """
)
print(out_sql.collect())
# shape: (5, 4)
# ┌─────────────┬───────┬────────────┬───────────────────┐
# │ employee_id ┆ name  ┆ manager_id ┆ backup_manager_id │
# │ ---         ┆ ---   ┆ ---        ┆ ---               │
# │ i64         ┆ str   ┆ i64        ┆ i64               │
# ╞═════════════╪═══════╪════════════╪═══════════════════╡
# │ 1           ┆ Ada   ┆ null       ┆ null              │
# │ 2           ┆ Bob   ┆ 1          ┆ 1                 │
# │ 5           ┆ Evan  ┆ 3          ┆ 3                 │
# │ 7           ┆ Grace ┆ null       ┆ null              │
# │ 8           ┆ Hana  ┆ 2          ┆ 2                 │
# └─────────────┴───────┴────────────┴───────────────────┘

null_safe_equal = (
    (c("manager_id") == c("backup_manager_id")).fill_null(False)
    | (c("manager_id").is_null() & c("backup_manager_id").is_null())
)

out_native = lf_emp.filter(
    null_safe_equal
).select(
    "employee_id",
    "name",
    "manager_id",
    "backup_manager_id",
)

assert_frame_equal(out_sql.collect(), out_native.collect())

##------------------------------------##

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        manager_id,
        backup_manager_id
    FROM self
    WHERE manager_id IS DISTINCT FROM backup_manager_id
    """
)
print(out_sql.collect())
# shape: (3, 4)
# ┌─────────────┬─────────┬────────────┬───────────────────┐
# │ employee_id ┆ name    ┆ manager_id ┆ backup_manager_id │
# │ ---         ┆ ---     ┆ ---        ┆ ---               │
# │ i64         ┆ str     ┆ i64        ┆ i64               │
# ╞═════════════╪═════════╪════════════╪═══════════════════╡
# │ 3           ┆ Charlie ┆ 1          ┆ null              │
# │ 4           ┆ Dana    ┆ null       ┆ 4                 │
# │ 6           ┆ Fay     ┆ 3          ┆ 2                 │
# └─────────────┴─────────┴────────────┴───────────────────┘

out_native = lf_emp.filter(
    ~null_safe_equal
).select(
    "employee_id",
    "name",
    "manager_id",
    "backup_manager_id",
)

assert_frame_equal(out_sql.collect(), out_native.collect())

##-------------------------------------------##

# Same as IS NOT DISTINCT FROM, using the shorthand <=> operator.
out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        manager_id,
        backup_manager_id
    FROM self
    WHERE manager_id <=> backup_manager_id
    """
)
print(out_sql.collect())

out_native = lf_emp.filter(
    null_safe_equal
).select(
    "employee_id",
    "name",
    "manager_id",
    "backup_manager_id",
)

assert_frame_equal(out_sql.collect(), out_native.collect())


# =========================================================================================
# 12. Date predicates
# =========================================================================================
'''
Date and datetime filtering is often better handled with explicit casting or
native Polars temporal expressions.

Because type-casting is covered in the next SQL file, this section keeps the SQL
example simple: use EXTRACT(YEAR FROM hire_date) to filter by year.

Native Polars equivalent:
    c("hire_date").dt.year() >= 2021

More temporal SQL functions are covered later.
'''

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        name,
        hire_date
    FROM self
    WHERE EXTRACT(YEAR FROM hire_date) >= 2021
    """
)
print(out_sql.collect())
# shape: (4, 3)
# ┌─────────────┬───────┬────────────┐
# │ employee_id ┆ name  ┆ hire_date  │
# │ ---         ┆ ---   ┆ ---        │
# │ i64         ┆ str   ┆ date       │
# ╞═════════════╪═══════╪════════════╡
# │ 2           ┆ Bob   ┆ 2021-06-01 │
# │ 5           ┆ Evan  ┆ 2022-07-08 │
# │ 7           ┆ Grace ┆ 2023-02-14 │
# │ 8           ┆ Hana  ┆ 2024-04-05 │
# └─────────────┴───────┴────────────┘

##---------------------------------------------##

out_native = lf_emp.filter(
    c("hire_date").dt.year() >= 2021
).select(
    "employee_id",
    "name",
    "hire_date",
)

assert_frame_equal(out_sql.collect(), out_native.collect())


# =========================================================================================
# 13. WHERE with SQLContext tables
# =========================================================================================
'''
The examples above use lf_emp.sql(...), where the frame is named self.

The same WHERE predicates work with named tables inside SQLContext.
'''

ctx = pl.SQLContext(employees=lf_emp)
out_sql = ctx.execute(
    """
    SELECT
        employee_id,
        name,
        dept,
        salary_usd
    FROM employees
    WHERE dept = 'Finance' AND salary_usd >= 100000
    """
)
print(out_sql.collect())
# shape: (1, 4)
# ┌─────────────┬──────┬─────────┬────────────┐
# │ employee_id ┆ name ┆ dept    ┆ salary_usd │
# │ ---         ┆ ---  ┆ ---     ┆ ---        │
# │ i64         ┆ str  ┆ cat     ┆ f64        │
# ╞═════════════╪══════╪═════════╪════════════╡
# │ 4           ┆ Dana ┆ Finance ┆ 130000.00  │
# └─────────────┴──────┴─────────┴────────────┘

out_native = lf_emp.filter(
    (c("dept") == "Finance") & (c("salary_usd") >= 100_000)
).select(
    "employee_id",
    "name",
    "dept",
    "salary_usd",
)

assert_frame_equal(out_sql.collect(), out_native.collect())


# =========================================================================================
# 14. Quick reference
# =========================================================================================
'''
Quick pandas/native Polars/SQL mapping:

Native Polars:
    lf.filter(c("salary_usd") >= 100_000)
SQL:
    WHERE salary_usd >= 100000

Native Polars:
    lf.filter((c("dept") == "IT") & (c("score_2024") > 90))
SQL:
    WHERE dept = 'IT' AND score_2024 > 90

Native Polars:
    lf.filter(c("dept").is_in(["IT", "Finance"]))
SQL:
    WHERE dept IN ('IT', 'Finance')

Native Polars:
    lf.filter(c("score_2024").is_between(90, 95))
SQL:
    WHERE score_2024 BETWEEN 90 AND 95

Native Polars:
    lf.filter(c("bonus_usd").is_null())
SQL:
    WHERE bonus_usd IS NULL

Native Polars:
    lf.filter(c("name").str.starts_with("A"))
SQL:
    WHERE name LIKE 'A%'

Native Polars:
    lf.filter(c("name").str.contains(r"^D|e$"))
SQL:
    WHERE name RLIKE '^D|e$'

Common mistakes:
+ Do not write WHERE bonus_usd = NULL; use IS NULL.
+ Do not use Python &, |, ~ inside SQL; use AND, OR, NOT.
+ Do not forget parentheses when mixing AND and OR.
+ Do not expect SELECT aliases to be available in WHERE in every SQL dialect.
  If needed, repeat the expression or use a subquery/CTE.
'''
