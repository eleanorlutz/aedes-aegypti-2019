import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as lsc

treatments = {"F": "naive_100ul_left_food_05percent", 
          "FE": "naive_100ul_left_food_extract",
          "Y": "naive_100ul_left_yeastRNA_1gL",
          "Q": "naive_100ul_left_quinine_10mM", 
          "I": "naive_100ul_left_indole_100uM",
          "O": "naive_100ul_left_o-cresol_100uM",
          "W": "naive_100ul_left_milliQ_water"}

fed = {"Starved": "1day", "Fed":"no"}

# Size of scatterpoints in all figures
s = 11

# Figure 3, Figure Supplemental 2
# Colors imported into all figures
c_grey = "#969696"
c_greyax = "#535353"

c_food = "#f55678"
c_extract = "#f47d54"
c_rna = "#f5e98e"
c_quinine = "#3bcfda"
c_indole = "#b88e42"
c_cresol = "#b9a179"
c_water = c_grey

# Figure 3, Figure 4
c_neutral = c_water
c_averse = c_quinine
c_attract = c_food

# Figure Supplemental 1
c_female = "#f47d54"
c_male = c_grey

# Figure 2
c_starve = "#90b60e"
c_fed = "#a07fb2"
c_acclimate = c_grey
c_neutral = "#859cbc"