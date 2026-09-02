'''
There are many ways to create a DataFrame in Polars. Here are some of the most common methods:

1. From a dictionary of Series: {"column_name": pl.Series(name, data)}

2. From a dictionary of lists or ndarrays: {"column_name": list_or_ndarray}

3. From 2D-List or 2D-Array: [[row1], [row2], ...] or np.array([[row1], [row2], ...])

4. From a structured or record array: np.array([(data1), (data2)], dtype=[("col1", type1), ("col2", type2)])

5. From a list of dictionaries: [{"col1": val1, "col2": val2}, ...]

6. From a dictionary of tuples / MultiIndex-like data: flatten to normal columns, or use Struct columns

7. From a list of namedtuples: [namedtuple1, namedtuple2, ...]

8. From a list of dataclasses: [dataclass1, dataclass2, ...]

9. Other constructors: pl.from_dict(), pl.from_dicts(), pl.from_records(), pl.from_numpy()

IMPORTANT DIFFERENCES FROM PANDAS:
+ Polars does NOT have custom row index labels or MultiIndex.
+ If you need an index-like value, store it as a normal column.
+ Polars is column-oriented, so dictionary-of-columns input is usually the most natural.
+ In Polars, use schema= instead of columns=.
+ For 2D row-wise input, explicitly pass orient="row".
'''

import numpy as np
import polars as pl

# =========================================================================================
# 1. From a dictionary of Series
# =========================================================================================
'''
In pandas, Series can have custom indexes and DataFrame construction aligns by index labels.
In Polars, Series do not have custom index labels, so all columns must have the same length.

If you need pandas-like index alignment, keep the labels as a normal column and join on that column.
'''

##--------------##
## Step-by-step ##
##--------------##

s_one = pl.Series("one", [1.0, 2.0, 3.0, None])
s_two = pl.Series("two", [1.0, 2.0, 3.0, 4.0])

data_dict = {
    "one": s_one,
    "two": s_two,
}

df = pl.DataFrame(data_dict)
print(df)
# shape: (4, 2)
# ┌──────┬─────┐
# │ one  ┆ two │
# │ ---  ┆ --- │
# │ f64  ┆ f64 │
# ╞══════╪═════╡
# │ 1.0  ┆ 1.0 │
# │ 2.0  ┆ 2.0 │
# │ 3.0  ┆ 3.0 │
# │ null ┆ 4.0 │
# └──────┴─────┘
'''Here, the dictionary keys become the column names.'''

##---------------------------------------------##
## With explicit row labels as a normal column ##
##---------------------------------------------##
'''
Polars has no index= argument. If you want labels like pandas index labels,
put those labels in a normal column.
'''

df = pl.DataFrame(
    data={
        "row_name": ["a", "b", "c", "d"],
        "one": [1.0, 2.0, 3.0, None],
        "two": [1.0, 2.0, 3.0, 4.0],
    }
)

print(df)
# shape: (4, 3)
# ┌──────────┬──────┬─────┐
# │ row_name ┆ one  ┆ two │
# │ ---      ┆ ---  ┆ --- │
# │ str      ┆ f64  ┆ f64 │
# ╞══════════╪══════╪═════╡
# │ a        ┆ 1.0  ┆ 1.0 │
# │ b        ┆ 2.0  ┆ 2.0 │
# │ c        ┆ 3.0  ┆ 3.0 │
# │ d        ┆ null ┆ 4.0 │
# └──────────┴──────┴─────┘

##----------------------------------##
## Emulating pandas index alignment ##
##----------------------------------##
'''
Pandas aligns Series by index labels automatically.
Polars does not. To align by labels, use a key column and joins.
'''

df_rows = pl.DataFrame({"row_name": ["a", "b", "c", "d"]})

df_one = pl.DataFrame(
    {
        "row_name": ["a", "b", "c"],
        "one": [1.0, 2.0, 3.0],
    }
)

df_two = pl.DataFrame(
    {
        "row_name": ["a", "b", "c", "d"],
        "two": [1.0, 2.0, 3.0, 4.0],
    }
)

