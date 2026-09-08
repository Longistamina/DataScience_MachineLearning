"""
There are many ways to change the column names of the frame.

About row names, frames from polars and tidypyrs don't have index system.
Therefore, if we want to create row names, we need to treat them as a column of the frames.

1. Change Column names:
    + tf.columns = new_names
    + tl.rename({...})
    + tl.rename(dict(zip(...)))
    + tl.rename(function)
    + tl.rename(lambda col: ...)
    + tl.select(f.all().name.replace(...))
    + tl.select(pl.all().name.prefix('pre_'))
    + tl.select(pl.all().name.suffix('_suf'))
    + Example: clean Pokemon dataframe column names (lazyframe implementation)

2. Change Row names:
    + tl.row_index(name='row_id', offset=0)
    + Create row index with `row_index` then modify it
"""

import tidypyrs as tp  # noqa: I001
import polars as pl
from tidypyrs import f
from pathlib import Path

pl.Config(tbl_width_chars=120)
data_dir = next(Path("/home").glob("**/DataScience*/data"))

tf_lifexp = tp.read_csv(data_dir/"life_expectancy.csv", schema_overrides={"Population":pl.Float64})
