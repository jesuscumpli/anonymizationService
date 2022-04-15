import random
import pandas as pd
import random
import hmac
import hashlib
from cryptography.fernet import Fernet

################################################################################
# FUNCTIONS TO SUBSTITUTE IDENTIFIERS WITH A REVERSIBLE AND SECURE PSEUDONYM   #
#########################################################################################
# TECHNIQUES BASED ON Guidelines on shaping technology according to GDPR provisions.pdf #
#########################################################################################
from utils.techniques.generateKeys import load_secret_key, load_encription_key

"""
input dataframe: dataset origen
input identifiers: column index from dataframe which are identifiers
objective: apply a pseudonymous technique to the specified identifiers columns
:return: Dataframe
"""


def pseudonymization_counter(dataframe, identifier):
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


def pseudonymization_rng(dataframe, identifier):
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


def pseudonymization_hmac(dataframe, identifier):
    """
    MAC is generally considered as a robust pseudonymisation technique from a data protection point of view, since
    reverting the pseudonym is infeasible, as long as the key has not be compromised.
    """
    secret_key = load_secret_key()
    digest_maker = hmac.new(secret_key, b'', hashlib.sha256)
    dfFinal = dataframe.copy(deep=True)
    for index, row in dfFinal.iterrows():
        msg = str(row[identifier])
        msg_bytes = msg.encode()
        digest_maker.update(msg_bytes)
        dfFinal[identifier][index] = digest_maker.hexdigest()
    return dfFinal


def pseudonymization_encryption(dataframe, identifier):
    """
    Fernet guarantees that a message encrypted using it cannot be manipulated or read without the key.
    Fernet is an implementation of symmetric (also known as “secret key”) authenticated cryptography.
    """
    encription_key = load_encription_key()
    fernet = Fernet(encription_key)
    dfFinal = dataframe.copy(deep=True)
    for index, row in dfFinal.iterrows():
        msg = str(row[identifier])
        msg_bytes = msg.encode()
        encMsg = fernet.encrypt(msg_bytes)
        dfFinal[identifier][index] = encMsg.decode()
    return dfFinal


def revert_pseudonymization_with_mapping_table(dfFinal, dfMapping, identifier):
    dfReversible = dfFinal.copy(deep=True)
    for index, row in dfMapping.iterrows():
        dfReversible.loc[dfReversible[identifier] == row["final"], identifier] = row["origen"]
    return dfReversible


def revert_pseudonymization_hmac(dfOrigen, dfFinal, identifier):
    secret_key = load_secret_key()
    digest_maker = hmac.new(secret_key, b'', hashlib.sha256)
    dfReversible = dfFinal.copy(deep=True)
    for index, row in dfOrigen.iterrows():
        msg = str(row[identifier])
        msg_bytes = msg.encode()
        digest_maker.update(msg_bytes)
        digest = digest_maker.hexdigest()
        dfReversible.loc[dfReversible[identifier] == digest, identifier] = row[identifier]
    return dfReversible


def revert_pseudonymization_encryption(dfFinal, identifier):
    key = load_encription_key()
    fernet = Fernet(key)
    dfReversible = dfFinal.copy(deep=True)
    for index, row in dfReversible.iterrows():
        msg = str(row[identifier])
        msg_bytes = msg.encode()
        decMsg = fernet.decrypt(msg_bytes)
        dfReversible[identifier][index] = decMsg.decode()
    return dfReversible
