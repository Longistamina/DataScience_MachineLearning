'''
Polars SQL set operations: UNION, UNION ALL, INTERSECT, EXCEPT, and BY NAME variants.

Main ideas:
1. Set operations combine the result of two or more SELECT statements vertically.
2. UNION removes duplicate rows.
3. UNION ALL keeps duplicate rows.
4. INTERSECT keeps rows that appear in both result sets.
5. EXCEPT keeps rows from the first result set that do not appear in the second result set.
6. BY NAME variants align columns by column name instead of by ordinal position.
7. Positional set operations require the SELECT branches to return compatible columns
   in compatible order.
8. BY NAME is useful when two sources have the same logical columns but different
   column order, or when one source has extra columns.

Important Polars SQL notes:
+ SQL set operations operate on SELECT outputs, not directly on Python objects.
+ SQLContext is the clearest way to register multiple named tables.
+ Set operations do not guarantee a teaching/reporting order by themselves.
  Sort the result after the SQL query, or use ORDER BY when appropriate.
+ UNION and INTERSECT/EXCEPT style operations are distinct by default.
+ UNION ALL keeps all rows, including duplicates.
+ UNION [ALL] BY NAME can combine columns from both sides and fill missing
  columns with null.
+ INTERSECT BY NAME and EXCEPT BY NAME compare commonly-named columns by name
  instead of by position.
+ Polars DataFrames have no custom row index, so set operations compare normal
  column values only.
'''

import datetime as dt

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(30)
pl.Config.set_tbl_cols(10)
pl.Config.set_float_precision(3)
pl.Config.set_tbl_width_chars(120)


# =========================================================================================
# 0. Setup data
# =========================================================================================
'''
The examples are self-contained so this file can run without external datasets.

We create two customer sources:
+ online_customers
+ retail_customers

Some customers appear in both sources with the same values. This makes UNION,
UNION ALL, INTERSECT, and EXCEPT easy to see.

We also create two profile tables with different column order / different columns
to demonstrate BY NAME set operations.
'''

df_online = pl.DataFrame(
    {
        "user_id": [1, 2, 3, 4, 5, 6],
        "user_name": ["Alice", "Bob", "Charlie", "Diana", "Evan", "Fiona"],
        "country": ["US", "US", "CA", "KR", "VN", "CA"],
        "channel": ["web", "web", "web", "ads", "web", "partner"],
        "is_active": [True, True, False, True, True, False],
        "signup_date": [
            dt.date(2024, 1, 3),
            dt.date(2024, 1, 5),
            dt.date(2024, 2, 10),
            dt.date(2024, 2, 12),
            dt.date(2024, 3, 1),
            dt.date(2024, 3, 15),
        ],
    }
)

df_retail = pl.DataFrame(
    {
        "user_id": [3, 4, 5, 7, 8, 9],
        "user_name": ["Charlie", "Diana", "Evan", "Gina", "Henry", "Ivy"],
        "country": ["CA", "KR", "VN", "US", "US", "KR"],
        "channel": ["store", "store", "store", "store", "event", "store"],
        "is_active": [False, True, True, True, False, True],
        "signup_date": [
            dt.date(2024, 2, 10),
            dt.date(2024, 2, 12),
            dt.date(2024, 3, 1),
            dt.date(2024, 4, 4),
            dt.date(2024, 4, 10),
            dt.date(2024, 5, 1),
        ],
    }
)

# Same logical keys as online/retail, but the column order is different and
# one table contains an extra age column.
df_profile_a = pl.DataFrame(
    {
        "user_id": [1, 2, 3],
        "user_name": ["Alice", "Bob", "Charlie"],
        "country": ["US", "US", "CA"],
    }
)

df_profile_b = pl.DataFrame(
    {
        "country": ["US", "CA", "KR", "JP"],
        "age": [30, 25, 29, 34],
        "user_name": ["Bob", "Charlie", "Diana", "Jun"],
        "user_id": [2, 3, 4, 10],
    }
)

