'''
Polars plotting examples.

Polars does not copy the pandas DataFrame.plot API exactly.
The current built-in plotting namespace is:

    df.plot

Important ideas:
+ Plotting is available on eager DataFrame objects, not LazyFrame objects.
+ Use LazyFrame to prepare/filter/aggregate data, then `.collect()` before plotting.
+ Polars' built-in `df.plot` delegates to Altair.
+ `df.plot.scatter(...)` is an alias of `df.plot.point(...)`.
+ `df.plot.line(...)` and `df.plot.bar(...)` are built-in shortcuts.
+ Other Altair mark names can be called through `df.plot.<mark_name>(...)`, such as
  `df.plot.area(...)`, `df.plot.arc(...)`, `df.plot.boxplot(...)`, and `df.plot.rect(...)`.
+ For more pandas-like plotting methods such as `.hist()`, `.kde()`, `.barh()`, `.hexbin()`,
  use the optional `hvplot.polars` accessor if hvPlot is installed.

This file intentionally skips pandas-only plotting helpers that Polars does not provide directly,
such as scatter_matrix, andrews_curves, parallel_coordinates, radviz, bootstrap_plot,
pd.plotting.table, and matplotlib converter registration.

########################################
1. Setup Data
2. Built-in Polars plotting with df.plot
   + Histogram-like plot using binned bar chart
   + Box plot
   + Pie-like chart using arc mark
   + Bar plot
   + Horizontal bar plot
   + Scatter / point plot
   + Line plot
   + Area plot
   + 2D binned heatmap, similar purpose to hexbin
3. Optional hvPlot accessor for more pandas-like methods
4. Advanced supported patterns built from Polars transformations
   + Correlation heatmap
   + Lag plot
   + Autocorrelation bar plot
'''

from pathlib import Path

import altair as alt
import polars as pl
from polars import col as c
from polars import selectors as cs

# Optional display settings
pl.Config.set_tbl_rows(10)
pl.Config.set_tbl_cols(12)
pl.Config.set_tbl_width_chars(120)
pl.Config.set_float_precision(4)

# Altair can display large transformed data in notebooks if you disable the default row limit.
# This is useful for tutorial examples, but you can remove it if you prefer Altair's default limit.
alt.data_transformers.disable_max_rows()

# Optional hvPlot support. The script still works without hvPlot; the hvPlot section is skipped.
try:
    import hvplot.polars  # noqa: F401
    import hvplot
    HAS_HVPLOT = True
except ImportError:
    HAS_HVPLOT = False

alt.renderers.enable("browser") # open plot in browser

data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))


#----------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 1. Setup Data ----------------------------------------------#
#----------------------------------------------------------------------------------------------------------#

###########################
## Pokemon dataset       ##
###########################

lf_pokemon = (
    pl.scan_csv(data_dir / "pokemon.csv")
    .drop("#")
    .rename(lambda name: name.strip())
    .select(pl.all().name.replace(r"\s+", "_").name.replace(".", "", literal=True))
    .with_columns(
        c("Type_1", "Type_2").cast(pl.Categorical),
        c("Legendary").cast(pl.Boolean),
    )
    .pipe(lambda f: f.with_columns(
        c("Generation").cast(pl.String).cast(pl.Enum(f.collect()["Generation"].cast(pl.String).unique().sort())),
    ))
)

df_pokemon = lf_pokemon.collect()

print(df_pokemon.glimpse())
# Rows: 800
# Columns: 12
# $ Name        <str> 'Bulbasaur', 'Ivysaur', 'Venusaur', 'VenusaurMega Venusaur', 'Charmander', 'Charmeleon', 'Charizard', 'CharizardMega Charizard X', 'CharizardMega Charizard Y', 'Squirtle'
# $ Type_1      <cat> Grass, Grass, Grass, Grass, Fire, Fire, Fire, Fire, Fire, Water
# $ Type_2      <cat> Poison, Poison, Poison, Poison, null, null, Flying, Dragon, Flying, null
# $ Total       <i64> 318, 405, 525, 625, 309, 405, 534, 634, 634, 314
# $ HP          <i64> 45, 60, 80, 80, 39, 58, 78, 78, 78, 44
# $ Attack      <i64> 49, 62, 82, 100, 52, 64, 84, 130, 104, 48
# $ Defense     <i64> 49, 63, 83, 123, 43, 58, 78, 111, 78, 65
# $ Sp_Atk      <i64> 65, 80, 100, 122, 60, 80, 109, 130, 159, 50
# $ Sp_Def      <i64> 65, 80, 100, 120, 50, 65, 85, 85, 115, 64
# $ Speed       <i64> 45, 60, 80, 80, 65, 80, 100, 100, 100, 43
# $ Generation <enum> 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
# $ Legendary  <bool> False, False, False, False, False, False, False, False, False, False

