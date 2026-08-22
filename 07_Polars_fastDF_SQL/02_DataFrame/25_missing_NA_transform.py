'''
1. Detect missing values:
   + df.select(pl.all().is_null()): Returns a DataFrame of the same shape as df, with True for missing values
   + df.null_count(): Returns the count of missing values in each column
   + df.glimpse(), df.schema, df.describe(): Provide a summary of the DataFrame

2. Detect non-missing values:
   + df.select(pl.all().is_not_null()): Returns a DataFrame of the same shape as df, with True for non-missing values
   + df.select(pl.all().is_not_null().sum()): Returns the count of non-missing values in each column

3. Drop missing values along columns:
   + Polars does NOT have drop_nulls(axis=1)
   + Use .pipe(...) + column metadata such as .null_count() to select columns to keep
   + how='all': keep columns that are not entirely null
   + how='any': keep columns that have no nulls
   + thresh=...: keep columns with at least a minimum number of non-null values

4. Drop missing values along rows:
   + df.drop_nulls(): drop rows with any null values
   + df.filter(~pl.all_horizontal(pl.all().is_null())): drop rows where all values are null
   + df.drop_nulls(subset=[...]): drop rows with nulls in selected columns

5. Fill missing values:
   + df.fill_null(value): Fill nulls with a scalar value
   + df.with_columns(...fill_null(...)): Fill different columns with different values
   + df.with_columns(cs.numeric().fill_null(cs.numeric().mean())): Fill numeric nulls with column means
   + df.fill_null(strategy='forward'): Forward fill
   + df.fill_null(strategy='backward'): Backward fill

6. Interpolate missing values:
   + c(...).interpolate(): native linear interpolation
   + c(...).interpolate(method='nearest'): native nearest-neighbor interpolation
   + Boundary nulls can be handled with forward/backward fill after interpolation
   + Polynomial/spline interpolation are NOT native Polars APIs; use Python/SciPy fallback if needed

7. Conditional filling:
   + pl.when(c(...).is_null()).then(...).otherwise(...)

8. Group-based filling, transform-style:
   + c(...).fill_null(c(...).mean().over('week'))
'''

import polars as pl
import polars.selectors as cs
from polars import col as c
from pathlib import Path
from scipy import interpolate

# Optional display settings
pl.Config.set_tbl_rows(10)
pl.Config.set_tbl_cols(10)
pl.Config.set_tbl_width_chars(120)
pl.Config.set_float_precision(6)


data_dir = Path('/home').rglob('*/DataScience_MachineLearning/data')
data_dir = next(data_dir)


lf_mkt = (
    pl.scan_csv(
        source=data_dir / 'marketing_data.csv',
        schema_overrides={
            'week': pl.Categorical,
            'Year': pl.Categorical,
        },
    )
    .rename(lambda col: col.lower().strip())
    .select(pl.all().name.replace(r"[^a-zA-Z]", "_"))
)

print(lf_mkt.collect().glimpse())
# Rows: 156
# Columns: 26
# $ week                      <cat> 19, 20, 21, 22, 23, 24, 25, 26, 27, 28
# $ year                      <cat> 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010
# $ market_share              <f64> 38.4, 36.8, 35.21, 35.03, 32.37, 29.67, 32.67, 40.11, 38.93, 32.4
# $ av_price_per_kg           <f64> 7.61, 7.6, 7.63, 7.22, 7.7, 7.74, 7.75, 7.44, 7.45, 7.64
# $ non_promo_price_per_kg    <f64> 7.77, 7.8, 7.85, 7.76, 7.78, 7.77, 7.77, 7.68, 7.7, 7.79
# ...

print(lf_mkt.collect_schema().names())
# ['week', 'year', 'market_share', 'av_price_per_kg', 'non_promo_price_per_kg', 'promo_vol_share', 'total_weigh', 'share_of_ean_weigh', 'avg_price_vs_plb', 'non_promo_price_vs_plb', 'promo_vol_sh_index_vs_plb', 'total_cm_shelf', 'shelf_share', 'top_of_mind', 'spontaneous', 'aided', 'penetration', 'competitor', 'grp_radio', 'reach_radio', 'grp_tv', 'reach_tv', 'reach_cinema', 'grp_outdoor', 'grp_print', 'share_of_spend']


# =========================================================================================
# 1. Detect missing values
# =========================================================================================

##-------------------------------##
## lf.select(pl.all().is_null()) ##
##-------------------------------##
'''Returns a DataFrame of the same shape as df, with True for missing values.'''

print(
    lf_mkt
    #.select(pl.all().is_null()) # all columns
    .select(pl.nth(range(0, 6)).is_null()) # First 6 columns
    .head()
    .collect()
)
# shape: (5, 6)
# ┌───────┬───────┬──────────────┬─────────────────┬────────────────────────┬─────────────────┐
# │ week  ┆ year  ┆ market_share ┆ av_price_per_kg ┆ non_promo_price_per_kg ┆ promo_vol_share │
# │ ---   ┆ ---   ┆ ---          ┆ ---             ┆ ---                    ┆ ---             │
# │ bool  ┆ bool  ┆ bool         ┆ bool            ┆ bool                   ┆ bool            │
# ╞═══════╪═══════╪══════════════╪═════════════════╪════════════════════════╪═════════════════╡
# │ false ┆ false ┆ false        ┆ false           ┆ false                  ┆ false           │
# │ false ┆ false ┆ false        ┆ false           ┆ false                  ┆ false           │
# │ false ┆ false ┆ false        ┆ false           ┆ false                  ┆ false           │
# │ false ┆ false ┆ false        ┆ false           ┆ false                  ┆ false           │
# │ false ┆ false ┆ false        ┆ false           ┆ false                  ┆ false           │
# └───────┴───────┴──────────────┴─────────────────┴────────────────────────┴─────────────────┘

