'''
Save Polars DataFrames to common file formats.

1. df.write_csv('file_name.csv')      # Save an eager DataFrame to CSV
2. df.write_excel('file_name.xlsx')   # Save an eager DataFrame to Excel
3. df.write_json('file_name.json')    # Save an eager DataFrame to JSON
4. df.write_ndjson('file_name.ndjson')# Save an eager DataFrame to newline-delimited JSON

Polars notes:
+ Polars does not have a row index like pandas, so there is no index=False argument.
+ Most write_* methods are eager DataFrame methods.
+ LazyFrame can stream directly to some formats with sink_* methods, such as sink_csv() and sink_ndjson().
+ For Excel and regular JSON, collect the LazyFrame first, then write the eager DataFrame.
'''

import datetime as dt
import json
from pathlib import Path

import polars as pl

save_dir = next(Path("/home").rglob("*/07_Polars_fastDF_SQL"))
save_dir = save_dir.joinpath("save")
save_dir.mkdir(parents=True, exist_ok=True)

df = pl.DataFrame(
    {
        "Name": ["Alice", "Bob", "Charlie", "David"],
        "Age": [25.0, 30.0, 35.0, None],
        "City": ["New York", "Paris", "Berlin", "Tokyo"],
        "Salary": [50000.75, 60000.50, 75000.25, 90000.00],
        "Date": [
            dt.date(2023, 1, 31),
            dt.date(2023, 2, 28),
            dt.date(2023, 3, 31),
            dt.date(2023, 4, 30),
        ],
    }
)

# Create a LazyFrame version for lazy/streaming examples.
lf = df.lazy()

print(df)
# shape: (4, 5)
# ┌─────────┬──────┬──────────┬──────────┬────────────┐
# │ Name    ┆ Age  ┆ City     ┆ Salary   ┆ Date       │
# │ ---     ┆ ---  ┆ ---      ┆ ---      ┆ ---        │
# │ str     ┆ f64  ┆ str      ┆ f64      ┆ date       │
# ╞═════════╪══════╪══════════╪══════════╪════════════╡
# │ Alice   ┆ 25.0 ┆ New York ┆ 50000.75 ┆ 2023-01-31 │
# │ Bob     ┆ 30.0 ┆ Paris    ┆ 60000.5  ┆ 2023-02-28 │
# │ Charlie ┆ 35.0 ┆ Berlin   ┆ 75000.25 ┆ 2023-03-31 │
# │ David   ┆ null ┆ Tokyo    ┆ 90000.0  ┆ 2023-04-30 │
# └─────────┴──────┴──────────┴──────────┴────────────┘


# =========================================================================================
# 1. df.write_csv('file_name.csv')
# =========================================================================================
'''
Pandas:
    df.to_csv(path_or_buf='file_name.csv', sep=',', index=False, na_rep='NaN')

Polars:
    df.write_csv(file='file_name.csv', separator=',', null_value='NaN')

Polars has no row index, so there is no index=False argument.
'''

# Eager DataFrame -> CSV
df.write_csv(
    file=save_dir / "df_to.csv",
    separator=",",      # Column separator
    include_header=True, # Write column names
    null_value="NaN",    # Represent null values as 'NaN' in the CSV file
    date_format="%Y-%m-%d",
)

# LazyFrame -> CSV directly with sink_csv()
# This can be useful for large lazy pipelines because it can stream the result to disk.
lf.sink_csv(
    path=save_dir / "lazy_to.csv",
    separator=",",
    include_header=True,
    null_value="NaN",
)


# =========================================================================================
# 2. df.write_excel('file_name.xlsx')
# =========================================================================================
'''
Pandas:
    df.to_excel(excel_writer='file_name.xlsx', sheet_name='Sheet1', index=False)

Polars:
    df.write_excel(workbook='file_name.xlsx', worksheet='Sheet1')

Polars writes Excel files from an eager DataFrame.
If your data is lazy, collect it first.

pip3 install xlsxwriter
'''

# Eager DataFrame -> Excel
df.write_excel(
    workbook=save_dir / "df_to.xlsx",
    worksheet="Sheet1",
    autofit=True,
)

# LazyFrame -> collect() -> Excel
# There is no LazyFrame.sink_excel() method.
lf.collect().write_excel(
    workbook=save_dir / "lazy_collected_to.xlsx",
    worksheet="Sheet1",
    autofit=True,
)


# =========================================================================================
# 3. df.write_json('file_name.json')
# =========================================================================================
'''
Pandas:
    df.to_json(path_or_buf='file_name.json', orient='records', indent=4, date_format='iso')

Polars:
    df.write_json(file='file_name.json', row_oriented=True, pretty=True)

row_oriented=True is the closest equivalent to pandas orient='records':
    [
        {"Name": "Alice", "Age": 25.0, ...},
        {"Name": "Bob", "Age": 30.0, ...}
    ]
'''

##-----------------------------##
## native polars .write_json() ##
##-----------------------------##

# Eager DataFrame -> JSON
df.write_json(file=save_dir / "df_to.json")

# LazyFrame -> collect() -> JSON
# There is no LazyFrame.sink_json() for regular JSON arrays.
lf.collect().write_json(file=save_dir / "lazy_collected_to.json")

##---------------------------------------------##
## use Python json for more readable json file ##
##---------------------------------------------##

(save_dir / "df_to_pretty.json").write_text(
    json.dumps(
        df.to_dicts(),
        indent=4,
        default=str,  # needed for Date / Datetime values
    ),
    encoding="utf-8",
)


# =========================================================================================
# 4. df.write_ndjson('file_name.ndjson')
# =========================================================================================
'''
NDJSON means newline-delimited JSON.
Each row is written as one JSON object on its own line.

This is similar to pandas:
    df.to_json(..., orient='records', lines=True)

Polars supports both:
    df.write_ndjson(...)
    lf.sink_ndjson(...)
'''

# Eager DataFrame -> NDJSON
df.write_ndjson(file=save_dir / "df_to.ndjson")

# LazyFrame -> NDJSON directly with sink_ndjson()
lf.sink_ndjson(path=save_dir / "lazy_to.ndjson")


# =========================================================================================
# 6. Quick summary
# =========================================================================================
'''
Pandas -> Polars mental map

1. CSV
   pandas: df.to_csv('file.csv', index=False, na_rep='NaN')
   polars: df.write_csv('file.csv', null_value='NaN')
   lazy:   lf.sink_csv('file.csv')

2. Excel
   pandas: df.to_excel('file.xlsx', index=False, sheet_name='Sheet1')
   polars: df.write_excel('file.xlsx', worksheet='Sheet1')
   lazy:   lf.collect().write_excel('file.xlsx')

3. JSON records
   pandas: df.to_json('file.json', orient='records', indent=4)
   polars: df.write_json('file.json')
   lazy:   lf.collect().write_json('file.json')
   Use Python json for pretty json file

4. JSON lines / NDJSON
   pandas: df.to_json('file.jsonl', orient='records', lines=True)
   polars: df.write_ndjson('file.ndjson')
   lazy:   lf.sink_ndjson('file.ndjson')
'''
