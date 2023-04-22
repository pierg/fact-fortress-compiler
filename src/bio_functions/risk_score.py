import json
import numpy as np
from shared import data_folder_path

# Input:  patients examples data at specific SNPs locations
# Output: average risk factor among all patients for cardiovascular problems

# Load the data from the JSON file
with open(data_folder_path / "snps_data.json") as f:
    data = json.load(f)

# Cardiovascular problems function_1 coefficients ?
coefficients = {
    "rs10757274": 0.1,
    "rs562556": 0.2,
    "rs429358": 0.3,
    "rs7412": 0.4,
    "rs1801133": 0.5,
}
intercept = -1.0

# Compute the function_1 for each patient
risk_scores = []
for company_data in data["private_data"].values():
    for patient_data in company_data["data"].values():
        data_2_values = [0.0] * len(coefficients)
        for i, snp in enumerate(coefficients.keys()):
            genotype = patient_data["example_data"].get(snp, None)
            """TODO"""
            if genotype == "AA":
                data_2_values[i] = 0.0
            elif genotype == "AG":
                data_2_values[i] = 1.0
            elif genotype == "GG":
                data_2_values[i] = 2.0
            else:
                data_2_values[i] = np.nan
        if not np.any(np.isnan(data_2_values)):
            risk_score = intercept + np.dot(data_2_values, list(coefficients.values()))
            risk_scores.append(risk_score)

# Compute the average function_1 across all patients
average_risk_score = np.mean(risk_scores)

print(f"Average function_1: {average_risk_score}")