##-----------------##
## lf.null_count() ##
##-----------------##
'''Returns the count of missing values in each column.'''

print(lf_mkt.null_count().collect()) # all columns

print(
    lf_mkt
    .select(pl.nth(range(0, 6)).null_count()) # First 6 columns
    .collect()
)
# shape: (1, 6)
# ┌──────┬──────┬──────────────┬─────────────────┬────────────────────────┬─────────────────┐
# │ week ┆ year ┆ market_share ┆ av_price_per_kg ┆ non_promo_price_per_kg ┆ promo_vol_share │
# │ ---  ┆ ---  ┆ ---          ┆ ---             ┆ ---                    ┆ ---             │
# │ u32  ┆ u32  ┆ u32          ┆ u32             ┆ u32                    ┆ u32             │
# ╞══════╪══════╪══════════════╪═════════════════╪════════════════════════╪═════════════════╡
# │ 0    ┆ 0    ┆ 0            ┆ 0               ┆ 0                      ┆ 0               │
# └──────┴──────┴──────────────┴─────────────────┴────────────────────────┴─────────────────┘


# If you want a vertical, easy-to-read version:
print(
    lf_mkt
    .null_count()
    .collect() # Must realize here for transpose to work
    .transpose(include_header=True, header_name='column', column_names=['n_null'])
    .filter(c('n_null') > 0)
)
# shape: (13, 2)
# ┌────────────────┬────────┐
# │ column         ┆ n_null │
# │ ---            ┆ ---    │
# │ str            ┆ u32    │
# ╞════════════════╪════════╡
# │ top_of_mind    ┆ 33     │
# │ spontaneous    ┆ 33     │
# │ aided          ┆ 33     │
# │ penetration    ┆ 33     │
# │ competitor     ┆ 45     │
# │ …              ┆ …      │
# │ reach_tv       ┆ 104    │
# │ reach_cinema   ┆ 138    │
# │ grp_outdoor    ┆ 155    │
# │ grp_print      ┆ 134    │
# │ share_of_spend ┆ 40     │
# └────────────────┴────────┘

##------------------------##
## lf.collect().glimpse() ##
##------------------------##
'''Provides a compact summary of shape, column names, dtypes, and sample values.'''

print(lf_mkt.collect().glimpse())


# =========================================================================================
# 2. Detect non-missing values
# =========================================================================================

##-----------------------------------##
## lf.select(pl.all().is_not_null()) ##
##-----------------------------------##
'''Returns a DataFrame of the same shape as df, with True for non-missing values.'''

print(
    lf_mkt
    #.select(pl.all().is_not_null())
    .select(pl.nth(range(0, 6)).is_not_null()) # First 6 columns
    .head()
    .collect()
)
# shape: (5, 6)
# ┌──────┬──────┬──────────────┬─────────────────┬────────────────────────┬─────────────────┐
# │ week ┆ year ┆ market_share ┆ av_price_per_kg ┆ non_promo_price_per_kg ┆ promo_vol_share │
# │ ---  ┆ ---  ┆ ---          ┆ ---             ┆ ---                    ┆ ---             │
# │ bool ┆ bool ┆ bool         ┆ bool            ┆ bool                   ┆ bool            │
# ╞══════╪══════╪══════════════╪═════════════════╪════════════════════════╪═════════════════╡
# │ true ┆ true ┆ true         ┆ true            ┆ true                   ┆ true            │
# │ true ┆ true ┆ true         ┆ true            ┆ true                   ┆ true            │
# │ true ┆ true ┆ true         ┆ true            ┆ true                   ┆ true            │
# │ true ┆ true ┆ true         ┆ true            ┆ true                   ┆ true            │
# │ true ┆ true ┆ true         ┆ true            ┆ true                   ┆ true            │
# └──────┴──────┴──────────────┴─────────────────┴────────────────────────┴─────────────────┘

##-----------------------------------------##
## lf.select(pl.all().is_not_null().sum()) ##
##-----------------------------------------##
'''Returns the count of non-missing values in each column.'''

print(
    lf_mkt
    #.select(pl.all().is_not_null().sum())
    .select(pl.nth(range(0, 6)).is_not_null().sum()) # First 6 columns
    .collect()
)
# shape: (1, 6)
# ┌──────┬──────┬──────────────┬─────────────────┬────────────────────────┬─────────────────┐
# │ week ┆ year ┆ market_share ┆ av_price_per_kg ┆ non_promo_price_per_kg ┆ promo_vol_share │
# │ ---  ┆ ---  ┆ ---          ┆ ---             ┆ ---                    ┆ ---             │
# │ u32  ┆ u32  ┆ u32          ┆ u32             ┆ u32                    ┆ u32             │
# ╞══════╪══════╪══════════════╪═════════════════╪════════════════════════╪═════════════════╡
# │ 156  ┆ 156  ┆ 156          ┆ 156             ┆ 156                    ┆ 156             │
# └──────┴──────┴──────────────┴─────────────────┴────────────────────────┴─────────────────┘

