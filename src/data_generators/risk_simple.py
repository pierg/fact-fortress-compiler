from utils.generate_configs import generate_configuration_file
import numpy as np
from utils.authorities import generate_authority


def generate_risk_simple(name: str, function: dict):
    # This script generates the data for the function_1 function

    authorities = []

    new_authority = generate_authority("Authority_A")
    authorities.append(new_authority)

    N_POSITIONS = 2  # number of positions in each individual's array
    N_INDIVIDUALS = 4  # number of individuals in the list
    PRECISION = 2

    # Generate individuals
    individuals = np.random.randint(0, 3, size=(N_INDIVIDUALS, N_POSITIONS))

    # Generate data_2 values
    data_2s = np.abs(np.random.normal(0, 1, size=N_POSITIONS))

    # Example of how to compute function_1s for each individual
    risk_scores = []
    for i in range(N_INDIVIDUALS):
        individual = individuals[i]
        risk_score = np.dot(individual, data_2s)
        risk_scores.append(risk_score)

    # Average of scores approximated to integer
    result = round(np.mean(risk_scores) * (PRECISION * 10))

    # Approximate data_2 values with integers with three decimal points precision
    data_2s_int = np.around(data_2s * (PRECISION * 10)).astype(int).tolist()

    # Compute individuals_int
    individuals_int = np.ravel(individuals).astype(int).tolist()

    # example usage
    data = [
        {
            "name": "Datas_HA",
            "description": "Datas of individuals from Authority A",
            "provider": "Authority_A",
            "values": individuals_int,
            "type": "int",
            "format": "u8",
            "shape": [N_POSITIONS, N_INDIVIDUALS],
        },
        {
            "name": "Beta_HA",
            "description": "Beta values of heart conditions from Authority A",
            "provider": "Authority_A",
            "values": data_2s_int,
            "type": "double",
            "precision": PRECISION,
            "format": "u8",
            "shape": [N_POSITIONS, 1],
        },
    ]

    generate_configuration_file(
        name=name,
        description="computes the average function_1s of a population",
        authorities=authorities,
        statement=result,
        data=data,
        function=function,
    )