lf_online = df_online.lazy()
lf_retail = df_retail.lazy()
lf_profile_a = df_profile_a.lazy()
lf_profile_b = df_profile_b.lazy()

ctx = pl.SQLContext(
    online=lf_online,
    retail=lf_retail,
    profile_a=lf_profile_a,
    profile_b=lf_profile_b,
)

print(df_online)
# shape: (6, 6)
# ┌─────────┬───────────┬─────────┬─────────┬───────────┬─────────────┐
# │ user_id ┆ user_name ┆ country ┆ channel ┆ is_active ┆ signup_date │
# │ ---     ┆ ---       ┆ ---     ┆ ---     ┆ ---       ┆ ---         │
# │ i64     ┆ str       ┆ str     ┆ str     ┆ bool      ┆ date        │
# ╞═════════╪═══════════╪═════════╪═════════╪═══════════╪═════════════╡
# │ 1       ┆ Alice     ┆ US      ┆ web     ┆ true      ┆ 2024-01-03  │
# │ 2       ┆ Bob       ┆ US      ┆ web     ┆ true      ┆ 2024-01-05  │
# │ 3       ┆ Charlie   ┆ CA      ┆ web     ┆ false     ┆ 2024-02-10  │
# │ 4       ┆ Diana     ┆ KR      ┆ ads     ┆ true      ┆ 2024-02-12  │
# │ 5       ┆ Evan      ┆ VN      ┆ web     ┆ true      ┆ 2024-03-01  │
# │ 6       ┆ Fiona     ┆ CA      ┆ partner ┆ false     ┆ 2024-03-15  │
# └─────────┴───────────┴─────────┴─────────┴───────────┴─────────────┘

print(df_retail)
# shape: (6, 6)
# ┌─────────┬───────────┬─────────┬─────────┬───────────┬─────────────┐
# │ user_id ┆ user_name ┆ country ┆ channel ┆ is_active ┆ signup_date │
# │ ---     ┆ ---       ┆ ---     ┆ ---     ┆ ---       ┆ ---         │
# │ i64     ┆ str       ┆ str     ┆ str     ┆ bool      ┆ date        │
# ╞═════════╪═══════════╪═════════╪═════════╪═══════════╪═════════════╡
# │ 3       ┆ Charlie   ┆ CA      ┆ store   ┆ false     ┆ 2024-02-10  │
# │ 4       ┆ Diana     ┆ KR      ┆ store   ┆ true      ┆ 2024-02-12  │
# │ 5       ┆ Evan      ┆ VN      ┆ store   ┆ true      ┆ 2024-03-01  │
# │ 7       ┆ Gina      ┆ US      ┆ store   ┆ true      ┆ 2024-04-04  │
# │ 8       ┆ Henry     ┆ US      ┆ event   ┆ false     ┆ 2024-04-10  │
# │ 9       ┆ Ivy       ┆ KR      ┆ store   ┆ true      ┆ 2024-05-01  │
# └─────────┴───────────┴─────────┴─────────┴───────────┴─────────────┘

print(df_profile_a)
# shape: (3, 3)
# ┌─────────┬───────────┬─────────┐
# │ user_id ┆ user_name ┆ country │
# │ ---     ┆ ---       ┆ ---     │
# │ i64     ┆ str       ┆ str     │
# ╞═════════╪═══════════╪═════════╡
# │ 1       ┆ Alice     ┆ US      │
# │ 2       ┆ Bob       ┆ US      │
# │ 3       ┆ Charlie   ┆ CA      │
# └─────────┴───────────┴─────────┘

print(df_profile_b)
# shape: (4, 4)
# ┌─────────┬─────┬───────────┬─────────┐
# │ country ┆ age ┆ user_name ┆ user_id │
# │ ---     ┆ --- ┆ ---       ┆ ---     │
# │ str     ┆ i64 ┆ str       ┆ i64     │
# ╞═════════╪═════╪═══════════╪═════════╡
# │ US      ┆ 30  ┆ Bob       ┆ 2       │
# │ CA      ┆ 25  ┆ Charlie   ┆ 3       │
# │ KR      ┆ 29  ┆ Diana     ┆ 4       │
# │ JP      ┆ 34  ┆ Jun       ┆ 10      │
# └─────────┴─────┴───────────┴─────────┘