df_aligned = (
    df_rows
    .join(df_one, on="row_name", how="left")
    .join(df_two, on="row_name", how="left")
)

print(df_aligned)
# shape: (4, 3)
# ┌──────────┬──────┬─────┐
# │ row_name ┆ one  ┆ two │
# │ ---      ┆ ---  ┆ --- │
# │ str      ┆ f64  ┆ f64 │
# ╞══════════╪══════╪═════╡
# │ a        ┆ 1.0  ┆ 1.0 │
# │ b        ┆ 2.0  ┆ 2.0 │
# │ c        ┆ 3.0  ┆ 3.0 │
# │ d        ┆ null ┆ 4.0 │
# └──────────┴──────┴─────┘


# =========================================================================================
# 2. From a dictionary of lists or ndarrays
# =========================================================================================

##------------##
## from lists ##
##------------##
'''
This is the most common and usually most efficient way to create a Polars DataFrame.
Each dictionary key becomes a column name, and each list becomes a column.
All columns must have the same length.
'''

df = pl.DataFrame(
    data={
        "column_1": [1, 3, 5, 7],
        "column_2": [2.0, 4.0, 6.0, 8.0],
        "column_3": ["a", "b", "c", "d"],
    }
)

print(df)
# shape: (4, 3)
# ┌──────────┬──────────┬──────────┐
# │ column_1 ┆ column_2 ┆ column_3 │
# │ ---      ┆ ---      ┆ ---      │
# │ i64      ┆ f64      ┆ str      │
# ╞══════════╪══════════╪══════════╡
# │ 1        ┆ 2.0      ┆ a        │
# │ 3        ┆ 4.0      ┆ b        │
# │ 5        ┆ 6.0      ┆ c        │
# │ 7        ┆ 8.0      ┆ d        │
# └──────────┴──────────┴──────────┘

##---------------##
## from ndarrays ##
##---------------##

df = pl.DataFrame(
    data={
        "column_1": np.array([1.5, 3.2, 5.7, 6.8]),
        "column_2": np.array([2.0, 4.9, 2.3, 1.2]),
    }
)

print(df)
# shape: (4, 2)
# ┌──────────┬──────────┐
# │ column_1 ┆ column_2 │
# │ ---      ┆ ---      │
# │ f64      ┆ f64      │
# ╞══════════╪══════════╡
# │ 1.5      ┆ 2.0      │
# │ 3.2      ┆ 4.9      │
# │ 5.7      ┆ 2.3      │
# │ 6.8      ┆ 1.2      │
# └──────────┴──────────┘

##--------------##
## Advanced way ##
##--------------##

df_score = pl.DataFrame(
    data={
        "name": ["Alice"] * 3 + ["Susan"] * 3,
        "subject": ["Math", "Science", "English"] * 2,
        "score": np.array([85, 90, 88, 92, 95, 89]),
    }
)

print(df_score)
# shape: (6, 3)
# ┌───────┬─────────┬───────┐
# │ name  ┆ subject ┆ score │
# │ ---   ┆ ---     ┆ ---   │
# │ str   ┆ str     ┆ i64   │
# ╞═══════╪═════════╪═══════╡
# │ Alice ┆ Math    ┆ 85    │
# │ Alice ┆ Science ┆ 90    │
# │ Alice ┆ English ┆ 88    │
# │ Susan ┆ Math    ┆ 92    │
# │ Susan ┆ Science ┆ 95    │
# │ Susan ┆ English ┆ 89    │
# └───────┴─────────┴───────┘

##-----------------##
## Explicit schema ##
##-----------------##
'''
Use schema= to control column names and dtypes.
A schema can be a dict: {"name": dtype}, or a list of (name, dtype) pairs.
'''

df_typed = pl.DataFrame(
    data={
        "name": ["Alice", "Susan"],
        "score": [85, 92],
    },
    schema={
        "name": pl.String,
        "score": pl.Int32,
    },
)

