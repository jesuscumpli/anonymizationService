import time

import pandas as pd
import numpy as np

from utils.Anonymization import Anonymization
from utils.techniques.generalization import generalization_categorical_semantic, \
    generalization_numerical_interval
from utils.techniques.pseudonymization import *
from scipy import stats

dfOrigen = pd.read_csv("../datasets/football_salaries.csv")
dfOrigen = dfOrigen.dropna()
dfOrigen = dfOrigen.sort_values(by='player', ascending=True)
dfOrigen = dfOrigen.head(100)

identifiers = ["player"]
quasi_identifiers = ["position", "team", "age"]
sensible = ["total_value", "avg_year"]

# # Pseudonimization identifiers
# dfFinal, dfMapping = pseudonymization_counter(dfOrigen, identifiers[0])
#
# # Generalization quasi_identifiers
# dfFinal = generalization_numerical_mask(dfFinal, "age", 1)

# dfFinal = generalization_categorical_semantic(dfFinal, "position", semantic_herarchy)
#
# # Generalization sensible
# intervals = [-np.inf, 0, 1000, 5000, 10000, 50000, 100000, 200000, 500000, 1000000, 5000000, 10000000, 50000000, 100000000,
#              200000000, 500000000, np.inf]
# dfFinal = generalization_numerical_interval(dfFinal, "total_value", intervals)
# dfFinal = generalization_numerical_interval(dfFinal, "avg_year", intervals)
# dfFinal = generalization_numerical_interval(dfFinal, "total_guaranteed", intervals)
# dfFinal = generalization_numerical_interval(dfFinal, "fully_guaranteed", intervals)

semantic_herarchy = {
    "defense": ["cornerback", "defensive-back", "safety", "linebacker", "interior-defensive-line"],
    "medium": ["center", "right-guard", "3-4-defensive-end"],
    "attack": ["offensive-line", "right-tackle", "punter", "quarterback"]
}
semantics = {}
semantics["position"] = semantic_herarchy

model = Anonymization(dfOrigen, identifiers, quasi_identifiers, sensible, semantics)

time1 = time.time()
dfFinal, best_utility = model.achieve_klt_random(k=2, l=2, t=0.2, stop_utility=0.7, MAX_ITERS=100)
time2 = time.time()
time_interval = time2 - time1
print("Tiempo: " + str(time_interval) + "; utility: " + str(best_utility))

model.reset_dataframe_final()

time1 = time.time()
dfFinal, best_utility = model.achieve_klt_backtracking(k=2, l=2, t=0.2, stop_utility=0.7, MAX_ITERS=100)
time2 = time.time()
time_interval = time2 - time1
print("Tiempo: " + str(time_interval) + "; utility: " + str(best_utility))

if model.check_k_anonymity(2):
    print("K ANONYMITY ACCEPTED!")
else:
    print("NO K ANONYMITY!!!!!")

if model.check_l_diversity(2):
    print("L DIVERSITY ACCEPTED!")
else:
    print("NO L DIVERSITY!!!!!")

if model.check_t_closeness(0.05):
    print("T CLOSENESS ACCEPTED!")
else:
    print("NO T CLOSENESS!!!!!")

print(len(model.dataframeFinal))
