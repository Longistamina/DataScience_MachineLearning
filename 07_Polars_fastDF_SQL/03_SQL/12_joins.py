# FILE VERSION: 12_sql_joins_v1
'''
Polars SQL joins.

Main ideas:
1. SQL joins combine rows from two or more tables.
2. In Polars SQL, joins are usually written through SQLContext because more than
   one table must be registered.
3. The most common join is an equi join: rows match when key columns are equal.
4. Polars SQL supports common SQL join syntax:
      INNER JOIN
      LEFT JOIN / LEFT OUTER JOIN
      RIGHT JOIN / RIGHT OUTER JOIN
      FULL JOIN / FULL OUTER JOIN
      CROSS JOIN
      LEFT SEMI JOIN
      LEFT ANTI JOIN
      USING (...)
      NATURAL JOIN
      non-equi ON conditions such as <, <=, >, >=, and !=
5. The native Polars equivalent is usually LazyFrame.join(...), and for non-equi
   joins it is LazyFrame.join_where(...).

Important Polars SQL notes:
+ Frame-level .sql(...) registers only one frame as self. For multi-table joins,
  SQLContext is usually clearer.
+ SQL join output order is not a safe thing to rely on unless you add ORDER BY.
+ If both tables contain columns with the same name, qualify them with table
  aliases in SQL, and give output aliases with AS.
+ FULL JOIN often needs COALESCE(left_key, right_key) if you want one combined key.
+ SEMI JOIN and ANTI JOIN return rows from one side depending on match existence;
  they do not attach columns from the other side.
+ NATURAL JOIN is concise but fragile because it automatically joins on all shared
  column names. Use explicit ON or USING for teaching and production code.
'''

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(30)
pl.Config.set_tbl_cols(9)
pl.Config.set_float_precision(3)
pl.Config.set_tbl_width_chars(120)


# =========================================================================================
# 0. Setup data
# =========================================================================================
'''
The examples are self-contained so this file can run without external datasets.

We create several related tables:
+ employees: one row per employee
+ departments: department lookup table
+ projects: project assignments, with repeated employee ids
+ salary_bands: salary ranges for a non-equi join
+ offices: location lookup table with a different key name

The data intentionally includes unmatched keys and nulls:
+ employee Frank has null dept_id
+ employee Grace has dept_id=99, which is not in departments
+ department Finance has no employees
+ project 106 has employee_id=9, which is not in employees
+ project 107 has null employee_id
'''

df_employees = pl.DataFrame(
    {
        "employee_id": [1, 2, 3, 4, 5, 6, 7, 8],
        "employee_name": ["Alice", "Bob", "Charlie", "Diana", "Evan", "Frank", "Grace", "Hana"],
        "dept_id": [10, 10, 20, 20, 30, None, 99, 40],
        "role": [
            "Engineer", "Engineer", "Sales Rep", "Sales Manager",
            "Marketer", "Analyst", "Contractor", "HR Specialist",
        ],
        "salary": [130_000, 95_000, 72_000, 115_000, 88_000, 70_000, 60_000, 78_000],
        "manager_id": [None, 1, 4, 1, 4, 5, None, 2],
        "office_code": ["NYC", "NYC", "SFO", "SFO", "LON", "LON", "REMOTE", "NYC"],
    }
)

df_departments = pl.DataFrame(
    {
        "dept_id": [10, 20, 30, 40, 50],
        "dept_name": ["Engineering", "Sales", "Marketing", "Human Resources", "Finance"],
        "region": ["North America", "North America", "Europe", "North America", "Europe"],
        "budget": [1_200_000, 800_000, 500_000, 300_000, 450_000],
    }
)

df_projects = pl.DataFrame(
    {
        "project_id": [101, 102, 103, 104, 105, 106, 107],
        "project_name": [
            "Search", "Billing", "Retail Expansion", "CRM", "Brand Refresh", "Data Cleanup", "Security Audit",
        ],
        "employee_id": [1, 2, 2, 4, 5, 9, None],
        "hours": [120, 80, 40, 100, 60, 30, 20],
    }
)

df_salary_bands = pl.DataFrame(
    {
        "band": ["low", "mid", "high", "executive"],
        "min_salary": [0, 80_000, 120_000, 180_000],
        "max_salary": [80_000, 120_000, 180_000, 1_000_000],
    }
)

df_offices = pl.DataFrame(
    {
        "code": ["NYC", "SFO", "LON", "BER"],
        "office_city": ["New York", "San Francisco", "London", "Berlin"],
        "timezone": ["America/New_York", "America/Los_Angeles", "Europe/London", "Europe/Berlin"],
    }
)

lf_employees = df_employees.lazy()
lf_departments = df_departments.lazy()
lf_projects = df_projects.lazy()
lf_salary_bands = df_salary_bands.lazy()
lf_offices = df_offices.lazy()

