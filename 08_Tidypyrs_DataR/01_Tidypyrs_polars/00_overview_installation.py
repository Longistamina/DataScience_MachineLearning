'''
``tidypyrs`` is a data frame library built on top of the blazingly fast polars library
that gives access to methods and functions familiar to R tidyverse users.

##------------------------------------------------------------------------------------##

pip install tidypyrs
uv pip install tidypyrs
'''

import tidypyrs as tp

tf = tp.TibbleFrame({
    "name": ["Jimmy", "Keith"],
    "band": ["Led Zeppelin", "Stones"],
})

print(
    tf
    .mutate(age = tp.Series([20, 23]))
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
