from utils.generate_configs import generate_configuration_json
import numpy as np
from utils.authorities import generate_authority


def generate_risk(name: str):
    # This script generates the data for the risk score function

    authorities = []

    new_authority = generate_authority("Hospital_A")
    authorities.append(new_authority)

    N_POSITIONS = 5  # number of positions in each individual's array
    N_INDIVIDUALS = 10  # number of individuals in the list
    PRECISION = 2

    # Generate individuals
    individuals = np.random.randint(0, 3, size=(N_INDIVIDUALS, N_POSITIONS))

    # Generate beta values
    betas = np.abs(np.random.normal(0, 1, size=N_POSITIONS))

    # Example of how to compute risk scores for each individual
    risk_scores = []
    for i in range(N_INDIVIDUALS):
        individual = individuals[i]
        risk_score = np.dot(individual, betas)
        risk_scores.append(risk_score)

    # Average of scores approximated to integer
    result = round(np.mean(risk_scores) * (PRECISION * 10))

    # Approximate beta values with integers with three decimal points precision
    betas_int = np.around(betas * (PRECISION * 10)).astype(int).tolist()

    # Compute individuals_int
    individuals_int = np.ravel(individuals).astype(int).tolist()

    # example usage
    data = [
        {
            "name": "Alleles_HA",
            "description": "Alleles of individuals from Hospital A",
            "provider": "Hospital_A",
            "values": individuals_int,
            "type": "int",
            "format": "u8",
            "shape": [N_POSITIONS, N_INDIVIDUALS],
        },
        {
            "name": "Beta_HA",
            "description": "Beta values of heart conditions from Hospital A",
            "provider": "Hospital_A",
            "values": betas_int,
            "type": "double",
            "precision": PRECISION,
            "format": "u8",
            "shape": [N_POSITIONS, 1],
        },
    ]

    generate_configuration_json(
        name=name,
        description="computes the average risk scores of a population",
        authorities=authorities,
        statement=result,
        data=data,
    )