print(df_employees)
# shape: (8, 7)
# ┌─────────────┬───────────────┬─────────┬───────────────┬────────┬────────────┬─────────────┐
# │ employee_id ┆ employee_name ┆ dept_id ┆ role          ┆ salary ┆ manager_id ┆ office_code │
# │ ---         ┆ ---           ┆ ---     ┆ ---           ┆ ---    ┆ ---        ┆ ---         │
# │ i64         ┆ str           ┆ i64     ┆ str           ┆ i64    ┆ i64        ┆ str         │
# ╞═════════════╪═══════════════╪═════════╪═══════════════╪════════╪════════════╪═════════════╡
# │ 1           ┆ Alice         ┆ 10      ┆ Engineer      ┆ 130000 ┆ null       ┆ NYC         │
# │ 2           ┆ Bob           ┆ 10      ┆ Engineer      ┆ 95000  ┆ 1          ┆ NYC         │
# │ 3           ┆ Charlie       ┆ 20      ┆ Sales Rep     ┆ 72000  ┆ 4          ┆ SFO         │
# │ 4           ┆ Diana         ┆ 20      ┆ Sales Manager ┆ 115000 ┆ 1          ┆ SFO         │
# │ 5           ┆ Evan          ┆ 30      ┆ Marketer      ┆ 88000  ┆ 4          ┆ LON         │
# │ 6           ┆ Frank         ┆ null    ┆ Analyst       ┆ 70000  ┆ 5          ┆ LON         │
# │ 7           ┆ Grace         ┆ 99      ┆ Contractor    ┆ 60000  ┆ null       ┆ REMOTE      │
# │ 8           ┆ Hana          ┆ 40      ┆ HR Specialist ┆ 78000  ┆ 2          ┆ NYC         │
# └─────────────┴───────────────┴─────────┴───────────────┴────────┴────────────┴─────────────┘

print(df_departments)
# shape: (5, 4)
# ┌─────────┬─────────────────┬───────────────┬─────────┐
# │ dept_id ┆ dept_name       ┆ region        ┆ budget  │
# │ ---     ┆ ---             ┆ ---           ┆ ---     │
# │ i64     ┆ str             ┆ str           ┆ i64     │
# ╞═════════╪═════════════════╪═══════════════╪═════════╡
# │ 10      ┆ Engineering     ┆ North America ┆ 1200000 │
# │ 20      ┆ Sales           ┆ North America ┆ 800000  │
# │ 30      ┆ Marketing       ┆ Europe        ┆ 500000  │
# │ 40      ┆ Human Resources ┆ North America ┆ 300000  │
# │ 50      ┆ Finance         ┆ Europe        ┆ 450000  │
# └─────────┴─────────────────┴───────────────┴─────────┘

print(df_projects)
# shape: (7, 4)
# ┌────────────┬──────────────────┬─────────────┬───────┐
# │ project_id ┆ project_name     ┆ employee_id ┆ hours │
# │ ---        ┆ ---              ┆ ---         ┆ ---   │
# │ i64        ┆ str              ┆ i64         ┆ i64   │
# ╞════════════╪══════════════════╪═════════════╪═══════╡
# │ 101        ┆ Search           ┆ 1           ┆ 120   │
# │ 102        ┆ Billing          ┆ 2           ┆ 80    │
# │ 103        ┆ Retail Expansion ┆ 2           ┆ 40    │
# │ 104        ┆ CRM              ┆ 4           ┆ 100   │
# │ 105        ┆ Brand Refresh    ┆ 5           ┆ 60    │
# │ 106        ┆ Data Cleanup     ┆ 9           ┆ 30    │
# │ 107        ┆ Security Audit   ┆ null        ┆ 20    │
# └────────────┴──────────────────┴─────────────┴───────┘

print(df_salary_bands)
# shape: (4, 3)
# ┌───────────┬────────────┬────────────┐
# │ band      ┆ min_salary ┆ max_salary │
# │ ---       ┆ ---        ┆ ---        │
# │ str       ┆ i64        ┆ i64        │
# ╞═══════════╪════════════╪════════════╡
# │ low       ┆ 0          ┆ 80000      │
# │ mid       ┆ 80000      ┆ 120000     │
# │ high      ┆ 120000     ┆ 180000     │
# │ executive ┆ 180000     ┆ 1000000    │
# └───────────┴────────────┴────────────┘

print(df_offices)
# shape: (4, 3)
# ┌──────┬───────────────┬─────────────────────┐
# │ code ┆ office_city   ┆ timezone            │
# │ ---  ┆ ---           ┆ ---                 │
# │ str  ┆ str           ┆ str                 │
# ╞══════╪═══════════════╪═════════════════════╡
# │ NYC  ┆ New York      ┆ America/New_York    │
# │ SFO  ┆ San Francisco ┆ America/Los_Angeles │
# │ LON  ┆ London        ┆ Europe/London       │
# │ BER  ┆ Berlin        ┆ Europe/Berlin       │
# └──────┴───────────────┴─────────────────────┘