#########################
## Air quality dataset ##
#########################

lf_aq = (
    pl.scan_csv(data_dir / "air_quality_no2_long.csv")
    .rename({"date.utc": "date"})
    .with_columns(
        c("city", "country", "location", "parameter", "unit").cast(pl.Categorical),
        c("date").str.strptime(
            dtype=pl.Datetime(time_zone="UTC"),
            format="%Y-%m-%d %H:%M:%S%z",
            strict=False,
        )
    )
)

df_aq = lf_aq.collect()

print(df_aq.head())
# shape: (5, 7)
# ┌───────┬─────────┬─────────────────────────┬──────────┬───────────┬─────────┬───────┐
# │ city  ┆ country ┆ date                    ┆ location ┆ parameter ┆ value   ┆ unit  │
# │ ---   ┆ ---     ┆ ---                     ┆ ---      ┆ ---       ┆ ---     ┆ ---   │
# │ cat   ┆ cat     ┆ datetime[μs, UTC]       ┆ cat      ┆ cat       ┆ f64     ┆ cat   │
# ╞═══════╪═════════╪═════════════════════════╪══════════╪═══════════╪═════════╪═══════╡
# │ Paris ┆ FR      ┆ 2019-06-21 00:00:00 UTC ┆ FR04014  ┆ no2       ┆ 20.0000 ┆ µg/m³ │
# │ Paris ┆ FR      ┆ 2019-06-20 23:00:00 UTC ┆ FR04014  ┆ no2       ┆ 21.8000 ┆ µg/m³ │
# │ Paris ┆ FR      ┆ 2019-06-20 22:00:00 UTC ┆ FR04014  ┆ no2       ┆ 26.5000 ┆ µg/m³ │
# │ Paris ┆ FR      ┆ 2019-06-20 21:00:00 UTC ┆ FR04014  ┆ no2       ┆ 24.9000 ┆ µg/m³ │
# │ Paris ┆ FR      ┆ 2019-06-20 20:00:00 UTC ┆ FR04014  ┆ no2       ┆ 21.4000 ┆ µg/m³ │
# └───────┴─────────┴─────────────────────────┴──────────┴───────────┴─────────┴───────┘


#----------------------------------------------------------------------------------------------------------#
#------------------------------ 2. Built-in Polars plotting with df.plot ----------------------------------#
#----------------------------------------------------------------------------------------------------------#
'''
Polars built-in plotting is eager:

    lf_query.collect().plot.<mark>(...)

The heavy data work can still be lazy. Collect only the prepared plotting data.
'''

#----------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 2.1 Histogram ----------------------------------------------#
#----------------------------------------------------------------------------------------------------------#
'''
Polars does not have a pandas-style `df.plot.hist()` method in the built-in Altair backend.
Use a binned bar chart instead.
'''

#----------
## Histogram-like plot of Attack
#----------

chart_hist_attack = (
    df_pokemon
    .plot
    .bar(
        x=alt.X("Attack:Q", bin=alt.Bin(maxbins=30), title="Attack"),
        y=alt.Y("count():Q", title="Count"),
    )
    .properties(width=650, height=350, title="Histogram-like Binned Bar Chart of Pokemon Attack")
)
chart_hist_attack.show()

#----------
## Histogram-like plot of Attack and Defense
#----------

# Convert wide columns to long format before plotting multiple variables.
df_attack_defense_long = (
    df_pokemon
    .select("Attack", "Defense")
    .unpivot(variable_name="stat", value_name="value")
)

chart_hist_attack_defense = (
    df_attack_defense_long
    .plot
    .bar(
        x=alt.X("value:Q", bin=alt.Bin(maxbins=30), title="Value"),
        y=alt.Y("count():Q", title="Count"),
        color="stat:N",
    )
    .properties(width=650, height=350, title="Histogram-like Plot of Attack and Defense")
)
chart_hist_attack_defense.show()