# =========================================================================================
# 1. UNION
# =========================================================================================
'''
UNION combines result sets and removes duplicate rows.

Here we intentionally select only user_id, user_name, and country.
Rows for Charlie, Diana, and Evan appear in both tables with the same selected
values, so UNION keeps only one copy of each.
'''

out_sql = ctx.execute(
    """
    SELECT
        user_id,
        user_name,
        country
    FROM online

    UNION

    SELECT
        user_id,
        user_name,
        country
    FROM retail
    """
)
print(out_sql.sort("user_id").collect())
# Expected idea: user_id 1 through 9, with duplicate 3/4/5 removed.
# shape: (9, 3)
# ┌─────────┬───────────┬─────────┐
# │ user_id ┆ user_name ┆ country │
# │ ---     ┆ ---       ┆ ---     │
# │ i64     ┆ str       ┆ str     │
# ╞═════════╪═══════════╪═════════╡
# │ 1       ┆ Alice     ┆ US      │
# │ 2       ┆ Bob       ┆ US      │
# │ 3       ┆ Charlie   ┆ CA      │
# │ 4       ┆ Diana     ┆ KR      │
# │ 5       ┆ Evan      ┆ VN      │
# │ 6       ┆ Fiona     ┆ CA      │
# │ 7       ┆ Gina      ┆ US      │
# │ 8       ┆ Henry     ┆ US      │
# │ 9       ┆ Ivy       ┆ KR      │
# └─────────┴───────────┴─────────┘

# Native Polars equivalent.
out_native = (
    pl.concat(
        [
            lf_online.select("user_id", "user_name", "country"),
            lf_retail.select("user_id", "user_name", "country"),
        ],
        how="vertical",
    )
    .unique()
    .sort("user_id")
)
print(out_native.collect())


# =========================================================================================
# 2. UNION ALL
# =========================================================================================
'''
UNION ALL combines result sets and keeps every row.

This means duplicate selected rows are preserved.
With 6 online rows and 6 retail rows, the result has 12 rows.
'''

out_sql = ctx.execute(
    """
    SELECT
        user_id,
        user_name,
        country
    FROM online

    UNION ALL

    SELECT
        user_id,
        user_name,
        country
    FROM retail
    """
)
print(out_sql.sort("user_id").collect())
# Expected idea: 12 rows; user_id 3, 4, and 5 each appear twice.
# shape: (12, 3)
# ┌─────────┬───────────┬─────────┐
# │ user_id ┆ user_name ┆ country │
# │ ---     ┆ ---       ┆ ---     │
# │ i64     ┆ str       ┆ str     │
# ╞═════════╪═══════════╪═════════╡
# │ 1       ┆ Alice     ┆ US      │
# │ 2       ┆ Bob       ┆ US      │
# │ 3       ┆ Charlie   ┆ CA      │
# │ 3       ┆ Charlie   ┆ CA      │
# │ 4       ┆ Diana     ┆ KR      │
# │ 4       ┆ Diana     ┆ KR      │
# │ 5       ┆ Evan      ┆ VN      │
# │ 5       ┆ Evan      ┆ VN      │
# │ 6       ┆ Fiona     ┆ CA      │
# │ 7       ┆ Gina      ┆ US      │
# │ 8       ┆ Henry     ┆ US      │
# │ 9       ┆ Ivy       ┆ KR      │
# └─────────┴───────────┴─────────┘

# Native Polars equivalent.
out_native = (
    pl.concat(
        [
            lf_online.select("user_id", "user_name", "country"),
            lf_retail.select("user_id", "user_name", "country"),
        ],
        how="vertical",
    )
    .sort("user_id")
)
print(out_native.collect())


