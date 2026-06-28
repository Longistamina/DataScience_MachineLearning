'''
Polars offers eager readers and lazy scanners to load data from many file formats.

This file mirrors the pandas guide for:
1. CSV / TSV files
2. Excel files
3. JSON / NDJSON files
4. XML files
5. URL / remote files

It also adds Polars-specific `scan_*` APIs.

##################################################################

Main pandas -> Polars mapping:

1. pd.read_csv()       -> pl.read_csv()       # eager DataFrame
                          pl.scan_csv()       # lazy LazyFrame

2. pd.read_excel()     -> pl.read_excel()     # eager DataFrame
                          # No native scan_excel()

3. pd.read_json()      -> pl.read_json()      # eager JSON DataFrame
                          pl.read_ndjson()    # eager newline-delimited JSON
                          pl.scan_ndjson()    # lazy newline-delimited JSON
                          pl.json_normalize() # flatten deserialized nested JSON

4. pd.read_xml()       -> no native pl.read_xml() in core Polars
                          # Use Python XML parsing, plugins, or convert first

5. pd.read_csv(url)    -> pl.read_csv(url)
                          pl.scan_csv(url)    # when supported by fsspec/cloud backends

Extra scan APIs covered near the end:
+ pl.scan_csv()
+ pl.scan_ndjson()
+ pl.scan_parquet()
+ pl.scan_ipc()
+ pl.scan_delta()
+ pl.scan_lines()
+ pl.scan_pyarrow_dataset()

Important Polars differences:
+ Polars has no custom row index like pandas. Keep id/date/index-like data as normal columns.
+ `usecols=` becomes `columns=` in eager read_csv/read_excel.
+ `dtype=` becomes `schema_overrides=` or full `schema=`.
+ `sep=` becomes `separator=`.
+ `parse_dates=` becomes `try_parse_dates=True` or explicit `.str.strptime(...)`.
+ `skiprows=` becomes `skip_rows=` or `skip_lines=`.
+ `nrows=` becomes `n_rows=`.
+ `skipfooter=` has no direct Polars CSV parameter; use comment handling or slice rows after reading.
+ Lazy scans return a LazyFrame and require `.collect()` to materialize a DataFrame.
'''

import json
from io import BytesIO, StringIO
from pathlib import Path
from urllib.request import urlopen
from xml.etree import ElementTree as ET

import polars as pl

# Try to find the same data directory used by the pandas guide.
data_dir = Path("/home").rglob("*/DataScience_MachineLearning/data")
data_dir = next(data_dir)


#---------------------------------------------------------------------------------------------------------#
#----------------------------------------- 1. pl.read_csv() ----------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
pl.read_csv() eagerly reads a CSV file into a Polars DataFrame.

Detailed documentation:
https://docs.pola.rs/api/python/stable/reference/api/polars.read_csv.html

Key parameters:
+ source: file path, file-like object, bytes, or sometimes remote source via fsspec
+ has_header: whether the first row contains column names
+ columns: subset of columns to read, by names or positions
+ new_columns: rename columns immediately after parsing
+ separator: field separator; equivalent to pandas sep/delimiter
+ skip_rows: number of valid CSV rows to skip before parsing the header
+ skip_lines: number of raw newline-delimited lines to skip
+ n_rows: number of rows to read
+ schema: full schema; disables inference
+ schema_overrides: partial dtype overrides; equivalent to many pandas dtype= use cases
+ null_values: strings to treat as null
+ try_parse_dates: attempt to parse date/datetime strings
+ row_index_name: create a row-number column; not the same as pandas index_col
+ comment_prefix: skip comment lines, useful for files with footer comments
+ truncate_ragged_lines: truncate lines that are longer than the schema
'''

#################
## Basic Usage ##
#################

df = pl.read_csv(data_dir/"emp.csv")

print(df)
# shape: (8, 5)
# columns: id, name, salary, start_date, dept

print(df.schema)
# Schema({'id': Int64, 'name': String, 'salary': Float64, 'start_date': String, 'dept': String})

###############################
## index_col= does not exist ##
###############################
'''
Polars DataFrames do not have custom row index labels.

Pandas:
    pd.read_csv(..., index_col="id")

Polars:
    keep "id" as a normal column.

