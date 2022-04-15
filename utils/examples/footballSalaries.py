import pandas as pd
import numpy as np
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

dfFinal = pseudonymization_encryption(dfOrigen, identifiers[0])
dfOrigen = revert_pseudonymization_encryption(dfFinal, identifiers[0])
dfOrigen = dfOrigen.sort_values(by='player', ascending=True)
print(dfOrigen)