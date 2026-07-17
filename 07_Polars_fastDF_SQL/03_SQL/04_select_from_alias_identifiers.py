# FILE VERSION: 04_select_from_alias_identifiers_v1
'''
Polars SQL: SELECT, FROM, aliases, and identifiers.

This file introduces the first real SQL query shape after learning how to create
or register SQL tables:

    SELECT ...
    FROM ...

Main ideas:
1. SELECT chooses output columns and controls their order.
2. SELECT * returns all columns.
3. AS gives an output column a new name.
4. FROM chooses the SQL table to query.
5. Frame-level .sql(...) automatically registers the calling DataFrame/LazyFrame
   as a SQL table named self by default.
6. Use table_name=... if you want a frame-level query to use another table name.
7. SQLContext lets you query named registered tables.
8. Table aliases make longer queries easier to read.
9. Double quotes are used for identifiers with spaces, dots, leading digits, or
   reserved-keyword-like names.
10. Single quotes are string literals, not column names.

Important Polars SQL differences from native Polars:
+ Native Polars selects columns with df.select(...) / lf.select(...).
+ Polars SQL selects columns with SELECT ... FROM ... .
+ Native Polars uses pl.col("column name") for unusual column names.
+ SQL uses double-quoted identifiers such as "column name".
+ Polars has no pandas-style row index; SELECT never carries a hidden index.

Docs checked while writing this file:
+ https://docs.pola.rs/user-guide/sql/select/
+ https://docs.pola.rs/user-guide/sql/intro/
+ https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.sql.html
+ https://docs.pola.rs/api/python/stable/reference/sql/python_api.html
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


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 0. Setup Data --------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
This file uses a small self-contained employee table.

It intentionally includes both normal SQL-friendly column names and messy column
names:

+ employee_id       normal identifier; can be used unquoted
+ dept              normal identifier; can be used unquoted
+ is_manager        normal identifier; can be used unquoted
+ employee name     contains a space; quote it in SQL
+ salary.usd        contains a dot; quote it in SQL
+ bonus usd         contains a space; quote it in SQL
+ 2024 score        starts with digits and has a space; quote it in SQL
+ hire date         contains a space; quote it in SQL

Native Polars can always refer to these names with pl.col("...").
SQL needs double quotes for the messy ones.
'''

df_emp = pl.DataFrame(
    {
        "employee_id": [1, 2, 3, 4, 5, 6],
        "employee name": ["Ada", "Bob", "Charlie", "Dana", "Evan", "Fay"],
        "dept": ["IT", "HR", "IT", "Finance", "IT", "Finance"],
        "salary.usd": [120_000.0, 90_000.0, 110_000.0, 130_000.0, 105_000.0, 115_000.0],
        "bonus usd": [10_000.0, 5_000.0, 7_500.0, 12_000.0, 6_000.0, 8_000.0],
        "2024 score": [93.0, 88.0, 96.5, 92.0, 89.5, 91.0],
        "is_manager": [True, False, False, True, False, True],
        "hire date": [
            dt.date(2020, 1, 15),
            dt.date(2021, 6, 1),
            dt.date(2019, 9, 20),
            dt.date(2018, 3, 10),
            dt.date(2022, 7, 8),
            dt.date(2017, 11, 30),
        ],
    }
).with_columns(c.dept.cast(pl.Categorical))

lf_emp = df_emp.lazy()

print(df_emp)
# shape: (6, 8)
# ┌─────────────┬───────────────┬─────────┬────────────┬───────────┬────────────┬────────────┬────────────┐
# │ employee_id ┆ employee name ┆ dept    ┆ salary.usd ┆ bonus usd ┆ 2024 score ┆ is_manager ┆ hire date  │
# │ ---         ┆ ---           ┆ ---     ┆ ---        ┆ ---       ┆ ---        ┆ ---        ┆ ---        │
# │ i64         ┆ str           ┆ cat     ┆ f64        ┆ f64       ┆ f64        ┆ bool       ┆ date       │
# ╞═════════════╪═══════════════╪═════════╪════════════╪═══════════╪════════════╪════════════╪════════════╡
# │ 1           ┆ Ada           ┆ IT      ┆ 120000.00  ┆ 10000.00  ┆ 93.00      ┆ true       ┆ 2020-01-15 │
# │ 2           ┆ Bob           ┆ HR      ┆ 90000.00   ┆ 5000.00   ┆ 88.00      ┆ false      ┆ 2021-06-01 │
# │ 3           ┆ Charlie       ┆ IT      ┆ 110000.00  ┆ 7500.00   ┆ 96.50      ┆ false      ┆ 2019-09-20 │
# │ 4           ┆ Dana          ┆ Finance ┆ 130000.00  ┆ 12000.00  ┆ 92.00      ┆ true       ┆ 2018-03-10 │
# │ 5           ┆ Evan          ┆ IT      ┆ 105000.00  ┆ 6000.00   ┆ 89.50      ┆ false      ┆ 2022-07-08 │
# │ 6           ┆ Fay           ┆ Finance ┆ 115000.00  ┆ 8000.00   ┆ 91.00      ┆ true       ┆ 2017-11-30 │
# └─────────────┴───────────────┴─────────┴────────────┴───────────┴────────────┴────────────┴────────────┘