# =========================================================================================
# 1. Register tables for SQL joins
# =========================================================================================
'''
For joins, SQLContext is usually the clearest entry point.

Each registered name becomes a SQL table name.
The registered objects can be eager DataFrames or LazyFrames.
SQLContext.execute(...) returns a LazyFrame by default, so call .collect() when you
want to materialize the result.
'''

ctx = pl.SQLContext(
    employees=lf_employees,
    departments=lf_departments,
    projects=lf_projects,
    salary_bands=lf_salary_bands,
    offices=lf_offices,
)

print(ctx.tables())
# ['departments', 'employees', 'offices', 'projects', 'salary_bands']

print(ctx.execute("SHOW TABLES", eager=True))
# shape: (5, 1)
# ┌──────────────┐
# │ name         │
# │ ---          │
# │ str          │
# ╞══════════════╡
# │ departments  │
# │ employees    │
# │ offices      │
# │ projects     │
# │ salary_bands │
# └──────────────┘


# =========================================================================================
# 2. INNER JOIN with ON
# =========================================================================================
'''
INNER JOIN keeps only rows that match on both sides.

Here, employees with dept_id 10, 20, 30, and 40 match departments.
Employees with dept_id null or 99 do not appear in the result.
Department 50 has no employees, so it also does not appear.
'''

out_sql = ctx.execute(
    """
    SELECT
        e.employee_id,
        e.employee_name,
        e.dept_id,
        d.dept_name,
        d.region,
        e.salary
    FROM employees AS e
    INNER JOIN departments AS d
        ON e.dept_id = d.dept_id
    ORDER BY e.employee_id
    """
)
print(out_sql.collect())
# shape: (6, 6)
# ┌─────────────┬───────────────┬─────────┬─────────────────┬───────────────┬────────┐
# │ employee_id ┆ employee_name ┆ dept_id ┆ dept_name       ┆ region        ┆ salary │
# │ ---         ┆ ---           ┆ ---     ┆ ---             ┆ ---           ┆ ---    │
# │ i64         ┆ str           ┆ i64     ┆ str             ┆ str           ┆ i64    │
# ╞═════════════╪═══════════════╪═════════╪═════════════════╪═══════════════╪════════╡
# │ 1           ┆ Alice         ┆ 10      ┆ Engineering     ┆ North America ┆ 130000 │
# │ 2           ┆ Bob           ┆ 10      ┆ Engineering     ┆ North America ┆ 95000  │
# │ 3           ┆ Charlie       ┆ 20      ┆ Sales           ┆ North America ┆ 72000  │
# │ 4           ┆ Diana         ┆ 20      ┆ Sales           ┆ North America ┆ 115000 │
# │ 5           ┆ Evan          ┆ 30      ┆ Marketing       ┆ Europe        ┆ 88000  │
# │ 8           ┆ Hana          ┆ 40      ┆ Human Resources ┆ North America ┆ 78000  │
# └─────────────┴───────────────┴─────────┴─────────────────┴───────────────┴────────┘

# Native Polars equivalent.
out_native = (
    lf_employees
    .join(lf_departments, on="dept_id", how="inner")
    .select("employee_id", "employee_name", "dept_id", "dept_name", "region", "salary")
    .sort("employee_id")
)
print(out_native.collect())


# =========================================================================================
# 3. LEFT JOIN / LEFT OUTER JOIN
# =========================================================================================
'''
LEFT JOIN keeps all rows from the left table.

When a left row has no matching right row, the right-side columns are null.
This is useful when the left table is your main table and the right table is a
lookup table.
'''

out_sql = ctx.execute(
    """
    SELECT
        e.employee_id,
        e.employee_name,
        e.dept_id,
        d.dept_name,
        d.region
    FROM employees AS e
    LEFT JOIN departments AS d
        ON e.dept_id = d.dept_id
    ORDER BY e.employee_id
    """
)
print(out_sql.collect())
# shape: (8, 5)
# ┌─────────────┬───────────────┬─────────┬─────────────────┬───────────────┐
# │ employee_id ┆ employee_name ┆ dept_id ┆ dept_name       ┆ region        │
# │ ---         ┆ ---           ┆ ---     ┆ ---             ┆ ---           │
# │ i64         ┆ str           ┆ i64     ┆ str             ┆ str           │
# ╞═════════════╪═══════════════╪═════════╪═════════════════╪═══════════════╡
# │ 1           ┆ Alice         ┆ 10      ┆ Engineering     ┆ North America │
# │ 2           ┆ Bob           ┆ 10      ┆ Engineering     ┆ North America │
# │ 3           ┆ Charlie       ┆ 20      ┆ Sales           ┆ North America │
# │ 4           ┆ Diana         ┆ 20      ┆ Sales           ┆ North America │
# │ 5           ┆ Evan          ┆ 30      ┆ Marketing       ┆ Europe        │
# │ 6           ┆ Frank         ┆ null    ┆ null            ┆ null          │
# │ 7           ┆ Grace         ┆ 99      ┆ null            ┆ null          │
# │ 8           ┆ Hana          ┆ 40      ┆ Human Resources ┆ North America │
# └─────────────┴───────────────┴─────────┴─────────────────┴───────────────┘