#----------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 2.2 Box plot ----------------------------------------------#
#----------------------------------------------------------------------------------------------------------#
'''
Altair has a boxplot mark, so Polars can call it through `df.plot.boxplot(...)`.
'''

#----------
## Box plot of Attack
#----------

chart_box_attack = (
    df_pokemon
    .plot
    .boxplot(y=alt.Y("Attack:Q", title="Attack"))
    .properties(width=350, height=350, title="Box Plot of Pokemon Attack")
)
chart_box_attack.show()

#----------
## Box plot of Attack by Generation
#----------

chart_box_generation = (
    df_pokemon
    .plot
    .boxplot(
        x=alt.X("Generation:N", title="Generation"),
        y=alt.Y("Attack:Q", title="Attack"),
    )
    .properties(width=650, height=350, title="Box Plot of Pokemon Attack by Generation")
)
chart_box_generation.show()


#----------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 2.3 Pie / Arc chart -----------------------------------------#
#----------------------------------------------------------------------------------------------------------#
'''
Polars does not have a dedicated `.plot.pie()` method.
Use Altair's arc mark through `df.plot.arc(...)`.
'''

df_generation_counts = (
    lf_pokemon
    .group_by("Generation")
    .agg(pl.len().alias("count"))
    .sort("Generation")
    .collect()
)

chart_pie_generation = (
    df_generation_counts
    .plot
    .arc(
        theta=alt.Theta("count:Q", title="Count"),
        color=alt.Color("Generation:N", title="Generation"),
    )
    .properties(width=450, height=450, title="Distribution of Pokemon Generation")
)
chart_pie_generation.show()


#----------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 2.4 Bar plot ----------------------------------------------#
#----------------------------------------------------------------------------------------------------------#

#----------
## Bar plot of Generation counts
#----------

chart_bar_generation = (
    df_generation_counts
    .plot
    .bar(
        x=alt.X("Generation:N", title="Generation"),
        y=alt.Y("count:Q", title="Count"),
    )
    .properties(width=650, height=350, title="Bar Plot of Pokemon Generation")
)
chart_bar_generation.show()

#----------
## Dodged bar plot of Generation and Legendary
#----------

df_gen_legend_counts = (
    lf_pokemon
    .group_by("Generation", "Legendary")
    .agg(pl.len().alias("count"))
    .sort("Generation", "Legendary")
    .collect()
)

chart_bar_dodged = (
    df_gen_legend_counts
    .plot
    .bar(
        x=alt.X("Generation:N", title="Generation"),
        xOffset=alt.XOffset("Legendary:N"),
        y=alt.Y("count:Q", title="Count"),
        color=alt.Color("Legendary:N", title="Legendary"),
    )
    .properties(width=650, height=350, title="Dodged Bar Plot of Generation and Legendary Status")
)
chart_bar_dodged.show()

#----------
## Stacked bar plot of Generation and Legendary
#----------

chart_bar_stacked = (
    df_gen_legend_counts
    .plot
    .bar(
        x=alt.X("Generation:N", title="Generation"),
        y=alt.Y("count:Q", title="Count"),
        color=alt.Color("Legendary:N", title="Legendary"),
    )
    .properties(width=650, height=350, title="Stacked Bar Plot of Generation and Legendary Status")
)
chart_bar_stacked.show()


#----------------------------------------------------------------------------------------------------------#
#---------------------------------------- 2.5 Horizontal Bar plot -----------------------------------------#
#----------------------------------------------------------------------------------------------------------#
'''
There is no separate `.plot.barh()` in built-in Polars plotting.
Use `.plot.bar(...)` and swap x/y encodings.
'''

chart_barh_generation = (
    df_generation_counts
    .plot
    .bar(
        x=alt.X("count:Q", title="Count"),
        y=alt.Y("Generation:N", title="Generation"),
    )
    .properties(width=650, height=350, title="Horizontal Bar Plot of Pokemon Generation")
)
chart_barh_generation.show()

chart_barh_stacked = (
    df_gen_legend_counts
    .plot
    .bar(
        x=alt.X("count:Q", title="Count"),
        y=alt.Y("Generation:N", title="Generation"),
        color=alt.Color("Legendary:N", title="Legendary"),
    )
    .properties(width=650, height=350, title="Stacked Horizontal Bar Plot of Generation and Legendary Status")
)
chart_barh_stacked.show()