# =========================================================================================
# 3. UNION ALL with a source label column
# =========================================================================================
'''
A common reporting pattern is to stack sources and keep a source label.

Because the source label differs between branches, matching customers are no
longer duplicate rows in the SELECT output. This is usually what you want when
you need to remember where each row came from.
'''

out_sql = ctx.execute(
    """
    SELECT
        'online' AS source_table,
        user_id,
        user_name,
        country,
        channel,
        is_active
    FROM online

    UNION ALL

    SELECT
        'retail' AS source_table,
        user_id,
        user_name,
        country,
        channel,
        is_active
    FROM retail
    """
)
print(out_sql.sort(["user_id", "source_table"]).collect())
# shape: (12, 6)
# ┌──────────────┬─────────┬───────────┬─────────┬─────────┬───────────┐
# │ source_table ┆ user_id ┆ user_name ┆ country ┆ channel ┆ is_active │
# │ ---          ┆ ---     ┆ ---       ┆ ---     ┆ ---     ┆ ---       │
# │ str          ┆ i64     ┆ str       ┆ str     ┆ str     ┆ bool      │
# ╞══════════════╪═════════╪═══════════╪═════════╪═════════╪═══════════╡
# │ online       ┆ 1       ┆ Alice     ┆ US      ┆ web     ┆ true      │
# │ online       ┆ 2       ┆ Bob       ┆ US      ┆ web     ┆ true      │
# │ online       ┆ 3       ┆ Charlie   ┆ CA      ┆ web     ┆ false     │
# │ retail       ┆ 3       ┆ Charlie   ┆ CA      ┆ store   ┆ false     │
# │ online       ┆ 4       ┆ Diana     ┆ KR      ┆ ads     ┆ true      │
# │ retail       ┆ 4       ┆ Diana     ┆ KR      ┆ store   ┆ true      │
# │ online       ┆ 5       ┆ Evan      ┆ VN      ┆ web     ┆ true      │
# │ retail       ┆ 5       ┆ Evan      ┆ VN      ┆ store   ┆ true      │
# │ online       ┆ 6       ┆ Fiona     ┆ CA      ┆ partner ┆ false     │
# │ retail       ┆ 7       ┆ Gina      ┆ US      ┆ store   ┆ true      │
# │ retail       ┆ 8       ┆ Henry     ┆ US      ┆ event   ┆ false     │
# │ retail       ┆ 9       ┆ Ivy       ┆ KR      ┆ store   ┆ true      │
# └──────────────┴─────────┴───────────┴─────────┴─────────┴───────────┘

# Native Polars equivalent.
out_native = (
    pl.concat(
        [
            lf_online.select(
                pl.lit("online").alias("source_table"),
                "user_id",
                "user_name",
                "country",
                "channel",
                "is_active",
            ),
            lf_retail.select(
                pl.lit("retail").alias("source_table"),
                "user_id",
                "user_name",
                "country",
                "channel",
                "is_active",
            ),
        ],
        how="vertical",
    )
    .sort(["user_id", "source_table"])
)
print(out_native.collect())


# =========================================================================================
# 4. INTERSECT
# =========================================================================================
'''
INTERSECT returns rows that appear in both SELECT outputs.

Here it finds customers whose selected values appear in both online and retail.
Because set operations are distinct by default, each matching row appears once.
'''

out_sql = ctx.execute(
    """
    SELECT
        user_id,
        user_name,
        country
    FROM online

    INTERSECT

    SELECT
        user_id,
        user_name,
        country
    FROM retail
    """
)
print(out_sql.sort("user_id").collect())
# Expected idea: Charlie, Diana, and Evan.
# shape: (3, 3)
# ┌─────────┬───────────┬─────────┐
# │ user_id ┆ user_name ┆ country │
# │ ---     ┆ ---       ┆ ---     │
# │ i64     ┆ str       ┆ str     │
# ╞═════════╪═══════════╪═════════╡
# │ 3       ┆ Charlie   ┆ CA      │
# │ 4       ┆ Diana     ┆ KR      │
# │ 5       ┆ Evan      ┆ VN      │
# └─────────┴───────────┴─────────┘