# Native Polars equivalent.
out_native = (
    lf_employees
    .join(lf_departments, on="dept_id", how="left")
    .select("employee_id", "employee_name", "dept_id", "dept_name", "region")
    .sort("employee_id")
)
print(out_native.collect())


# =========================================================================================
# 4. RIGHT JOIN / RIGHT OUTER JOIN
# =========================================================================================
'''
RIGHT JOIN keeps all rows from the right table.

Here departments is the right table, so Finance appears even though it has no
employee. Columns from employees are null for unmatched right-side departments.

Native Polars has how="right". Another common way to think about a right join is:
    departments LEFT JOIN employees
with the table order reversed.
'''

out_sql = ctx.execute(
    """
    SELECT
        d.dept_id,
        d.dept_name,
        e.employee_id,
        e.employee_name
    FROM employees AS e
    RIGHT JOIN departments AS d
        ON e.dept_id = d.dept_id
    ORDER BY d.dept_id, e.employee_id
    """
)
print(out_sql.collect())
# shape: (7, 4)
# ┌─────────┬─────────────────┬─────────────┬───────────────┐
# │ dept_id ┆ dept_name       ┆ employee_id ┆ employee_name │
# │ ---     ┆ ---             ┆ ---         ┆ ---           │
# │ i64     ┆ str             ┆ i64         ┆ str           │
# ╞═════════╪═════════════════╪═════════════╪═══════════════╡
# │ 10      ┆ Engineering     ┆ 1           ┆ Alice         │
# │ 10      ┆ Engineering     ┆ 2           ┆ Bob           │
# │ 20      ┆ Sales           ┆ 3           ┆ Charlie       │
# │ 20      ┆ Sales           ┆ 4           ┆ Diana         │
# │ 30      ┆ Marketing       ┆ 5           ┆ Evan          │
# │ 40      ┆ Human Resources ┆ 8           ┆ Hana          │
# │ 50      ┆ Finance         ┆ null        ┆ null          │
# └─────────┴─────────────────┴─────────────┴───────────────┘

# Native Polars equivalent.
out_native = (
    lf_employees
    .join(lf_departments, on="dept_id", how="right")
    .select("dept_id", "dept_name", "employee_id", "employee_name")
    .sort("dept_id", "employee_id", nulls_last=True)
)
print(out_native.collect())


# =========================================================================================
# 5. FULL JOIN / FULL OUTER JOIN
# =========================================================================================
'''
FULL JOIN keeps all rows from both sides.

Rows that match are combined.
Rows that exist only on the left have nulls for right-side columns.
Rows that exist only on the right have nulls for left-side columns.

A practical FULL JOIN often uses COALESCE to combine the left/right key into one
readable key column.
'''

out_sql = ctx.execute(
    """
    SELECT
        COALESCE(e.dept_id, d.dept_id) AS dept_id,
        e.employee_id,
        e.employee_name,
        d.dept_name,
        d.region
    FROM employees AS e
    FULL JOIN departments AS d
        ON e.dept_id = d.dept_id
    ORDER BY dept_id, employee_id
    """
)
print(out_sql.collect())
# shape: (9, 5)
# ┌─────────┬─────────────┬───────────────┬─────────────────┬───────────────┐
# │ dept_id ┆ employee_id ┆ employee_name ┆ dept_name       ┆ region        │
# │ ---     ┆ ---         ┆ ---           ┆ ---             ┆ ---           │
# │ i64     ┆ i64         ┆ str           ┆ str             ┆ str           │
# ╞═════════╪═════════════╪═══════════════╪═════════════════╪═══════════════╡
# │ 10      ┆ 1           ┆ Alice         ┆ Engineering     ┆ North America │
# │ 10      ┆ 2           ┆ Bob           ┆ Engineering     ┆ North America │
# │ 20      ┆ 3           ┆ Charlie       ┆ Sales           ┆ North America │
# │ 20      ┆ 4           ┆ Diana         ┆ Sales           ┆ North America │
# │ 30      ┆ 5           ┆ Evan          ┆ Marketing       ┆ Europe        │
# │ 40      ┆ 8           ┆ Hana          ┆ Human Resources ┆ North America │
# │ 50      ┆ null        ┆ null          ┆ Finance         ┆ Europe        │
# │ 99      ┆ 7           ┆ Grace         ┆ null            ┆ null          │
# │ null    ┆ 6           ┆ Frank         ┆ null            ┆ null          │
# └─────────┴─────────────┴───────────────┴─────────────────┴───────────────┘