This is usually better for Polars because filtering, joining, grouping, and sorting
all work directly with normal columns.
'''

df = pl.read_csv(data_dir/"emp.csv")
print(df)
# shape: (8, 5)
# id remains a normal column.

# If you really want a row-number column, use row_index_name.
df_with_row_number = pl.read_csv(
    source=data_dir/"emp.csv",
    row_index_name="row_nr",
    row_index_offset=0,
)
print(df_with_row_number)
# shape: (8, 6)
# columns: row_nr, id, name, salary, start_date, dept

######################
## Specify columns= ##
######################
'''
Pandas uses usecols=.
Polars uses columns= for eager CSV reading.

columns= accepts:
+ column names
+ zero-based integer positions
'''

df = pl.read_csv(
    source=data_dir/"emp.csv",
    columns=["name", "salary", "dept"],
)
print(df)
# shape: (8, 3)
# columns: name, salary, dept


# Read columns by position: 1=name, 2=salary, 4=dept.
df = pl.read_csv(
    source=data_dir/"emp.csv",
    columns=[1, 2, 4],
)
print(df)
# shape: (8, 3)
# columns: name, salary, dept

###############################
## Specify schema_overrides= ##
###############################
'''
Pandas dtype= is usually translated to Polars schema_overrides=.

Common Polars dtypes:
+ pl.String
+ pl.Int64
+ pl.Float64
+ pl.Boolean
+ pl.Date
+ pl.Datetime
+ pl.Categorical
'''

df = pl.read_csv(
    source=data_dir/"emp.csv",
    columns=["name", "salary", "dept", "start_date"],
    schema_overrides={
        "name": pl.String,
        "salary": pl.Float64,
        "dept": pl.Categorical,
    },
)
print(df.schema)
# Schema({'name': String, 'salary': Float64, 'start_date': String, 'dept': Categorical})

##########################
## Specify parse_dates= ##
##########################
'''
Polars does not have pandas-style parse_dates=["col"].

Option 1:
    try_parse_dates=True

Option 2:
    read as strings and explicitly parse with .str.strptime(...)

try_parse_dates=True attempts to infer date/datetime columns.
If inference does not succeed, the column remains pl.String.
'''

#-----------
## Automatic date parsing
#-----------

df = pl.read_csv(
    source=data_dir / "emp.csv",
    schema_overrides={
        "name": pl.String,
        "salary": pl.Float64,
        "dept": pl.Categorical,
    },
    try_parse_dates=True,
)
print(df.schema)
# start_date is typically parsed as Date for ISO-like values such as 2012-01-01.

#-----------
## Explicit date parsing after reading
#-----------

df = (
    pl.read_csv(data_dir / "emp.csv")
    .with_columns(
        pl.col("start_date").str.strptime(pl.Date, "%Y-%m-%d").alias("start_date")
    )
)
print(df.schema)
# Schema({'id': Int64, 'name': String, 'salary': Float64, 'start_date': Date, 'dept': String})

#-----------
## pandas parse_dates=True with index_col= is not a Polars pattern
#-----------
'''
Pandas often reads a date column as the index.
In Polars, keep the date as a regular column and mark/sort/filter by that column.
'''

df = (
    pl.read_csv(data_dir/"emp.csv", try_parse_dates=True)
    .sort("start_date")
)
print(df)
# start_date is a normal column, not an index.

#################################
## With has_header/new_columns ##
#################################
'''
Pandas:
    header=0, names=[...]

Polars:
    has_header=True/False
    new_columns=[...]

If the original file has a header row and you want to override the names,
keep has_header=True and pass new_columns=.
'''

df = pl.read_csv(
    source=data_dir / "emp.csv",
    has_header=True,
    new_columns=["ID", "NAME", "SALARY", "START_DATE", "DEPT"],
)
print(df)
# shape: (8, 5)
# columns: ID, NAME, SALARY, START_DATE, DEPT

#-------

'''
If a CSV has no header row, set has_header=False and provide new_columns=.
Polars will otherwise create names such as column_1, column_2, ...
'''

# df_no_header = pl.read_csv(
#     source=data_dir/"emp_no_header.csv",
#     has_header=False,
#     new_columns=["id", "name", "salary", "start_date", "dept"],
# )
# print(df_no_header)

##################################
## Read TSV file with separator ##
##################################
'''
Pandas:
    sep="\t"

Polars:
    separator="\t"
