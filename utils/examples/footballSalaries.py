import pandas as pd
import numpy as np

from utils.techniques.generalization import generalization_numerical_mask, generalization_numerical_interval, \
    generalization_categorical_semantic
from utils.techniques.generateKeys import generate_encryption_key, generate_secret_key
from utils.techniques.pseudonymization import *

dfOrigen = pd.read_csv("../datasets/football_salaries.csv")
dfOrigen = dfOrigen.sort_values(by='player', ascending=True)
print(dfOrigen)

identifiers = ["player"]
quasi_identifiers = ["position", "team", "age"]
sensible = []
non_sensible = ["total_value", "avg_year", "total_guaranteed", "fully_guaranteed", "free_agency"]

# dfFinal, dfMapping = pseudonymization_counter(dfOrigen, identifiers[0])
# dfOrigen = revert_pseudonymization_with_mapping_table(dfFinal, dfMapping, identifiers[0])
# dfOrigen = dfOrigen.sort_values(by='player', ascending=True)
# print(dfOrigen)

# RNG PRODUCE COLISIONES
# dfFinal, dfMapping = pseudonymization_rng(dfOrigen, identifiers[0])
# dfOrigen = revert_pseudonymization_with_mapping_table(dfFinal, dfMapping, identifiers[0])
# dfOrigen = dfOrigen.sort_values(by='player', ascending=True)
# print(dfOrigen)


# dfFinal = pseudonymization_hmac(dfOrigen, identifiers[0])
# dfOrigen = revert_pseudonymization_hmac(dfOrigen, dfFinal, identifiers[0])
# dfOrigen = dfOrigen.sort_values(by='player', ascending=True)
# print(dfOrigen)

# dfFinal = pseudonymization_encryption(dfOrigen, identifiers[0])
# dfOrigen = revert_pseudonymization_encryption(dfFinal, identifiers[0])
# dfOrigen = dfOrigen.sort_values(by='player', ascending=True)
# print(dfOrigen)

# dfFinal = generalization_numerical_mask(dfOrigen, "age", 1)
# dfFinal = generalization_numerical_interval(dfOrigen, "age", [16, 18, 21, 25, 30, 40, 50])

dict = {
    "defense": ["cornerback", "defensive-back", "safety", "linebacker", "interior-defensive-line"],
    "medium": ["center", "right-guard", "3-4-defensive-end"],
    "attack": ["offensive-line", "right-tackle", "punter", "quarterback"]
}
dfFinal = generalization_categorical_semantic(dfOrigen, "position", dict)
print(dfFinal)
