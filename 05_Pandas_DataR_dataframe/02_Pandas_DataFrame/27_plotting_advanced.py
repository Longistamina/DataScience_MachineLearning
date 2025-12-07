'''
pandas.plotting offers several advanced plotting functions that can be used to visualize data in a DataFrame. 

##################################

1. pd.plotting.scatter_matrix()

2. pd.plotting.andrews_curves()

3. pd.plotting.parallel_coordinates()

4. pd.plotting.radviz()

5. pd.plotting.lag_plot()

6. pd.plotting.autocorrelation_plot()

7. pd.plotting.bootstrap_plot()

8. pd.plotting.boxplot()

9. pd.plotting.table()

10. pd.plotting.register_matplotlib_converters()

11. pd.plotting.deregister_matplotlib_converters()
'''

import pandas as pd
import matplotlib.pyplot as plt

# General DataFrame
df_pokemon = (
    pd.read_csv(
        filepath_or_buffer="05_Pandas_DataR_dataframe/data/pokemon.csv",
        dtype={
            "Type 1": "category",
            "Type 2": "category",
            "Generation": "category",
            "Legendary": "bool"
        }
    )
    .drop(columns=["#"])
    .pipe(lambda df: df.set_axis(df.columns.str.strip().str.replace(r"\s+", "_", regex=True).str.replace(".", ""), axis=1))
    .assign(Generation = lambda df: df['Generation'].cat.as_ordered())
)

