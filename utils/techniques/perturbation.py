#############################################
# FUNCTIONS WITH PERTURBATION TECHNIQUES  #
#############################################

"""
input dataframe: dataset origen
input col_index: column index from dataframe to generalize
objective: apply a perturbation technique to the specified columns
:return: Dataframe
"""

import numpy as np


def perturbation_noise_addition(dataframe, col_index):
    dfFinal = dataframe.copy(deep=True)
    std = dfFinal[col_index].std(ddof=0)
    mean = np.mean(dfFinal[col_index], axis=None)
    if not std:
        std = 1
    noise = np.random.normal(mean, std, len(dfFinal[col_index])).astype(int)
    dfFinal[col_index] = dfFinal[col_index] + noise
    return dfFinal


def perturbation_permutation(dataframe, col_index):
    dfFinal = dataframe.copy(deep=True)
    dfFinal[col_index] = np.random.permutation(dfFinal[col_index])
    return dfFinal


def perturbation_micro_aggregation(dataframe, col_index, num_group):
    dfFinal = dataframe.copy(deep=True)
    dfFinal = dfFinal.sort_values(by=col_index, ascending=True)
    num_items_group = num_group * len(dfFinal.index)
    i = 0
    while i < len(dfFinal.index):
        mean_subgroup = np.mean(dfFinal[col_index].tolist()[int(i): int(i + num_items_group)])
        j = 0
        while j < num_items_group:
            # dfFinal[col_index][j] = mean_subgroup
            dfFinal.at[j, col_index] = mean_subgroup
            j += 1
        i += num_items_group
    return dfFinal