# Vertical version, showing only columns that have at least one missing value:
print(
    lf_mkt
    .select(pl.all().is_not_null().sum())
    .collect()
    .transpose(include_header=True, header_name='column', column_names=['n_not_null'])
    .pipe(lambda df: df.filter(c('n_not_null') < df.select(pl.len()).item()))
)
# shape: (5, 2)
# ┌──────────────┬────────────┐
# │ column       ┆ n_not_null │
# │ ---          ┆ ---        │
# │ str          ┆ u32        │
# ╞══════════════╪════════════╡
# │ grp_radio    ┆ 14         │
# │ reach_radio  ┆ 14         │
# │ reach_cinema ┆ 18         │
# │ grp_outdoor  ┆ 1          │
# │ grp_print    ┆ 22         │
# └──────────────┴────────────┘
'''
df.select(pl.len()).item()) is to get the n_rows.

So, if any column has n_not_null < n_rows,
this means that column has null value
-> filter them!!!
'''


# =========================================================================================
# 3. Drop missing values along columns
# =========================================================================================

##---------------------------------------------------##
## Drop columns where all values are null: how='all' ##
##---------------------------------------------------##
'''
Polars does not use axis=1 for dropping nulls.
To drop columns, first inspect each column's null count, then select the columns to keep.

how='all' equivalent:
Keep columns where null_count < number of rows.
'''

print(
    lf_mkt
    .pipe(lambda lf: lf.select([
        c(col)
        for col in lf.collect_schema().names()
        if lf.select(c(col).null_count()).collect().item() < lf.select(pl.len()).collect().item() # check ``null_count < number of rows``
    ]))
    #.select(pl.nth(range(0, 8)))
    .head()
    .collect()
)
# shape: (5, 26)
# ┌──────┬──────┬────────────┬────────────┬────────────┬───┬──────────┬────────────┬────────────┬───────────┬────────────┐
# │ week ┆ year ┆ market_sha ┆ av_price_p ┆ non_promo_ ┆ … ┆ reach_tv ┆ reach_cine ┆ grp_outdoo ┆ grp_print ┆ share_of_s │
# │ ---  ┆ ---  ┆ re         ┆ er_kg      ┆ price_per_ ┆   ┆ ---      ┆ ma         ┆ r          ┆ ---       ┆ pend       │
# │ cat  ┆ cat  ┆ ---        ┆ ---        ┆ kg         ┆   ┆ f64      ┆ ---        ┆ ---        ┆ f64       ┆ ---        │
# │      ┆      ┆ f64        ┆ f64        ┆ ---        ┆   ┆          ┆ f64        ┆ i64        ┆           ┆ f64        │
# │      ┆      ┆            ┆            ┆ f64        ┆   ┆          ┆            ┆            ┆           ┆            │
# ╞══════╪══════╪════════════╪════════════╪════════════╪═══╪══════════╪════════════╪════════════╪═══════════╪════════════╡
# │ 19   ┆ 2010 ┆ 38.400000  ┆ 7.610000   ┆ 7.770000   ┆ … ┆ null     ┆ null       ┆ null       ┆ null      ┆ null       │
# │ 20   ┆ 2010 ┆ 36.800000  ┆ 7.600000   ┆ 7.800000   ┆ … ┆ null     ┆ null       ┆ null       ┆ null      ┆ null       │
# │ 21   ┆ 2010 ┆ 35.210000  ┆ 7.630000   ┆ 7.850000   ┆ … ┆ null     ┆ null       ┆ null       ┆ null      ┆ null       │
# │ 22   ┆ 2010 ┆ 35.030000  ┆ 7.220000   ┆ 7.760000   ┆ … ┆ null     ┆ null       ┆ null       ┆ null      ┆ null       │
# │ 23   ┆ 2010 ┆ 32.370000  ┆ 7.700000   ┆ 7.780000   ┆ … ┆ null     ┆ null       ┆ null       ┆ null      ┆ null       │
# └──────┴──────┴────────────┴────────────┴────────────┴───┴──────────┴────────────┴────────────┴───────────┴────────────┘

##----------------------------------------------##
## Drop columns with any null values: how='any' ##
##----------------------------------------------##
'''
how='any' equivalent:
Keep columns where null_count == 0.
'''

print(
    lf_mkt
    .pipe(lambda lf: lf.select([
        c(col)
        for col in lf.collect_schema().names()
        if lf.select(c(col).null_count()).collect().item() == 0 # check if ``null_count == 0`` to keep
    ]))
    .head()
    .collect()
)
# shape: (5, 13)
# ┌──────┬──────┬────────────┬────────────┬────────────┬───┬────────────┬────────────┬───────────┬───────────┬───────────┐
# │ week ┆ year ┆ market_sha ┆ av_price_p ┆ non_promo_ ┆ … ┆ avg_price_ ┆ non_promo_ ┆ promo_vol ┆ total_cm_ ┆ shelf_sha │
# │ ---  ┆ ---  ┆ re         ┆ er_kg      ┆ price_per_ ┆   ┆ vs_plb     ┆ price_vs_p ┆ _sh_index ┆ shelf     ┆ re        │
# │ cat  ┆ cat  ┆ ---        ┆ ---        ┆ kg         ┆   ┆ ---        ┆ lb         ┆ _vs_plb   ┆ ---       ┆ ---       │
# │      ┆      ┆ f64        ┆ f64        ┆ ---        ┆   ┆ f64        ┆ ---        ┆ ---       ┆ f64       ┆ f64       │
# │      ┆      ┆            ┆            ┆ f64        ┆   ┆            ┆ f64        ┆ f64       ┆           ┆           │
# ╞══════╪══════╪════════════╪════════════╪════════════╪═══╪════════════╪════════════╪═══════════╪═══════════╪═══════════╡
# │ 19   ┆ 2010 ┆ 38.400000  ┆ 7.610000   ┆ 7.770000   ┆ … ┆ 2.010000   ┆ 2.200000   ┆ 2.020000  ┆ 754253.00 ┆ 0.250000  │
# │      ┆      ┆            ┆            ┆            ┆   ┆            ┆            ┆           ┆ 0000      ┆           │
# │ 20   ┆ 2010 ┆ 36.800000  ┆ 7.600000   ┆ 7.800000   ┆ … ┆ 2.000000   ┆ 2.190000   ┆ 1.590000  ┆ 752248.70 ┆ 0.250000  │
# │      ┆      ┆            ┆            ┆            ┆   ┆            ┆            ┆           ┆ 0000      ┆           │
# │ 21   ┆ 2010 ┆ 35.210000  ┆ 7.630000   ┆ 7.850000   ┆ … ┆ 2.070000   ┆ 2.230000   ┆ 1.030000  ┆ 750244.40 ┆ 0.250000  │
# │      ┆      ┆            ┆            ┆            ┆   ┆            ┆            ┆           ┆ 0000      ┆           │
# │ 22   ┆ 2010 ┆ 35.030000  ┆ 7.220000   ┆ 7.760000   ┆ … ┆ 1.900000   ┆ 2.120000   ┆ 1.040000  ┆ 748240.10 ┆ 0.250000  │
# │      ┆      ┆            ┆            ┆            ┆   ┆            ┆            ┆           ┆ 0000      ┆           │
# │ 23   ┆ 2010 ┆ 32.370000  ┆ 7.700000   ┆ 7.780000   ┆ … ┆ 2.180000   ┆ 2.150000   ┆ 0.660000  ┆ 746235.80 ┆ 0.250000  │
# │      ┆      ┆            ┆            ┆            ┆   ┆            ┆            ┆           ┆ 0000      ┆           │
# └──────┴──────┴────────────┴────────────┴────────────┴───┴────────────┴────────────┴───────────┴───────────┴───────────┘

