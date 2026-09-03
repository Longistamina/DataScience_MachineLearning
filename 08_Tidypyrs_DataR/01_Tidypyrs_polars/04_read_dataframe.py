'''
tidypyrs supports several wrappers of polars reading functions, including:
    + tp.read_csv
    + tp.read_excel
    + tp.scan_csv
    + tp.read_parquet (not demo here)
'''

import tidypyrs as tp  # noqa: I001
from pathlib import Path

data_dir = next(Path("/home").glob("**/DataScience*/data"))


# =================================================
# 1. tp.read_csv()
# =================================================

tf_baseball = tp.read_csv(data_dir/"baseball.csv")

print(tf_baseball)
# shape: (1_015, 7)
# ┌─────────────────┬──────┬────────────────┬────────┬────────┬───────┬─────────────┐
# │ Name            ┆ Team ┆ Position       ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---             ┆ ---  ┆ ---            ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ str             ┆ str  ┆ str            ┆ i64    ┆ i64    ┆ f64   ┆ str         │
# ╞═════════════════╪══════╪════════════════╪════════╪════════╪═══════╪═════════════╡
# │ Adam_Donachie   ┆ BAL  ┆ Catcher        ┆ 74     ┆ 180    ┆ 22.99 ┆ Catcher     │
# │ Paul_Bako       ┆ BAL  ┆ Catcher        ┆ 74     ┆ 215    ┆ 34.69 ┆ Catcher     │
# │ Ramon_Hernandez ┆ BAL  ┆ Catcher        ┆ 72     ┆ 210    ┆ 30.78 ┆ Catcher     │
# │ Kevin_Millar    ┆ BAL  ┆ First_Baseman  ┆ 72     ┆ 210    ┆ 35.43 ┆ Infielder   │
# │ Chris_Gomez     ┆ BAL  ┆ First_Baseman  ┆ 73     ┆ 188    ┆ 35.71 ┆ Infielder   │
# │ …               ┆ …    ┆ …              ┆ …      ┆ …      ┆ …     ┆ …       │
# │ Brad_Thompson   ┆ STL  ┆ Relief_Pitcher ┆ 73     ┆ 190    ┆ 25.08 ┆ Pitcher     │
# │ Tyler_Johnson   ┆ STL  ┆ Relief_Pitcher ┆ 74     ┆ 180    ┆ 25.73 ┆ Pitcher     │
# │ Chris_Narveson  ┆ STL  ┆ Relief_Pitcher ┆ 75     ┆ 205    ┆ 25.19 ┆ Pitcher     │
# │ Randy_Keisler   ┆ STL  ┆ Relief_Pitcher ┆ 75     ┆ 190    ┆ 31.01 ┆ Pitcher     │
# │ Josh_Kinney     ┆ STL  ┆ Relief_Pitcher ┆ 73     ┆ 195    ┆ 27.92 ┆ Pitcher     │
# └─────────────────┴──────┴────────────────┴────────┴────────┴───────┴─────────────┘

print(type(tf_baseball))
# <class 'tidypyrs.tibble_frame.TibbleFrame'>


# =================================================
# 2. tp.read_exce;()
# =================================================

tf_emp = tp.read_excel(data_dir/"emp_sheetname.xlsx", sheet_id=1) # `sheet_id=0` will read all sheets into a dictionary
print(tf_emp) # `sheet_id=1` read the first sheets
# shape: (8, 5)
# ┌─────┬──────────┬────────┬────────────┬────────────┐
# │ id  ┆ name     ┆ salary ┆ start_date ┆ dept       │
# │ --- ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ str ┆ str      ┆ f64    ┆ date       ┆ str        │
# ╞═════╪══════════╪════════╪════════════╪════════════╡
# │ 1   ┆ Rick     ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ 2   ┆ Dan      ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# │ 3   ┆ Michelle ┆ 611.0  ┆ 2014-11-15 ┆ IT         │
# │ 4   ┆ Ryan     ┆ 729.0  ┆ 2014-05-11 ┆ HR         │
# │     ┆ Gary     ┆ 843.25 ┆ 2015-03-27 ┆ Finance    │
# │ 6   ┆ Nina     ┆ 578.0  ┆ 2013-05-21 ┆ IT         │
# │ 7   ┆ Simon    ┆ 632.8  ┆ 2013-07-30 ┆ Operations │
# │ 8   ┆ Guru     ┆ 722.5  ┆ 2014-06-17 ┆ Finance    │
# └─────┴──────────┴────────┴────────────┴────────────┘

