##########################################
# FUNCTIONS WITH ANONYMITY PROPERTIES  #
##########################################
import random
from scipy import stats
from utils.techniques.generalization import generalization_categorical_semantic, generalization_mask, \
    generalization_numerical_interval
from utils.techniques.perturbation import *

"""
Definition of K-ANONYMITY:
For each individual in the dataset, there should be
other at least k-1 individuals with the same quasi-identifiers
◦ Not a technique, but a goal or property
◦ Can be achieved using generalization, suppression, micro-aggregation, etc.
"""

"""
Definition of L-DIVERSITY:
On each group there should be at least L different
values for a sensitive attribute
◦ This is intended to prevent some attacks on k-anonymous databases such as
the background knowledge attack
"""

"""
Definition of T-CLOSENESS:
On each group, the distribution of values should be
similar to the original data distribution
"""


class Anonymization:
    def __init__(self, dataframeOrigen, identifiers_index, quasi_identifiers_index, sensible_index,
                 categories_hierarchy):
        """
        :param identifiers_index: column index of identifiers
        :param quasi_identifiers_index: column index of quasi_identifiers
        :param sensible_index: column index of sensible data
        """
        self.dataframeOrigen = dataframeOrigen.copy(deep=True)
        self.dataframeFinal = dataframeOrigen.copy(deep=True)
        self.identifiers_index = identifiers_index
        self.quasi_identifiers_index = quasi_identifiers_index
        self.sensible_index = sensible_index
        self.categories_hierarchy = categories_hierarchy
        self.k = 0
        self.l = 0
        self.t = 0
        self.utility = 1.0
        self.iter = 0
        self.MAX_ITERS = None
        self.stop_utility = None
        self.list_cols = None
        self.get_k_anonymity()  # Get the actual K
        self.get_l_diversity()  # Get the actual L
        self.get_t_closeness()  # Get the actual T

    def reset_dataframe_final(self):
        self.dataframeFinal = self.dataframeOrigen.copy(deep=True)
        self.k = 0
        self.l = 0
        self.t = 0
        self.utility = 1.0
        self.iter = 0
        self.MAX_ITERS = None
        self.stop_utility = None
        self.list_cols = None

    def __generate_groups__(self, df):
        """
        Iterate the self.dataframeFinal and generate a list of groups with the same quasi-identifiers
        """
        groups_index = {}
        for index, row in df.iterrows():
            valueQuasiIdentifier = ""
            for i in self.quasi_identifiers_index:
                valueQuasiIdentifier += str(row[i])
            if not valueQuasiIdentifier in groups_index:
                groups_index[valueQuasiIdentifier] = []
            groups_index[valueQuasiIdentifier].append(index)
        return groups_index

    def get_k_anonymity(self):
        """
        Check if dataframeFinal has k-anonymity property
        :return: k
        - Check if the number of unique rows by a list of columns are greater than k
        """
        unique_counts_rows = self.dataframeFinal.value_counts(self.quasi_identifiers_index)
        self.k = unique_counts_rows.min()
        return self.k

    def check_k_anonymity(self, k):
        """
        Check if dataframeFinal has k-anonymity property
        :param k: k property
        :return: Boolean
        - Check if the number of unique rows by a list of columns are greater than k
        """
        unique_counts_rows = self.dataframeFinal.value_counts(self.quasi_identifiers_index).tolist()
        return all(n >= k for n in unique_counts_rows)

    def check_l_diversity(self, l):
        """
        Check if dataframeFinal has l-diversity property.
        - Check if each group in self.groups has l samples with different sensitive values.
        :param l: l property
        :return: Boolean
        """
        groups_index = self.__generate_groups__(self.dataframeFinal)
        for key, rows_index in groups_index.items():
            l_res = 0
            sensitiveValues = {}

            for i in self.sensible_index:
                sensitiveValues[i] = []

            for index in rows_index:
                for i in self.sensible_index:
                    value = self.dataframeFinal.at[index, i]
                    if value not in sensitiveValues[i]:
                        sensitiveValues[i].append(value)

            for i in self.sensible_index:
                length = len(sensitiveValues[i])
                if length < l:
                    return False
        return True

    def get_l_diversity(self):
        groups_index = self.__generate_groups__(self.dataframeFinal)
        l = len(self.dataframeFinal)
        for key, rows_index in groups_index.items():
            sensitiveValues = {}

            for i in self.sensible_index:
                sensitiveValues[i] = []

            for index in rows_index:
                for i in self.sensible_index:
                    value = self.dataframeFinal.at[index, i]
                    if value not in sensitiveValues[i]:
                        sensitiveValues[i].append(value)

            for i in self.sensible_index:
                length = len(sensitiveValues[i])
                if length < l:
                    l = length
        self.l = l
        return l

    def check_t_closeness(self, t):
        """
        Check if dataframeFinal has t-closeness property
        - Check if each group in self.groups has the same distribution with the self.dataframeOrigen
        :param t: t property
        :return: Boolean
        """
        groups_index = self.__generate_groups__(self.dataframeFinal)
        for key, rows_index in groups_index.items():
            dfAux = self.dataframeFinal[self.dataframeFinal.index.isin(rows_index)]
            for col in self.sensible_index:
                statistic, pvalue = stats.ks_2samp(self.dataframeOrigen[col], dfAux[col])
                if statistic < t:  # Reject Null Hypothesis, accept Alternative Hypothesis (The distributions are different)
                    return False
        return True

    def get_t_closeness(self):
        t = 1.0
        groups_index = self.__generate_groups__(self.dataframeFinal)
        for key, rows_index in groups_index.items():
            dfAux = self.dataframeFinal[self.dataframeFinal.index.isin(rows_index)]
            for col in self.sensible_index:
                statistic, pvalue = stats.ks_2samp(self.dataframeOrigen[col], dfAux[col])
                if statistic < t:
                    t = statistic
        self.t = t
        return t

    """
    ACHIEVE K-L-T IN ONE METHOD
    """

    def __achieve_klt__(self, df, k=None, l=None, t=None):
        """
        Delete all the groups has not achieve k-anonymity, l-diversity or t-closeness
        :param t: t-property
        :return: dataframeFinal
        """
        dfResult = df.copy(deep=True)
        dfGroups = self.__generate_groups__(df)
        for key, rows_index in dfGroups.items():
            if k is not None:
                # K-ANONYMITY
                if len(rows_index) < k:
                    dfResult.drop(dfGroups[key], axis=0, inplace=True)
                    continue
            if t is not None:
                # T-CLOSENESS
                dfAux = df[df.index.isin(rows_index)]
                statistic = 0.0
                for col in self.sensible_index:
                    statistic, pvalue = stats.ks_2samp(df[col], dfAux[col])
                    if statistic < t:
                        dfResult.drop(dfGroups[key], axis=0, inplace=True)
                        break
                if statistic < t:
                    continue
            if l is not None:
                # L-DIVERSITY
                sensitiveValues = {}
                for i in self.sensible_index:
                    sensitiveValues[i] = []
                for index in rows_index:
                    for i in self.sensible_index:
                        value = dfResult.at[index, i]
                        if value not in sensitiveValues[i]:
                            sensitiveValues[i].append(value)
                for i in self.sensible_index:
                    length = len(sensitiveValues[i])
                    if length < l:
                        dfResult.drop(dfGroups[key], axis=0, inplace=True)
                        break
        return dfResult

    def achieve_klt_backtracking(self, k, l, t, stop_utility=1.0, MAX_ITERS=1000):
        perturbation = 1.0
        df = self.dataframeFinal
        best_df = self.__achieve_klt__(df, k, l, t)
        best_utility = (float(len(best_df)) / len(df)) / perturbation
        list_cols = self.quasi_identifiers_index.copy()
        list_cols.extend(self.sensible_index)
        random.shuffle(list_cols)
        self.iter = 0
        self.MAX_ITERS = MAX_ITERS
        self.stop_utility = stop_utility
        self.list_cols = list_cols
        best_df, best_utility = self.__achieve_klt_backtracking__(0, k, l, t, df, perturbation, best_utility, best_df)
        self.dataframeFinal = best_df
        self.get_k_anonymity()
        self.get_l_diversity()
        self.get_t_closeness()
        self.utility = best_utility
        return best_df, best_utility

    def __achieve_klt_backtracking__(self, start, k, l, t, df, perturbation, best_utility, best_df):
        """
        Add generalization and perturbation techniques
        """
        if best_utility >= self.stop_utility:
            return best_df, best_utility

        self.iter += 1
        if self.iter > self.MAX_ITERS:
            return best_df, best_utility

        for i in range(start, len(self.list_cols)):
            col = self.list_cols[i]
            best_df, best_utility = self.__achieve_klt_backtracking__(start + 1, k, l, t, df, perturbation,
                                                                      best_utility, best_df)
            if best_utility >= self.stop_utility:
                return best_df, best_utility
            # GENERALIZATION CATEGORIES
            try:
                categories = self.categories_hierarchy.get(col)
                if categories is not None:
                    newDf = generalization_categorical_semantic(df, col, categories)
                    dfResult = self.__achieve_klt__(newDf, k, l, t)
                    utility = (float(len(dfResult)) / len(df)) / (perturbation + 0.1)
                    if utility > best_utility:
                        best_df = dfResult
                        best_utility = utility
                    best_df, best_utility = self.__achieve_klt_backtracking__(start + 1, k, l, t, newDf,
                                                                              perturbation + 0.1,
                                                                              best_utility, best_df)
                    if best_utility >= self.stop_utility:
                        return best_df, best_utility
            except:
                pass
            # GENERALIZATION NUMERICAL
            try:
                steps = [0.1, 0.25, 0.4]
                for step in steps:
                    newDf = generalization_numerical_interval(df, col, step)
                    dfResult = self.__achieve_klt__(newDf, k, l, t)
                    utility = (float(len(dfResult)) / len(df)) / (perturbation + step * 0.1)
                    if utility > best_utility:
                        best_df = dfResult
                        best_utility = utility
                    best_df, best_utility = self.__achieve_klt_backtracking__(start + 1, k, l, t, newDf,
                                                                              perturbation + step * 0.1,
                                                                              best_utility, best_df)
                    if best_utility >= self.stop_utility:
                        return best_df, best_utility
            except:
                pass
            # GENERALIZATION MASK
            average_length_strings = int(df[col].apply(str).apply(len).mean())
            step = max(int(average_length_strings / 3), 1)
            quantiles = np.arange(1, average_length_strings, step)
            for num_mask in quantiles:
                newDf = generalization_mask(df, col, num_mask)
                dfResult = self.__achieve_klt__(newDf, k, l, t)
                utility = (float(len(dfResult)) / len(df)) / (perturbation + (average_length_strings / num_mask * 0.1))
                if utility > best_utility:
                    best_df = dfResult
                    best_utility = utility
                best_df, best_utility = self.__achieve_klt_backtracking__(start + 1, k, l, t, newDf,
                                                                          perturbation + (
                                                                                  average_length_strings / num_mask * 0.1),
                                                                          best_utility, best_df)
                if best_utility >= self.stop_utility:
                    return best_df, best_utility
            # PERTURBATION TECHNIQUES
            try:
                newDf = perturbation_permutation(df, col)
                dfResult = self.__achieve_klt__(newDf, k, l, t)
                utility = (float(len(dfResult)) / len(df)) / (perturbation + 0.1)
                if utility > best_utility:
                    best_df = dfResult
                    best_utility = utility
                best_df, best_utility = self.__achieve_klt_backtracking__(start + 1, k, l, t, newDf,
                                                                          perturbation + 0.1,
                                                                          best_utility, best_df)
                if best_utility >= self.stop_utility:
                    return best_df, best_utility
            except:
                pass
            try:
                newDf = perturbation_noise_addition(df, col)
                dfResult = self.__achieve_klt__(newDf, k, l, t)
                utility = (float(len(dfResult)) / len(df)) / (perturbation + 0.1)
                if utility > best_utility:
                    best_df = dfResult
                    best_utility = utility
                best_df, best_utility = self.__achieve_klt_backtracking__(start + 1, k, l, t, newDf,
                                                                          perturbation + 0.1,
                                                                          best_utility, best_df)
                if best_utility >= self.stop_utility:
                    return best_df, best_utility
            except:
                pass
            try:
                num_groups = np.arange(0.1, 0.9, 0.2)
                for num_group in num_groups:
                    newDf = perturbation_micro_aggregation(df, col, num_group)
                    dfResult = self.__achieve_klt__(newDf, k, l, t)
                    utility = (float(len(dfResult)) / len(df)) / (perturbation + num_group)
                    if utility > best_utility:
                        best_df = dfResult
                        best_utility = utility
                    best_df, best_utility = self.__achieve_klt_backtracking__(start + 1, k, l, t, newDf,
                                                                              perturbation + num_group,
                                                                              best_utility, best_df)
                    if best_utility >= self.stop_utility:
                        return best_df, best_utility
            except:
                pass
        return best_df, best_utility

    def achieve_klt_random(self, k, l, t, stop_utility=1.0, MAX_ITERS=1000):
        perturbation = 1.0
        df = self.dataframeFinal
        best_df = self.__achieve_klt__(df, k, l, t)
        best_utility = (float(len(best_df)) / len(df)) / perturbation
        self.stop_utility = stop_utility
        for i in range(MAX_ITERS):
            best_df, best_utility = self.__achieve_klt_random__(k, l, t, df, perturbation, best_utility, best_df)
            if best_utility >= self.stop_utility:
                break
        self.dataframeFinal = best_df
        self.get_k_anonymity()
        self.get_l_diversity()
        self.get_t_closeness()
        self.utility = best_utility
        return best_df, best_utility

    def __achieve_klt_random__(self, k, l, t, df, perturbation, best_utility, best_df):
        if best_utility >= self.stop_utility:
            return best_df, best_utility
        list_cols = self.quasi_identifiers_index.copy()
        list_cols.extend(self.sensible_index)
        i = random.randint(0, len(list_cols) - 1)
        col = list_cols[i]
        best_df, best_utility = self.__generate_random_technique__(k, l, t, df, perturbation, best_utility, best_df,
                                                                   col)
        return best_df, best_utility

    def __generate_random_technique__(self, k, l, t, df, perturbation, best_utility, best_df, col):
        n = random.randint(0, 5)
        if n == 0:
            # GENERALIZATION CATEGORIES
            try:
                categories = self.categories_hierarchy.get(col)
                if categories is not None:
                    newDf = generalization_categorical_semantic(df, col, categories)
                    dfResult = self.__achieve_klt__(newDf, k, l, t)
                    utility = (float(len(dfResult)) / len(df)) / (perturbation + 0.1)
                    if utility > best_utility:
                        best_df = dfResult
                        best_utility = utility
                    if best_utility >= self.stop_utility:
                        return best_df, best_utility
            except:
                pass
        elif n == 1:
            # GENERALIZATION NUMERICAL
            try:
                steps = [0.1, 0.2, 0.25, 0.3, 0.4, 0.5]
                n = random.randint(0, len(steps) - 1)
                step = steps[n]
                newDf = generalization_numerical_interval(df, col, step)
                dfResult = self.__achieve_klt__(newDf, k, l, t)
                utility = (float(len(dfResult)) / len(df)) / (perturbation + step * 0.1)
                if utility > best_utility:
                    best_df = dfResult
                    best_utility = utility
                if best_utility >= self.stop_utility:
                    return best_df, best_utility
            except:
                pass
        elif n == 2:
            # GENERALIZATION MASK
            average_length_strings = int(df[col].apply(str).apply(len).mean())
            step = max(int(average_length_strings / 3), 1)
            quantiles = np.arange(1, average_length_strings, step)
            n = random.randint(0, len(quantiles) - 1)
            num_mask = quantiles[n]
            newDf = generalization_mask(df, col, num_mask)
            dfResult = self.__achieve_klt__(newDf, k, l, t)
            utility = (float(len(dfResult)) / len(df)) / (perturbation + (average_length_strings / num_mask * 0.1))
            if utility > best_utility:
                best_df = dfResult
                best_utility = utility
            if best_utility >= self.stop_utility:
                return best_df, best_utility
        # PERTURBATION TECHNIQUES
        elif n == 3:
            try:
                newDf = perturbation_permutation(df, col)
                dfResult = self.__achieve_klt__(newDf, k, l, t)
                utility = (float(len(dfResult)) / len(df)) / (perturbation + 0.1)
                if utility > best_utility:
                    best_df = dfResult
                    best_utility = utility
                if best_utility >= self.stop_utility:
                    return best_df, best_utility
            except:
                pass
        elif n == 4:
            try:
                newDf = perturbation_noise_addition(df, col)
                dfResult = self.__achieve_klt__(newDf, k, l, t)
                utility = (float(len(dfResult)) / len(df)) / (perturbation + 0.1)
                if utility > best_utility:
                    best_df = dfResult
                    best_utility = utility
                if best_utility >= self.stop_utility:
                    return best_df, best_utility
            except:
                pass
        elif n == 5:
            try:
                num_groups = np.arange(0.1, 0.9, 0.2)
                for num_group in num_groups:
                    newDf = perturbation_micro_aggregation(df, col, num_group)
                    dfResult = self.__achieve_klt__(newDf, k, l, t)
                    utility = (float(len(dfResult)) / len(df)) / (perturbation + num_group)
                    if utility > best_utility:
                        best_df = dfResult
                        best_utility = utility
                    if best_utility >= self.stop_utility:
                        return best_df, best_utility
            except:
                pass
        return best_df, best_utility

    def integrate_arx(self):
        """
        integrate ARX
        """