##------------------------------------##
## Drop columns by non-null threshold ##
##------------------------------------##
'''
thresh equivalent:
Keep columns with at least 2/3 non-missing values.
'''

min_non_null = 2 / 3 * lf_mkt.select(pl.len()).collect().item()

print(
    lf_mkt
    .pipe(lambda lf: lf.select([
        c(col)
        for col in lf.collect_schema().names()
        if lf.select(c(col).is_not_null().sum()).collect().item() >= min_non_null
    ]))
    .head()
    .collect()
)
# shape: (5, 19)
# ┌──────┬──────┬─────────────┬─────────────┬────────────┬───┬────────────┬───────┬────────────┬────────────┬────────────┐
# │ week ┆ year ┆ market_shar ┆ av_price_pe ┆ non_promo_ ┆ … ┆ spontaneou ┆ aided ┆ penetratio ┆ competitor ┆ share_of_s │
# │ ---  ┆ ---  ┆ e           ┆ r_kg        ┆ price_per_ ┆   ┆ s          ┆ ---   ┆ n          ┆ ---        ┆ pend       │
# │ cat  ┆ cat  ┆ ---         ┆ ---         ┆ kg         ┆   ┆ ---        ┆ f64   ┆ ---        ┆ f64        ┆ ---        │
# │      ┆      ┆ f64         ┆ f64         ┆ ---        ┆   ┆ f64        ┆       ┆ f64        ┆            ┆ f64        │
# │      ┆      ┆             ┆             ┆ f64        ┆   ┆            ┆       ┆            ┆            ┆            │
# ╞══════╪══════╪═════════════╪═════════════╪════════════╪═══╪════════════╪═══════╪════════════╪════════════╪════════════╡
# │ 19   ┆ 2010 ┆ 38.400000   ┆ 7.610000    ┆ 7.770000   ┆ … ┆ null       ┆ null  ┆ null       ┆ null       ┆ null       │
# │ 20   ┆ 2010 ┆ 36.800000   ┆ 7.600000    ┆ 7.800000   ┆ … ┆ null       ┆ null  ┆ null       ┆ null       ┆ null       │
# │ 21   ┆ 2010 ┆ 35.210000   ┆ 7.630000    ┆ 7.850000   ┆ … ┆ null       ┆ null  ┆ null       ┆ null       ┆ null       │
# │ 22   ┆ 2010 ┆ 35.030000   ┆ 7.220000    ┆ 7.760000   ┆ … ┆ null       ┆ null  ┆ null       ┆ null       ┆ null       │
# │ 23   ┆ 2010 ┆ 32.370000   ┆ 7.700000    ┆ 7.780000   ┆ … ┆ null       ┆ null  ┆ null       ┆ null       ┆ null       │
# └──────┴──────┴─────────────┴─────────────┴────────────┴───┴────────────┴───────┴────────────┴────────────┴────────────┘


# =========================================================================================
# 4. Drop missing values along rows
# =========================================================================================

# Keep columns with at least 2/3 non-missing values, matching the previous section.
lf_mkt2 = (
    lf_mkt
    .pipe(lambda lf: lf.select([
        c(col)
        for col in lf.collect_schema().names()
        if lf.select(c(col).is_not_null().sum()).collect().item() >= min_non_null
    ]))
)

print(lf_mkt2.collect().shape)
# (156, 19)

print(
    lf_mkt2
    .null_count()
    .collect()
    .transpose(include_header=True, header_name='column', column_names=['n_null'])
    .filter(c('n_null') > 0)
)
# shape: (6, 2)
# ┌────────────────┬────────┐
# │ column         ┆ n_null │
# │ ---            ┆ ---    │
# │ str            ┆ u32    │
# ╞════════════════╪════════╡
# │ top_of_mind    ┆ 33     │
# │ spontaneous    ┆ 33     │
# │ aided          ┆ 33     │
# │ penetration    ┆ 33     │
# │ competitor     ┆ 45     │
# │ share_of_spend ┆ 40     │
# └────────────────┴────────┘

