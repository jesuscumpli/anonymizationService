import time

import pandas as pd
import numpy as np

from utils.Anonymization import Anonymization
from utils.techniques.generalization import generalization_categorical_semantic, \
    generalization_numerical_interval
from utils.techniques.pseudonymization import *
from scipy import stats

dfOrigen = pd.read_csv("../datasets/Churn Modeling.csv")
dfOrigen = dfOrigen.dropna()
dfOrigen.drop(['RowNumber'], axis=1, inplace=True)
# dfOrigen = dfOrigen.sort_values(by='player', ascending=True)
dfOrigen = dfOrigen.head(500)

identifiers = ["CustomerId"]
quasi_identifiers = ["Surname", "Geography", "Gender", "Age"]
sensible = ["CreditScore", "EstimatedSalary"]
semantic_herarchy = {
    "Europe": ["Spain", "France", "Germany"],
}
semantics = {}
semantics["Geography"] = semantic_herarchy

model = Anonymization(dfOrigen, identifiers, quasi_identifiers, sensible, semantics)

time1 = time.time()
dfFinal, best_utility = model.achieve_klt_random(k=2, l=2, t=0.2, stop_utility=0.2, MAX_ITERS=500)
time2 = time.time()
time_interval = time2 - time1
print("Tiempo: " + str(time_interval) + "; utility: " + str(best_utility))

#model.reset_dataframe_final()

#time1 = time.time()
#dfFinal, best_utility = model.achieve_klt_backtracking(k=2, l=2, t=0.2, stop_utility=0.5, MAX_ITERS=100)
#time2 = time.time()
#time_interval = time2 - time1
#print("Tiempo: " + str(time_interval) + "; utility: " + str(best_utility))

if model.check_k_anonymity(2):
    print("K ANONYMITY ACCEPTED!")
else:
    print("NO K ANONYMITY!!!!!")

if model.check_l_diversity(2):
    print("L DIVERSITY ACCEPTED!")
else:
    print("NO L DIVERSITY!!!!!")

if model.check_t_closeness(0.2):
    print("T CLOSENESS ACCEPTED!")
else:
    print("NO T CLOSENESS!!!!!")

print(len(model.dataframeFinal))
