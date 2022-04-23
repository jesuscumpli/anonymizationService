import pandas as pd
import numpy as np

from utils.Anonymization import Anonymization
from utils.techniques.generalization import generalization_numerical_mask, generalization_categorical_semantic, \
    generalization_numerical_interval
from utils.techniques.pseudonymization import *
from scipy import stats

dfOrigen = pd.read_csv("../datasets/football_salaries.csv")
dfOrigen = dfOrigen.dropna()
dfOrigen = dfOrigen.sort_values(by='player', ascending=True)

identifiers = ["player"]
quasi_identifiers = ["position", "team", "age"]
sensible = ["total_value", "avg_year", "total_guaranteed", "fully_guaranteed"]
non_sensible = ["free_agency"]

# Pseudonimization identifiers
dfFinal, dfMapping = pseudonymization_counter(dfOrigen, identifiers[0])

# Generalization quasi_identifiers
dfFinal = generalization_numerical_mask(dfFinal, "age", 1)
semantic_herarchy = {
    "defense": ["cornerback", "defensive-back", "safety", "linebacker", "interior-defensive-line"],
    "medium": ["center", "right-guard", "3-4-defensive-end"],
    "attack": ["offensive-line", "right-tackle", "punter", "quarterback"]
}
dfFinal = generalization_categorical_semantic(dfFinal, "position", semantic_herarchy)

# Generalization sensible
intervals = [-np.inf, 0, 1000, 5000, 10000, 50000, 100000, 200000, 500000, 1000000, 5000000, 10000000, 50000000, 100000000,
             200000000, 500000000, np.inf]
dfFinal = generalization_numerical_interval(dfFinal, "total_value", intervals)
dfFinal = generalization_numerical_interval(dfFinal, "avg_year", intervals)
dfFinal = generalization_numerical_interval(dfFinal, "total_guaranteed", intervals)
dfFinal = generalization_numerical_interval(dfFinal, "fully_guaranteed", intervals)

data1 = dfFinal.value_counts(quasi_identifiers)

model = Anonymization(dfFinal, identifiers, quasi_identifiers, non_sensible, sensible)

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
