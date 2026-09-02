'''
``tidypolars`` is a data frame library built on top of the blazingly fast polars library
that gives access to methods and functions familiar to R tidyverse users.

##------------------------------------------------------------------------------------##

# Installation (my fork):
git clone https://github.com/Longistamina/tidypolars.git
cd tidypolars

# then activate your python venv (``conda activate``, ``source /path/to/venv/bin/activate``, ``source /path/to/venv/bin/activate.fish``, ...)

pip install .
'''

import tidypolars as tp
import polars as pl

df = tp.tibble({
    "name": ["Jimmy", "Keith"],
    "band": ["Led Zeppelin", "Stones"],
})

print(
    df
    .mutate(age = pl.Series([20, 23]))
    .select("name", "band", "age")
)
# shape: (2, 3)
# ┌───────┬──────────────┬─────┐
# │ name  ┆ band         ┆ age │
# │ ---   ┆ ---          ┆ --- │
# │ str   ┆ str          ┆ i64 │
# ╞═══════╪══════════════╪═════╡
# │ Jimmy ┆ Led Zeppelin ┆ 20  │
# │ Keith ┆ Stones       ┆ 23  │
# └───────┴──────────────┴─────┘