'''

df = pl.read_csv(
    source=data_dir/"emp.tsv",
    separator="\t",
)
print(df)
# shape: (8, 5)
# columns may include: Unnamed: 0, name, salary, start_date, dept

#-------
'''
No index_col= in Polars.
If the first column is an ID-like column, keep it or rename it.
'''

df = pl.read_csv(
    source=data_dir/"emp.tsv",
    separator="\t",
).rename({"": "id"})
print(df)
# shape: (8, 5)
# columns: id, name, salary, start_date, dept

########################
## Handle null values ##
########################
'''
Pandas:
    na_values=["?"]

Polars:
    null_values=["?"]

Polars uses null as the missing value marker.
'''

df = pl.read_csv(
    source=data_dir/"emp.tsv",
    separator="\t",
    null_values=["?"],
).rename({"": "id"})
print(df)
# The "?" value is now null.

print(df.null_count())
# Shows null counts by column.

#-------

# You can also specify null values per column.
df = pl.read_csv(
    source=data_dir / "emp.tsv",
    separator="\t",
    null_values={"": "?"},
).rename({"": "id"})
print(df)

####################################
## Read with skip_rows and n_rows ##
####################################
'''
Pandas:
    skiprows=2
    nrows=4

Polars:
    skip_rows=2      # skips valid CSV rows and respects quotes/comments
    skip_lines=2     # skips raw lines; does not respect CSV quoting
    n_rows=4
'''

# Skip the first 2 corrupted rows.
df = pl.read_csv(
    source=data_dir/"emp_skiprows.tsv",
    separator="\t",
    skip_rows=2,
)
print(df)
# shape: (8, 5)

#-------

# Skip 2 rows and read only 4 rows.
df = pl.read_csv(
    source=data_dir/"emp_skiprows.tsv",
    separator="\t",
    skip_rows=2,
    n_rows=4,
)
print(df)
# shape: (4, 5)

######################################
## skip_rows_after_header= examples ##
######################################
'''
skip_rows_after_header= is useful when a file has a valid header but then has
one or more metadata rows immediately after the header.
'''

# df = pl.read_csv(
#     source=data_dir / "file_with_header_then_metadata.csv",
#     skip_rows_after_header=1,
# )
# print(df)

############################################
## Read with skipfooter= equivalent notes ##
############################################
'''
Polars does not have a direct skipfooter= parameter for CSV.

Common workarounds:
1. If footer lines start with a marker such as #, use comment_prefix="#".
2. Otherwise, read the file and remove the last N rows afterwards.
3. For very large files, clean the file before reading or use a streaming/preprocessing step.
'''

# Option 1: footer lines are comments.
df = pl.read_csv(
    source=data_dir/"emp_skipfooter.csv",
    comment_prefix="#",
    null_values=[" "],
)
print(df)
# Footer lines starting with # are skipped.

#-------

# Option 2: read first, then remove the final 2 rows.
df_raw = pl.read_csv(
    source=data_dir / "emp_skipfooter.csv",
    null_values=[" "],
    ignore_errors=True,
)

df_without_footer = df_raw.slice(0, max(0, df_raw.height - 2))

print(df_without_footer)
# Last 2 rows removed after reading.

############################################
## Bad/ragged CSV lines and comment lines ##
############################################
'''
For malformed CSV data, useful options include:
+ ignore_errors=True
+ truncate_ragged_lines=True
+ comment_prefix="#"

Do not rely on these as a substitute for cleaning severely corrupted files.
'''

# Example: ignore schema mismatch errors where possible.
df = pl.read_csv(
    source=data_dir/"emp.csv",
    ignore_errors=True,
)
print(df)


#---------------------------------------------------------------------------------------------------------#
#----------------------------------------- 2. pl.scan_csv() ----------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
pl.scan_csv() lazily reads one or more CSV files and returns a LazyFrame.

Why scan_csv() is important:
+ It does not immediately read the whole file.
+ It lets Polars push filters and projections into the scan.
+ It can reduce memory usage and improve performance.
+ It supports glob patterns and multiple files.

Detailed documentation:
https://docs.pola.rs/api/python/stable/reference/api/polars.scan_csv.html

Important:
+ scan_csv() returns a LazyFrame.
+ Use .collect() to execute the query and return a DataFrame.
+ There is no eager columns= parameter in scan_csv(). Use .select(...) after scanning;
  Polars can push the projection down to the scan.
'''

#########################
## Basic lazy CSV scan ##
#########################

lf = pl.scan_csv(data_dir/"emp.csv")

print(lf)
# naive plan: Csv SCAN ...

