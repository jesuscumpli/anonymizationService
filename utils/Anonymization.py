##########################################
# FUNCTIONS WITH ANONYMITY PROPERTIES  #
##########################################
import numpy as np
import pandas as pd
from scipy import stats

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
    def __init__(self, dataframe, identifiers_index, quasi_identifiers_index, non_sensible_index, sensible_index):
        """
        :param dataframe: Dataframe of the dataset
        :param identifiers_index: column index of identifiers
        :param quasi_identifiers_index: column index of quasi_identifiers
        :param non_sensible_index: column index of non_sensible data
        :param sensible_index: column index of sensible data
        """
        self.dataframeOrigen = dataframe.copy(deep=True)
        self.dataframeFinal = dataframe.copy(deep=True)
        self.groups = None  # List of groups of rows with the same quasi-identifiers
        self.groups_index = None # List of groups of index with the same quasi-identifiers
        self.identifiers_index = identifiers_index
        self.quasi_identifiers_index = quasi_identifiers_index
        self.sensible_index = sensible_index
        self.non_sensible_index = non_sensible_index
        self.generate_groups()

    def generate_groups(self):
        """
        Iterate the self.dataframeFinal and generate a list of groups with the same quasi-identifiers
        """
        self.groups = {}
        self.groups_index = {}
        for index, row in self.dataframeFinal.iterrows():
            valueQuasiIdentifier = ""
            for i in self.quasi_identifiers_index:
                valueQuasiIdentifier += str(row[i])
            if not valueQuasiIdentifier in self.groups:
                self.groups[valueQuasiIdentifier] = []
                self.groups_index[valueQuasiIdentifier] = []
            self.groups[valueQuasiIdentifier].append(row)
            self.groups_index[valueQuasiIdentifier].append(index)

    def achieve_k_anonymity(self, k):
        """
        Get at least k-1 individuals with the same
        quasi-identifiers for each individual in the dataset.
        Delete groups which lower k size array.
        :param k: k value of k-anonymity property
        :return: dataframeFinal
        """
        keys_to_del = []
        for key, value in self.groups.items():
            if len(value) < k:
                self.dataframeFinal.drop(self.groups_index[key], axis=0, inplace=True)
                keys_to_del.append(key)
        for key in keys_to_del:
            del self.groups[key]
            del self.groups_index[key]

    def check_k_anonymity_better(self, k):
        """
        Check if dataframeFinal has k-anonymity property
        :param k: k property
        :return: Boolean
        - Check if the number of unique rows by a list of columns are greater than k
        """
        unique_counts_rows = self.dataframeFinal.value_counts(self.quasi_identifiers_index).tolist()
        return all(n >= k for n in unique_counts_rows)

    def check_k_anonymity(self, k):
        """
        Check if dataframeFinal has k-anonymity property
        :param k: k property
        :return: Boolean
        - Check if each group in self.groups has k samples.
        """
        for key, rows in self.groups_index.items():
            if len(rows) < k:
                return False
        return True

    def achieve_l_diversity(self, l):
        """
        Delete groups; until get at least L different
        values for a sensitive attribute in each group.
        :param l: l-property
        :return: dataframeFinal
        """
        keys_to_del = []
        for key, rows in self.groups.items():
            l_res = 0
            sensitiveValues = {}
            for i in self.sensible_index:
                sensitiveValues[i] = []
            for row in rows:
                for i in self.sensible_index:
                    value = row[i]
                    if value not in sensitiveValues[i]:
                        sensitiveValues[i].append(value)
            for i in self.sensible_index:
                length = len(sensitiveValues[i])
                if length >= l_res:
                    l_res = length
            if l_res < l:
                self.dataframeFinal.drop(self.groups_index[key], axis=0, inplace=True)
                keys_to_del.append(key)
        for key in keys_to_del:
            del self.groups[key]
            del self.groups_index[key]


    def check_l_diversity(self, l):
        """
        Check if dataframeFinal has l-diversity property.
        - Check if each group in self.groups has l samples with different sensitive values.
        :param l: l property
        :return: Boolean
        """
        for key, rows in self.groups.items():
            l_res = 0
            sensitiveValues = {}

            for i in self.sensible_index:
                sensitiveValues[i] = []

            for row in rows:
                for i in self.sensible_index:
                    value = row[i]
                    if value not in sensitiveValues[i]:
                        sensitiveValues[i].append(value)

            for i in self.sensible_index:
                length = len(sensitiveValues[i])
                if length >= l_res:
                    l_res = length
            if l_res < l:
                return False
        return True

    def achieve_t_closeness(self, t):
        """
        Delete all the groups has not a similar distribution of dataframeOrigen.
        :param t: t-property
        :return: dataframeFinal
        """
        keys_to_del = []
        for key, rows in self.groups.items():
            df = pd.DataFrame(rows)
            for col in self.sensible_index:
                statistic, pvalue = stats.ks_2samp(self.dataframeOrigen[col], df[col])
                if pvalue <= t:
                    self.dataframeFinal.drop(self.groups_index[key], axis=0, inplace=True)
                    keys_to_del.append(key)
                    break
        for key in keys_to_del:
            del self.groups[key]
            del self.groups_index[key]

    def check_t_closeness(self, t):
        """
        Check if dataframeFinal has t-closeness property
        - Check if each group in self.groups has the same distribution with the self.dataframeOrigen
        :param t: t property
        :return: Boolean
        """
        for key, rows in self.groups.items():
            df2 = pd.DataFrame(rows)
            for col in self.sensible_index:
                statistic, pvalue = stats.ks_2samp(self.dataframeOrigen[col], df2[col])
                if pvalue <= t:
                    return False
        return True

    def integrate_arx(self):
        """
        integrate ARX
        """
