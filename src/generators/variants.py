from utils.generate_configs import generate_configuration_json
import numpy as np
from utils.authorities import generate_authority


def generate_variants(name: str):
    # This script generates the data for the variants analysis function

    authorities = []

    new_authority = generate_authority("Clinic_A")
    authorities.append(new_authority)

    new_authority = generate_authority("Clinic_B")
    authorities.append(new_authority)

    N_POSITIONS = 10  # number of positions in each individual's array
    N_INDIVIDUALS = 2  # number of individuals in the list
    PRECISION = 1

    # Generate individuals
    individuals_a = np.random.randint(0, 4, size=N_INDIVIDUALS)

    individuals_b = np.random.randint(0, 4, size=N_INDIVIDUALS)

    # Example of how to compute the variants in the genome
    # TODO
    result = 10

    # example usage
    data = [
        {
            "name": "Genome_individuals_CA",
            "description": "Genome sequence of individuals from Clinic A",
            "provider": "Clinic_A",
            "values": individuals_a.tolist(),
            "type": "int",
            "format": "u8",
            "shape": [N_INDIVIDUALS, 1],
        },
        {
            "name": "Genome_individuals_CB",
            "description": "Genome sequence of individuals from Clinic B",
            "provider": "Clinic_B",
            "values": individuals_b.tolist(),
            "type": "int",
            "format": "u8",
            "shape": [N_INDIVIDUALS, 1],
        },
    ]

    generate_configuration_json(
        name=name,
        description="computes the average risk scores of a population",
        authorities=authorities,
        statement=result,
        data=data,
    )