#----------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 2.6 Scatter plot -------------------------------------------#
#----------------------------------------------------------------------------------------------------------#
'''
`df.plot.scatter(...)` is an alias for `df.plot.point(...)`.
'''

chart_scatter_attack_defense = (
    df_pokemon
    .plot
    .scatter(
        x=alt.X("Attack:Q", title="Attack"),
        y=alt.Y("Defense:Q", title="Defense"),
        color=alt.Color("Type_1:N", title="Type 1"),
    )
    .properties(width=650, height=400, title="Scatter Plot of Pokemon Attack vs Defense")
    .configure_point(opacity=0.65)
)
chart_scatter_attack_defense.show()

# Same result using `.point(...)` directly.
chart_point_attack_defense = (
    df_pokemon
    .plot
    .point(x="Attack", y="Defense", color="Legendary")
    .properties(width=650, height=400, title="Point Plot of Attack vs Defense by Legendary Status")
)
chart_point_attack_defense.show()


#----------------------------------------------------------------------------------------------------------#
#----------------------------- 2.7 2D binned heatmap, similar purpose to hexbin ---------------------------#
#----------------------------------------------------------------------------------------------------------#
'''
The built-in Altair backend does not expose a true hexbin mark.
A common alternative is a 2D binned heatmap using rectangular bins.
'''

chart_2d_binned = (
    df_pokemon
    .plot
    .rect(
        x=alt.X("Attack:Q", bin=alt.Bin(maxbins=30), title="Attack"),
        y=alt.Y("Defense:Q", bin=alt.Bin(maxbins=30), title="Defense"),
        color=alt.Color("count():Q", title="Count"),
    )
    .properties(width=650, height=400, title="2D Binned Heatmap of Attack vs Defense")
)
chart_2d_binned.show()


#----------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 2.8 Line plot ---------------------------------------------#
#----------------------------------------------------------------------------------------------------------#

#----------
## Line plot for Paris
#----------

df_aq_paris = (
    lf_aq
    .filter(c("city") == "Paris")
    .sort("date")
    .collect()
)

chart_line_paris = (
    df_aq_paris
    .plot
    .line(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("value:Q", title="NO2 Level (µg/m³)"),
    )
    .properties(width=750, height=350, title="Line Plot of NO2 Levels in Paris Over Time")
)
chart_line_paris.show()

#----------
## Line plot for all cities
#----------

df_aq_sorted = lf_aq.sort("date").collect()

chart_line_cities = (
    df_aq_sorted
    .plot
    .line(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("value:Q", title="NO2 Level (µg/m³)"),
        color=alt.Color("city:N", title="City"),
    )
    .properties(width=750, height=350, title="Line Plot of NO2 Levels by City")
)
chart_line_cities.show()


#----------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 2.9 Area plot ---------------------------------------------#
#----------------------------------------------------------------------------------------------------------#
'''
Use Altair's area mark through `df.plot.area(...)`.
For multiple series, convert wide data to long format first.
'''

df_business = pl.DataFrame({
    "date": pl.date_range(
        start=pl.date(2018, 1, 31),
        end=pl.date(2018, 6, 30),
        interval="1mo",
        eager=True,
    ),
    "sales": [3, 2, 3, 9, 10, 6],
    "signups": [5, 5, 6, 12, 14, 13],
    "visits": [20, 42, 28, 62, 81, 50],
})

df_business_long = df_business.unpivot(
    index="date",
    variable_name="metric",
    value_name="value",
)

# Stacked area plot by default.
chart_area_stacked = (
    df_business_long
    .plot
    .area(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("value:Q", title="Value"),
        color=alt.Color("metric:N", title="Metric"),
    )
    .properties(width=750, height=350, title="Stacked Area Plot of Business Metrics")
)
chart_area_stacked.show()

# Unstacked area plot: use stack=None and opacity.
chart_area_unstacked = (
    df_business_long
    .plot
    .area(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("value:Q", stack=None, title="Value"),
        color=alt.Color("metric:N", title="Metric"),
        opacity=alt.value(0.45),
    )
    .properties(width=750, height=350, title="Unstacked Area Plot of Business Metrics")
)
chart_area_unstacked.show()