# Materialize the LazyFrame.
df = lf.collect()

print(df)
# shape: (8, 5)

########################################
## Projection pushdown with .select() ##
########################################
'''
This is the lazy equivalent of pandas usecols=.
The optimizer can avoid reading unneeded columns.
'''

lf = (
    pl.scan_csv(data_dir / "emp.csv")
    .select(["name", "salary", "dept"])
)

df = lf.collect()

print(df)
# shape: (8, 3)
# columns: name, salary, dept

#######################################
## Predicate pushdown with .filter() ##
#######################################
'''
Filters can be pushed down to the scan so less data is loaded.
'''

lf = (
    pl.scan_csv(data_dir / "emp.csv", try_parse_dates=True)
    .filter(pl.col("salary") >= 650)
    .select(["name", "salary", "start_date", "dept"])
)

df = lf.collect()

print(df)
# Employees with salary >= 650.

#####################################################
## scan_csv with schema_overrides and date parsing ##
#####################################################

lf = pl.scan_csv(
    source=data_dir / "emp.csv",
    schema_overrides={
        "id": pl.Int64,
        "name": pl.String,
        "salary": pl.Float64,
        "dept": pl.Categorical,
    },
    try_parse_dates=True,
)

print(lf.collect_schema())
# Lazy schema without collecting all data.

print(lf.collect())

###################################
## scan_csv with separator / TSV ##
###################################

lf = pl.scan_csv(
    source=data_dir / "emp.tsv",
    separator="\t",
    null_values=["?"],
)

df = lf.collect()

print(df)

######################################
## scan_csv with with_column_names= ##
######################################
'''
with_column_names= lets you transform column names before the query is planned.
This exists on scan_csv(), not read_csv().
'''

lf = pl.scan_csv(
    source=data_dir / "emp.csv",
    with_column_names=lambda cols: [name.lower() for name in cols],
)
print(lf.collect())
# All column names lowercased.

#############################################
## scan_csv over many files with glob=True ##
#############################################
'''
scan_csv() can read multiple files via glob patterns.
include_file_paths= can add the source file path as a column.
'''

# Example pattern; adjust to your folder.
lf = pl.scan_csv(
    source=str(data_dir/"emp*.csv"),
    glob=True,
    include_file_paths="source_file",
    ignore_errors=True,
)

# Only collect a small sample in examples.
df_sample = lf.head(5).collect()

print(df_sample)

#############################################
## scan_csv with n_rows and row_index_name ##
#############################################

lf = pl.scan_csv(
    source=data_dir / "emp.csv",
    n_rows=4,
    row_index_name="row_nr",
)
print(lf.collect())
# shape: (4, 6)
# columns: row_nr, id, name, salary, start_date, dept

############################################
## Lazy vs eager anti-pattern explanation ##
############################################
'''
Avoid this pattern for large files:

    pl.read_csv("large.csv").lazy()

It first materializes the whole CSV eagerly and then converts to LazyFrame.
For large CSV files, prefer:

    pl.scan_csv("large.csv")
'''


#---------------------------------------------------------------------------------------------------------#
#----------------------------------------- 3. pl.read_excel() --------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
pl.read_excel() eagerly reads Excel spreadsheet data into a Polars DataFrame.

Detailed documentation:
https://docs.pola.rs/api/python/stable/reference/api/polars.read_excel.html

Key parameters:
+ source: Excel file path, file-like object, or multiple workbooks
+ sheet_id: sheet number; 1 means first sheet, 2 means second sheet, 0 means all sheets
+ sheet_name: sheet name or list/tuple of sheet names
+ table_name: read a named table object from the workbook
+ engine: parser engine; current default is "calamine"
+ columns: subset of columns by name or position
+ schema_overrides: dtype overrides
+ has_header: whether first row has headers
+ infer_schema_length: number of rows used for type inference

