'''
datar allows applying plotnine's ggplot into the processing pipeline
'''

import datar.all as dr
from datar import f
import pandas as pd
import plotnine as pln

########################

tb_baseball = (
    pd.read_csv("05_Pandas_DataR_dataframe/data/baseball.csv")
    >> dr.select(f.Name, f.Position, f.Height, f.Weight)
    >> dr.mutate(Position = dr.as_factor(f.Position))
)


print(tb_baseball >> dr.slice_head(4))
#               Name       Position  Height  Weight
#           <object>     <category> <int64> <int64>
# 0    Adam_Donachie        Catcher      74     180
# 1        Paul_Bako        Catcher      74     215
# 2  Ramon_Hernandez        Catcher      72     210
# 3     Kevin_Millar  First_Baseman      72     210

##########################################################################
##           Use plotnine to draw scatter plot Height ~ Weight          ##
##########################################################################

(
    tb_baseball
    >> pln.ggplot()
    + pln.theme_seaborn()
    + pln.geom_point(pln.aes(x="Weight", y="Height", color="Position"))
    + pln.geom_smooth(pln.aes(x="Weight", y="Height"), method="lm", se=False, color="black")
    + pln.ggtitle("Scatter plot Height ~ Weight colored by Position")
).show()

#########################################################################
##           Use plotnine to draw boxplot Height ~ Position            ##
#########################################################################

(
    tb_baseball
    >> pln.ggplot()
    + pln.theme_seaborn()
    + pln.geom_boxplot(pln.aes(x="Position", y="Height", fill="Position"), notch=True)
    + pln.coord_flip()
    + pln.ggtitle("Boxplot Height ~ Position")
).show()