##-----------------------##
## Drop rows: how='any'  ##
##-----------------------##
'''Drop rows having at least one null value.'''

print(
    lf_mkt2
    .drop_nulls()
    .collect()
    .shape
)
# shape: (105, 19)

##----------------------##
## Drop rows: how='all' ##
##----------------------##
'''Drop rows where all values are null.'''

print(
    lf_mkt2
    .remove(pl.all_horizontal(pl.all().is_null()))
    #.filter(~pl.all_horizontal(pl.all().is_null()))
    .collect()
    .shape
)
# (156, 19)
# No rows are dropped because no rows are entirely null.

##-----------------------##
## Drop rows with subset ##
##-----------------------##
'''Drop rows with missing values in selected columns.'''

print(
    lf_mkt2
    .drop_nulls(subset=['top_of_mind', 'spontaneous'])
    .null_count()
    .collect()
    .transpose(include_header=True, header_name='column', column_names=['n_null'])
    .filter(c('n_null') > 0)
)
# shape: (2, 2)
# ┌────────────────┬────────┐
# │ column         ┆ n_null │
# │ ---            ┆ ---    │
# │ str            ┆ u32    │
# ╞════════════════╪════════╡
# │ competitor     ┆ 12     │
# │ share_of_spend ┆ 7      │
# └────────────────┴────────┘

print(
    lf_mkt2
    .drop_nulls(subset=['top_of_mind', 'spontaneous'])
    .collect()
    .shape
)
# (123, 19)


# =========================================================================================
# 5. Fill missing values
# =========================================================================================

# Drop categorical columns before numeric filling.
lf_missing = lf_mkt.drop(['week', 'year'])

##----------------##
## df.fill_null() ##
##----------------##
'''Fill every null value with the same scalar value.'''

print(
    lf_missing
    .fill_null(0)
    .head()
    .collect()
)
# shape: (5, 24)
# ┌───────────┬───────────┬───────────┬───────────┬───────────┬───┬──────────┬──────────┬──────────┬──────────┬──────────┐
# │ market_sh ┆ av_price_ ┆ non_promo ┆ promo_vol ┆ total_wei ┆ … ┆ reach_tv ┆ reach_ci ┆ grp_outd ┆ grp_prin ┆ share_of │
# │ are       ┆ per_kg    ┆ _price_pe ┆ _share    ┆ gh        ┆   ┆ ---      ┆ nema     ┆ oor      ┆ t        ┆ _spend   │
# │ ---       ┆ ---       ┆ r_kg      ┆ ---       ┆ ---       ┆   ┆ f64      ┆ ---      ┆ ---      ┆ ---      ┆ ---      │
# │ f64       ┆ f64       ┆ ---       ┆ f64       ┆ i64       ┆   ┆          ┆ f64      ┆ i64      ┆ f64      ┆ f64      │
# │           ┆           ┆ f64       ┆           ┆           ┆   ┆          ┆          ┆          ┆          ┆          │
# ╞═══════════╪═══════════╪═══════════╪═══════════╪═══════════╪═══╪══════════╪══════════╪══════════╪══════════╪══════════╡
# │ 38.400000 ┆ 7.610000  ┆ 7.770000  ┆ 26.870000 ┆ 84        ┆ … ┆ 0.000000 ┆ 0.000000 ┆ 0        ┆ 0.000000 ┆ 0.000000 │
# │ 36.800000 ┆ 7.600000  ┆ 7.800000  ┆ 29.420000 ┆ 84        ┆ … ┆ 0.000000 ┆ 0.000000 ┆ 0        ┆ 0.000000 ┆ 0.000000 │
# │ 35.210000 ┆ 7.630000  ┆ 7.850000  ┆ 27.270000 ┆ 82        ┆ … ┆ 0.000000 ┆ 0.000000 ┆ 0        ┆ 0.000000 ┆ 0.000000 │
# │ 35.030000 ┆ 7.220000  ┆ 7.760000  ┆ 52.480000 ┆ 88        ┆ … ┆ 0.000000 ┆ 0.000000 ┆ 0        ┆ 0.000000 ┆ 0.000000 │
# │ 32.370000 ┆ 7.700000  ┆ 7.780000  ┆ 16.110000 ┆ 82        ┆ … ┆ 0.000000 ┆ 0.000000 ┆ 0        ┆ 0.000000 ┆ 0.000000 │
# └───────────┴───────────┴───────────┴───────────┴───────────┴───┴──────────┴──────────┴──────────┴──────────┴──────────┘

##----------------------------------------------##
## Fill different columns with different values ##
##----------------------------------------------##
'''Use with_columns() and fill_null() to fill selected columns differently.'''

