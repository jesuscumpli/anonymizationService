import pandas as pd

from utils.techniques.perturbation import perturbation_micro_aggregation

""""
dfOrigen = pd.read_csv("../datasets/Customer_Behaviour.csv")
dfFinal = perturbation_noise_addition(dfOrigen, "Purchased")
dfFinal = perturbation_noise_addition(dfOrigen, "Age")
dfFinal = perturbation_noise_addition(dfOrigen, "EstimatedSalary")
"""
dfOrigen = pd.read_csv("../datasets/Churn Modeling.csv")
print(dfOrigen)
dfFinal = perturbation_micro_aggregation(dfOrigen, "NumOfProducts", 0.10)
print(dfFinal)