Important:
+ Polars has no native scan_excel(). Excel reading is eager.
+ For lazy workflows, read Excel once and convert to Parquet/IPC/CSV, then use scan_parquet/scan_ipc/scan_csv.
'''

# Depending on your environment, Excel support may require extra packages.
# Modern Polars defaults to the calamine engine through fastexcel.
# pip install fastexcel openpyxl
# conda install -c conda-forge fastexcel openpyxl

#################
## Basic Usage ##
#################

df = pl.read_excel(data_dir / "emp_sheetname.xlsx")

print(df)
# shape: (8, 5)
# columns: id, name, salary, start_date, dept

print(df.schema)

#########################
## Specify sheet_name= ##
#########################

# Read by sheet name.
df = pl.read_excel(
    source=data_dir/"emp_sheetname.xlsx",
    sheet_name="city",
)
print(df)
# shape: (8, 2)
# columns: name, city

#-------
'''
Polars sheet_id is 1-based.
Pandas sheet_name=1 means second sheet.
Polars sheet_id=2 means second sheet.
'''

df = pl.read_excel(
    source=data_dir/"emp_sheetname.xlsx",
    sheet_id=2,
)
print(df)
# second sheet

#-------

# Load all sheets as a dictionary of {sheet_name: DataFrame}.
all_sheets = pl.read_excel(
    source=data_dir/"emp_sheetname.xlsx",
    sheet_id=0,
)

print(type(all_sheets))
# <class 'dict'>

print(all_sheets.keys())
# dict_keys([...])

###############################
## columns= and dtype schema ##
###############################

# Select only a few columns from the workbook.
df = pl.read_excel(
    source=data_dir/"emp_sheetname.xlsx",
    columns=["name", "salary", "dept"],
    schema_overrides={
        "name": pl.String,
        "salary": pl.Float64,
        "dept": pl.Categorical,
    },
)

print(df)
print(df.schema)

##############################
## Read a named Excel table ##
##############################
'''
If the workbook contains an Excel named table, use table_name=.
The table name is unique across the workbook.
'''

# df_table = pl.read_excel(
#     source=data_dir / "workbook_with_table.xlsx",
#     table_name="SalesTable",
# )
# print(df_table)

###########################################
## No native scan_excel() in Polars core ##
###########################################
'''
For lazy processing, a common workflow is:
1. Read Excel eagerly once.
2. Write to a columnar format such as Parquet.
3. Use scan_parquet() for repeated lazy analysis.
'''

# excel_df = pl.read_excel(data_dir / "emp_sheetname.xlsx")
# excel_df.write_parquet(data_dir / "emp_from_excel.parquet")
# lf = pl.scan_parquet(data_dir / "emp_from_excel.parquet")
# print(lf.filter(pl.col("salary") > 650).collect())


#---------------------------------------------------------------------------------------------------------#
#----------------------------------------- 4. JSON / NDJSON ----------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
Polars has several JSON-related tools:

1. pl.read_json()
   + Eager reader for normal JSON data.
   + Good for JSON arrays / objects that fit in memory.

2. pl.read_ndjson()
   + Eager reader for newline-delimited JSON.
   + Each line should be a separate JSON object.

3. pl.scan_ndjson()
   + Lazy scanner for newline-delimited JSON.
   + Use this for large JSON-lines files.

4. pl.json_normalize()
   + Flattens already-deserialized nested Python dict/list data.
   + Similar spirit to pandas json_normalize(), but it does not have pandas record_path=.
     Select the nested list manually before passing it to pl.json_normalize().

Detailed documentation:
https://docs.pola.rs/api/python/stable/reference/api/polars.read_json.html
https://docs.pola.rs/api/python/stable/reference/api/polars.read_ndjson.html
https://docs.pola.rs/api/python/stable/reference/api/polars.scan_ndjson.html
https://docs.pola.rs/api/python/stable/reference/api/polars.json_normalize.html
'''

##########################
## pl.read_json() basic ##
##########################

# For a JSON file on disk.
df = pl.read_json(data_dir/"emps.json")
print(df)
# shape depends on the JSON orientation/structure.

#-------

# For a JSON string or file-like object.
json_str = '''
[
    {"id": 1, "name": "Rick", "salary": 623.30, "dept": "IT"},
    {"id": 2, "name": "Dan", "salary": 515.20, "dept": "Operations"},
    {"id": 3, "name": "Michelle", "salary": 611.00, "dept": "IT"}
]
'''

df = pl.read_json(StringIO(json_str))

print(df)
# shape: (3, 4)
# columns: id, name, salary, dept

#-------

# Declare or override schema.
df = pl.read_json(
    StringIO(json_str),
    schema={
        "id": pl.Int64,
        "name": pl.String,
        "salary": pl.Float64,
        "dept": pl.String,
    },
)

print(df.schema)