# Native Polars equivalent.
# For full joins, keep both key columns, then coalesce them manually.
out_native = (
    lf_employees
    .join(lf_departments, on="dept_id", how="full", suffix="_dept")
    .with_columns(
        pl.coalesce(c("dept_id"), c("dept_id_dept")).alias("dept_id_combined")
    )
    .select(
        c("dept_id_combined").alias("dept_id"),
        "employee_id",
        "employee_name",
        "dept_name",
        "region",
    )
    .sort("dept_id", "employee_id", nulls_last=True)
)
print(out_native.collect())


# =========================================================================================
# 6. USING when key names match
# =========================================================================================
'''
When both tables have the same key column name, SQL can use USING (key).

USING is shorter than ON e.dept_id = d.dept_id.
For teaching and debugging, ON is often clearer, but USING is convenient for
simple equi joins.
'''

out_sql = ctx.execute(
    """
    SELECT
        e.employee_id,
        e.employee_name,
        dept_id,
        d.dept_name
    FROM employees AS e
    LEFT JOIN departments AS d
        USING (dept_id)
    ORDER BY e.employee_id
    """
)
print(out_sql.collect())
# shape: (8, 4)
# ┌─────────────┬───────────────┬─────────┬─────────────────┐
# │ employee_id ┆ employee_name ┆ dept_id ┆ dept_name       │
# │ ---         ┆ ---           ┆ ---     ┆ ---             │
# │ i64         ┆ str           ┆ i64     ┆ str             │
# ╞═════════════╪═══════════════╪═════════╪═════════════════╡
# │ 1           ┆ Alice         ┆ 10      ┆ Engineering     │
# │ 2           ┆ Bob           ┆ 10      ┆ Engineering     │
# │ 3           ┆ Charlie       ┆ 20      ┆ Sales           │
# │ 4           ┆ Diana         ┆ 20      ┆ Sales           │
# │ 5           ┆ Evan          ┆ 30      ┆ Marketing       │
# │ 6           ┆ Frank         ┆ null    ┆ null            │
# │ 7           ┆ Grace         ┆ 99      ┆ null            │
# │ 8           ┆ Hana          ┆ 40      ┆ Human Resources │
# └─────────────┴───────────────┴─────────┴─────────────────┘

# Native Polars equivalent: same-name key join.
out_native = (
    lf_employees
    .join(lf_departments, on="dept_id", how="left")
    .select("employee_id", "employee_name", "dept_id", "dept_name")
    .sort("employee_id")
)
print(out_native.collect())


# =========================================================================================
# 7. Join on different key column names
# =========================================================================================
'''
When the key names differ, use ON with qualified column names.

Here employees.office_code matches offices.code.
'''

out_sql = ctx.execute(
    """
    SELECT
        e.employee_id,
        e.employee_name,
        e.office_code,
        o.office_city,
        o.timezone
    FROM employees AS e
    LEFT JOIN offices AS o
        ON e.office_code = o.code
    ORDER BY e.employee_id
    """
)
print(out_sql.collect())
# shape: (8, 5)
# ┌─────────────┬───────────────┬─────────────┬───────────────┬─────────────────────┐
# │ employee_id ┆ employee_name ┆ office_code ┆ office_city   ┆ timezone            │
# │ ---         ┆ ---           ┆ ---         ┆ ---           ┆ ---                 │
# │ i64         ┆ str           ┆ str         ┆ str           ┆ str                 │
# ╞═════════════╪═══════════════╪═════════════╪═══════════════╪═════════════════════╡
# │ 1           ┆ Alice         ┆ NYC         ┆ New York      ┆ America/New_York    │
# │ 2           ┆ Bob           ┆ NYC         ┆ New York      ┆ America/New_York    │
# │ 3           ┆ Charlie       ┆ SFO         ┆ San Francisco ┆ America/Los_Angeles │
# │ 4           ┆ Diana         ┆ SFO         ┆ San Francisco ┆ America/Los_Angeles │
# │ 5           ┆ Evan          ┆ LON         ┆ London        ┆ Europe/London       │
# │ 6           ┆ Frank         ┆ LON         ┆ London        ┆ Europe/London       │
# │ 7           ┆ Grace         ┆ REMOTE      ┆ null          ┆ null                │
# │ 8           ┆ Hana          ┆ NYC         ┆ New York      ┆ America/New_York    │
# └─────────────┴───────────────┴─────────────┴───────────────┴─────────────────────┘

# Native Polars equivalent: left_on / right_on.
out_native = (
    lf_employees
    .join(lf_offices, left_on="office_code", right_on="code", how="left")
    .select("employee_id", "employee_name", "office_code", "office_city", "timezone")
    .sort("employee_id")
)
print(out_native.collect())


# =========================================================================================
# 8. CROSS JOIN
# =========================================================================================
'''
CROSS JOIN returns the Cartesian product.

Every row from the left table is paired with every row from the right table.
This can grow very quickly, so use it carefully.

Here we make a tiny table of scenarios and pair every department with every
scenario.
'''