#----------------------------------------------------------------------------------------------------------#
#----------------------- 3. Optional hvPlot accessor for more pandas-like methods -------------------------#
#----------------------------------------------------------------------------------------------------------#
'''
If hvPlot is installed, `import hvplot.polars` registers a `.hvplot` accessor on Polars DataFrames.
This is closer to pandas' plotting style and supports methods such as:

    .hvplot.hist(...)
    .hvplot.kde(...)
    .hvplot.density(...)
    .hvplot.box(...)
    .hvplot.bar(...)
    .hvplot.barh(...)
    .hvplot.scatter(...)
    .hvplot.hexbin(...)
    .hvplot.line(...)
    .hvplot.area(...)

This section is guarded so the file does not fail if hvPlot is not installed.
'''

if HAS_HVPLOT:
    # Histogram
    hv_hist_attack = df_pokemon.hvplot.hist(
        y="Attack",
        bins=30,
        title="hvPlot Histogram of Pokemon Attack",
        xlabel="Attack",
        ylabel="Count",
        width=650,
        height=350,
    )
    hvplot.show(hv_hist_attack)

    # KDE / density
    hv_kde_attack = df_pokemon.hvplot.kde(
        y="Attack",
        title="hvPlot KDE of Pokemon Attack",
        xlabel="Attack",
        width=650,
        height=350,
    )
    hvplot.show(hv_kde_attack)

    # Box plot
    hv_box_attack_generation = df_pokemon.hvplot.box(
        y="Attack",
        by="Generation",
        title="hvPlot Box Plot of Attack by Generation",
        width=650,
        height=350,
    )
    hvplot.show(hv_box_attack_generation)

    # Bar and horizontal bar
    hv_bar_generation = df_generation_counts.hvplot.bar(
        x="Generation",
        y="count",
        title="hvPlot Bar Plot of Pokemon Generation",
        width=650,
        height=350,
    )
    hvplot.show(hv_bar_generation)

    hv_barh_generation = df_generation_counts.hvplot.barh(
        x="Generation",
        y="count",
        title="hvPlot Horizontal Bar Plot of Pokemon Generation",
        width=650,
        height=350,
    )
    hvplot.show(hv_barh_generation)

    # Scatter
    hv_scatter_attack_defense = df_pokemon.hvplot.scatter(
        x="Attack",
        y="Defense",
        by="Type_1",
        title="hvPlot Scatter Plot of Attack vs Defense",
        width=650,
        height=400,
    )
    hvplot.show(hv_scatter_attack_defense)

    # Hexbin
    hv_hexbin_attack_defense = df_pokemon.hvplot.hexbin(
        x="Attack",
        y="Defense",
        gridsize=25,
        title="hvPlot Hexbin Plot of Attack vs Defense",
        width=650,
        height=400,
    )
    hvplot.show(hv_hexbin_attack_defense)

    # Line
    hv_line_paris = df_aq_paris.hvplot.line(
        x="date",
        y="value",
        title="hvPlot Line Plot of NO2 Levels in Paris",
        width=750,
        height=350,
    )
    hvplot.show(hv_line_paris)

    # Area
    hv_area_business = df_business.hvplot.area(
        x="date",
        y=["sales", "signups", "visits"],
        stacked=True,
        title="hvPlot Stacked Area Plot of Business Metrics",
        width=750,
        height=350,
    )
    hvplot.show(hv_area_business)
else:
    print("hvPlot is not installed; skipping optional hvplot.polars examples.")


#----------------------------------------------------------------------------------------------------------#
#-------------------- 4. Advanced supported patterns built from Polars transformations --------------------#
#----------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------------#
#------------------------------------------ 4.1 Correlation heatmap ---------------------------------------#
#----------------------------------------------------------------------------------------------------------#
'''
Polars does not provide pandas' `pd.plotting.scatter_matrix()`.
A compact supported alternative is to compute correlations with Polars, reshape to long format,
and plot a heatmap with a rect mark.
'''

numeric_cols = [
    col_name
    for col_name, dtype in lf_pokemon.select(cs.numeric()).collect_schema().items()
    if col_name != "Total"
]

df_corr = df_pokemon.select(numeric_cols).corr()

df_corr_long = (
    df_corr
    .with_columns(pl.Series("feature_x", numeric_cols))
    .unpivot(
        index="feature_x",
        variable_name="feature_y",
        value_name="correlation",
    )
)