#######################################
## Normalize nested JSON with Polars ##
#######################################
'''
Pandas:
    pd.json_normalize(data=json_obj, record_path=["Mathematics", "book"])

Polars:
    json_obj = json.load(...)
    books = json_obj["Mathematics"]["book"]
    pl.json_normalize(books)
'''

with open(data_dir/"books.json", "r", encoding="utf-8") as f:
    json_obj = json.load(f)

books = json_obj["Mathematics"]["book"]

df_books = pl.json_normalize(
    books,
    separator=".",
    max_level=None,
)

print(df_books)
# Nested dict fields are flattened with dot-separated names.

#-------

# You can normalize to a limited depth.
df_books_level_1 = pl.json_normalize(
    books,
    separator=".",
    max_level=1,
)
print(df_books_level_1)

############################
## pl.read_ndjson() eager ##
############################
'''
NDJSON means newline-delimited JSON:
{"id": 1, "name": "Rick"}
{"id": 2, "name": "Dan"}
{"id": 3, "name": "Michelle"}

Use pl.read_ndjson() for eager loading.
'''

ndjson_str = '''
{"id": 1, "name": "Rick", "salary": 623.30}
{"id": 2, "name": "Dan", "salary": 515.20}
{"id": 3, "name": "Michelle", "salary": 611.00}
'''.strip()

df = pl.read_ndjson(StringIO(ndjson_str))

print(df)
# shape: (3, 3)

#-------

# From a file path.
# df = pl.read_ndjson(
#     source=data_dir / "employees.ndjson",
#     schema_overrides={"salary": pl.Float64},
# )
# print(df)

###########################
## pl.scan_ndjson() lazy ##
###########################
'''
There is no pl.scan_json() for a single JSON array in core Polars.
The lazy JSON scanner is for newline-delimited JSON: pl.scan_ndjson().
'''

# lf = pl.scan_ndjson(
#     source=data_dir / "employees.ndjson",
#     schema_overrides={"salary": pl.Float64},
# )
#
# df = (
#     lf.filter(pl.col("salary") > 600)
#     .select(["id", "name", "salary"])
#     .collect()
# )
#
# print(df)


#---------------------------------------------------------------------------------------------------------#
#----------------------------------------- 5. XML data ---------------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
Pandas has pd.read_xml().
Core Polars does not currently expose a native pl.read_xml() or pl.scan_xml().

Practical Polars workflows for XML:
1. Parse simple XML with Python's xml.etree.ElementTree, then build pl.DataFrame.
2. Use a third-party Polars plugin or another XML library if the XML is complex.
3. Convert XML to CSV/JSON/Parquet first, then read or scan with Polars.

The helper below works for simple XML where each child under the root represents one row,
and each grandchild represents one column.
It also keeps XML attributes as columns.
'''

def read_simple_xml_to_polars(path, row_tag=None) -> pl.DataFrame:
    """Read simple row-oriented XML into a Polars DataFrame.

    Parameters
    ----------
    path:
        XML file path.
    row_tag:
        Optional tag name for row elements. If omitted, direct children of the root
        are treated as rows.

    Returns
    -------
    pl.DataFrame
        DataFrame built from XML attributes and child element text.
    """
    root = ET.parse(path).getroot()

    if row_tag is None:
        rows = list(root)
    else:
        rows = root.findall(f".//{row_tag}")

    records = []

    for row in rows:
        record = dict(row.attrib)

        for child in row:
            # For simple XML, text values become column values.
            record[child.tag] = child.text.strip() if child.text is not None else None

        records.append(record)

    return pl.DataFrame(records)

###############
## Example 1 ##
###############

# Equivalent spirit to: pd.read_xml(data_dir / "cd.xml")
df_cd = read_simple_xml_to_polars(data_dir/"cd.xml")
print(df_cd)
# shape: (10, 6)
# columns may include: TITLE, ARTIST, COUNTRY, COMPANY, PRICE, YEAR

# Cast numeric columns after parsing because XML text is read as strings.
df_cd = df_cd.with_columns(
    pl.col("PRICE").cast(pl.Float64, strict=False),
    pl.col("YEAR").cast(pl.Int64, strict=False),
)

print(df_cd.schema)

###############
## Example 2 ##
###############

# Equivalent spirit to: pd.read_xml(data_dir / "food.xml")
df_food = read_simple_xml_to_polars(data_dir / "food.xml")
print(df_food)
# shape: (5, 4)
# columns may include: name, price, description, calories

df_food = df_food.with_columns(
    pl.col("calories").cast(pl.Int64, strict=False)
)
print(df_food.schema)

#####################
## Nested XML note ##
#####################
'''
For deeply nested XML, write a custom parser for your desired row shape.
Do not expect a generic XML-to-table conversion to always infer the table correctly.
'''

# Example pattern for a custom parser:
# root = ET.parse(data_dir / "complex.xml").getroot()
# records = []
# for item in root.findall(".//item"):
#     records.append({
#         "id": item.get("id"),
#         "title": item.findtext("title"),
#         "price": item.findtext("details/price"),
#     })
# df = pl.DataFrame(records)


#---------------------------------------------------------------------------------------------------------#
#--------------------------------------- 6. Read data from URL -------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
Polars can read from local files and, depending on installed dependencies/backends,
remote files and cloud locations.

For simple public CSV URLs, pl.read_csv(url) often works directly.
If not, download bytes with urllib/request/fsspec and pass a BytesIO object.
'''

