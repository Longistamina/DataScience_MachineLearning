'''
1. Create group-by object:
   + Using df.groupby("key") or df.groupby(["key1", "key2"])
   + Using df.groupby(by = df["key"]) or df.groupby(by = [df["key1"], df["key2"]])

2. df.groupby() object attritubes
   + group_obj.groups
   + group_obj.indices
   + group_obj.ngroups

3. Iterate over groups within a group-by object: for name, group in group_obj

4. Select specific groups in a group-by object: 
   + single-key groupby object: group_obj.get_group("name") 
   + multi-key groupby object: group_obj.get_group(("name1", "name2"))
'''

import pandas as pd

import warnings
warnings.filterwarnings("ignore")

df_pokemon = (
    pd.read_csv(
        filepath_or_buffer = "05_Pandas_DataR_dataframe/data/pokemon.csv",
        dtype = {
            "Type 1": "category",
            "Type 2": "category",
            "Generation": "category",
            "Legendary": "bool"
        }
    )
    .drop(columns = ["#"])
    .pipe(lambda df: df.set_axis(df.columns.str.strip().str.replace(r"\s+", "_", regex = True).str.replace(".", ""), axis=1))
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


#----------------------------------------------------------------------------------------------------------#
#---------------------------------------- 1. Create group-by object ---------------------------------------#
#----------------------------------------------------------------------------------------------------------#

#############################################################
## Using df.groupby("key") or df.groupby(["key1", "key2"]) ##
#############################################################

grouped_single_key = df_pokemon.groupby("Type_1")
print(grouped_single_key)
# <pandas.core.groupby.generic.DataFrameGroupBy object at 0x7f4481bd2ba0>

grouped_multi_keys = df_pokemon.groupby(["Type_1", "Type_2"])
print(grouped_multi_keys)
# <pandas.core.groupby.generic.DataFrameGroupBy object at 0x7f4481bd3c50>

###################################################################################
## Using df.groupby(by = df["key"]) or df.groupby(by = [df["key1"], df["key2"]]) ##
###################################################################################

grouped_single_key = df_pokemon.groupby(by = df_pokemon["Type_1"])
print(grouped_single_key)
# <pandas.core.groupby.generic.DataFrameGroupBy object at 0x7f4481be8f50>

grouped_multi_keys = df_pokemon.groupby(by = [df_pokemon["Type_1"], df_pokemon["Type_2"]])
print(grouped_multi_keys)
# <pandas.core.groupby.generic.DataFrameGroupBy object at 0x7f4481bea060>


#---------------------------------------------------------------------------------------------------------#
#---------------------------------- 2. df.groupby() object attritubes ------------------------------------#
#---------------------------------------------------------------------------------------------------------#

######################
## group_obj.groups ##
######################
'''A dictionary mapping group names to row labels'''

print(grouped_single_key.groups)
# {'Bug': [10, 11, 12, 13, 14, 15, 15, 46, ...], 'Dark': [197, 198, 215, 228, 229, ...], ...}

print(grouped_multi_keys.groups)
# {('Bug', 'Electric'): [595, 596], ('Bug', 'Fighting'): [214, 214], ('Bug', 'Fire'): [636, 637], ...}

#######################
## group_obj.indices ##
#######################
'''A dictionary mapping group names to row indices (array style)'''

print(grouped_single_key.indices)
# {'Bug': array([ 13,  14,  15,  16,  17,  18,  19,  51,  52,  53,  54, 132, 136,
#        137, 179, 180, 181, 182, 208, 219, 220, 228, 229, 230, 231, 232,
#        288, 289, 290, 291, 292, 307, 308, 314, 315, 316, 342, 343, 446,
#        447, 457, 458, 459, 460, 461, 462, 463, 520, 600, 601, 602, 603,
#        604, 605, 618, 619, 649, 650, 656, 657, 677, 678, 693, 697, 698,
#        717, 732, 733, 734]), 'Dark': array([212, 213, 233, 246, 247, 248, 284, 285, 326, 327, 392, 393, 478,
#        512, 549, 568, 569, 620, 621, 631, 632, 685, 686, 690, 691, 694,
#        695, 696, 756, 757, 793]), 'Dragon': array([159, 160, 161, 365, 366, 406, 407, 408, 409, 417, 418, 419, 420,
#        425, 426, 491, 492, 493, 494, 671, 672, 673, 682, 706, 707, 710,
#        711, 712, 774, 775, 776, 794]), 'Electric': array([ 30,  31,  88,  89, 108, 109, 134, 146, 157, 186, 193, 194, 195,
#        196, 258, 262, 337, 338, 339, 340, 341, 448, 449, 450, 464, 513,
#        517, 531, 532, 533, 534, 535, 536, 581, 582, 648, 663, 664, 665,
#        704, 705, 764, 765, 772]), 'Fairy': array([ 40,  41, 187, 189, 190, 225, 226, 519, 737, 738, 739, 752, 753,
#        754, 755, 770, 792]), 'Fighting': array([ 61,  62,  72,  73,  74, 114, 115, 255, 256, 320, 321, 334, 335,
#        336, 496, 497, 498, 592, 593, 594, 598, 599, 680, 681, 742, 743,
#        771]), 'Fire': array([  4,   5,   6,   7,   8,  42,  43,  63,  64,  83,  84, 135, 147,
#        158, 169, 170, 171, 236, 237, 259, 263, 270, 276, 277, 278, 279,
#        352, 353, 354, 355, 435, 436, 437, 518, 542, 557, 558, 559, 572,
#        573, 614, 615, 616, 692, 721, 722, 723, 730, 731, 735, 736, 799]), ...}

print(grouped_multi_keys.indices)
# {('Bug', 'Electric'): array([656, 657]), ('Bug', 'Fighting'): array([231, 232]), 
# ('Bug', 'Fire'): array([697, 698]), 
# ('Bug', 'Flying'): array([ 15, 132, 137, 179, 180, 208, 290, 308, 315, 461, 462, 463, 520, 734]), ...}

#######################
## group_obj.ngroups ##
#######################
'''The number of groups'''

print(grouped_single_key.ngroups)
# 18

print(grouped_multi_keys.ngroups)
# 136


#-----------------------------------------------------------------------------------------------------------#
#---------------------------- 3. Iterate over groups within a group-by object ------------------------------#
#-----------------------------------------------------------------------------------------------------------#

#####################################
## Iterate over grouped_single_key ##
#####################################

for name, group in grouped_single_key:
    print(f"Group name: {name}")
    print(group.head(3))  # Print the first 3 rows of each group
    print("="*99)

# Group name: Bug
#           Name Type_1  Type_2  Total  HP  Attack  Defense  Sp_Atk  Sp_Def  Speed Generation  Legendary
# 13    Caterpie    Bug     NaN    195  45      30       35      20      20     45          1      False
# 14     Metapod    Bug     NaN    205  50      20       55      25      25     30          1      False
# 15  Butterfree    Bug  Flying    395  60      45       50      90      80     70          1      False
# ===================================================================================================
# Group name: Dark
#         Name Type_1  Type_2  Total  HP  Attack  Defense  Sp_Atk  Sp_Def  Speed Generation  Legendary
# 212  Umbreon   Dark     NaN    525  95      65      110      60     130     65          2      False
# 213  Murkrow   Dark  Flying    405  60      85       42      85      42     91          2      False
# 233  Sneasel   Dark     Ice    430  55      95       55      35      75    115          2      False

#####################################
## Iterate over grouped_multi_keys ##
#####################################

for name, group in grouped_multi_keys:  # Iterate over the first 4 groups
    print(f"Group name: {name}")
    print(group.head(3))  # Print the first 3 rows of each group
    print("="*99)

# Group name: ('Bug', 'Electric')
#            Name Type_1    Type_2  Total  HP  Attack  Defense  Sp_Atk  Sp_Def  Speed Generation  Legendary
# 656      Joltik    Bug  Electric    319  50      47       50      57      50     65          5      False
# 657  Galvantula    Bug  Electric    472  70      77       60      97      60    108          5      False
# ===================================================================================================
# Group name: ('Bug', 'Fighting')
#                         Name Type_1    Type_2  Total  HP  Attack  Defense  Sp_Atk  Sp_Def  Speed Generation  Legendary
# 231                Heracross    Bug  Fighting    500  80     125       75      40      95     85          2      False
# 232  HeracrossMega Heracross    Bug  Fighting    600  80     185      115      40     105     75          2      False
# ===================================================================================================
# Group name: ('Bug', 'Fire')
#           Name Type_1 Type_2  Total  HP  Attack  Defense  Sp_Atk  Sp_Def  Speed Generation  Legendary
# 697   Larvesta    Bug   Fire    360  55      85       55      50      55     60          5      False
# 698  Volcarona    Bug   Fire    550  85      60       65     135     105    100          5      False


#-------------------------------------------------------------------------------------------------------#
#------------------------- 4. Select specific groups in a group-by object ------------------------------#
#-------------------------------------------------------------------------------------------------------#

############################
## With single group name ##
############################

print(grouped_single_key.get_group("Fire").head())
#                         Name Type_1  Type_2  Total  HP  Attack  Defense  Sp_Atk  Sp_Def  Speed Generation  Legendary
# 4                 Charmander   Fire     NaN    309  39      52       43      60      50     65          1      False
# 5                 Charmeleon   Fire     NaN    405  58      64       58      80      65     80          1      False
# 6                  Charizard   Fire  Flying    534  78      84       78     109      85    100          1      False
# 7  CharizardMega Charizard X   Fire  Dragon    634  78     130      111     130      85    100          1      False
# 8  CharizardMega Charizard Y   Fire  Flying    634  78     104       78     159     115    100          1      False

###############################
## With multiple group names ##
###############################

print(grouped_multi_keys.get_group(("Water", "Flying")).head())
#          Name Type_1  Type_2  Total  HP  Attack  Defense  Sp_Atk  Sp_Def  Speed Generation  Legendary
# 140  Gyarados  Water  Flying    540  95     125       79      60     100     81          1      False
# 244   Mantine  Water  Flying    465  65      40       70      80     140     70          2      False
# 301   Wingull  Water  Flying    270  40      30       30      55      30     85          3      False
# 302  Pelipper  Water  Flying    430  60      50      100      85      70     65          3      False
# 508   Mantyke  Water  Flying    345  45      20       50      60     120     50          4      False