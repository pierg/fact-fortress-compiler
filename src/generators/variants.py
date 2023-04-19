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

    N_POSITIONS = 5  # number of positions in each individual's array
    N_INDIVIDUALS = 5  # number of individuals in the list

    # Generate individuals
    individuals_a = np.random.randint(0, 4, size=(N_INDIVIDUALS, N_POSITIONS))
    individuals_b = np.random.randint(0, 4, size=(N_INDIVIDUALS, N_POSITIONS))

    # Example of how to compute the variants in the genome
    # TODO
    result = 10

    individuals_int_a = np.ravel(individuals_a).astype(int).tolist()

    individuals_int_b = np.ravel(individuals_b).astype(int).tolist()

    # example usage
    data = [
        {
            "name": "Genome_individuals_CA",
            "description": "Genome sequence of individuals from Clinic A",
            "provider": "Clinic_A",
            "values": individuals_int_a,
            "type": "int",
            "format": "u8",
            "shape": [N_INDIVIDUALS, N_POSITIONS],
        },
        {
            "name": "Genome_individuals_CB",
            "description": "Genome sequence of individuals from Clinic B",
            "provider": "Clinic_B",
            "values": individuals_int_b,
            "type": "int",
            "format": "u8",
            "shape": [N_INDIVIDUALS, N_POSITIONS],
        },
    ]

    generate_configuration_json(
        name=name,
        description="analyse the variants in the genomes of the individuals",
        authorities=authorities,
        statement=result,
        data=data,
    )