print(df_typed)
# shape: (2, 2)
# ┌───────┬───────┐
# │ name  ┆ score │
# │ ---   ┆ ---   │
# │ str   ┆ i32   │
# ╞═══════╪═══════╡
# │ Alice ┆ 85    │
# │ Susan ┆ 92    │
# └───────┴───────┘

##-----------------------------##
## strict=False for soft casts ##
##-----------------------------##
'''
By default, strict=True. If a value does not match the target dtype, Polars raises an error.
With strict=False, Polars tries to cast values. Values that cannot be cast become null.
'''

df_loose = pl.DataFrame(
    data={
        "id": [1, 2, 3],
        "score": [95, "bad", 88],
    },
    schema={
        "id": pl.Int64,
        "score": pl.Int64,
    },
    strict=False,
)

print(df_loose)
# shape: (3, 2)
# ┌─────┬───────┐
# │ id  ┆ score │
# │ --- ┆ ---   │
# │ i64 ┆ i64   │
# ╞═════╪═══════╡
# │ 1   ┆ 95    │
# │ 2   ┆ null  │
# │ 3   ┆ 88    │
# └─────┴───────┘


# =========================================================================================
# 3. From 2D-List or 2D-Array
# =========================================================================================

##--------------##
## from 2D-List ##
##--------------##
'''
In pandas, you pass columns= for column names.
In Polars, pass schema= for column names and orient="row" when each inner list is a row.
'''

df_2d_list = pl.DataFrame(
    data=[
        ["row_1", 1, 2.0, "a"],
        ["row_2", 3, 4.0, "b"],
        ["row_3", 5, 6.0, "c"],
        ["row_4", 7, 8.0, "d"],
    ],
    schema=["row_name", "column_1", "column_2", "column_3"],
    orient="row",
)

print(df_2d_list)
# shape: (4, 4)
# ┌──────────┬──────────┬──────────┬──────────┐
# │ row_name ┆ column_1 ┆ column_2 ┆ column_3 │
# │ ---      ┆ ---      ┆ ---      ┆ ---      │
# │ str      ┆ i64      ┆ f64      ┆ str      │
# ╞══════════╪══════════╪══════════╪══════════╡
# │ row_1    ┆ 1        ┆ 2.0      ┆ a        │
# │ row_2    ┆ 3        ┆ 4.0      ┆ b        │
# │ row_3    ┆ 5        ┆ 6.0      ┆ c        │
# │ row_4    ┆ 7        ┆ 8.0      ┆ d        │
# └──────────┴──────────┴──────────┴──────────┘

##---------------##
## from 2D-Array ##
##---------------##
'''
NumPy arrays usually have one dtype for the whole array.
For mixed numeric/string data, a list of rows or list of dictionaries is often clearer.
'''

array_2d = np.array(
    [
        [1.5, 2.0],
        [3.2, 4.0],
        [5.7, 6.0],
        [6.8, 8.0],
    ]
)

df_2d_array = pl.DataFrame(
    data=array_2d,
    schema=["col_1", "col_2"],
    orient="row",
)

print(df_2d_array)
# shape: (4, 2)
# ┌───────┬───────┐
# │ col_1 ┆ col_2 │
# │ ---   ┆ ---   │
# │ f64   ┆ f64   │
# ╞═══════╪═══════╡
# │ 1.5   ┆ 2.0   │
# │ 3.2   ┆ 4.0   │
# │ 5.7   ┆ 6.0   │
# │ 6.8   ┆ 8.0   │
# └───────┴───────┘

##------------------------------------##
## from 2D-Array with pl.from_numpy() ##
##------------------------------------##

df_from_numpy = pl.from_numpy(
    data=array_2d,
    schema=["col_1", "col_2"],
    orient="row",
)

print(df_from_numpy)
# Same result as df_2d_array.


# =========================================================================================
# 4. From a structured or record array
# =========================================================================================
'''
Structured arrays contain named fields.
A very explicit and reliable Polars pattern is to build a dictionary of columns from those fields.
'''