print(
    lf_missing
    .with_columns(
        c('top_of_mind').fill_null(c('top_of_mind').mean()),
        c('spontaneous').fill_null(c('spontaneous').median()),
        c('aided').fill_null(c('aided').min()),
        c('penetration').fill_null(c('penetration').max()),
    )
    .select('top_of_mind', 'spontaneous', 'aided', 'penetration')
    .collect()
)
# shape: (156, 4)
# ┌─────────────┬─────────────┬───────────┬─────────────┐
# │ top_of_mind ┆ spontaneous ┆ aided     ┆ penetration │
# │ ---         ┆ ---         ┆ ---       ┆ ---         │
# │ f64         ┆ f64         ┆ f64       ┆ f64         │
# ╞═════════════╪═════════════╪═══════════╪═════════════╡
# │ 50.465041   ┆ 78.200000   ┆ 95.700000 ┆ 76.800000   │
# │ 50.465041   ┆ 78.200000   ┆ 95.700000 ┆ 76.800000   │
# │ 50.465041   ┆ 78.200000   ┆ 95.700000 ┆ 76.800000   │
# │ 50.465041   ┆ 78.200000   ┆ 95.700000 ┆ 76.800000   │
# │ 50.465041   ┆ 78.200000   ┆ 95.700000 ┆ 76.800000   │
# │ …           ┆ …           ┆ …         ┆ …           │
# │ 50.200000   ┆ 83.700000   ┆ 99.500000 ┆ 71.600000   │
# │ 50.200000   ┆ 83.700000   ┆ 99.500000 ┆ 71.600000   │
# │ 50.200000   ┆ 83.700000   ┆ 99.500000 ┆ 71.600000   │
# │ 50.200000   ┆ 83.700000   ┆ 99.500000 ┆ 71.600000   │
# │ 50.200000   ┆ 83.700000   ┆ 99.500000 ┆ 71.600000   │
# └─────────────┴─────────────┴───────────┴─────────────┘

##--------------------------------------##
## Fill numeric nulls with column means ##
##--------------------------------------##
'''Fill missing values in every numeric column with that column's mean.'''

print(
    lf_missing
    .with_columns(
        cs.numeric().fill_null(cs.numeric().mean())
    )
    .head()
    .collect()
)
# shape: (5, 24)
# ┌───────────┬───────────┬───────────┬───────────┬───────────┬───┬──────────┬──────────┬──────────┬──────────┬──────────┐
# │ market_sh ┆ av_price_ ┆ non_promo ┆ promo_vol ┆ total_wei ┆ … ┆ reach_tv ┆ reach_ci ┆ grp_outd ┆ grp_prin ┆ share_of │
# │ are       ┆ per_kg    ┆ _price_pe ┆ _share    ┆ gh        ┆   ┆ ---      ┆ nema     ┆ oor      ┆ t        ┆ _spend   │
# │ ---       ┆ ---       ┆ r_kg      ┆ ---       ┆ ---       ┆   ┆ f64      ┆ ---      ┆ ---      ┆ ---      ┆ ---      │
# │ f64       ┆ f64       ┆ ---       ┆ f64       ┆ f64       ┆   ┆          ┆ f64      ┆ f64      ┆ f64      ┆ f64      │
# │           ┆           ┆ f64       ┆           ┆           ┆   ┆          ┆          ┆          ┆          ┆          │
# ╞═══════════╪═══════════╪═══════════╪═══════════╪═══════════╪═══╪══════════╪══════════╪══════════╪══════════╪══════════╡
# │ 38.400000 ┆ 7.610000  ┆ 7.770000  ┆ 26.870000 ┆ 84.000000 ┆ … ┆ 38.15188 ┆ 6.800000 ┆ 1127.000 ┆ 14.90454 ┆ 45.31402 │
# │           ┆           ┆           ┆           ┆           ┆   ┆ 5        ┆          ┆ 000      ┆ 5        ┆ 7        │
# │ 36.800000 ┆ 7.600000  ┆ 7.800000  ┆ 29.420000 ┆ 84.000000 ┆ … ┆ 38.15188 ┆ 6.800000 ┆ 1127.000 ┆ 14.90454 ┆ 45.31402 │
# │           ┆           ┆           ┆           ┆           ┆   ┆ 5        ┆          ┆ 000      ┆ 5        ┆ 7        │
# │ 35.210000 ┆ 7.630000  ┆ 7.850000  ┆ 27.270000 ┆ 82.000000 ┆ … ┆ 38.15188 ┆ 6.800000 ┆ 1127.000 ┆ 14.90454 ┆ 45.31402 │
# │           ┆           ┆           ┆           ┆           ┆   ┆ 5        ┆          ┆ 000      ┆ 5        ┆ 7        │
# │ 35.030000 ┆ 7.220000  ┆ 7.760000  ┆ 52.480000 ┆ 88.000000 ┆ … ┆ 38.15188 ┆ 6.800000 ┆ 1127.000 ┆ 14.90454 ┆ 45.31402 │
# │           ┆           ┆           ┆           ┆           ┆   ┆ 5        ┆          ┆ 000      ┆ 5        ┆ 7        │
# │ 32.370000 ┆ 7.700000  ┆ 7.780000  ┆ 16.110000 ┆ 82.000000 ┆ … ┆ 38.15188 ┆ 6.800000 ┆ 1127.000 ┆ 14.90454 ┆ 45.31402 │
# │           ┆           ┆           ┆           ┆           ┆   ┆ 5        ┆          ┆ 000      ┆ 5        ┆ 7        │
# └───────────┴───────────┴───────────┴───────────┴───────────┴───┴──────────┴──────────┴──────────┴──────────┴──────────┘

##--------------##
## Forward fill ##
##--------------##

s_missing = pl.Series('x', [1, None, None, 4, 5, None, 7])

print(s_missing.fill_null(strategy='forward'))
# [1, 1, 1, 4, 5, 5, 7]

##---------------##
## Backward fill ##
##---------------##

print(s_missing.fill_null(strategy='backward'))
# [1, 4, 4, 4, 5, 7, 7]


# =========================================================================================
# 6. Interpolate missing values
# =========================================================================================

# Drop categorical columns before interpolation.
lf_missing = lf_mkt.drop(['week', 'year'])