print(df_emp.schema)


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 1. SELECT * FROM self ----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
SELECT * returns every column from the table.

Because this is a LazyFrame-level query, the calling frame is available in SQL
as the special table name self.

Native Polars equivalent:
    lf_emp.select(pl.all())
'''

out_sql = lf_emp.sql(
    """
    SELECT *
    FROM self
    """
)

print(type(out_sql))
print(out_sql.collect())
# <class 'polars.lazyframe.frame.LazyFrame'>
# shape: (6, 8)
# ┌─────────────┬───────────────┬─────────┬────────────┬───────────┬────────────┬────────────┬────────────┐
# │ employee_id ┆ employee name ┆ dept    ┆ salary.usd ┆ bonus usd ┆ 2024 score ┆ is_manager ┆ hire date  │
# │ ---         ┆ ---           ┆ ---     ┆ ---        ┆ ---       ┆ ---        ┆ ---        ┆ ---        │
# │ i64         ┆ str           ┆ cat     ┆ f64        ┆ f64       ┆ f64        ┆ bool       ┆ date       │
# ╞═════════════╪═══════════════╪═════════╪════════════╪═══════════╪════════════╪════════════╪════════════╡
# │ 1           ┆ Ada           ┆ IT      ┆ 120000.00  ┆ 10000.00  ┆ 93.00      ┆ true       ┆ 2020-01-15 │
# │ 2           ┆ Bob           ┆ HR      ┆ 90000.00   ┆ 5000.00   ┆ 88.00      ┆ false      ┆ 2021-06-01 │
# │ 3           ┆ Charlie       ┆ IT      ┆ 110000.00  ┆ 7500.00   ┆ 96.50      ┆ false      ┆ 2019-09-20 │
# │ 4           ┆ Dana          ┆ Finance ┆ 130000.00  ┆ 12000.00  ┆ 92.00      ┆ true       ┆ 2018-03-10 │
# │ 5           ┆ Evan          ┆ IT      ┆ 105000.00  ┆ 6000.00   ┆ 89.50      ┆ false      ┆ 2022-07-08 │
# │ 6           ┆ Fay           ┆ Finance ┆ 115000.00  ┆ 8000.00   ┆ 91.00      ┆ true       ┆ 2017-11-30 │
# └─────────────┴───────────────┴─────────┴────────────┴───────────┴────────────┴────────────┴────────────┘

out_native = lf_emp.select(pl.all())

assert_frame_equal(out_sql.collect(), out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------ 2. SELECT explicit columns and order ------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
SELECT controls the output columns and their order.

Here, the output keeps only three columns and reorders them.

The column "employee name" has a space, so it is double-quoted in SQL.
'''

out_sql = lf_emp.sql(
    """
    SELECT
        "employee name",
        dept,
        employee_id
    FROM self
    """
)

print(out_sql.collect())
# shape: (6, 3)
# ┌───────────────┬─────────┬─────────────┐
# │ employee name ┆ dept    ┆ employee_id │
# │ ---           ┆ ---     ┆ ---         │
# │ str           ┆ cat     ┆ i64         │
# ╞═══════════════╪═════════╪═════════════╡
# │ Ada           ┆ IT      ┆ 1           │
# │ Bob           ┆ HR      ┆ 2           │
# │ Charlie       ┆ IT      ┆ 3           │
# │ Dana          ┆ Finance ┆ 4           │
# │ Evan          ┆ IT      ┆ 5           │
# │ Fay           ┆ Finance ┆ 6           │
# └───────────────┴─────────┴─────────────┘