print(type(tf_emp))
# <class 'tidypyrs.tibble_frame.TibbleFrame'>


# =================================================
# 2. tp.scan_csv(): read into TibbleLazy
# =================================================

tl_air = tp.scan_csv(data_dir/"air_quality_no2_long.csv")

print(tl_air)
# naive plan: (run LazyFrame.explain(optimized=True) to see the optimized plan)
# Csv SCAN [/home/longdpt/Documents/Academic/DataScience_MachineLearning/data/air_quality_no2_long.csv]
# PROJECT */7 COLUMNS
# ESTIMATED ROWS: 2267

print(type(tl_air))
# <class 'tidypyrs.tibble_lazy.TibbleLazy'>

print(tl_air.collect())
# shape: (2_068, 7)
# ┌────────┬─────────┬───────────────────────────┬────────────────────┬───────────┬───────┬───────┐
# │ city   ┆ country ┆ date.utc                  ┆ location           ┆ parameter ┆ value ┆ unit  │
# │ ---    ┆ ---     ┆ ---                       ┆ ---                ┆ ---       ┆ ---   ┆ ---   │
# │ str    ┆ str     ┆ str                       ┆ str                ┆ str       ┆ f64   ┆ str   │
# ╞════════╪═════════╪═══════════════════════════╪════════════════════╪═══════════╪═══════╪═══════╡
# │ Paris  ┆ FR      ┆ 2019-06-21 00:00:00+00:00 ┆ FR04014            ┆ no2       ┆ 20.0  ┆ µg/m³ │
# │ Paris  ┆ FR      ┆ 2019-06-20 23:00:00+00:00 ┆ FR04014            ┆ no2       ┆ 21.8  ┆ µg/m³ │
# │ Paris  ┆ FR      ┆ 2019-06-20 22:00:00+00:00 ┆ FR04014            ┆ no2       ┆ 26.5  ┆ µg/m³ │
# │ Paris  ┆ FR      ┆ 2019-06-20 21:00:00+00:00 ┆ FR04014            ┆ no2       ┆ 24.9  ┆ µg/m³ │
# │ Paris  ┆ FR      ┆ 2019-06-20 20:00:00+00:00 ┆ FR04014            ┆ no2       ┆ 21.4  ┆ µg/m³ │
# │ …      ┆ …       ┆ …                         ┆ …                  ┆ …         ┆ …     ┆ …     │
# │ London ┆ GB      ┆ 2019-05-07 06:00:00+00:00 ┆ London Westminster ┆ no2       ┆ 26.0  ┆ µg/m³ │
# │ London ┆ GB      ┆ 2019-05-07 04:00:00+00:00 ┆ London Westminster ┆ no2       ┆ 16.0  ┆ µg/m³ │
# │ London ┆ GB      ┆ 2019-05-07 03:00:00+00:00 ┆ London Westminster ┆ no2       ┆ 19.0  ┆ µg/m³ │
# │ London ┆ GB      ┆ 2019-05-07 02:00:00+00:00 ┆ London Westminster ┆ no2       ┆ 19.0  ┆ µg/m³ │
# │ London ┆ GB      ┆ 2019-05-07 01:00:00+00:00 ┆ London Westminster ┆ no2       ┆ 23.0  ┆ µg/m³ │
# └────────┴─────────┴───────────────────────────┴────────────────────┴───────────┴───────┴───────┘
