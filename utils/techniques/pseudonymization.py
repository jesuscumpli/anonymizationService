import random
import pandas as pd
import random

################################################################################
# FUNCTIONS TO SUBSTITUTE IDENTIFIERS WITH A REVERSIBLE AND SECURE PSEUDONYM   #
#########################################################################################
# TECHNIQUES BASED ON Guidelines on shaping technology according to GDPR provisions.pdf #
#########################################################################################

"""
input dataframe: dataset origen
input identifiers: column index from dataframe which are identifiers
objective: apply a pseudonymous technique to the specified identifiers columns
:return: Dataframe
"""


def counter_pseudonymization(dataframe, identifier):
    """
    Counter is the simplest pseudonymous function. The identifiers are substituted by a number
     chosen by a monotonic counter. First, a seed 𝑠 is set to 0 (for instance) and then it is incremented.
     It is critical that the values produced by the counter never repeat to prevent any ambiguity.
    """
    dfFinal = dataframe.copy(deep=True)
    dfFinal = dfFinal.sample(frac=1).reset_index(drop=True)  # Shuffle rows
    mapping_table = {
        "origen": [],
        "final": []
    }
    counter = 1
    for index, row in dfFinal.iterrows():
        mapping_table["origen"].append(dfFinal[identifier][index])
        dfFinal[identifier][index] = counter
        mapping_table["final"].append(counter)
        counter += 1
    dfMapping = pd.DataFrame(mapping_table)
    return dfFinal, dfMapping


def rng_pseudonymization(dataframe, identifier):
    """
    Two options are available to create this mapping: a true random number generator or a cryptographic pseudo-random
    generator. It should be noted that in both cases, without due care, collisions can occur.
    """
    dfFinal = dataframe.copy(deep=True)
    random.seed()
    limit = len(dfFinal) * 3  # Multiply for 3 to avoid a big number of collisions
    mapping_table = {
        "origen": [],
        "final": []
    }
    for index, row in dfFinal.iterrows():
        mapping_table["origen"].append(dfFinal[identifier][index])
        pseudo_number = random.randint(1, limit)
        dfFinal[identifier][index] = pseudo_number
        mapping_table["final"].append(pseudo_number)
    dfMapping = pd.DataFrame(mapping_table)
    return dfFinal, dfMapping


def pseudonymization_mac(dataframe, identifiers):
    pass


def pseudonymization_encryption(dataframe, identifiers):
    pass


def pseudonymization_email(dataframe, identifiers):
    pass


def pseudonymization_ip_address(dataframe, identifiers):
    pass


def revert_pseudonymization_with_mapping_table(dfFinal, dfMapping, identifier):
    dfReversible = dfFinal.copy(deep=True)
    for index, row in dfMapping.iterrows():
        dfReversible.loc[dfReversible[identifier] == row["final"], identifier] = row["origen"]
    return dfReversible