# Native Polars equivalent: distinct left rows semi-joined with distinct right rows.
keys = ["user_id", "user_name", "country"]
out_native = (
    lf_online
    .select(keys)
    .unique()
    .join(
        lf_retail.select(keys).unique(),
        on=keys,
        how="semi",
    )
    .sort("user_id")
)
print(out_native.collect())


# =========================================================================================
# 5. EXCEPT
# =========================================================================================
'''
EXCEPT returns rows from the first SELECT output that do not appear in the second
SELECT output.

Order matters:
    online EXCEPT retail
is not the same as:
    retail EXCEPT online
'''

out_sql = ctx.execute(
    """
    SELECT
        user_id,
        user_name,
        country
    FROM online

    EXCEPT

    SELECT
        user_id,
        user_name,
        country
    FROM retail
    """
)
print(out_sql.sort("user_id").collect())
# Expected idea: Alice, Bob, and Fiona.
# shape: (3, 3)
# ┌─────────┬───────────┬─────────┐
# │ user_id ┆ user_name ┆ country │
# │ ---     ┆ ---       ┆ ---     │
# │ i64     ┆ str       ┆ str     │
# ╞═════════╪═══════════╪═════════╡
# │ 1       ┆ Alice     ┆ US      │
# │ 2       ┆ Bob       ┆ US      │
# │ 6       ┆ Fiona     ┆ CA      │
# └─────────┴───────────┴─────────┘

# Native Polars equivalent: distinct left rows anti-joined with distinct right rows.
out_native = (
    lf_online
    .select(keys)
    .unique()
    .join(
        lf_retail.select(keys).unique(),
        on=keys,
        how="anti",
    )
    .sort("user_id")
)
print(out_native.collect())


# =========================================================================================
# 6. Reverse EXCEPT direction
# =========================================================================================
'''
This example shows why EXCEPT direction matters.

Now we keep retail customers that do not appear in online.
'''

out_sql = ctx.execute(
    """
    SELECT
        user_id,
        user_name,
        country
    FROM retail

    EXCEPT

    SELECT
        user_id,
        user_name,
        country
    FROM online
    """
)
print(out_sql.sort("user_id").collect())
# Expected idea: Gina, Henry, and Ivy.
# shape: (3, 3)
# ┌─────────┬───────────┬─────────┐
# │ user_id ┆ user_name ┆ country │
# │ ---     ┆ ---       ┆ ---     │
# │ i64     ┆ str       ┆ str     │
# ╞═════════╪═══════════╪═════════╡
# │ 7       ┆ Gina      ┆ US      │
# │ 8       ┆ Henry     ┆ US      │
# │ 9       ┆ Ivy       ┆ KR      │
# └─────────┴───────────┴─────────┘

# Native Polars equivalent.
out_native = (
    lf_retail
    .select(keys)
    .unique()
    .join(
        lf_online.select(keys).unique(),
        on=keys,
        how="anti",
    )
    .sort("user_id")
)
print(out_native.collect())


# =========================================================================================
# 7. Set operations after filtering
# =========================================================================================
'''
Each branch of a set operation is a normal SELECT query.

This means each branch can have its own WHERE filter, computed columns, aliases,
and selected columns.

Example:
    active online users
    UNION
    active retail users
'''

out_sql = ctx.execute(
    """
    SELECT
        user_id,
        user_name,
        country,
        'active' AS user_status
    FROM online
    WHERE is_active

    UNION

    SELECT
        user_id,
        user_name,
        country,
        'active' AS user_status
    FROM retail
    WHERE is_active
    """
)
print(out_sql.sort("user_id").collect())
# shape: (6, 4)
# ┌─────────┬───────────┬─────────┬─────────────┐
# │ user_id ┆ user_name ┆ country ┆ user_status │
# │ ---     ┆ ---       ┆ ---     ┆ ---         │
# │ i64     ┆ str       ┆ str     ┆ str         │
# ╞═════════╪═══════════╪═════════╪═════════════╡
# │ 1       ┆ Alice     ┆ US      ┆ active      │
# │ 2       ┆ Bob       ┆ US      ┆ active      │
# │ 4       ┆ Diana     ┆ KR      ┆ active      │
# │ 5       ┆ Evan      ┆ VN      ┆ active      │
# │ 7       ┆ Gina      ┆ US      ┆ active      │
# │ 9       ┆ Ivy       ┆ KR      ┆ active      │
# └─────────┴───────────┴─────────┴─────────────┘