# Create an empty structured record
record = np.zeros(
    shape=(2,),
    dtype=[("A", "i4"), ("B", "f4"), ("C", "U10")],
)

print(record)
# [(0, 0., '') (0, 0., '')]

# Fill the structured record with data
record[:] = [(1, 2.0, "Hello"), (2, 3.0, "World")]
print(record)
# [(1, 2., 'Hello') (2, 3., 'World')]

# Create DataFrame from the structured record fields
# This preserves the field names as column names.
df = pl.DataFrame(
    data={field: record[field] for field in record.dtype.names}
)

print(df)
# shape: (2, 3)
# ┌─────┬─────┬───────┐
# │ A   ┆ B   ┆ C     │
# │ --- ┆ --- ┆ ---   │
# │ i32 ┆ f32 ┆ str   │
# ╞═════╪═════╪═══════╡
# │ 1   ┆ 2.0 ┆ Hello │
# │ 2   ┆ 3.0 ┆ World │
# └─────┴─────┴───────┘

##-----------------##
## With row labels ##
##-----------------##
'''
Polars has no index= argument, so row labels should be stored as a normal column.
'''

df = pl.DataFrame(
    data={
        "row_name": ["first", "second"],
        **{field: record[field] for field in record.dtype.names},
    }
)

print(df)
# shape: (2, 4)
# ┌──────────┬─────┬─────┬───────┐
# │ row_name ┆ A   ┆ B   ┆ C     │
# │ ---      ┆ --- ┆ --- ┆ ---   │
# │ str      ┆ i32 ┆ f32 ┆ str   │
# ╞══════════╪═════╪═════╪═══════╡
# │ first    ┆ 1   ┆ 2.0 ┆ Hello │
# │ second   ┆ 2   ┆ 3.0 ┆ World │
# └──────────┴─────┴─────┴───────┘


# =========================================================================================
# 5. From a list of dictionaries
# =========================================================================================
'''
A list of dictionaries is row-oriented: each dictionary represents one row.
Missing keys become null values.

This is common when data comes from JSON, APIs, or manually-created row records.
'''

##--------------##
## Step-by-step ##
##--------------##

list_of_dicts = [
    {"a": 1, "b": 2},
    {"a": 5, "b": 10, "c": 20},
]

df = pl.DataFrame(list_of_dicts)
print(df)
# shape: (2, 3)
# ┌─────┬─────┬──────┐
# │ a   ┆ b   ┆ c    │
# │ --- ┆ --- ┆ ---  │
# │ i64 ┆ i64 ┆ i64  │
# ╞═════╪═════╪══════╡
# │ 1   ┆ 2   ┆ null │
# │ 5   ┆ 10  ┆ 20   │
# └─────┴─────┴──────┘

##-----------------##
## With row labels ##
##-----------------##

df = pl.DataFrame(
    data=[
        {"row_name": "row_1", "a": 1.4, "b": 2.3},
        {"row_name": "row_2", "a": 5, "b": 10, "c": 20},
    ]
)

print(df)
# shape: (2, 4)
# ┌──────────┬─────┬──────┬──────┐
# │ row_name ┆ a   ┆ b    ┆ c    │
# │ ---      ┆ --- ┆ ---  ┆ ---  │
# │ str      ┆ f64 ┆ f64  ┆ i64  │
# ╞══════════╪═════╪══════╪══════╡
# │ row_1    ┆ 1.4 ┆ 2.3  ┆ null │
# │ row_2    ┆ 5.0 ┆ 10.0 ┆ 20   │
# └──────────┴─────┴──────┴──────┘

##-----------------##
## pl.from_dicts() ##
##-----------------##
'''
pl.from_dicts() is the explicit constructor for a sequence/list of row dictionaries.
You can pass a schema to control dtypes or load only selected columns.
'''

df = pl.from_dicts(
    data=list_of_dicts,
    schema={"a": pl.Float64, "b": pl.Int64, "c": pl.Int64},
)