out_native = lf_emp.select(
    c("employee name"),
    c("dept"),
    c("employee_id"),
)

assert_frame_equal(out_sql.collect(), out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 3. AS column aliases --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Use AS to rename output columns.

This is similar to using .alias(...) in native Polars expressions.

Note:
+ The original DataFrame/LazyFrame is not mutated.
+ Aliases only affect the query result.
'''

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id AS id,
        "employee name" AS name,
        dept AS department,
        "salary.usd" AS salary
    FROM self
    """
)

print(out_sql.collect())
# shape: (6, 4)
# ┌─────┬─────────┬────────────┬───────────┐
# │ id  ┆ name    ┆ department ┆ salary    │
# │ --- ┆ ---     ┆ ---        ┆ ---       │
# │ i64 ┆ str     ┆ cat        ┆ f64       │
# ╞═════╪═════════╪════════════╪═══════════╡
# │ 1   ┆ Ada     ┆ IT         ┆ 120000.00 │
# │ 2   ┆ Bob     ┆ HR         ┆ 90000.00  │
# │ 3   ┆ Charlie ┆ IT         ┆ 110000.00 │
# │ 4   ┆ Dana    ┆ Finance    ┆ 130000.00 │
# │ 5   ┆ Evan    ┆ IT         ┆ 105000.00 │
# │ 6   ┆ Fay     ┆ Finance    ┆ 115000.00 │
# └─────┴─────────┴────────────┴───────────┘

out_native = lf_emp.select(
    c("employee_id").alias("id"),
    c("employee name").alias("name"),
    c("dept").alias("department"),
    c("salary.usd").alias("salary"),
)

assert_frame_equal(out_sql.collect(), out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 4. Alias expressions -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
SELECT can compute derived columns.

The expression below adds salary and bonus to create total compensation.
The output column name comes from AS total_compensation.

Native Polars equivalent:
    (c("salary.usd") + c("bonus usd")).alias("total_compensation")
'''

out_sql = lf_emp.sql(
    """
    SELECT
        employee_id,
        "employee name" AS name,
        "salary.usd" + "bonus usd" AS total_compensation,
        "2024 score" AS score_2024
    FROM self
    """
)

print(out_sql.collect())
# shape: (6, 4)
# ┌─────────────┬─────────┬────────────────────┬────────────┐
# │ employee_id ┆ name    ┆ total_compensation ┆ score_2024 │
# │ ---         ┆ ---     ┆ ---                ┆ ---        │
# │ i64         ┆ str     ┆ f64                ┆ f64        │
# ╞═════════════╪═════════╪════════════════════╪════════════╡
# │ 1           ┆ Ada     ┆ 130000.00          ┆ 93.00      │
# │ 2           ┆ Bob     ┆ 95000.00           ┆ 88.00      │
# │ 3           ┆ Charlie ┆ 117500.00          ┆ 96.50      │
# │ 4           ┆ Dana    ┆ 142000.00          ┆ 92.00      │
# │ 5           ┆ Evan    ┆ 111000.00          ┆ 89.50      │
# │ 6           ┆ Fay     ┆ 123000.00          ┆ 91.00      │
# └─────────────┴─────────┴────────────────────┴────────────┘

out_native = lf_emp.select(
    c("employee_id"),
    c("employee name").alias("name"),
    (c("salary.usd") + c("bonus usd")).alias("total_compensation"),
    c("2024 score").alias("score_2024"),
)

assert_frame_equal(out_sql.collect(), out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 5. Quoted identifiers --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Use double quotes for identifiers that are not simple names.

Common cases:
+ spaces:        "employee name"
+ dots:          "salary.usd"
+ leading digit: "2024 score"
+ reserved-like names: "select", "from", "group", etc.

Do NOT use single quotes for column names. Single quotes create string literals.
'''

out_sql = lf_emp.sql(
    """
    SELECT
        "employee name" AS name,
        "salary.usd" AS salary,
        "bonus usd" AS bonus,
        "2024 score" AS score_2024,
        "hire date" AS hire_date
    FROM self
    """
)

print(out_sql.collect())
# shape: (6, 5)
# ┌─────────┬───────────┬──────────┬────────────┬────────────┐
# │ name    ┆ salary    ┆ bonus    ┆ score_2024 ┆ hire_date  │
# │ ---     ┆ ---       ┆ ---      ┆ ---        ┆ ---        │
# │ str     ┆ f64       ┆ f64      ┆ f64        ┆ date       │
# ╞═════════╪═══════════╪══════════╪════════════╪════════════╡
# │ Ada     ┆ 120000.00 ┆ 10000.00 ┆ 93.00      ┆ 2020-01-15 │
# │ Bob     ┆ 90000.00  ┆ 5000.00  ┆ 88.00      ┆ 2021-06-01 │
# │ Charlie ┆ 110000.00 ┆ 7500.00  ┆ 96.50      ┆ 2019-09-20 │
# │ Dana    ┆ 130000.00 ┆ 12000.00 ┆ 92.00      ┆ 2018-03-10 │
# │ Evan    ┆ 105000.00 ┆ 6000.00  ┆ 89.50      ┆ 2022-07-08 │
# │ Fay     ┆ 115000.00 ┆ 8000.00  ┆ 91.00      ┆ 2017-11-30 │
# └─────────┴───────────┴──────────┴────────────┴────────────┘

out_native = lf_emp.select(
    c("employee name").alias("name"),
    c("salary.usd").alias("salary"),
    c("bonus usd").alias("bonus"),
    c("2024 score").alias("score_2024"),
    c("hire date").alias("hire_date"),
)

assert_frame_equal(out_sql.collect(), out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------- 6. Single quotes are string literals -------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
This example shows the difference between:

    'employee name'    a string literal
    "employee name"    the actual column named employee name

This is a common source of confusion when moving from native DataFrame syntax
to SQL syntax.
'''

out_sql = lf_emp.sql(
    """
    SELECT
        'employee name' AS literal_text,
        "employee name" AS actual_column
    FROM self
    """
)

print(out_sql.collect())
# shape: (6, 2)
# ┌───────────────┬───────────────┐
# │ literal_text  ┆ actual_column │
# │ ---           ┆ ---           │
# │ str           ┆ str           │
# ╞═══════════════╪═══════════════╡
# │ employee name ┆ Ada           │
# │ employee name ┆ Bob           │
# │ employee name ┆ Charlie       │
# │ employee name ┆ Dana          │
# │ employee name ┆ Evan          │
# │ employee name ┆ Fay           │
# └───────────────┴───────────────┘

out_native = lf_emp.select(
    pl.lit("employee name").alias("literal_text"),
    c("employee name").alias("actual_column"),
)

assert_frame_equal(out_sql.collect(), out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 7. Table aliases -------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
A table alias gives the table a short temporary name inside the query.

This is especially useful later for joins and subqueries, but it is also valid
for a single table.

Here:
    FROM self AS e

means:
    e is a short name for self inside this query.

Then columns can be qualified with the alias:
    e.employee_id
    e.dept
    e."employee name"
'''

out_sql = lf_emp.sql(
    """
    SELECT
        e.employee_id,
        e."employee name" AS name,
        e.dept,
        e.is_manager
    FROM self AS e
    """
)

print(out_sql.collect())
# shape: (6, 4)
# ┌─────────────┬─────────┬─────────┬────────────┐
# │ employee_id ┆ name    ┆ dept    ┆ is_manager │
# │ ---         ┆ ---     ┆ ---     ┆ ---        │
# │ i64         ┆ str     ┆ cat     ┆ bool       │
# ╞═════════════╪═════════╪═════════╪════════════╡
# │ 1           ┆ Ada     ┆ IT      ┆ true       │
# │ 2           ┆ Bob     ┆ HR      ┆ false      │
# │ 3           ┆ Charlie ┆ IT      ┆ false      │
# │ 4           ┆ Dana    ┆ Finance ┆ true       │
# │ 5           ┆ Evan    ┆ IT      ┆ false      │
# │ 6           ┆ Fay     ┆ Finance ┆ true       │
# └─────────────┴─────────┴─────────┴────────────┘

out_native = lf_emp.select(
    c("employee_id"),
    c("employee name").alias("name"),
    c("dept"),
    c("is_manager"),
)

assert_frame_equal(out_sql.collect(), out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------- 8. Custom frame-level table_name= ----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Frame-level .sql(...) uses self by default, but you can choose another table
name with table_name=... .

This can make examples more readable when self feels too abstract.
'''

out_sql = lf_emp.sql(
    table_name="employees",
    query="""
    SELECT
        employee_id,
        "employee name" AS name,
        dept
    FROM employees
    """,
)

print(out_sql.collect())
# shape: (6, 3)
# ┌─────────────┬─────────┬─────────┐
# │ employee_id ┆ name    ┆ dept    │
# │ ---         ┆ ---     ┆ ---     │
# │ i64         ┆ str     ┆ cat     │
# ╞═════════════╪═════════╪═════════╡
# │ 1           ┆ Ada     ┆ IT      │
# │ 2           ┆ Bob     ┆ HR      │
# │ 3           ┆ Charlie ┆ IT      │
# │ 4           ┆ Dana    ┆ Finance │
# │ 5           ┆ Evan    ┆ IT      │
# │ 6           ┆ Fay     ┆ Finance │
# └─────────────┴─────────┴─────────┘

out_native = lf_emp.select(
    c("employee_id"),
    c("employee name").alias("name"),
    c("dept"),
)

assert_frame_equal(out_sql.collect(), out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 9. SQLContext registered table names ---------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
SQLContext is useful when you want explicit table names and/or multiple tables.

This file is still about SELECT/FROM, not joins, so we query only one registered
table here. The join examples belong in the later joins file.
'''

ctx = pl.SQLContext(employees=lf_emp)

out_sql = ctx.execute(
    """
    SELECT
        employees.employee_id,
        employees.dept,
        employees."salary.usd" AS salary
    FROM employees
    """
)

print(out_sql.collect())

out_native = lf_emp.select(
    c("employee_id"),
    c("dept"),
    c("salary.usd").alias("salary"),
)

assert_frame_equal(out_sql.collect(), out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 10. Reserved-like column names ---------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Some column names are awkward because they look like SQL keywords.

The safest pattern is to quote them with double quotes.

Native Polars has no problem with these names as long as you use pl.col("...").
'''

df_keyword = pl.DataFrame(
    {
        "select": ["a", "b", "c"],
        "from": [10, 20, 30],
        "normal_col": [True, False, True],
    }
)

lf_keyword = df_keyword.lazy()

out_sql = lf_keyword.sql(
    """
    SELECT
        "select" AS selected_value,
        "from" AS from_value,
        normal_col
    FROM self
    """
)

print(out_sql.collect())

out_native = lf_keyword.select(
    c("select").alias("selected_value"),
    c("from").alias("from_value"),
    c("normal_col"),
)

assert_frame_equal(out_sql.collect(), out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 11. What not to do ----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
The following examples are shown as strings only. They are intentionally not
executed.

1. Single quotes do NOT select a column:

    SELECT 'dept' FROM self

This returns the literal string 'dept' for every row. Use this instead:

    SELECT dept FROM self

2. Messy column names need double quotes:

    SELECT employee name FROM self

This is invalid or ambiguous SQL. Use this instead:

    SELECT "employee name" FROM self

3. A dot inside a column name must be quoted:

    SELECT salary.usd FROM self

This may be interpreted like table_or_alias.column. Use this instead:

    SELECT "salary.usd" FROM self

4. Prefer double quotes for SQL identifiers, not Python-style quotes/backticks.
   Single quotes are for string values.
'''

bad_examples = [
    "SELECT 'dept' FROM self",
    "SELECT employee name FROM self",
    "SELECT salary.usd FROM self",
]

print("Examples intentionally not executed:")
for query in bad_examples:
    print(query)


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 12. Quick summary ----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Quick map: native Polars -> Polars SQL

1. Select all columns
   Native: lf.select(pl.all())
   SQL:    SELECT * FROM self

2. Select/reorder columns
   Native: lf.select("dept", "employee_id")
   SQL:    SELECT dept, employee_id FROM self

3. Rename output columns
   Native: c("employee name").alias("name")
   SQL:    "employee name" AS name

4. Use a messy column name
   Native: c("salary.usd")
   SQL:    "salary.usd"

5. Refer to a table explicitly
   Native: variable name in Python, e.g. lf_emp
   SQL:    FROM self, FROM employees, or FROM table_alias

6. Use a table alias
   SQL:    FROM self AS e
           SELECT e.employee_id, e."employee name"

7. String literal vs identifier
   SQL:    'dept' is the text dept
           dept is the column named dept
           "employee name" is the column named employee name
'''
