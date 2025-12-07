'''
Draw basic plots using DataFrame.plot() method or DataFrame.plot.<plotting_method>().

##########################

1. Histogram: 
   + df.plot(kind="hist") 
   + df.plot.hist()

2. Density/KDE plot: 
   + df.plot(kind="density"/"kde")
   + df.plot.density()
   + df.plot.kde()

3. Box plot: 
   + df.plot(kind="box")
   + df.plot.box()

4. Pie chart: 
   + df.plot(kind="pie")
   + df.plot.pie()

5. Bar plot: 
   + df.plot(kind="bar")
   + df.plot.bar()

6. Horizontal Bar plot: 
   + df.plot(kind="barh")
   + df.plot.barh()

7. Scatter plot: 
   + df.plot(kind="scatter", x=<x_column>, y=<y_column>), 
   + df.plot.scatter(x=<x_column>, y=<y_column>)

8. Hexbin plot: 
    + df.plot(kind="hexbin", x=<x_column>, y=<y_column>, gridsize=<size>)
    + df.plot.hexbin(x=<x_column>, y=<y_column>, gridsize=<size>)

9. Line plot: 
   + df.plot(kinde="line")
   + df.plot()
   + df.plot.line()

10. Area plot: 
   + df.plot(kind="area")
   + df.plot.area()
'''

import pandas as pd
import matplotlib.pyplot as plt

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

print(df_pokemon.info())
# RangeIndex: 800 entries, 0 to 799
# Data columns (total 12 columns):
#  #   Column      Non-Null Count  Dtype   
# ---  ------      --------------  -----   
#  0   Name        800 non-null    object  
#  1   Type_1      800 non-null    category
#  2   Type_2      414 non-null    category
#  3   Total       800 non-null    int64   
#  4   HP          800 non-null    int64   
#  5   Attack      800 non-null    int64   
#  6   Defense     800 non-null    int64   
#  7   Sp_Atk      800 non-null    int64   
#  8   Sp_Def      800 non-null    int64   
#  9   Speed       800 non-null    int64   
#  10  Generation  800 non-null    category
#  11  Legendary   800 non-null    bool    
# dtypes: bool(1), category(3), int64(7), object(1)
# memory usage: 54.7+ KB


#--------------------------------------------------------------------------------------------------------#
#------------------------------------------ 1. Histogram ------------------------------------------------#
#--------------------------------------------------------------------------------------------------------#
'''
Histogram describes the distribution of a numerical variable by splitting the data into bins (intervals) 
and counting the number of observations that fall into each bin.
'''

################################
##    df.plot(kind="hist")    ##
################################

#----------
## Draw histogram of "Attack" column
#----------

