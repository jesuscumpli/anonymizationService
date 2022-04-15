import pandas as pd
import numpy as np

from utils.techniques.pseudonymization import *

dfOrigen = pd.read_csv("../datasets/football_salaries.csv")
dfOrigen = dfOrigen.sort_values(by='player', ascending=True)
print(dfOrigen)

identifiers = ["player"]
quasi_identifiers = ["position", "team", "age"]
sensible = []
non_sensible = ["total_value", "avg_year", "total_guaranteed", "fully_guaranteed", "free_agency"]

# dfFinal, dfMapping = counter_pseudonymization(dfOrigen, identifiers[0])
# dfOrigen = revert_pseudonymization_with_mapping_table(dfFinal, dfMapping, identifiers[0])
# dfOrigen = dfOrigen.sort_values(by='player', ascending=True)
# print(dfOrigen)

# RNG PRODUCE COLISIONES
# dfFinal, dfMapping = rng_pseudonymization(dfOrigen, identifiers[0])
# dfOrigen = revert_pseudonymization_with_mapping_table(dfFinal, dfMapping, identifiers[0])
# dfOrigen = dfOrigen.sort_values(by='player', ascending=True)
# print(dfOrigen)

