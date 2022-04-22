#############################################
# FUNCTIONS WITH GENERALIZATION TECHNIQUES  #
#############################################

"""
input dataframe: dataset origen
input col: column index from dataframe to generalize
objective: apply a generalization technique to the specified columns
:return: Dataframe
"""
import numpy as np
import pandas as pd
from scipy import stats

def generalization_numerical_interval(dataframe, col, intervals):
    dfFinal = dataframe.copy(deep=True)
    dfFinal[col] = pd.cut(dfFinal[col], bins=intervals)
    return dfFinal

def generalization_numerical_mask(dataframe, col, num_mask):
    dfFinal = dataframe.copy(deep=True)
    mask = "*" * num_mask
    for index, row in dfFinal.iterrows():
        number = str(row[col])
        masked = number[:-num_mask] + mask
        dfFinal[col][index] = masked
    return dfFinal

def generalization_categorical_semantic(dataframe, col, hierarchy):
    dfFinal = dataframe.copy(deep=True)
    for index, row in dfFinal.iterrows():
        value = str(row[col])
        res = "Other"
        for key, values in hierarchy.items():
            if value in values:
                res = key
                break
        dfFinal[col][index] = res
    return dfFinal