print(df)
# shape: (2, 3)
# ┌─────┬─────┬──────┐
# │ a   ┆ b   ┆ c    │
# │ --- ┆ --- ┆ ---  │
# │ f64 ┆ i64 ┆ i64  │
# ╞═════╪═════╪══════╡
# │ 1.0 ┆ 2   ┆ null │
# │ 5.0 ┆ 10  ┆ 20   │
# └─────┴─────┴──────┘

##--------------------------------------##
## Partial schema: select loaded fields ##
##--------------------------------------##
'''
For list-of-dictionaries input, a partial schema can be used to load only selected fields.
Here, column c is omitted from the result.
'''

df_partial = pl.from_dicts(
    data=list_of_dicts,
    schema={"a": pl.Int64, "b": pl.Int64},
)

print(df_partial)
# shape: (2, 2)
# ┌─────┬─────┐
# │ a   ┆ b   │
# │ --- ┆ --- │
# │ i64 ┆ i64 │
# ╞═════╪═════╡
# │ 1   ┆ 2   │
# │ 5   ┆ 10  │
# └─────┴─────┘


# =========================================================================================
# 6. From a dictionary of tuples / MultiIndex-like data
# =========================================================================================
'''
Pandas can create MultiIndex rows/columns from dictionaries with tuple keys.
Polars does NOT have MultiIndex.

Polars alternatives:
1. Flatten the tuple labels into normal column names.
2. Store row levels as normal columns.
3. Use Struct columns if you want nested groups of fields.
'''

##-------------------------------------------##
## Flatten MultiIndex-like data into columns ##
##-------------------------------------------##

multi_like_rows = [
    {
        "level_0": "A",
        "level_1": "B",
        "a_b": 1.0,
        "a_a": 4.0,
        "a_c": 5.0,
        "b_a": 8.0,
        "b_b": 10.0,
    },
    {
        "level_0": "A",
        "level_1": "C",
        "a_b": 2.0,
        "a_a": 3.0,
        "a_c": 6.0,
        "b_a": 7.0,
        "b_b": None,
    },
    {
        "level_0": "A",
        "level_1": "D",
        "a_b": None,
        "a_a": None,
        "a_c": None,
        "b_a": None,
        "b_b": 9.0,
    },
]

df_flat = pl.from_dicts(
    data=multi_like_rows,
    schema=["level_0", "level_1", "a_b", "a_a", "a_c", "b_a", "b_b"],
)

print(df_flat)
# shape: (3, 7)
# ┌─────────┬─────────┬──────┬──────┬──────┬──────┬──────┐
# │ level_0 ┆ level_1 ┆ a_b  ┆ a_a  ┆ a_c  ┆ b_a  ┆ b_b  │
# │ ---     ┆ ---     ┆ ---  ┆ ---  ┆ ---  ┆ ---  ┆ ---  │
# │ str     ┆ str     ┆ f64  ┆ f64  ┆ f64  ┆ f64  ┆ f64  │
# ╞═════════╪═════════╪══════╪══════╪══════╪══════╪══════╡
# │ A       ┆ B       ┆ 1.0  ┆ 4.0  ┆ 5.0  ┆ 8.0  ┆ 10.0 │
# │ A       ┆ C       ┆ 2.0  ┆ 3.0  ┆ 6.0  ┆ 7.0  ┆ null │
# │ A       ┆ D       ┆ null ┆ null ┆ null ┆ null ┆ 9.0  │
# └─────────┴─────────┴──────┴──────┴──────┴──────┴──────┘

##---------------------##
## Use Struct columns  ##
##---------------------##
'''
A Struct column groups multiple fields into one nested column.
This is often the closest Polars idea to grouped columns, but it is NOT a MultiIndex.
'''

df_struct = (
    df_flat
    .with_columns(
        pl.struct(["a_b", "a_a", "a_c"]).alias("a"),
        pl.struct(["b_a", "b_b"]).alias("b"),
    )
    .select(["level_0", "level_1", "a", "b"])
)

