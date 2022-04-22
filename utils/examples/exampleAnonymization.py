
import pandas as pd
import numpy as np

from utils.Anonymization import Anonymization
from utils.techniques.pseudonymization import *
from scipy import stats

dfOrigen = pd.read_csv("../datasets/football_salaries.csv")
dfOrigen = dfOrigen.dropna()
dfOrigen = dfOrigen.sort_values(by='player', ascending=True)

identifiers = ["player"]
quasi_identifiers = ["position", "team", "age"]
sensible = ["total_value"]
non_sensible = ["avg_year", "total_guaranteed", "fully_guaranteed", "free_agency"]

data1 = dfOrigen.value_counts(quasi_identifiers)

model = Anonymization(dfOrigen, identifiers, quasi_identifiers, non_sensible, sensible)

model.achieve_k_anonymity(2)
if model.check_k_anonymity_better(2):
    print("K ANONYMITY ACCEPTED!")
else:
    print("NO K ANONYMITY!!!!!")

model.achieve_l_diversity(2)
if model.check_l_diversity(2):
    print("L DIVERSITY ACCEPTED!")
else:
    print("NO L DIVERSITY!!!!!")

model.achieve_t_closeness(0.05)
if model.check_t_closeness(0.05):
    print("T CLOSENESS ACCEPTED!")
else:
    print("NO T CLOSENESS!!!!!")

print(len(model.dataframeFinal))