print(
    lf_missing
    .null_count()
    .collect()
    .transpose(include_header=True, header_name='column', column_names=['n_null'])
    .filter(c('n_null') > 0)
)
# shape: (13, 2)
# ┌────────────────┬────────┐
# │ column         ┆ n_null │
# │ ---            ┆ ---    │
# │ str            ┆ u32    │
# ╞════════════════╪════════╡
# │ top_of_mind    ┆ 33     │
# │ spontaneous    ┆ 33     │
# │ aided          ┆ 33     │
# │ penetration    ┆ 33     │
# │ competitor     ┆ 45     │
# │ …              ┆ …      │
# │ reach_tv       ┆ 104    │
# │ reach_cinema   ┆ 138    │
# │ grp_outdoor    ┆ 155    │
# │ grp_print      ┆ 134    │
# │ share_of_spend ┆ 40     │
# └────────────────┴────────┘

##-----------------------------##
## Native linear interpolation ##
##-----------------------------##
'''
Polars supports native linear interpolation with .interpolate().
Unlike pandas limit_direction='both', interpolation may not fill every boundary null.
Add backward/forward fill if you want to fill boundary nulls too.
'''

lf_interpolated_linear = (
    lf_missing
    .with_columns(
        cs.numeric()
        .interpolate() # native linear interpolation
        .fill_null(strategy='backward') # fill boundary nulls
        .fill_null(strategy='forward') # fill boundary nulls
    )
)

print(
    lf_interpolated_linear
    .null_count()
    .collect()
    .transpose(include_header=True, header_name='column', column_names=['n_null'])
    .filter(c('n_null') > 0)
)
# All missing values are filled unless a column has no non-null value at all.

##---------------------------------------##
## Native nearest-neighbor interpolation ##
##---------------------------------------##
'''
Polars also supports nearest-neighbor interpolation.
Boundary nulls can again be handled by adding backward/forward fill.
'''

lf_interpolated_nearest = (
    lf_missing
    .with_columns(
        cs.numeric()
        .interpolate(method='nearest') # fill with nearest
        .fill_null(strategy='backward')
        .fill_null(strategy='forward')
    )
)

print(
    lf_interpolated_nearest
    .null_count()
    .collect()
    .transpose(include_header=True, header_name='column', column_names=['n_null'])
    .filter(c('n_null') > 0)
)

##----------------------------------------------------##
## Polynomial / spline interpolation: Python fallback ##
##----------------------------------------------------##
'''
Polars does NOT provide native polynomial or spline interpolation methods.
If you need those methods, collect the relevant numeric columns and use SciPy.
This keeps the fallback explicit instead of pretending it is a native Polars expression.
'''

# Example: quadratic interpolation for one column with SciPy.
# This pattern can be repeated for other columns when needed.
print(
    lf_missing
    .select("share_of_spend")
    .with_row_index("row_id")
    .pipe(
        lambda lf: (
            lambda df: pl.DataFrame({
                "row_id": df["row_id"],
                "share_of_spend_poly2": (
                    lambda x, y: interpolate.interp1d(
                        x=x[y.is_not_null().to_numpy()],
                        y=y.drop_nulls().to_numpy(),
                        kind="quadratic",
                        bounds_error=False,
                        fill_value="extrapolate",
                    )(x)
                )(
                    df["row_id"].to_numpy(),
                    df["share_of_spend"],
                ),
            })
        )(lf.collect())
    )
    .head()
)
# shape: (5, 2)
# ┌────────┬──────────────────────┐
# │ row_id ┆ share_of_spend_poly2 │
# │ ---    ┆ ---                  │
# │ u32    ┆ f64                  │
# ╞════════╪══════════════════════╡
# │ 0      ┆ -15450.444954        │
# │ 1      ┆ -14582.662697        │
# │ 2      ┆ -13739.791254        │
# │ 3      ┆ -12921.830624        │
# │ 4      ┆ -12128.780807        │
# └────────┴──────────────────────┘


# =========================================================================================
# 7. Conditional filling
# =========================================================================================

# Drop categorical columns before numeric conditional filling.
lf_missing = lf_mkt.drop(['week', 'year'])

##------------------------------------------##
## Fill every numeric null with column mean ##
##------------------------------------------##
'''
Equivalent idea to np.where(df.isna(), df.mean(), df), but written as Polars expressions.
'''

lf_filled = (
    lf_missing
    .with_columns(
        pl.when(cs.numeric().is_null())
        .then(cs.numeric().mean())
        .otherwise(cs.numeric())
    )
)

print(lf_filled.null_count().collect())
# All missing values are filled.

##-----------------------------------------##
## Conditional filling using other columns ##
##-----------------------------------------##
'''
Example pattern:
If column C is null, fill it with A + B; otherwise keep C.
Here we demonstrate the pattern using share_of_spend as the target column.
'''

print(
    lf_mkt
    .with_columns(
        pl.when(c('share_of_spend').is_null())
        .then(c('grp_tv').fill_null(0) + c('grp_radio').fill_null(0))
        .otherwise(c('share_of_spend'))
        .alias('share_of_spend_filled_conditionally')
    )
    .select('share_of_spend', 'grp_tv', 'grp_radio', 'share_of_spend_filled_conditionally')
    .head(10)
    .collect()
)
# shape: (10, 4)
# ┌────────────────┬────────┬───────────┬─────────────────────────────────┐
# │ share_of_spend ┆ grp_tv ┆ grp_radio ┆ share_of_spend_filled_conditio… │
# │ ---            ┆ ---    ┆ ---       ┆ ---                             │
# │ f64            ┆ f64    ┆ f64       ┆ f64                             │
# ╞════════════════╪════════╪═══════════╪═════════════════════════════════╡
# │ null           ┆ null   ┆ null      ┆ 0.000000                        │
# │ null           ┆ null   ┆ null      ┆ 0.000000                        │
# │ null           ┆ null   ┆ null      ┆ 0.000000                        │
# │ null           ┆ null   ┆ null      ┆ 0.000000                        │
# │ null           ┆ null   ┆ null      ┆ 0.000000                        │
# │ null           ┆ null   ┆ null      ┆ 0.000000                        │
# │ null           ┆ null   ┆ null      ┆ 0.000000                        │
# │ null           ┆ null   ┆ null      ┆ 0.000000                        │
# │ null           ┆ null   ┆ null      ┆ 0.000000                        │
# │ null           ┆ null   ┆ null      ┆ 0.000000                        │
# └────────────────┴────────┴───────────┴─────────────────────────────────┘



