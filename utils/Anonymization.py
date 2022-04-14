##########################################
# FUNCTIONS WITH ANONYMITY PROPERTIES  #
##########################################

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
        self.groups = None  # List of groups of samples with the same quasi-identifiers
        self.identifiers_index = identifiers_index
        self.quasi_identifiers_index = quasi_identifiers_index
        self.sensible_index = sensible_index
        self.non_sensible_index = non_sensible_index

    def generate_groups(self):
        """
        Iterate the self.dataframeFinal and generate a list of groups with the same quasi-identifiers
        """
        self.groups = []
        pass

    def achieve_k_anonymity(self, k):
        """
        Apply diferent techniques in the dataframe Origen until get at least k-1 individuals with the same
        quasi-identifiers for each individual in the dataset.
        - Check if each group in self.groups has k samples.
        :param k: k value of k-anonymity property
        :return: dataframeFinal
        """
        pass

    def check_k_anonymity(self, k):
        """
        Check if dataframeFinal has k-anonymity property
        :param k: k property
        :return: Boolean
        """
        pass

    def achieve_l_diversity(self, l):
        """
        Apply diferent techniques in the dataframe Origen until get at least L different
        values for a sensitive attribute in each group.
        :param l: l-property
        :return: dataframeFinal
        """
        pass

    def check_l_diversity(self, k):
        """
        Check if dataframeFinal has l-diversity property.
        - Check if each group in self.groups has l samples with different sensitive values.
        :param l: l property
        :return: Boolean
        """
        pass

    def achieve_t_closeness(self, t):
        """
        Apply diferent techniques in the dataframeOrigen until get all the groups has a similar distribution of
        dataframeOrigen.
        :param t: t-property
        :return: dataframeFinal
        """
        pass

    def check_t_closeness(self, k):
        """
        Check if dataframeFinal has l-diversity property
        - Check if each group in self.groups has the same distribution with the self.dataframeOrigen
        :param t: t property
        :return: Boolean
        """
        pass

    def integrate_arx(self):
        """
        integrate ARX
        """