df_pokemon.plot(
    kind="hist",
    y="Attack",
    bins=30,                     # Number of bins (intervals)
    color="skyblue",             # Color of the bars
    edgecolor="black",           # Color of the bar edges
    alpha=0.7,                   # Transparency level (0 to 1)
    title="Histogram of Pokemon Attack",  # Title of the plot
    xlabel="Attack",             # Label for the x-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw histogram of "Attack" and "Defense" columns
#----------

df_pokemon.plot(
    kind="hist",
    y=["Attack", "Defense"],
    bins=30,                     # Number of bins (intervals)
    color=["skyblue", "salmon"], # Colors for each column
    edgecolor="black",           # Color of the bar edges
    alpha=0.7,                   # Transparency level (0 to 1)
    title="Histogram of Pokemon Attack and Defense",  # Title of the plot
    xlabel="Value",              # Label for the x-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

##########################
##    df.plot.hist()    ##
##########################

#----------
## Draw histogram of "Attack" column
#----------

df_pokemon.plot.hist(
    y="Attack",
    bins=30,                     # Number of bins (intervals)
    color="skyblue",             # Color of the bars
    edgecolor="black",           # Color of the bar edges
    alpha=0.7,                   # Transparency level (0 to 1)
    title="Histogram of Pokemon Attack",  # Title of the plot
    xlabel="Attack",             # Label for the x-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw histogram of "Attack" and "Defense" columns
#----------

df_pokemon.plot.hist(
    y=["Attack", "Defense"],
    bins=30,                     # Number of bins (intervals)
    color=["skyblue", "salmon"], # Colors for each column
    edgecolor="black",           # Color of the bar edges
    alpha=0.7,                   # Transparency level (0 to 1)
    title="Histogram of Pokemon Attack and Defense",  # Title of the plot
    xlabel="Value",              # Label for the x-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot


#--------------------------------------------------------------------------------------------------------#
#------------------------------------------ 2. Density/KDE plot -----------------------------------------#
#--------------------------------------------------------------------------------------------------------#
'''
Density plot (or Kernel Density Estimate - KDE) is a smoothed version of the histogram that estimates
the probability density function of a continuous variable.
'''

###################################
##    df.plot(kind="density")    ##
###################################

#----------
## Draw density plot of "Attack" column
#----------

# kind="density"
df_pokemon.plot(
    kind="density",
    y="Attack",
    color="blue",             # Color of the density line
    title="Density Plot of Pokemon Attack",  # Title of the plot
    xlabel="Attack",             # Label for the x-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

# kind="kde"
df_pokemon.plot(
    kind="kde",
    y="Attack",
    color="blue",             # Color of the density line
    title="Density Plot of Pokemon Attack",  # Title of the plot
    xlabel="Attack",             # Label for the x-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw density plot of "Attack" and "Defense" columns
#----------

# kind="density"
df_pokemon.plot(
    kind="density",
    y=["Attack", "Defense"],
    color=["blue", "red"], # Colors for each column
    title="Density Plot of Pokemon Attack and Defense",  # Title of the plot
    xlabel="Value",              # Label for the x-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

# kind="kde"
df_pokemon.plot(
    kind="kde",
    y=["Attack", "Defense"],
    color=["blue", "red"], # Colors for each column
    title="Density Plot of Pokemon Attack and Defense",  # Title of the plot
    xlabel="Value",              # Label for the x-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

#############################
##    df.plot.density()    ##
#############################

#----------
## Draw density plot of "Attack" column
#----------

df_pokemon.plot.density(
    y="Attack",
    color="blue",             # Color of the density line
    title="Density Plot of Pokemon Attack",  # Title of the plot
    xlabel="Attack",             # Label for the x-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw density plot of "Attack" and "Defense" columns
#----------

df_pokemon.plot.density(
    y=["Attack", "Defense"],
    color=["blue", "red"], # Colors for each column
    title="Density Plot of Pokemon Attack and Defense",  # Title of the plot
    xlabel="Value",              # Label for the x-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

#########################
##    df.plot.kde()    ##
#########################

#----------
## Draw density plot of "Attack" column
#----------

df_pokemon.plot.kde(
    y="Attack",
    color="blue",             # Color of the density line
    title="Density Plot of Pokemon Attack",  # Title of the plot
    xlabel="Attack",             # Label for the x-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw density plot of "Attack" and "Defense" columns
#----------

df_pokemon.plot.kde(
    y=["Attack", "Defense"],
    color=["blue", "red"], # Colors for each column
    title="Density Plot of Pokemon Attack and Defense",  # Title of the plot
    xlabel="Value",              # Label for the x-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot


#--------------------------------------------------------------------------------------------------------#
#------------------------------------------- 3. Box plot ------------------------------------------------#
#--------------------------------------------------------------------------------------------------------#
'''
Box plot (or box-and-whisker plot) is a graphical representation of the distribution of a dataset
that displays the median, quartiles, and potential outliers.

Also support notched box plot by setting notch=True.
'''

###############################
##    df.plot(kind="box")    ##
###############################

#----------
## Draw box plot of "Attack" column
#----------

df_pokemon.plot(
    kind="box",
    column="Attack",
    color="purple",             # Color of the box
    title="Box Plot of Pokemon Attack",  # Title of the plot
    ylabel="Attack",             # Label for the y-axis
    figsize=(8, 6)              # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw box plot of "Attack" between different "Generation"
#----------

df_pokemon.plot(
    kind="box",
    column="Attack",            # Dependent variable
    by="Generation",            # Group by "Generation" column
    notch=True,
    color="purple",             # Color of the box
    title="Box Plot of Pokemon Attack by Generation",  # Title of the plot
    ylabel="Attack",             # Label for the y-axis
    xlabel="Generation",         # Label for the x-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

#########################
##    df.plot.box()    ##
#########################

#----------
## Draw box plot of "Attack" column
#----------

df_pokemon.plot.box(
    column="Attack",           # Dependent variable
    color="green",             # Color of the box
    title="Box Plot of Pokemon Attack",  # Title of the plot
    ylabel="Attack",             # Label for the y-axis
    figsize=(8, 6)              # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw box plot of "Attack" between different "Generation"
#----------

df_pokemon.plot.box(
    column="Attack",            # Dependent variable
    by="Generation",            # Group by "Generation" column
    notch=True,
    color="green",             # Color of the box
    title="Box Plot of Pokemon Attack by Generation",  # Title of the plot
    ylabel="Attack",             # Label for the y-axis
    xlabel="Generation",         # Label for the x-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot


#--------------------------------------------------------------------------------------------------------#
#------------------------------------------- 4. Pie chart -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------#
'''
Pie chart is a circular statistical graphic that is divided into slices to illustrate numerical proportions.

Useful for categorical data with a small number of categories.
'''

###############################
##    df.plot(kind="pie")    ##
###############################

#----------
## Draw pie chart of "Generation" column
#----------

generation_counts = df_pokemon['Generation'].value_counts().sort_index()

generation_counts.plot(
    kind="pie",
    autopct="%1.1f%%",         # Format for displaying percentages
    startangle=140,            # Starting angle of the pie chart
    colors=plt.cm.Paired.colors, # Color map for the slices
    title="Distribution of Pokemon Generation",  # Title of the plot
    ylabel="",                  # Remove default y-label
    figsize=(8, 8)              # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw subplot pie charts of "Type_1" and "Type_2" columns
#----------

type1_counts = df_pokemon['Type_1'].value_counts()
type2_counts = df_pokemon['Type_2'].value_counts()

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

type1_counts.plot(
    kind="pie",
    autopct="%1.1f%%",         # Format for displaying percentages
    startangle=140,            # Starting angle of the pie chart
    colors=plt.cm.Paired.colors, # Color map for the slices
    title="Distribution of Pokemon Type 1",  # Title of the plot
    ylabel="",                  # Remove default y-label
    ax=axes[0]                  # First subplot
)

type2_counts.plot(
    kind="pie",
    autopct="%1.1f%%",         # Format for displaying percentages
    startangle=140,            # Starting angle of the pie chart
    colors=plt.cm.Paired.colors, # Color map for the slices
    title="Distribution of Pokemon Type 2",  # Title of the plot
    ylabel="",                  # Remove default y-label
    ax=axes[1]                  # Second subplot
)

plt.show() # Display the plot

#########################
##    df.plot.pie()    ##
#########################

#----------
## Draw pie chart of "Generation" column
#----------

generation_counts = df_pokemon['Generation'].value_counts().sort_index()

generation_counts.plot.pie(
    autopct="%1.1f%%",         # Format for displaying percentages
    startangle=140,            # Starting angle of the pie chart
    colors=plt.cm.Paired.colors, # Color map for the slices
    title="Distribution of Pokemon Generation",  # Title of the plot
    ylabel="",                  # Remove default y-label
    figsize=(8, 8)              # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw subplot pie charts of "Type_1" and "Type_2" columns
#----------

type1_counts = df_pokemon['Type_1'].value_counts()
type2_counts = df_pokemon['Type_2'].value_counts()

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

type1_counts.plot.pie(
    autopct="%1.1f%%",         # Format for displaying percentages
    startangle=140,            # Starting angle of the pie chart
    colors=plt.cm.Paired.colors, # Color map for the slices
    title="Distribution of Pokemon Type 1",  # Title of the plot
    ylabel="",                  # Remove default y-label
    ax=axes[0]                  # First subplot
)

type2_counts.plot.pie(
    autopct="%1.1f%%",         # Format for displaying percentages
    startangle=140,            # Starting angle of the pie chart
    colors=plt.cm.Paired.colors, # Color map for the slices
    title="Distribution of Pokemon Type 2",  # Title of the plot
    ylabel="",                  # Remove default y-label
    ax=axes[1]                  # Second subplot
)

plt.show() # Display the plot


#--------------------------------------------------------------------------------------------------------#
#------------------------------------------ 5. Bar plot -------------------------------------------------#
#--------------------------------------------------------------------------------------------------------#
'''
Bar plot is a graphical representation of categorical data using rectangular bars, 
where the length of each bar is proportional to the value it represents.

Pandas also supports stacked and dodged bar plots by setting stacked=True/False.
'''

###############################
##    df.plot(kind="bar")    ##
###############################

#----------
## Draw bar plot of "Generation" column
#----------

generation_counts = df_pokemon['Generation'].value_counts().sort_index()

generation_counts.plot(
    kind="bar",
    color="green",             # Color of the bars
    edgecolor="black",           # Color of the bar edges
    alpha=0.7,                   # Transparency level (0 to 1)
    title="Bar Plot of Pokemon Generation",  # Title of the plot
    xlabel="Generation",         # Label for the x-axis
    ylabel="Count",              # Label for the y-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw dodged bar plot of "Generation" and "Legendary" columns
#----------

gen_legd_counts = pd.crosstab(df_pokemon['Generation'], df_pokemon['Legendary'])
# Legendary   False  True 
# Generation              
# 1             160      6
# 2             101      5
# 3             142     18
# 4             108     13
# 5             150     15
# 6              74      8

gen_legd_counts.plot(
    kind="bar",
    stacked=False,             # Dodged bar plot
    color=["green", "brown"], # Colors for each category
    edgecolor="black",           # Color of the bar edges
    alpha=0.7,                   # Transparency level (0 to 1)
    title="Bar Plot of Pokemon Generation and Legendary Status",  # Title of the plot
    xlabel="Generation",         # Label for the x-axis
    ylabel="Count",              # Label for the y-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw stacked bar plot of "Generation" and "Legendary" columns
#----------

gen_legd_counts = pd.crosstab(df_pokemon['Generation'], df_pokemon['Legendary'])

gen_legd_counts.plot(
    kind="bar",
    stacked=True,              # Stacked bar plot
    color=["green", "brown"], # Colors for each category
    edgecolor="black",           # Color of the bar edges
    alpha=0.7,                   # Transparency level (0 to 1)
    title="Stacked Bar Plot of Pokemon Generation and Legendary Status",  # Title of the plot
    xlabel="Generation",         # Label for the x-axis
    ylabel="Count",              # Label for the y-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

#########################
##    df.plot.bar()    ##
#########################

#----------
## Draw bar plot of "Generation" column
#----------

generation_counts = df_pokemon['Generation'].value_counts().sort_index()

generation_counts.plot.bar(
    color="green",             # Color of the bars
    edgecolor="black",           # Color of the bar edges
    alpha=0.7,                   # Transparency level (0 to 1)
    title="Bar Plot of Pokemon Generation",  # Title of the plot
    xlabel="Generation",         # Label for the x-axis
    ylabel="Count",              # Label for the y-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw dodged bar plot of "Generation" and "Legendary" columns
#----------

gen_legd_counts = pd.crosstab(df_pokemon['Generation'], df_pokemon['Legendary'])

gen_legd_counts.plot.bar(
    stacked=False,             # Dodged bar plot
    color=["green", "brown"], # Colors for each category
    edgecolor="black",           # Color of the bar edges
    alpha=0.7,                   # Transparency level (0 to 1)
    title="Bar Plot of Pokemon Generation and Legendary Status",  # Title of the plot
    xlabel="Generation",         # Label for the x-axis
    ylabel="Count",              # Label for the y-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw stacked bar plot of "Generation" and "Legendary" columns
#----------

gen_legd_counts = pd.crosstab(df_pokemon['Generation'], df_pokemon['Legendary'])

gen_legd_counts.plot.bar(
    stacked=True,              # Stacked bar plot
    color=["green", "brown"], # Colors for each category
    edgecolor="black",           # Color of the bar edges
    alpha=0.7,                   # Transparency level (0 to 1)
    title="Stacked Bar Plot of Pokemon Generation and Legendary Status",  # Title of the plot
    xlabel="Generation",         # Label for the x-axis
    ylabel="Count",              # Label for the y-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot


#--------------------------------------------------------------------------------------------------------#
#---------------------------------------- 6. Horizontal Bar plot ----------------------------------------#
#--------------------------------------------------------------------------------------------------------#
'''
Horizontal bar plot is similar to a vertical bar plot, but the bars are oriented horizontally.
'''

###############################
##   df.plot(kind="barh")    ##
###############################

#----------
## Draw horizontal bar plot of "Generation" column
#----------

generation_counts = df_pokemon['Generation'].value_counts().sort_index()

generation_counts.plot(
    kind="barh",
    color="orange",             # Color of the bars
    edgecolor="black",           # Color of the bar edges
    alpha=0.7,                   # Transparency level (0 to 1)
    title="Horizontal Bar Plot of Pokemon Generation",  # Title of the plot
    xlabel="Count",              # Label for the x-axis
    ylabel="Generation",         # Label for the y-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw dodged horizontal bar plot of "Generation" and "Legendary" columns
#----------

gen_legd_counts = pd.crosstab(df_pokemon['Generation'], df_pokemon['Legendary'])

gen_legd_counts.plot(
    kind="barh",
    stacked=False,             # Dodged horizontal bar plot
    color=["orange", "purple"], # Colors for each category
    edgecolor="black",           # Color of the bar edges
    alpha=0.7,                   # Transparency level (0 to 1)
    title="Horizontal Bar Plot of Pokemon Generation and Legendary Status",  # Title of the plot
    xlabel="Count",              # Label for the x-axis
    ylabel="Generation",         # Label for the y-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw stacked horizontal bar plot of "Generation" and "Legendary" columns
#----------

gen_legd_counts = pd.crosstab(df_pokemon['Generation'], df_pokemon['Legendary'])

gen_legd_counts.plot(
    kind="barh",
    stacked=True,              # Stacked horizontal bar plot
    color=["orange", "purple"], # Colors for each category
    edgecolor="black",           # Color of the bar edges
    alpha=0.7,                   # Transparency level (0 to 1)
    title="Stacked Horizontal Bar Plot of Pokemon Generation and Legendary Status",  # Title of the plot
    xlabel="Count",              # Label for the x-axis
    ylabel="Generation",         # Label for the y-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

##########################
##    df.plot.barh()    ##
##########################

#----------
## Draw horizontal bar plot of "Generation" column
#----------

generation_counts = df_pokemon['Generation'].value_counts().sort_index()

generation_counts.plot.barh(
    color="orange",             # Color of the bars
    edgecolor="black",           # Color of the bar edges
    alpha=0.7,                   # Transparency level (0 to 1)
    title="Horizontal Bar Plot of Pokemon Generation",  # Title of the plot
    xlabel="Count",              # Label for the x-axis
    ylabel="Generation",         # Label for the y-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw dodged horizontal bar plot of "Generation" and "Legendary" columns
#----------

gen_legd_counts = pd.crosstab(df_pokemon['Generation'], df_pokemon['Legendary'])

gen_legd_counts.plot.barh(
    stacked=False,             # Dodged horizontal bar plot
    color=["orange", "purple"], # Colors for each category
    edgecolor="black",           # Color of the bar edges
    alpha=0.7,                   # Transparency level (0 to 1)
    title="Horizontal Bar Plot of Pokemon Generation and Legendary Status",  # Title of the plot
    xlabel="Count",              # Label for the x-axis
    ylabel="Generation",         # Label for the y-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw stacked horizontal bar plot of "Generation" and "Legendary" columns
#----------

gen_legd_counts = pd.crosstab(df_pokemon['Generation'], df_pokemon['Legendary'])

gen_legd_counts.plot.barh(
    stacked=True,              # Stacked horizontal bar plot
    color=["orange", "purple"], # Colors for each category
    edgecolor="black",           # Color of the bar edges
    alpha=0.7,                   # Transparency level (0 to 1)
    title="Stacked Horizontal Bar Plot of Pokemon Generation and Legendary Status",  # Title of the plot
    xlabel="Count",              # Label for the x-axis
    ylabel="Generation",         # Label for the y-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot


#---------------------------------------------------------------------------------------------------------#
#------------------------------------------ 7. Scatter plot ----------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
Scatter plot is a graphical representation of the relationship between two continuous variables,
where each point represents an observation in the dataset.
'''

#################################
##   df.plot(kind="scatter")   ##
#################################

# Draw scatter plot of "Attack" vs "Defense" columns
df_pokemon.plot(
    kind="scatter",
    x="Attack",                 # x-axis variable
    y="Defense",                # y-axis variable
    color="blue",               # Color of the points
    alpha=0.6,                  # Transparency level (0 to 1)
    title="Scatter Plot of Pokemon Attack vs Defense",  # Title of the plot
    xlabel="Attack",            # Label for the x-axis
    ylabel="Defense",           # Label for the y-axis
    figsize=(10, 6)             # Size of the figure
)
plt.show() # Display the plot

############################
##   df.plot.scatter()    ##
############################

# Draw scatter plot of "Attack" vs "Defense" columns
df_pokemon.plot.scatter(
    x="Attack",                 # x-axis variable
    y="Defense",                # y-axis variable
    color="brown",               # Color of the points
    alpha=0.6,                  # Transparency level (0 to 1)
    title="Scatter Plot of Pokemon Attack vs Defense",  # Title of the plot
    xlabel="Attack",            # Label for the x-axis
    ylabel="Defense",           # Label for the y-axis
    figsize=(10, 6)             # Size of the figure
)
plt.show() # Display the plot


#--------------------------------------------------------------------------------------------------------#
#------------------------------------------ 8. Hexbin plot ----------------------------------------------#
#--------------------------------------------------------------------------------------------------------#
'''
Hexbin plot is a two-dimensional histogram 
that uses hexagonal bins to represent the density of points in a scatter plot, 
useful for visualizing the relationship between two continuous variables, especially with large datasets.
'''

################################
##   df.plot(kind="hexbin")   ##
################################

# Draw hexbin plot of "Attack" vs "Defense" columns
df_pokemon.plot(
    kind="hexbin",
    x="Attack",                 # x-axis variable
    y="Defense",                # y-axis variable
    gridsize=25,                # Number of hexagons in the x-direction
    cmap="Blues",               # Color map for the hexagons
    title="Hexbin Plot of Pokemon Attack vs Defense",  # Title of the plot
    xlabel="Attack",            # Label for the x-axis
    ylabel="Defense",           # Label for the y-axis
    figsize=(10, 6)             # Size of the figure
)
plt.show() # Display the plot

############################
##    df.plot.hexbin()    ##
############################

# Draw hexbin plot of "Attack" vs "Defense" columns
df_pokemon.plot.hexbin(
    x="Attack",                 # x-axis variable
    y="Defense",                # y-axis variable
    gridsize=25,                # Number of hexagons in the x-direction
    cmap="viridis",             # Color map for the hexagons
    title="Hexbin Plot of Pokemon Attack vs Defense",  # Title of the plot
    xlabel="Attack",            # Label for the x-axis
    ylabel="Defense",           # Label for the y-axis
    figsize=(10, 6)             # Size of the figure
)
plt.show() # Display the plot


#--------------------------------------------------------------------------------------------------------#
#------------------------------------------- 9. Line plot -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------#
'''
Line plot is a graphical representation of data points connected by straight lines,
often used to visualize trends over time or ordered categories.
'''

df_aq = (
    pd.read_csv("05_Pandas_DataR_dataframe/data/air_quality_no2_long.csv")
    .rename(columns={"date.utc": "date"})
    .assign(date = lambda df: pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S%z"))
)

print(df_aq.info())
# RangeIndex: 2068 entries, 0 to 2067
# Data columns (total 7 columns):
#  #   Column     Non-Null Count  Dtype              
# ---  ------     --------------  -----              
#  0   city       2068 non-null   object             
#  1   country    2068 non-null   object             
#  2   date       2068 non-null   datetime64[ns, UTC]
#  3   location   2068 non-null   object             
#  4   parameter  2068 non-null   object             
#  5   value      2068 non-null   float64            
#  6   unit       2068 non-null   object             
# dtypes: datetime64[ns, UTC](1), float64(1), object(5)
# memory usage: 113.2+ KB

################################
##    df.plot(kind="line")    ##
################################

#----------
## Draw line plot of "date" vs "value" columns for city "Paris"
#----------

(
    df_aq.copy()
    .query('city == "Paris"')
    .set_index("date")
    .sort_index()
    .drop(columns=["city", "country", "location", "parameter", "unit"]) # Keep only relevant columns
    .plot(
        kind="line",
        y="value",                  # y-axis variable
        color="skyblue",            # Color of the line
        marker="o",                 # Marker style for data points
        linestyle="--",             # Line style
        title="Line Plot of NO2 Levels in Paris Over Time",  # Title of the plot
        xlabel="Date",              # Label for the x-axis
        ylabel="NO2 Level (µg/m³)", # Label for the y-axis
        figsize=(12, 6)             # Size of the figure
    )
)
plt.show() # Display the plot

#----------
## Draw line plot of "date" vs "value" columns for all cities
#----------

(
    df_aq.copy()
    .set_index("date")
    .sort_index()
    .pivot(columns="city", values="value") # Reshape data to have cities as columns
    .drop(columns=["country", "location", "parameter", "unit"], errors="ignore") # Keep only relevant columns
    .plot(
        kind="line",
        color=["skyblue", "orange", "green"], # Colors for each city
        marker=None,                 # Don't use markers for data points
        linestyle="-",              # Line style
        title="Line Plot of NO2 Levels in Paris, London, and Madrid Over Time",  # Title of the plot
        xlabel="Date",              # Label for the x-axis
        ylabel="NO2 Level (µg/m³)", # Label for the y-axis
        figsize=(12, 6)             # Size of the figure
    )
)
plt.show() # Display the plot

##########################
##    df.plot.line()    ##
##########################

#----------
## Draw line plot of "date" vs "value" columns for city "Paris"
#----------

(
    df_aq.copy()
    .query('city == "Paris"')
    .set_index("date")
    .sort_index()
    .drop(columns=["city", "country", "location", "parameter", "unit"]) # Keep only relevant columns
    .plot.line(
        y="value",                  # y-axis variable
        color="skyblue",            # Color of the line
        marker="o",                 # Marker style for data points
        linestyle="--",             # Line style
        title="Line Plot of NO2 Levels in Paris Over Time",  # Title of the plot
        xlabel="Date",              # Label for the x-axis
        ylabel="NO2 Level (µg/m³)", # Label for the y-axis
        figsize=(12, 6)             # Size of the figure
    )
)
plt.show() # Display the plot

#----------
## Draw line plot of "date" vs "value" columns for all cities
#----------

(
    df_aq.copy()
    .set_index("date")
    .sort_index()
    .pivot(columns="city", values="value") # Reshape data to have cities as columns
    .drop(columns=["country", "location", "parameter", "unit"], errors="ignore") # Keep only relevant columns
    .plot.line(
        color=["skyblue", "orange", "green"], # Colors for each city
        marker=None,                 # Don't use markers for data points
        linestyle="-",              # Line style
        title="Line Plot of NO2 Levels in Paris, London, and Madrid Over Time",  # Title of the plot
        xlabel="Date",              # Label for the x-axis
        ylabel="NO2 Level (µg/m³)", # Label for the y-axis
        figsize=(12, 6)             # Size of the figure
    )
)
plt.show() # Display the plot


#--------------------------------------------------------------------------------------------------------#
#------------------------------------------ 10. Area plot -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------#
'''
Area plot is a graphical representation of data where the area between the line and the x-axis is filled,
often used to visualize cumulative totals over time or ordered categories.

Pandas also supports stacked and unstacked area plots by setting stacked=True/False.
'''

df_business = pd.DataFrame({
    'sales': [3, 2, 3, 9, 10, 6],
    'signups': [5, 5, 6, 12, 14, 13],
    'visits': [20, 42, 28, 62, 81, 50],
}, index=pd.date_range(start='2018/01/01', end='2018/07/01',
                       freq='ME'))

print(df_business)
#             sales  signups  visits
# 2018-01-31      3        5      20
# 2018-02-28      2        5      42
# 2018-03-31      3        6      28
# 2018-04-30      9       12      62
# 2018-05-31     10       14      81
# 2018-06-30      6       13      50

################################
##    df.plot(kind="area")    ##
################################

#----------
## Draw stacked (default) area plot of all columns
#----------

df_business.plot(
    kind="area",
    color=["skyblue", "orange", "green"], # Colors for each category
    alpha=0.5,                  # Transparency level (0 to 1)
    title="Unstacked Area Plot of Business Metrics Over Time",  # Title of the plot
    xlabel="Date",              # Label for the x-axis
    ylabel="Value",             # Label for the y-axis
    figsize=(10, 6)             # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw unstacked area plot of all columns
#----------

df_business.plot(
    kind="area",
    stacked=False,              # Unstacked area plot
    color=["skyblue", "orange", "green"], # Colors for each category
    alpha=0.5,                  # Transparency level (0 to 1)
    title="Unstacked Area Plot of Business Metrics Over Time",  # Title of the plot
    xlabel="Date",              # Label for the x-axis
    ylabel="Value",             # Label for the y-axis
    figsize=(10, 6)             # Size of the figure
)
plt.show() # Display the plot

##########################
##    df.plot.area()    ##
##########################

#----------
## Draw stacked (default) area plot of all columns
#----------

df_business.plot.area(
    color=["skyblue", "orange", "green"], # Colors for each category
    alpha=0.5,                  # Transparency level (0 to 1)
    title="Unstacked Area Plot of Business Metrics Over Time",  # Title of the plot
    xlabel="Date",              # Label for the x-axis
    ylabel="Value",             # Label for the y-axis
    figsize=(10, 6)             # Size of the figure
)
plt.show() # Display the plot

#----------
## Draw unstacked area plot of all columns
#----------

df_business.plot.area(
    stacked=False,              # Unstacked area plot
    color=["skyblue", "orange", "green"], # Colors for each category
    alpha=0.5,                  # Transparency level (0 to 1)
    title="Unstacked Area Plot of Business Metrics Over Time",  # Title of the plot
    xlabel="Date",              # Label for the x-axis
    ylabel="Value",             # Label for the y-axis
    figsize=(10, 6)             # Size of the figure
)
plt.show() # Display the plot