df_scenarios = pl.DataFrame(
    {
        "scenario": ["base", "stretch"],
        "budget_multiplier": [1.0, 1.2],
    }
)

lf_scenarios = df_scenarios.lazy()
ctx.register("scenarios", lf_scenarios)

out_sql = ctx.execute(
    """
    SELECT
        d.dept_name,
        s.scenario,
        d.budget,
        d.budget * s.budget_multiplier AS scenario_budget
    FROM departments AS d
    CROSS JOIN scenarios AS s
    ORDER BY d.dept_id, s.scenario
    """
)
print(out_sql.collect())
# shape: (10, 4)
# ┌─────────────────┬──────────┬─────────┬─────────────────┐
# │ dept_name       ┆ scenario ┆ budget  ┆ scenario_budget │
# │ ---             ┆ ---      ┆ ---     ┆ ---             │
# │ str             ┆ str      ┆ i64     ┆ f64             │
# ╞═════════════════╪══════════╪═════════╪═════════════════╡
# │ Engineering     ┆ base     ┆ 1200000 ┆ 1200000.000     │
# │ Engineering     ┆ stretch  ┆ 1200000 ┆ 1440000.000     │
# │ Sales           ┆ base     ┆ 800000  ┆ 800000.000      │
# │ Sales           ┆ stretch  ┆ 800000  ┆ 960000.000      │
# │ Marketing       ┆ base     ┆ 500000  ┆ 500000.000      │
# │ Marketing       ┆ stretch  ┆ 500000  ┆ 600000.000      │
# │ Human Resources ┆ base     ┆ 300000  ┆ 300000.000      │
# │ Human Resources ┆ stretch  ┆ 300000  ┆ 360000.000      │
# │ Finance         ┆ base     ┆ 450000  ┆ 450000.000      │
# │ Finance         ┆ stretch  ┆ 450000  ┆ 540000.000      │
# └─────────────────┴──────────┴─────────┴─────────────────┘

# Native Polars equivalent.
out_native = (
    lf_departments
    .join(lf_scenarios, how="cross")
    .select(
        "dept_name",
        "scenario",
        "budget",
        (c("budget") * c("budget_multiplier")).alias("scenario_budget"),
    )
    .sort("dept_name", "scenario")
)
print(out_native.collect())


# =========================================================================================
# 9. SEMI JOIN
# =========================================================================================
'''
SEMI JOIN keeps rows from the left table that have at least one match on the
right table.

It is existence filtering, not column attachment.
The right table's columns do not appear in the result.

Here we keep employees that have at least one project.
Bob appears only once even though he has two project rows.
'''

out_sql = ctx.execute(
    """
    SELECT
        e.employee_id,
        e.employee_name,
        e.role
    FROM employees AS e
    LEFT SEMI JOIN projects AS p
        ON e.employee_id = p.employee_id
    ORDER BY e.employee_id
    """
)
print(out_sql.collect())
# shape: (4, 3)
# ┌─────────────┬───────────────┬───────────────┐
# │ employee_id ┆ employee_name ┆ role          │
# │ ---         ┆ ---           ┆ ---           │
# │ i64         ┆ str           ┆ str           │
# ╞═════════════╪═══════════════╪═══════════════╡
# │ 1           ┆ Alice         ┆ Engineer      │
# │ 2           ┆ Bob           ┆ Engineer      │
# │ 4           ┆ Diana         ┆ Sales Manager │
# │ 5           ┆ Evan          ┆ Marketer      │
# └─────────────┴───────────────┴───────────────┘

# Native Polars equivalent.
out_native = (
    lf_employees
    .join(lf_projects, on="employee_id", how="semi")
    .select("employee_id", "employee_name", "role")
    .sort("employee_id")
)
print(out_native.collect())


# =========================================================================================
# 10. ANTI JOIN
# =========================================================================================
'''
ANTI JOIN keeps rows from the left table that do NOT have a match on the right
table.

Here we find employees with no project assignments.
'''

out_sql = ctx.execute(
    """
    SELECT
        e.employee_id,
        e.employee_name,
        e.role
    FROM employees AS e
    LEFT ANTI JOIN projects AS p
        ON e.employee_id = p.employee_id
    ORDER BY e.employee_id
    """
)
print(out_sql.collect())
# shape: (4, 3)
# ┌─────────────┬───────────────┬───────────────┐
# │ employee_id ┆ employee_name ┆ role          │
# │ ---         ┆ ---           ┆ ---           │
# │ i64         ┆ str           ┆ str           │
# ╞═════════════╪═══════════════╪═══════════════╡
# │ 3           ┆ Charlie       ┆ Sales Rep     │
# │ 6           ┆ Frank         ┆ Analyst       │
# │ 7           ┆ Grace         ┆ Contractor    │
# │ 8           ┆ Hana          ┆ HR Specialist │
# └─────────────┴───────────────┴───────────────┘