print(df_struct)
# shape: (3, 4)
# ┌─────────┬─────────┬──────────────────┬──────────────┐
# │ level_0 ┆ level_1 ┆ a                ┆ b            │
# │ ---     ┆ ---     ┆ ---              ┆ ---          │
# │ str     ┆ str     ┆ struct[3]        ┆ struct[2]    │
# ╞═════════╪═════════╪══════════════════╪══════════════╡
# │ A       ┆ B       ┆ {1.0,4.0,5.0}    ┆ {8.0,10.0}  │
# │ A       ┆ C       ┆ {2.0,3.0,6.0}    ┆ {7.0,null}  │
# │ A       ┆ D       ┆ {null,null,null} ┆ {null,9.0}  │
# └─────────┴─────────┴──────────────────┴──────────────┘


# =========================================================================================
# 7. From a list of namedtuples
# =========================================================================================

from collections import namedtuple

##-----------##
## 2D points ##
##-----------##

point_2d = namedtuple("Point", "x y")

points_2d = [
    point_2d(0, 0),
    point_2d(1, 2),
    point_2d(2, 4),
    point_2d(3, 6),
]

df = pl.DataFrame(
    data=points_2d,
    schema=list(point_2d._fields),
    orient="row",
)

print(df)
# shape: (4, 2)
# ┌─────┬─────┐
# │ x   ┆ y   │
# │ --- ┆ --- │
# │ i64 ┆ i64 │
# ╞═════╪═════╡
# │ 0   ┆ 0   │
# │ 1   ┆ 2   │
# │ 2   ┆ 4   │
# │ 3   ┆ 6   │
# └─────┴─────┘

##-----------##
## 3D points ##
##-----------##

point_3d = namedtuple("Point3D", "x y z")

points_3d = [
    point_3d(0, 0, 0),
    point_3d(1, 2, 3),
    point_3d(2, 4, 6),
    point_3d(3, 6, 9),
]

df = pl.DataFrame(
    data=points_3d,
    schema=list(point_3d._fields),
    orient="row",
)

print(df)
# shape: (4, 3)
# ┌─────┬─────┬─────┐
# │ x   ┆ y   ┆ z   │
# │ --- ┆ --- ┆ --- │
# │ i64 ┆ i64 ┆ i64 │
# ╞═════╪═════╪═════╡
# │ 0   ┆ 0   ┆ 0   │
# │ 1   ┆ 2   ┆ 3   │
# │ 2   ┆ 4   ┆ 6   │
# │ 3   ┆ 6   ┆ 9   │
# └─────┴─────┴─────┘

##-------------------------------------##
## Namedtuples as dictionaries instead ##
##-------------------------------------##
'''Another clear approach is to convert namedtuples to dictionaries and use pl.from_dicts().'''

df = pl.from_dicts([p._asdict() for p in points_2d])
print(df)
# Same 2D points result.


# =========================================================================================
# 8. From a list of dataclasses
# =========================================================================================

from dataclasses import asdict, make_dataclass

point_dc = make_dataclass("Point", [("x", int), ("y", int)])

points = [
    point_dc(0, 0),
    point_dc(3, 5),
    point_dc(4, 7),
    point_dc(2, 2),
]

'''
Polars does not need dataclass-specific magic.
Convert dataclass objects to dictionaries, then use pl.from_dicts().
'''

df = pl.from_dicts([asdict(point) for point in points])

print(df)
# shape: (4, 2)
# ┌─────┬─────┐
# │ x   ┆ y   │
# │ --- ┆ --- │
# │ i64 ┆ i64 │
# ╞═════╪═════╡
# │ 0   ┆ 0   │
# │ 3   ┆ 5   │
# │ 4   ┆ 7   │
# │ 2   ┆ 2   │
# └─────┴─────┘

##-------------------------------------##
## Dataclass list with explicit schema ##
##-------------------------------------##

student_dc = make_dataclass(
    "StudentScore",
    [("name", str), ("subject", str), ("score", int)],
)

