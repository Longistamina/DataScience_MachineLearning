import statistics
import time

import numpy as np
import polars as pl
import tidypyrs as tp
from polars import col as c
from tidypyrs import f

lf = pl.LazyFrame({
    "x": np.random.uniform(-1., 1.01, 1_000_000),
    "y": np.random.uniform(-1., 1.01, 1_000_000),
    "z": np.random.uniform(-1., 1.01, 1_000_000)
})

tl = tp.as_tl(lf)

##------------------------##
## polars LazyFrame query ##
##------------------------##

polars_query = (
    lf
    .with_columns((c("x").pow(2) + c("y").pow(2) + c("z").pow(2)).sqrt().alias("norm"))
    .with_columns(
        pl.when(c("norm") <= 0.35).then(pl.lit("low"))
        .when(c("norm") <= 0.7).then(pl.lit("medium"))
        .otherwise(pl.lit("high"))
        .alias("magnitude")
    )
    .pipe(lambda lf: lf.with_columns(
        c("magnitude").cast(pl.String).cast(pl.Enum(lf.select("magnitude").collect().to_series().cast(pl.String).unique().sort()))
    ))
)

end = time.perf_counter()

##---------------------------##
## tidypyrs TibbleLazy query ##
##---------------------------##

tidypyrs_query = (
    tl
    .mutate(
        (f("x").pow(2) + f("y").pow(2) + f("z").pow(2)).sqrt().alias("norm"),

        tp.when(f("norm") <= 0.35).then(tp.lit("low"))
        .when(f("norm") <= 0.7).then(tp.lit("medium"))
        .otherwise(tp.lit("high"))
        .alias("magnitude"),

        f("magnitude").pipe(tp.as_enum, f.pull("magnitude")),

        parallel=False
    )
)

##---------------------------------##
##            Benchmark            ##
##---------------------------------##

# Warm up both query plans.
polars_query.collect()
tidypyrs_query.collect()

polars_times = []
tidypyrs_times = []

for _ in range(100):
    start = time.perf_counter()
    polars_query.collect()
    polars_times.append(time.perf_counter() - start)

    start = time.perf_counter()
    tidypyrs_query.collect()
    tidypyrs_times.append(time.perf_counter() - start)

##-------------------------------##
##            Results            ##
##-------------------------------##

polars_plan = polars_query.explain(optimized=True)
tidypyrs_plan = tidypyrs_query.explain(optimized=True)
print(f"Same query plan: {polars_plan == tidypyrs_plan}\n")
# Same query plan: True

print("Polars median (second):", statistics.median(polars_times))
print("Tidypyrs median (second):", statistics.median(tidypyrs_times))
# Polars median (second): 0.003103318498688168
# Tidypyrs median (second): 0.0030748055014555575