# Native Polars equivalent.
out_native = (
    pl.concat(
        [
            lf_online
            .filter(c("is_active"))
            .select("user_id", "user_name", "country", pl.lit("active").alias("user_status")),
            lf_retail
            .filter(c("is_active"))
            .select("user_id", "user_name", "country", pl.lit("active").alias("user_status")),
        ],
        how="vertical",
    )
    .unique()
    .sort("user_id")
)
print(out_native.collect())


# =========================================================================================
# 8. UNION BY NAME
# =========================================================================================
'''
UNION BY NAME aligns columns by column name instead of by position.

This is useful when two SELECT branches have different column order.
It can also combine columns from both sides and fill missing columns with null.

Here profile_a has columns:
    user_id, user_name, country

profile_b has columns:
    country, age, user_name, user_id

UNION BY NAME creates the union of column names.
Rows from profile_a have null age values.
'''

out_sql = ctx.execute(
    """
    SELECT * FROM profile_a

    UNION BY NAME

    SELECT * FROM profile_b
    """
)
print(out_sql.sort("user_id").collect())
# shape: (7, 4)
# ┌─────────┬───────────┬─────────┬──────┐
# │ user_id ┆ user_name ┆ country ┆ age  │
# │ ---     ┆ ---       ┆ ---     ┆ ---  │
# │ i64     ┆ str       ┆ str     ┆ i64  │
# ╞═════════╪═══════════╪═════════╪══════╡
# │ 1       ┆ Alice     ┆ US      ┆ null │
# │ 2       ┆ Bob       ┆ US      ┆ 30   │
# │ 2       ┆ Bob       ┆ US      ┆ null │
# │ 3       ┆ Charlie   ┆ CA      ┆ null │
# │ 3       ┆ Charlie   ┆ CA      ┆ 25   │
# │ 4       ┆ Diana     ┆ KR      ┆ 29   │
# │ 10      ┆ Jun       ┆ JP      ┆ 34   │
# └─────────┴───────────┴─────────┴──────┘

# Native Polars equivalent.
out_native = (
    pl.concat(
        [lf_profile_a, lf_profile_b],
        how="diagonal_relaxed",
    )
    .unique()
    .sort("user_id")
)
print(out_native.collect())


# =========================================================================================
# 9. UNION ALL BY NAME
# =========================================================================================
'''
UNION ALL BY NAME also aligns columns by name, but keeps all rows.

This is the closest SQL equivalent of a Polars diagonal concatenation when you
want to preserve duplicates.
'''

out_sql = ctx.execute(
    """
    SELECT * FROM profile_a

    UNION ALL BY NAME

    SELECT * FROM profile_b
    """
)
print(out_sql.sort("user_id").collect())
# shape: (7, 4)
# ┌─────────┬───────────┬─────────┬──────┐
# │ user_id ┆ user_name ┆ country ┆ age  │
# │ ---     ┆ ---       ┆ ---     ┆ ---  │
# │ i64     ┆ str       ┆ str     ┆ i64  │
# ╞═════════╪═══════════╪═════════╪══════╡
# │ 1       ┆ Alice     ┆ US      ┆ null │
# │ 2       ┆ Bob       ┆ US      ┆ null │
# │ 2       ┆ Bob       ┆ US      ┆ 30   │
# │ 3       ┆ Charlie   ┆ CA      ┆ null │
# │ 3       ┆ Charlie   ┆ CA      ┆ 25   │
# │ 4       ┆ Diana     ┆ KR      ┆ 29   │
# │ 10      ┆ Jun       ┆ JP      ┆ 34   │
# └─────────┴───────────┴─────────┴──────┘