chart_corr_heatmap = (
    df_corr_long
    .plot
    .rect(
        x=alt.X("feature_x:N", title="Feature"),
        y=alt.Y("feature_y:N", title="Feature"),
        color=alt.Color("correlation:Q", title="Correlation"),
    )
    .properties(width=500, height=500, title="Correlation Heatmap of Pokemon Numeric Features")
)
chart_corr_heatmap.show()


#----------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 4.2 Lag plot -----------------------------------------------#
#----------------------------------------------------------------------------------------------------------#
'''
Polars does not have a dedicated `lag_plot` function.
Use `shift(...)` to build the lagged series, then plot current value vs lagged value.
'''

df_lag = (
    lf_aq
    .filter((c("country") == "FR") & (c("city") == "Paris"))
    .sort("date")
    .select("date", "value")
    .with_columns(c("value").shift(1).alias("value_lag1"))
    .drop_nulls()
    .collect()
)

chart_lag = (
    df_lag
    .plot
    .scatter(
        x=alt.X("value_lag1:Q", title="NO2 Level at time t-1"),
        y=alt.Y("value:Q", title="NO2 Level at time t"),
    )
    .properties(width=550, height=400, title="Lag Plot of NO2 Levels in Paris, Lag = 1")
    .configure_point(opacity=0.65)
)
chart_lag.show()


#----------------------------------------------------------------------------------------------------------#
#-------------------------------------- 4.3 Autocorrelation bar plot --------------------------------------#
#----------------------------------------------------------------------------------------------------------#
'''
Polars does not have a dedicated `autocorrelation_plot` function.
Compute lag correlations with expressions, then plot the result as a bar chart.
'''

max_lag = 24

df_autocorr = pl.DataFrame({
    "lag": list(range(1, max_lag + 1)),
    "autocorrelation": [
        df_aq_paris
        .select(pl.corr(c("value"), c("value").shift(lag)))
        .item()
        for lag in range(1, max_lag + 1)
    ],
})

chart_autocorr = (
    df_autocorr
    .plot
    .bar(
        x=alt.X("lag:O", title="Lag"),
        y=alt.Y("autocorrelation:Q", title="Autocorrelation"),
    )
    .properties(width=650, height=350, title="Autocorrelation of NO2 Levels in Paris")
)
chart_autocorr.show()


#----------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 5. Summary -----------------------------------------------#
#----------------------------------------------------------------------------------------------------------#
'''
Pandas plotting idea                  Polars-supported approach
--------------------------------------------------------------------------------------------
df.plot(kind="hist")                 df.plot.bar(...) with binned x encoding
                                       or optional df.hvplot.hist(...)

df.plot(kind="density"/"kde")        optional df.hvplot.kde(...) / df.hvplot.density(...)

df.plot(kind="box")                  df.plot.boxplot(...)
                                       or optional df.hvplot.box(...)

df.plot(kind="pie")                  df.plot.arc(...)

df.plot(kind="bar")                  df.plot.bar(...)

df.plot(kind="barh")                 df.plot.bar(...) with x/y swapped
                                       or optional df.hvplot.barh(...)

df.plot(kind="scatter")              df.plot.scatter(...) or df.plot.point(...)

df.plot(kind="hexbin")               df.plot.rect(...) as a 2D binned heatmap
                                       or optional df.hvplot.hexbin(...)

df.plot(kind="line")                 df.plot.line(...)
                                       or optional df.hvplot.line(...)

df.plot(kind="area")                 df.plot.area(...)
                                       or optional df.hvplot.area(...)

pd.plotting.scatter_matrix            no direct Polars plotting API; skipped
pd.plotting.andrews_curves            no direct Polars plotting API; skipped
pd.plotting.parallel_coordinates      no direct Polars plotting API; skipped
pd.plotting.radviz                    no direct Polars plotting API; skipped
pd.plotting.bootstrap_plot            no direct Polars plotting API; skipped
pd.plotting.table                     no direct Polars plotting API; skipped
pd.plotting.register_*_converters     pandas/matplotlib-specific; skipped

Polars mental model:
+ Use LazyFrame for data preparation.
+ Use `.collect()` to get the final eager plotting DataFrame.
+ Use `df.plot` for built-in Altair charts.
+ Use `import hvplot.polars` and `df.hvplot` when you want a more pandas-like plotting API.
'''