student_scores = [
    student_dc("Alice", "Math", 85),
    student_dc("Alice", "Science", 90),
    student_dc("Susan", "Math", 92),
]

df = pl.from_dicts(
    data=[asdict(row) for row in student_scores],
    schema={
        "name": pl.String,
        "subject": pl.String,
        "score": pl.Int32,
    },
)

print(df)
# shape: (3, 3)
# ┌───────┬─────────┬───────┐
# │ name  ┆ subject ┆ score │
# │ ---   ┆ ---     ┆ ---   │
# │ str   ┆ str     ┆ i32   │
# ╞═══════╪═════════╪═══════╡
# │ Alice ┆ Math    ┆ 85    │
# │ Alice ┆ Science ┆ 90    │
# │ Susan ┆ Math    ┆ 92    │
# └───────┴─────────┴───────┘


# =========================================================================================
# 9. Other constructors
# =========================================================================================

##----------------##
## pl.from_dict() ##
##----------------##
'''
pl.from_dict() constructs a DataFrame from a dictionary of sequences.
It is essentially the explicit function version of pl.DataFrame({...}).
'''

df = pl.from_dict(
    data=dict([("A", [1, 2, 3]), ("B", [4, 5, 6])])
)
print(df)
# shape: (3, 2)
# ┌─────┬─────┐
# │ A   ┆ B   │
# │ --- ┆ --- │
# │ i64 ┆ i64 │
# ╞═════╪═════╡
# │ 1   ┆ 4   │
# │ 2   ┆ 5   │
# │ 3   ┆ 6   │
# └─────┴─────┘

##--------------------------------------------##
## pandas orient="index" equivalent in Polars ##
##--------------------------------------------##
'''
Pandas DataFrame.from_dict(..., orient="index") uses dictionary keys as row indexes.
Polars has no row index, so keep those keys in a normal column.
'''

df = pl.from_records(
    data=[
        ("A", 1, 2, 3),
        ("B", 4, 5, 6),
    ],
    schema=["row_name", "one", "two", "three"],
    orient="row",
)

print(df)
# shape: (2, 4)
# ┌──────────┬─────┬─────┬───────┐
# │ row_name ┆ one ┆ two ┆ three │
# │ ---      ┆ --- ┆ --- ┆ ---   │
# │ str      ┆ i64 ┆ i64 ┆ i64   │
# ╞══════════╪═════╪═════╪═══════╡
# │ A        ┆ 1   ┆ 2   ┆ 3     │
# │ B        ┆ 4   ┆ 5   ┆ 6     │
# └──────────┴─────┴─────┴───────┘

##-----------------##
## pl.from_dicts() ##
##-----------------##
'''pl.from_dicts() is for a sequence of dictionaries, where each dictionary is a row.'''

df = pl.from_dicts(
    data=[
        {"A": 1, "B": 4},
        {"A": 2, "B": 5},
        {"A": 3, "B": 6},
    ]
)
print(df)
# shape: (3, 2)
# ┌─────┬─────┐
# │ A   ┆ B   │
# │ --- ┆ --- │
# │ i64 ┆ i64 │
# ╞═════╪═════╡
# │ 1   ┆ 4   │
# │ 2   ┆ 5   │
# │ 3   ┆ 6   │
# └─────┴─────┘

##-------------------##
## pl.from_records() ##
##-------------------##
'''
pl.from_records() constructs a DataFrame from a sequence of sequences.
Use orient="row" when each tuple/list is one row.
'''

record_rows = [
    (1, 2.0, "Hello"),
    (2, 3.0, "World"),
]

df = pl.from_records(
    data=record_rows,
    schema=["A", "B", "C"],
    orient="row",
)

print(df)
# shape: (2, 3)
# ┌─────┬─────┬───────┐
# │ A   ┆ B   ┆ C     │
# │ --- ┆ --- ┆ ---   │
# │ i64 ┆ f64 ┆ str   │
# ╞═════╪═════╪═══════╡
# │ 1   ┆ 2.0 ┆ Hello │
# │ 2   ┆ 3.0 ┆ World │
# └─────┴─────┴───────┘