# Native Polars equivalent.
out_native = (
    pl.concat(
        [lf_profile_a, lf_profile_b],
        how="diagonal_relaxed",
    )
    .sort("user_id")
)
print(out_native.collect())


# =========================================================================================
# 10. Positional matching vs BY NAME matching
# =========================================================================================
'''
Normal UNION, INTERSECT, and EXCEPT match columns by position.

BY NAME variants match columns by name.

If two SELECT lists have the same logical columns but in a different order, either:
1. write the SELECT columns in the same order manually, or
2. use a BY NAME operation when it is appropriate.

For teaching, the safest pattern is to write explicit SELECT lists.
'''

# Explicit positional version: both branches deliberately return user_id,
# user_name, country in the same order.
out_sql = ctx.execute(
    """
    SELECT
        user_id,
        user_name,
        country
    FROM profile_a

    UNION

    SELECT
        user_id,
        user_name,
        country
    FROM profile_b
    """
)
print(out_sql.sort("user_id").collect())
# shape: (5, 3)
# ┌─────────┬───────────┬─────────┐
# │ user_id ┆ user_name ┆ country │
# │ ---     ┆ ---       ┆ ---     │
# │ i64     ┆ str       ┆ str     │
# ╞═════════╪═══════════╪═════════╡
# │ 1       ┆ Alice     ┆ US      │
# │ 2       ┆ Bob       ┆ US      │
# │ 3       ┆ Charlie   ┆ CA      │
# │ 4       ┆ Diana     ┆ KR      │
# │ 10      ┆ Jun       ┆ JP      │
# └─────────┴───────────┴─────────┘

# BY NAME version: this still works even if SELECT * exposes a different column order.
out_sql = ctx.execute(
    """
    SELECT * FROM profile_a

    UNION BY NAME

    SELECT * FROM profile_b
    """
)
print(out_sql.sort("user_id").collect())


# =========================================================================================
# 11. INTERSECT BY NAME
# =========================================================================================
'''
INTERSECT BY NAME returns rows that appear in both result sets, matching columns
by name rather than by position.

To keep this example focused, both SELECT branches project the same three column
names but in different order.
'''

out_sql = ctx.execute(
    """
    SELECT
        user_id,
        user_name,
        country
    FROM profile_a

    INTERSECT BY NAME

    SELECT
        country,
        user_name,
        user_id
    FROM profile_b
    """
)
print(out_sql.sort("user_id").collect())
# Expected idea: Bob and Charlie.
# shape: (2, 3)
# ┌─────────┬───────────┬─────────┐
# │ user_id ┆ user_name ┆ country │
# │ ---     ┆ ---       ┆ ---     │
# │ i64     ┆ str       ┆ str     │
# ╞═════════╪═══════════╪═════════╡
# │ 2       ┆ Bob       ┆ US      │
# │ 3       ┆ Charlie   ┆ CA      │
# └─────────┴───────────┴─────────┘


# Native Polars equivalent.
out_native = (
    lf_profile_a
    .select("user_id", "user_name", "country")
    .unique()
    .join(
        lf_profile_b.select("user_id", "user_name", "country").unique(),
        on=["user_id", "user_name", "country"],
        how="semi",
    )
    .sort("user_id")
)
print(out_native.collect())


# =========================================================================================
# 12. EXCEPT BY NAME
# =========================================================================================
'''
EXCEPT BY NAME returns rows from the first result set that do not appear in the
second result set, matching columns by name rather than by position.
'''

