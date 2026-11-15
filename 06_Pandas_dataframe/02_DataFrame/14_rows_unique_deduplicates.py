'''
1. `df["col"].unique()`: get unique values of a single column
2. `df.drop_duplicates(subset=[...])`: remove duplicate rows of columns subset
'''

import pandas as pd

df = pd.DataFrame(
    {
        "brand": ["Yum Yum", "Yum Yum", "Indomie", "Indomie", "Indomie"],
        "style": ["cup", "cup", "cup", "pack", "pack"],
        "rating": [4, 4, 3.5, 15, 5],
    }
)

print(df)
#      brand style  rating
# 0  Yum Yum   cup     4.0
# 1  Yum Yum   cup     4.0
# 2  Indomie   cup     3.5
# 3  Indomie  pack    15.0
# 4  Indomie  pack     5.0

# ======================================================================================
# 1. `df["col"].unique()`: get unique values of a single column
# =======================================================================================

print(
    df["brand"].unique()
)
# <ArrowStringArray>
# ['Yum Yum', 'Indomie']
# Length: 2, dtype: str

print(
    df["rating"].unique()
)
# [ 4.   3.5 15.   5. ]

# ======================================================================================
# 2. `df.drop_duplicates(subset=[...])`: remove duplicate rows of columns subset
# ======================================================================================

print(
    df
    .drop_duplicates()
)
#      brand style  rating
# 0  Yum Yum   cup     4.0
# 2  Indomie   cup     3.5
# 3  Indomie  pack    15.0
# 4  Indomie  pack     5.0

print(
    df
    .drop_duplicates(subset=["brand", "style"])
)
#      brand style  rating
# 0  Yum Yum   cup     4.0
# 2  Indomie   cup     3.5
# 3  Indomie  pack    15.0