##-----------------------------------##
## pl.from_records() with row labels ##
##-----------------------------------##
'''
Equivalent to pandas from_records(..., index=[...]):
store the labels in a normal column.
'''

df = pl.from_records(
    data=[
        ("first", 1, 2.0, "Hello"),
        ("second", 2, 3.0, "World"),
    ],
    schema=["row_name", "A", "B", "C"],
    orient="row",
)

print(df)
# shape: (2, 4)
# ┌──────────┬─────┬─────┬───────┐
# │ row_name ┆ A   ┆ B   ┆ C     │
# │ ---      ┆ --- ┆ --- ┆ ---   │
# │ str      ┆ i64 ┆ f64 ┆ str   │
# ╞══════════╪═════╪═════╪═══════╡
# │ first    ┆ 1   ┆ 2.0 ┆ Hello │
# │ second   ┆ 2   ┆ 3.0 ┆ World │
# └──────────┴─────┴─────┴───────┘

##---------------------------------------##
## pandas index="C" equivalent in Polars ##
##---------------------------------------##
'''
Pandas can use a column as the index.
In Polars, keep that field as a normal column; optionally move it to the front.
'''

df_c_first = df.select(["C", "A", "B"])
print(df_c_first)
# shape: (2, 3)
# ┌───────┬─────┬─────┐
# │ C     ┆ A   ┆ B   │
# │ ---   ┆ --- ┆ --- │
# │ str   ┆ i64 ┆ f64 │
# ╞═══════╪═════╪═════╡
# │ Hello ┆ 1   ┆ 2.0 │
# │ World ┆ 2   ┆ 3.0 │
# └───────┴─────┴─────┘

##-----------------##
## pl.from_numpy() ##
##-----------------##
'''
pl.from_numpy() is the explicit constructor for NumPy ndarrays.
It is slower than creating from columnar memory, but useful when data already exists as an ndarray.
'''

array_2d = np.array(
    [
        [1, 4],
        [2, 5],
        [3, 6],
    ]
)

df = pl.from_numpy(
    data=array_2d,
    schema=["A", "B"],
    orient="row",
)

print(df)
# shape: (3, 2)
# ┌─────┬─────┐
# │ A   ┆ B   │
# │ --- ┆ --- │
# │ i64 ┆ i64 │
# ╞═════╪═════╡
# │ 1   ┆ 4   │
# │ 2   ┆ 5   │
# │ 3   ┆ 6   │
# └─────┴─────┘

##-----------------##
## Empty DataFrame ##
##-----------------##
'''
You can create an empty DataFrame with a predefined schema.
This is useful when you want to append/concatenate later or define a contract.
'''

df_empty = pl.DataFrame(
    schema={
        "name": pl.String,
        "score": pl.Int64,
        "passed": pl.Boolean,
    }
)

print(df_empty)
# shape: (0, 3)
# ┌──────┬───────┬────────┐
# │ name ┆ score ┆ passed │
# │ ---  ┆ ---   ┆ ---    │
# │ str  ┆ i64   ┆ bool   │
# ╞══════╪═══════╪════════╡
# └──────┴───────┴────────┘

##--------------------##
## LazyFrame creation ##
##--------------------##
'''
Polars also has LazyFrame for lazy query execution.
Use .collect() to materialize the result as a DataFrame.
'''

lf = pl.LazyFrame(
    data={
        "A": [1, 2, 3],
        "B": [4, 5, 6],
    }
)

print(lf)
# naive plan: (run LazyFrame.explain(optimized=True) to see the optimized plan)
# DF ["A", "B"]; PROJECT */2 COLUMNS

print(lf.collect())
# shape: (3, 2)
# ┌─────┬─────┐
# │ A   ┆ B   │
# │ --- ┆ --- │
# │ i64 ┆ i64 │
# ╞═════╪═════╡
# │ 1   ┆ 4   │
# │ 2   ┆ 5   │
# │ 3   ┆ 6   │
# └─────┴─────┘