out_sql = ctx.execute(
    """
    SELECT
        user_id,
        user_name,
        country
    FROM profile_a

    EXCEPT BY NAME

    SELECT
        country,
        user_name,
        user_id
    FROM profile_b
    """
)
print(out_sql.sort("user_id").collect())
# Expected idea: Alice.
# shape: (1, 3)
# ┌─────────┬───────────┬─────────┐
# │ user_id ┆ user_name ┆ country │
# │ ---     ┆ ---       ┆ ---     │
# │ i64     ┆ str       ┆ str     │
# ╞═════════╪═══════════╪═════════╡
# │ 1       ┆ Alice     ┆ US      │
# └─────────┴───────────┴─────────┘

# Native Polars equivalent.
out_native = (
    lf_profile_a
    .select("user_id", "user_name", "country")
    .unique()
    .join(
        lf_profile_b.select("user_id", "user_name", "country").unique(),
        on=["user_id", "user_name", "country"],
        how="anti",
    )
    .sort("user_id")
)
print(out_native.collect())


# =========================================================================================
# 13. Chaining after a SQL set operation
# =========================================================================================
'''
ctx.execute(...) returns a LazyFrame by default.

That means you can continue with native Polars methods after the SQL set
operation. This is useful when native Polars is clearer for the next step.
'''

combined_lf = ctx.execute(
    """
    SELECT
        'online' AS source_table,
        user_id,
        user_name,
        country,
        is_active
    FROM online

    UNION ALL

    SELECT
        'retail' AS source_table,
        user_id,
        user_name,
        country,
        is_active
    FROM retail
    """
)

out = (
    combined_lf
    .group_by("country")
    .agg(
        pl.len().alias("n_rows"),
        c("user_id").n_unique().alias("n_unique_users"),
        c("user_id").filter(c("is_active")).n_unique().alias("n_active_users"),
    )
    .sort("country")
)
print(out.collect())


# =========================================================================================
# 14. pl.sql example
# =========================================================================================
'''
When variables are available in the Python scope, top-level pl.sql(...) can also
query them by variable name.

SQLContext is still better for larger tutorials because table registration is
explicit. This example is included because pl.sql(...) is convenient in notebooks.
'''

# Make small LazyFrame variables with simple names for pl.sql(...).
left = lf_online.select("user_id", "user_name", "country")
right = lf_retail.select("user_id", "user_name", "country")

out_sql = pl.sql(
    """
    SELECT * FROM left

    INTERSECT

    SELECT * FROM right
    """
)
print(out_sql.sort("user_id").collect())
# shape: (3, 3)
# ┌─────────┬───────────┬─────────┐
# │ user_id ┆ user_name ┆ country │
# │ ---     ┆ ---       ┆ ---     │
# │ i64     ┆ str       ┆ str     │
# ╞═════════╪═══════════╪═════════╡
# │ 3       ┆ Charlie   ┆ CA      │
# │ 4       ┆ Diana     ┆ KR      │
# │ 5       ┆ Evan      ┆ VN      │
# └─────────┴───────────┴─────────┘


# =========================================================================================
# 15. Common mistakes
# =========================================================================================
'''
Common SQL set operation mistakes:

1. Confusing UNION and UNION ALL.

   UNION removes duplicate output rows.
   UNION ALL keeps duplicate output rows.

2. Forgetting that duplicate checks apply to the SELECT output.

   If you add a source label such as 'online' vs 'retail', rows that previously
   looked duplicated may no longer be duplicates.

3. Expecting normal UNION to align by column names.

   Normal UNION / INTERSECT / EXCEPT match columns by position.
   Use explicit SELECT lists or BY NAME variants when column order differs.

4. Using incompatible column counts or incompatible dtypes.

   Positional set operations need compatible SELECT outputs.
   Fix this with explicit SELECT lists and CAST(...) when necessary.

5. Forgetting that EXCEPT is directional.

   A EXCEPT B means rows in A that are not in B.
   B EXCEPT A means rows in B that are not in A.

6. Expecting deterministic row order.

   Add ORDER BY in SQL or sort the returned LazyFrame/DataFrame when row order
   matters for display, tests, or reports.

7. Expecting pandas index behavior.

   Polars has no custom row index, so set operations compare normal columns only.
'''
