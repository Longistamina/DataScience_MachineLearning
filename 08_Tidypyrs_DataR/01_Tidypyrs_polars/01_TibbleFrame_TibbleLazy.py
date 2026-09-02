'''
`tidypyrs` provides `TibbleFrame` and `TibbleLazy`
as mapping versions of `polars` `DataFrame` and `LazyFrame`.

Use `TibbleFrame.lazy()` to convert into `TibbleLazy`.
Use `TibbleLazy.collect()` to convert into `TibbleFrame`.
'''

import tidypyrs as tp

# =================================================================================================
# 1. `TibbleFrame`
# =================================================================================================

##------------------------##
## Create a `TibbleFrame` ##
##------------------------##

tf = tp.TibbleFrame(
    name=["Alice", "Bob", "Carter", "Denver"],
    age=[23, 25, 20, 29],
    score=[98.2, 85.6, 95., 80.]
)

print(tf)
# shape: (4, 3)
# ┌────────┬─────┬───────┐
# │ name   ┆ age ┆ score │
# │ ---    ┆ --- ┆ ---   │
# │ str    ┆ i64 ┆ f64   │
# ╞════════╪═════╪═══════╡
# │ Alice  ┆ 23  ┆ 98.2  │
# │ Bob    ┆ 25  ┆ 85.6  │
# │ Carter ┆ 20  ┆ 95.0  │
# │ Denver ┆ 29  ┆ 80.0  │
# └────────┴─────┴───────┘

##--------------------------------------------------##
## Call `TibbleFrame.lazy()` to become `TibbleLazy` ##
##--------------------------------------------------##

tl = tf.lazy()
print(tl)
# naive plan: (run LazyFrame.explain(optimized=True) to see the optimized plan)
# DF ["name", "age", "score"]; PROJECT */3 COLUMNS

# =================================================================================================
# 2. `TibbleLazy`
# =================================================================================================

##-----------------------##
## Create a `TibbleLazy` ##
##-----------------------##

tl = tp.TibbleLazy({
    "kings": ["Charles", "Louis", "Edward", "Mason"],
    "queens": ["Anne", "Mary", "Loraine", "Fern"],
    "rank": [1, 4, 2, 3]
})

print(tl)
# naive plan: (run LazyFrame.explain(optimized=True) to see the optimized plan)
# DF ["kings", "queens", "rank"]; PROJECT */3 COLUMNS

##-----------------------------------------------------##
## Call `TibbleLazy.collect()` to become `TibbleFrame` ##
##-----------------------------------------------------##

tf = tl.collect()
print(tf)
# shape: (4, 3)
# ┌─────────┬─────────┬──────┐
# │ kings   ┆ queens  ┆ rank │
# │ ---     ┆ ---     ┆ ---  │
# │ str     ┆ str     ┆ i64  │
# ╞═════════╪═════════╪══════╡
# │ Charles ┆ Anne    ┆ 1    │
# │ Louis   ┆ Mary    ┆ 4    │
# │ Edward  ┆ Loraine ┆ 2    │
# │ Mason   ┆ Fern    ┆ 3    │
# └─────────┴─────────┴──────┘