# =========================================================================================
# 8. Group-based filling, transform
# =========================================================================================

# Keep week as the grouping key, drop only year.
lf_missing = lf_mkt.drop('year')

print(
    lf_missing
    .null_count()
    .collect()
    .transpose(include_header=True, header_name='column', column_names=['n_null'])
    .filter(c('n_null') > 0)
)
# shape: (13, 2)
# ┌────────────────┬────────┐
# │ column         ┆ n_null │
# │ ---            ┆ ---    │
# │ str            ┆ u32    │
# ╞════════════════╪════════╡
# │ top_of_mind    ┆ 33     │
# │ spontaneous    ┆ 33     │
# │ aided          ┆ 33     │
# │ penetration    ┆ 33     │
# │ competitor     ┆ 45     │
# │ …              ┆ …      │
# │ reach_tv       ┆ 104    │
# │ reach_cinema   ┆ 138    │
# │ grp_outdoor    ┆ 155    │
# │ grp_print      ┆ 134    │
# │ share_of_spend ┆ 40     │
# └────────────────┴────────┘

##---------------------------------------------##
## Fill nulls with the mean of each week group ##
##---------------------------------------------##
'''
Pandas idea:
df_missing.fillna(df_missing.groupby('week').transform('mean'))

Polars equivalent:
Use a window expression with .over('week').
Each row receives the mean of its own week group for that column.
'''

numeric_cols = lf_missing.select(cs.numeric()).collect_schema().names()

lf_group_filled = (
    lf_missing
    .with_columns([
        c(col).fill_null(c(col).mean().over('week')).alias(col)
        for col in numeric_cols
    ])
)

print(
    lf_group_filled
    .null_count()
    .collect()
    .transpose(include_header=True, header_name='column', column_names=['n_null'])
    .filter(c('n_null') > 0)
)
# shape: (7, 2)
# ┌──────────────┬────────┐
# │ column       ┆ n_null │
# │ ---          ┆ ---    │
# │ str          ┆ u32    │
# ╞══════════════╪════════╡
# │ grp_radio    ┆ 114    │
# │ reach_radio  ┆ 114    │
# │ grp_tv       ┆ 27     │
# │ reach_tv     ┆ 27     │
# │ reach_cinema ┆ 102    │
# │ grp_outdoor  ┆ 153    │
# │ grp_print    ┆ 96     │
# └──────────────┴────────┘

print(lf_group_filled.head().collect())
# shape: (5, 25)
# ┌──────┬───────────┬───────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬───────────┬───────────┐
# │ week ┆ market_sh ┆ av_price_ ┆ non_promo ┆ promo_vol ┆ … ┆ reach_tv  ┆ reach_cin ┆ grp_outdo ┆ grp_print ┆ share_of_ │
# │ ---  ┆ are       ┆ per_kg    ┆ _price_pe ┆ _share    ┆   ┆ ---       ┆ ema       ┆ or        ┆ ---       ┆ spend     │
# │ cat  ┆ ---       ┆ ---       ┆ r_kg      ┆ ---       ┆   ┆ f64       ┆ ---       ┆ ---       ┆ f64       ┆ ---       │
# │      ┆ f64       ┆ f64       ┆ ---       ┆ f64       ┆   ┆           ┆ f64       ┆ f64       ┆           ┆ f64       │
# │      ┆           ┆           ┆ f64       ┆           ┆   ┆           ┆           ┆           ┆           ┆           │
# ╞══════╪═══════════╪═══════════╪═══════════╪═══════════╪═══╪═══════════╪═══════════╪═══════════╪═══════════╪═══════════╡
# │ 19   ┆ 38.400000 ┆ 7.610000  ┆ 7.770000  ┆ 26.870000 ┆ … ┆ null      ┆ null      ┆ null      ┆ null      ┆ 0.155019  │
# │ 20   ┆ 36.800000 ┆ 7.600000  ┆ 7.800000  ┆ 29.420000 ┆ … ┆ null      ┆ null      ┆ null      ┆ null      ┆ 0.000000  │
# │ 21   ┆ 35.210000 ┆ 7.630000  ┆ 7.850000  ┆ 27.270000 ┆ … ┆ 0.602000  ┆ null      ┆ null      ┆ null      ┆ 0.177186  │
# │ 22   ┆ 35.030000 ┆ 7.220000  ┆ 7.760000  ┆ 52.480000 ┆ … ┆ 20.382000 ┆ null      ┆ null      ┆ null      ┆ 34.323685 │
# │ 23   ┆ 32.370000 ┆ 7.700000  ┆ 7.780000  ┆ 16.110000 ┆ … ┆ 40.245000 ┆ null      ┆ null      ┆ null      ┆ 50.000000 │
# └──────┴───────────┴───────────┴───────────┴───────────┴───┴───────────┴───────────┴───────────┴───────────┴───────────┘


'''
Some missing values may remain because certain week groups have all-null values
for particular columns, so the group mean is also null.
'''