# Native Polars equivalent.
out_native = (
    lf_employees
    .join(lf_projects, on="employee_id", how="anti")
    .select("employee_id", "employee_name", "role")
    .sort("employee_id")
)
print(out_native.collect())


# =========================================================================================
# 11. Self join
# =========================================================================================
'''
A self join joins a table to itself.

Use table aliases to distinguish the two roles.
Here employees is used once as employee rows and once as manager rows.
'''

out_sql = ctx.execute(
    """
    SELECT
        e.employee_id,
        e.employee_name,
        e.manager_id,
        m.employee_name AS manager_name
    FROM employees AS e
    LEFT JOIN employees AS m
        ON e.manager_id = m.employee_id
    ORDER BY e.employee_id
    """
)
print(out_sql.collect())
# shape: (8, 4)
# ┌─────────────┬───────────────┬────────────┬──────────────┐
# │ employee_id ┆ employee_name ┆ manager_id ┆ manager_name │
# │ ---         ┆ ---           ┆ ---        ┆ ---          │
# │ i64         ┆ str           ┆ i64        ┆ str          │
# ╞═════════════╪═══════════════╪════════════╪══════════════╡
# │ 1           ┆ Alice         ┆ null       ┆ null         │
# │ 2           ┆ Bob           ┆ 1          ┆ Alice        │
# │ 3           ┆ Charlie       ┆ 4          ┆ Diana        │
# │ 4           ┆ Diana         ┆ 1          ┆ Alice        │
# │ 5           ┆ Evan          ┆ 4          ┆ Diana        │
# │ 6           ┆ Frank         ┆ 5          ┆ Evan         │
# │ 7           ┆ Grace         ┆ null       ┆ null         │
# │ 8           ┆ Hana          ┆ 2          ┆ Bob          │
# └─────────────┴───────────────┴────────────┴──────────────┘

# Native Polars equivalent.
lf_managers = lf_employees.select(
    c("employee_id").alias("manager_id_lookup"),
    c("employee_name").alias("manager_name"),
)
out_native = (
    lf_employees
    .join(lf_managers, left_on="manager_id", right_on="manager_id_lookup", how="left")
    .select("employee_id", "employee_name", "manager_id", "manager_name")
    .sort("employee_id")
)
print(out_native.collect())


# =========================================================================================
# 12. Join plus aggregation: projects per employee
# =========================================================================================
'''
A common workflow is:
1. join a detail table to a lookup table
2. aggregate the joined result

Here we join employees to projects, then summarize the project workload per
employee. LEFT JOIN keeps employees with no projects.
'''

out_sql = ctx.execute(
    """
    SELECT
        e.employee_id,
        e.employee_name,
        COUNT(p.project_id) AS n_projects,
        COALESCE(SUM(p.hours), 0) AS total_project_hours
    FROM employees AS e
    LEFT JOIN projects AS p
        ON e.employee_id = p.employee_id
    GROUP BY e.employee_id, e.employee_name
    ORDER BY e.employee_id
    """
)
print(out_sql.collect())
# shape: (8, 4)
# ┌─────────────┬───────────────┬────────────┬─────────────────────┐
# │ employee_id ┆ employee_name ┆ n_projects ┆ total_project_hours │
# │ ---         ┆ ---           ┆ ---        ┆ ---                 │
# │ i64         ┆ str           ┆ u32        ┆ i64                 │
# ╞═════════════╪═══════════════╪════════════╪═════════════════════╡
# │ 1           ┆ Alice         ┆ 1          ┆ 120                 │
# │ 2           ┆ Bob           ┆ 2          ┆ 120                 │
# │ 3           ┆ Charlie       ┆ 0          ┆ 0                   │
# │ 4           ┆ Diana         ┆ 1          ┆ 100                 │
# │ 5           ┆ Evan          ┆ 1          ┆ 60                  │
# │ 6           ┆ Frank         ┆ 0          ┆ 0                   │
# │ 7           ┆ Grace         ┆ 0          ┆ 0                   │
# │ 8           ┆ Hana          ┆ 0          ┆ 0                   │
# └─────────────┴───────────────┴────────────┴─────────────────────┘

# Native Polars equivalent.
out_native = (
    lf_employees
    .join(lf_projects, on="employee_id", how="left")
    .group_by("employee_id", "employee_name")
    .agg(
        c("project_id").count().alias("n_projects"),
        c("hours").sum().fill_null(0).alias("total_project_hours"),
    )
    .sort("employee_id")
)
print(out_native.collect())


# =========================================================================================
# 13. Duplicate column names and qualification
# =========================================================================================
'''
When both tables have a column with the same name, qualify columns with table
aliases and explicitly choose output names.

This avoids ambiguity and makes the output stable.

For example, both employees and projects have employee_id. The SELECT below
chooses one employee_id and renames project columns clearly.
'''