url = "https://raw.githubusercontent.com/laxmimerit/All-CSV-ML-Data-Files-Download/refs/heads/master/jamesbond.csv"

###########################
## Direct URL read_csv() ##
###########################

# Direct read. This requires network access and appropriate backend support.
df_jamesbond = pl.read_csv(url)
print(df_jamesbond.head())
# shape: (5, 7)
# columns include Film, Year, Actor, Director, Box Office, Budget, Bond Actor Salary

###########################################
## Fallback: URL bytes -> BytesIO -> CSV ##
###########################################
'''
If direct URL reading is unavailable in your environment, use this fallback.
This is eager because the bytes are downloaded first.
'''

with urlopen(url) as response:
    csv_bytes = response.read()

df_jamesbond = pl.read_csv(BytesIO(csv_bytes))

print(df_jamesbond.head())

########################################
## Lazy scan_csv() from remote source ##
########################################
'''
pl.scan_csv() can scan local files, glob patterns, and supported remote/cloud paths.
For cloud object stores, pass storage_options= or rely on environment credentials.

For simple HTTP URLs, support may depend on fsspec/remote backend behavior.
When scanning works, use select/filter before collect() to get lazy benefits.
'''

# lf = (
#     pl.scan_csv(url)
#     .select(["Film", "Year", "Actor", "Box Office"])
#     .filter(pl.col("Year") >= 2000)
# )
#
# df_recent_bond = lf.collect()
# print(df_recent_bond)

#################################
## Cloud/object-store examples ##
#################################

# AWS S3 example.
# lf = pl.scan_csv(
#     "s3://my-bucket/path/to/*.csv",
#     storage_options={
#         "aws_region": "us-east-1",
#         # credentials are usually read from environment/instance role
#     },
# )
# print(lf.select(["col1", "col2"]).collect())

# Hugging Face example.
# lf = pl.scan_csv(
#     "hf://datasets/username/dataset/train.csv",
#     storage_options={"token": "..."},
# )
# print(lf.head().collect())


#---------------------------------------------------------------------------------------------------------#
#----------------------------------- 7. Other Polars scan APIs -------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
Polars has many scan APIs besides scan_csv().
These return LazyFrame objects and are designed for lazy query optimization.

The most common lazy scan format is Parquet because it is columnar and supports
excellent projection/predicate pushdown.
'''


#---------------------------------------------------------------------------------------------------------#
#-------------------------------------- 7.1 pl.scan_parquet() -------------------------------------------#
#---------------------------------------------------------------------------------------------------------#

'''
Use scan_parquet() for Parquet files.
This is often the best format for repeated analytics.
'''

# Convert CSV to Parquet once.
# pl.read_csv(data_dir / "emp.csv", try_parse_dates=True).write_parquet(data_dir / "emp.parquet")

# Then scan lazily.
# lf = pl.scan_parquet(data_dir / "emp.parquet")
#
# df = (
#     lf.filter(pl.col("salary") > 650)
#     .select(["name", "salary", "dept"])
#     .collect()
# )
#
# print(df)

# Scan many Parquet files.
# lf = pl.scan_parquet(str(data_dir / "parquet_folder" / "*.parquet"), glob=True)
# print(lf.head(10).collect())


#---------------------------------------------------------------------------------------------------------#
#-------------------------------------- 7.2 pl.scan_ipc() ------------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
IPC/Feather files are Arrow-based columnar files.
Use scan_ipc() for lazy scanning of IPC/Feather v2 files.
'''