# Time series DataFrame
df_aq = (
    pd.read_csv("05_Pandas_DataR_dataframe/data/air_quality_no2_long.csv")
    .rename(columns={"date.utc": "date"})
    .assign(date = lambda df: pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S%z"))
)

# Time series as Series
s_aq = (
    df_aq.copy()
    .query("(country == 'FR') & (city == 'Paris')")
    .set_index("date")
    .reindex(columns=["value"])
    .squeeze()
)

print(s_aq.head())
# date
# 2019-06-21 00:00:00+00:00    20.0
# 2019-06-20 23:00:00+00:00    21.8
# 2019-06-20 22:00:00+00:00    26.5
# 2019-06-20 21:00:00+00:00    24.9
# 2019-06-20 20:00:00+00:00    21.4
# Name: value, dtype: float64

#---------------------------------------------------------------------------------------------------------#
#------------------------------------ 1. pd.plotting.scatter_matrix() ------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
Creates a matrix of scatter plots for visualizing relationships between multiple

Parameters:
# frame: DataFrame to plot
# alpha: Transparency level (0.0-1.0, default 0.5)
# figsize: Figure size as (width, height) tuple
# diagonal: 'hist' or 'kde' for diagonal plots
# marker: Matplotlib marker style (default '.')
# range_padding: Axis range padding (default 0.05)

When to Use:
# Exploring correlations in multivariate data
# Understanding data distribution patterns
# Initial data analysis phase
# Comparing multiple numeric variables simultaneously
'''

#####################
## diagonal="hist" ##
#####################

pd.plotting.scatter_matrix(
    frame=df_pokemon.select_dtypes(include="number").drop(columns="Total"),
    alpha=0.5,
    figsize=(10, 10),
    diagonal="hist",
    marker="x",
    grid=True,
    hist_kwds={"bins": 20, "color": "gray"},
    range_padding=0.1
)
plt.title("Scatter Matrix with Histograms on Diagonal")
plt.show()

####################
## diagonal="kde" ##
####################

pd.plotting.scatter_matrix(
    frame=df_pokemon.select_dtypes(include="number").drop(columns="Total"),
    alpha=0.5,
    figsize=(10, 10),
    diagonal="kde",
    marker="o",
    grid=True,
    hist_kwds={"bins": 20, "color": "gray"},
    density_kwds={"color": "gray"},
    range_padding=0.1
)
plt.title("Scatter Matrix with KDE on Diagonal")
plt.show()


#---------------------------------------------------------------------------------------------------------#
#------------------------------ 2. pd.plotting.andrews_curves() ------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
Visualizes multivariate data by mapping each observation to a function using Fourier series transformation

Parameters:
# frame: DataFrame with data to plot
# class_column: Column name containing class labels
# samples: Number of points per curve (default 200)
# color: Colors for different classes
# colormap: Matplotlib colormap

When to Use:
# Visualizing clusters in high-dimensional data
# Comparing different classes/groups
# Pattern recognition in multivariate datasets
# Data classification visualization
'''

pd.plotting.andrews_curves(
    frame=df_pokemon[["Attack", "Defense", "Type_1"]],
    class_column="Type_1",
    samples=200,
    colormap="tab20",
    alpha=0.5,
    linewidth=1
)
plt.title("Andrews Curves of Pokémon by Type 1")
plt.show()


#---------------------------------------------------------------------------------------------------------#
#--------------------------------- 3. pd.plotting.parallel_coordinates() ---------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
Creates parallel coordinate plots for multivariate data visualization 
where each vertical axis represents a variable.

Parameters:
# frame: DataFrame to plot
# class_column: Column containing class names
# cols: List of columns to include (optional)
# color: Colors for different classes
# use_columns: Use columns as x-tick labels
# colormap: Colormap for line colors
# axvlines: Add vertical lines at each variable (default True)
# sort_labels: Sort class labels (default False)

When to Use:
# Visualizing high-dimensional data patterns
# Comparing multiple groups across several variables
# Identifying outliers and clusters
# Understanding variable relationships
'''

pd.plotting.parallel_coordinates(
    frame=df_pokemon[["Attack", "Defense", "Legendary"]],
    class_column="Legendary",
    colormap="tab10",
    axvlines=True,
    sort_labels=True,
    alpha=0.5,
    linewidth=1
)
plt.title("Parallel Coordinates Plot of Pokémon by Type 1")
plt.show()


#---------------------------------------------------------------------------------------------------------#
#------------------------------------- 4. pd.plotting.radviz() -------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
Projects N-dimensional data onto a 2D circular plot 
where each variable is positioned on the circle circumference.

Parameters:
# frame: DataFrame to plot
# class_column: Column with class names
# color: Colors for each category
# colormap: Matplotlib colormap

When to Use:
# Visualizing high-dimensional data in 2D
# Understanding variable influence on classifications
# Exploring data clustering patterns
# Dimensionality reduction visualization
'''

pd.plotting.radviz(
    frame=df_pokemon[["Attack", "Defense", "Speed", "Type_1"]],
    class_column="Type_1",
    colormap="tab20",
    alpha=0.5,
    linewidth=1
)
plt.title("Radviz Plot of Pokémon by Type 1")
plt.show()


#---------------------------------------------------------------------------------------------------------#
#-------------------------------------- 5. pd.plotting.lag_plot() ----------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
Creates scatter plot of time series vs. lagged version to detect patterns and autocorrelation.

Parameters:
# series: Time series data (pandas Series)
# lag: Lag length for scatter plot (default 1)
# ax: Matplotlib axes object
# **kwds: Additional matplotlib scatter arguments

When to Use:
# Time series analysis
# Detecting patterns and trends
# Checking for randomness in data
# Autocorrelation visualization
'''

pd.plotting.lag_plot(
    series=s_aq,
    lag=1,
    alpha=0.5,
    c="blue",
    marker="o"
)
plt.title("Lag Plot of NO2 Levels in Paris (Lag=1)")
plt.xlabel("NO2 Level at time t")
plt.show()


#---------------------------------------------------------------------------------------------------------#
#-------------------------------- 6. pd.plotting.autocorrelation_plot() ----------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
Plots autocorrelation function for time series with confidence bands for significance testing.

Parameters:
# series: Time series data (pandas Series)
# ax: Matplotlib axes object
# **kwargs: Additional matplotlib arguments

When to Use:
# Time series analysis
# Checking for seasonal patterns
# Testing for randomness
# ARIMA model diagnostics
'''

pd.plotting.autocorrelation_plot(
    series=s_aq,
    alpha=0.5,
    color="blue",
    marker="o"
)
plt.title("Autocorrelation Plot of NO2 Levels in Paris")
plt.show()


#---------------------------------------------------------------------------------------------------------#
#------------------------------------ 7. pd.plotting.bootstrap_plot() ------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
Bootstrap plot for uncertainty estimation showing sampling distribution of statistics.

Parameters:
# series: pandas Series for bootstrapping
# fig: Matplotlib figure object
# size: Sample size for each bootstrap (default 50)
# samples: Number of bootstrap samples (default 500)
# **kwds: Additional matplotlib arguments

When to Use:
# Statistical inference
# Uncertainty quantification
# Confidence interval estimation
# Non-parametric statistics
'''

pd.plotting.bootstrap_plot(
    series=s_aq,
    size=100,
    samples=200,
    color="darkgreen",
    alpha=0.1,
    linewidth=0.5
)
plt.title("Bootstrap Plot of NO2 Levels in Paris")
plt.show()


#---------------------------------------------------------------------------------------------------------#
#-------------------------------------- 8. pd.plotting.boxplot() -----------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
Creates box-and-whisker plots from DataFrame columns with optional grouping.

Parameters:
# data: DataFrame to plot
# column: Column name(s) to plot
# by: Column to group by
# fontsize: Font size for labels
# rot: Rotation angle for labels (default 0)
# grid: Show grid (default True)
# figsize: Figure size tuple
# return_type: 'axes', 'dict', 'both', or None

When to Use:
# Comparing distributions across groups
# Identifying outliers
# Exploratory data analysis
# Statistical summaries visualization
'''

# Attack ~ Legendary
pd.plotting.boxplot(
    data=df_pokemon,
    column="Attack",
    by="Legendary",
    notch=True,
    fontsize=8,
    rot=45,
    grid=True,
    figsize=(10, 6),
    return_type="axes"
)
plt.title("Boxplot of Pokémon Attack by Legendary Status")
plt.suptitle("")  # Suppress the automatic 'Boxplot grouped by ...' title
plt.show()

# Attack ~ Type_1 + Legendary
pd.plotting.boxplot(
    data=df_pokemon,
    column="Attack",
    by=["Type_1", "Legendary"],
    notch=True,
    fontsize=8,
    rot=45,
    grid=True,
    figsize=(10, 6),
    return_type="axes"
)
plt.title("Boxplot of Pokémon Attack by Type 1 and Legendary Status")
plt.suptitle("")  # Suppress the automatic 'Boxplot grouped by ...' title
plt.show()


#---------------------------------------------------------------------------------------------------------#
#-------------------------------------- 9. pd.plotting.table() -------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
Helper function to convert DataFrame/Series to matplotlib table for combined visualizations.

Parameters:
# ax: Matplotlib axes object
# data: DataFrame or Series data
# **kwargs: Additional table formatting arguments

When to Use:
# Adding data tables to plots
# Creating combined chart-table visualizations
# Detailed data presentation with plots
'''

fig, ax = plt.subplots(figsize=(8, 4))

pd.plotting.table(
    ax=ax,
    data=df_aq.query("(country == 'FR') & (city == 'Paris')").head(5).set_index("date"),
    loc="upper right",
    colWidths=[0.2] * len(df_aq.columns),
    cellLoc="center",
    rowLoc="center",
    fontsize=8
)
ax.set_title("NO2 Levels in Paris with Data Table")
ax.axis("off") # Hide the axes for table only
plt.show()


#---------------------------------------------------------------------------------------------------------#
#-------------------------- 10. pd.plotting.register_matplotlib_converters() -----------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
Registers pandas formatters and converters with matplotlib for proper datetime plotting.

Key Features:
# Modifies global matplotlib.units.registry dictionary
# Adds custom converters for pandas datetime objects
# Essential for plotting time-based data

When to Use:
# Plotting datetime/period data with matplotlib
# Resolving datetime plotting errors
# Ensuring proper date formatting in plots

https://pandas.pydata.org/docs/reference/api/pandas.plotting.register_matplotlib_converters.html
'''


#---------------------------------------------------------------------------------------------------------#
#------------------------ 11. pd.plotting.deregister_matplotlib_converters() -----------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
Removes pandas formatters and converters from matplotlib, restoring original state.

When to Use:
# Reverting matplotlib converter changes
# Troubleshooting plotting issues
# Restoring default matplotlib behavior

https://pandas.pydata.org/docs/reference/api/pandas.plotting.deregister_matplotlib_converters.html
'''