out_sql = ctx.execute(
    """
    SELECT
        e.employee_id AS employee_id,
        e.employee_name AS employee_name,
        p.project_id AS project_id,
        p.project_name AS project_name,
        p.hours AS project_hours
    FROM employees AS e
    INNER JOIN projects AS p
        ON e.employee_id = p.employee_id
    ORDER BY e.employee_id, p.project_id
    """
)
print(out_sql.collect())
# shape: (5, 5)
# ┌─────────────┬───────────────┬────────────┬──────────────────┬───────────────┐
# │ employee_id ┆ employee_name ┆ project_id ┆ project_name     ┆ project_hours │
# │ ---         ┆ ---           ┆ ---        ┆ ---              ┆ ---           │
# │ i64         ┆ str           ┆ i64        ┆ str              ┆ i64           │
# ╞═════════════╪═══════════════╪════════════╪══════════════════╪═══════════════╡
# │ 1           ┆ Alice         ┆ 101        ┆ Search           ┆ 120           │
# │ 2           ┆ Bob           ┆ 102        ┆ Billing          ┆ 80            │
# │ 2           ┆ Bob           ┆ 103        ┆ Retail Expansion ┆ 40            │
# │ 4           ┆ Diana         ┆ 104        ┆ CRM              ┆ 100           │
# │ 5           ┆ Evan          ┆ 105        ┆ Brand Refresh    ┆ 60            │
# └─────────────┴───────────────┴────────────┴──────────────────┴───────────────┘

# Native Polars equivalent.
out_native = (
    lf_employees
    .join(lf_projects, on="employee_id", how="inner", suffix="_project")
    .select(
        c("employee_id").alias("employee_id"),
        c("employee_name").alias("employee_name"),
        c("project_id").alias("project_id"),
        c("project_name").alias("project_name"),
        c("hours").alias("project_hours"),
    )
    .sort("employee_id", "project_id")
)
print(out_native.collect())


# =========================================================================================
# 14. NATURAL JOIN
# =========================================================================================
'''
NATURAL JOIN automatically joins on all columns with the same name in both tables.

This can be convenient for tiny examples, but it is usually too implicit for
larger projects. If another shared column name is added later, the join behavior
can change.

Use explicit ON or USING in most real code.
'''

out_sql = ctx.execute(
    """
    SELECT
        employee_id,
        employee_name,
        dept_id,
        dept_name
    FROM employees
    NATURAL INNER JOIN departments
    ORDER BY employee_id
    """
)
print(out_sql.collect())
# shape: (6, 4)
# ┌─────────────┬───────────────┬─────────┬─────────────────┐
# │ employee_id ┆ employee_name ┆ dept_id ┆ dept_name       │
# │ ---         ┆ ---           ┆ ---     ┆ ---             │
# │ i64         ┆ str           ┆ i64     ┆ str             │
# ╞═════════════╪═══════════════╪═════════╪═════════════════╡
# │ 1           ┆ Alice         ┆ 10      ┆ Engineering     │
# │ 2           ┆ Bob           ┆ 10      ┆ Engineering     │
# │ 3           ┆ Charlie       ┆ 20      ┆ Sales           │
# │ 4           ┆ Diana         ┆ 20      ┆ Sales           │
# │ 5           ┆ Evan          ┆ 30      ┆ Marketing       │
# │ 8           ┆ Hana          ┆ 40      ┆ Human Resources │
# └─────────────┴───────────────┴─────────┴─────────────────┘

# Safer explicit equivalent.
out_sql_explicit = ctx.execute(
    """
    SELECT
        e.employee_id,
        e.employee_name,
        e.dept_id,
        d.dept_name
    FROM employees AS e
    INNER JOIN departments AS d
        ON e.dept_id = d.dept_id
    ORDER BY e.employee_id
    """
)
print(out_sql_explicit.collect())


# =========================================================================================
# 17. Join quick map
# =========================================================================================
'''
Quick SQL -> native Polars map:

SQL:
    SELECT ... FROM left INNER JOIN right ON left.k = right.k
Polars:
    left.join(right, on="k", how="inner")

SQL:
    SELECT ... FROM left LEFT JOIN right ON left.k = right.k
Polars:
    left.join(right, on="k", how="left")

SQL:
    SELECT ... FROM left RIGHT JOIN right ON left.k = right.k
Polars:
    left.join(right, on="k", how="right")

SQL:
    SELECT ... FROM left FULL JOIN right ON left.k = right.k
Polars:
    left.join(right, on="k", how="full")

SQL:
    SELECT ... FROM left CROSS JOIN right
Polars:
    left.join(right, how="cross")

SQL:
    SELECT ... FROM left LEFT SEMI JOIN right ON left.k = right.k
Polars:
    left.join(right, on="k", how="semi")

SQL:
    SELECT ... FROM left LEFT ANTI JOIN right ON left.k = right.k
Polars:
    left.join(right, on="k", how="anti")

SQL:
    SELECT ... FROM left JOIN right ON left.x >= right.lo AND left.x < right.hi
Polars:
    left.join_where(right, c("x") >= c("lo"), c("x") < c("hi"))
'''
