'''
TibbleFrame support two methods:
    + `as_polars()`: convert to `polars.DataFrame`
    + `as_pandas()`: convert to `pandas.DataFrame`

TibbleLazy support only one method:
    + `as_polars()`: convert to `polars.LazyFrame`

(Use `tl.collect().as_pandas()` to convert to `pandas.DataFrame`)
'''

import tidypyrs as tp  # noqa: I001


# =======================================================================
# 1. `TibbleFrame.as_polars()` and `TibbleFrame.as_pandas()`
# =======================================================================

tf = tp.TibbleFrame(
    name=["Alice", "Bob", "Carter", "Denver"],
    age=[23, 25, 20, 29],
    score=[98.2, 85.6, 95., 80.]
)

##----------------##
## tf.as_polars() ##
##----------------##

plf = tf.as_polars()

print(type(plf))
# <class 'polars.dataframe.frame.DataFrame'>

##----------------##
## tf.as_pandas() ##
##----------------##

pdf = tf.as_pandas()

print(type(pdf))
# <class 'pandas.DataFrame'>


# =========================================================================
# 2. `TibbleLazy.as_polars()` and `TibbleLazy.collect().as_pandas()`
# =========================================================================

tl = tp.TibbleLazy({
    "kings": ["Charles", "Louis", "Edward", "Mason"],
    "queens": ["Anne", "Mary", "Loraine", "Fern"],
    "rank": [1, 4, 2, 3]
})

##----------------##
## tl.as_polars() ##
##----------------##

plf = tl.as_polars()

print(type(plf))
# <class 'polars.lazyframe.frame.LazyFrame'>
'''LazyFrame, not DataFrame'''

##--------------------------##
## tl.collect().as_pandas() ##
##--------------------------##

pdf = tl.collect().as_pandas()

print(type(pdf))
# <class 'pandas.DataFrame'>