# pl.read_csv(data_dir / "emp.csv").write_ipc(data_dir / "emp.feather")
# lf = pl.scan_ipc(data_dir / "emp.feather")
# print(lf.select(["name", "dept"]).collect())


#---------------------------------------------------------------------------------------------------------#
#-------------------------------------- 7.3 pl.scan_ndjson() ---------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
Use scan_ndjson() for newline-delimited JSON.
This is the JSON format that Polars can scan lazily in core Polars.
'''

# lf = pl.scan_ndjson(data_dir / "employees.ndjson")
# print(lf.filter(pl.col("salary") > 600).collect())


#---------------------------------------------------------------------------------------------------------#
#-------------------------------------- 7.4 pl.scan_lines() ----------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
scan_lines() lazily scans plain text lines.
It is useful when each line is a record that you want to parse with expressions.
'''

# lf = pl.scan_lines(data_dir / "server.log")
# df = (
#     lf.rename({"line": "raw"})
#     .filter(pl.col("raw").str.contains("ERROR"))
#     .collect()
# )
# print(df)


#---------------------------------------------------------------------------------------------------------#
#-------------------------------------- 7.5 pl.scan_delta() ----------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
scan_delta() lazily scans Delta Lake tables.
This requires the optional Delta Lake dependencies and a valid Delta table.
'''

# lf = pl.scan_delta("/path/to/delta_table")
# print(lf.select(["customer_id", "amount"]).collect())


#---------------------------------------------------------------------------------------------------------#
#---------------------------------- 7.6 pl.scan_pyarrow_dataset() ----------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
scan_pyarrow_dataset() can scan a PyArrow Dataset lazily through Polars.
Use it when a dataset is already managed through pyarrow.dataset.
'''

# import pyarrow.dataset as ds
#
# dataset = ds.dataset(str(data_dir / "parquet_folder"), format="parquet")
# lf = pl.scan_pyarrow_dataset(dataset)
# print(lf.head().collect())


#---------------------------------------------------------------------------------------------------------#
#--------------------------------------- 8. Quick reference ----------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
Quick pandas -> Polars reference

CSV:
    pd.read_csv(path)
    pl.read_csv(path)

CSV lazy:
    # pandas has no direct equivalent
    pl.scan_csv(path).filter(...).select(...).collect()

Use selected columns:
    pd.read_csv(path, usecols=["a", "b"])
    pl.read_csv(path, columns=["a", "b"])
    pl.scan_csv(path).select(["a", "b"]).collect()

Dtypes:
    pd.read_csv(path, dtype={"x": "float64"})
    pl.read_csv(path, schema_overrides={"x": pl.Float64})
    pl.scan_csv(path, schema_overrides={"x": pl.Float64})

Parse dates:
    pd.read_csv(path, parse_dates=["date"])
    pl.read_csv(path, try_parse_dates=True)
    pl.read_csv(path).with_columns(pl.col("date").str.strptime(pl.Date, "%Y-%m-%d"))

Header and column names:
    pd.read_csv(path, header=0, names=[...])
    pl.read_csv(path, has_header=True, new_columns=[...])

TSV:
    pd.read_csv(path, sep="\t")
    pl.read_csv(path, separator="\t")

Null values:
    pd.read_csv(path, na_values=["?"])
    pl.read_csv(path, null_values=["?"])

Skip rows and row limit:
    pd.read_csv(path, skiprows=2, nrows=5)
    pl.read_csv(path, skip_rows=2, n_rows=5)

Skip footer:
    pd.read_csv(path, skipfooter=2, engine="python")
    # no direct Polars parameter; use comment_prefix="#" or slice after read

Excel:
    pd.read_excel(path, sheet_name="Sheet1")
    pl.read_excel(path, sheet_name="Sheet1")

JSON:
    pd.read_json(path)
    pl.read_json(path)

JSON normalize:
    pd.json_normalize(json_obj, record_path=["a", "b"])
    pl.json_normalize(json_obj["a"]["b"])

NDJSON lazy:
    pl.scan_ndjson(path).collect()

XML:
    pd.read_xml(path)
    # no native pl.read_xml(); parse with ElementTree or another XML tool, then pl.DataFrame(records)

URL:
    pd.read_csv(url)
    pl.read_csv(url)
    pl.scan_csv(url)  # if supported by your remote/fsspec/cloud backend
'''
