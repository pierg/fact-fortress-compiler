from utils.generate_configs import generate_configuration_file
import numpy as np
from utils.authorities import generate_authority


def generate_risk_data(
    authority: dict,
    n_positions: int = 2,
    n_individuals: int = 4,
    precision: int = 2,
) -> dict:
    """
    Generate synthetic genetic data for a given number of individuals.'
    The data generates contains:
        - allele counts for each genome position in each individual
        - beta values for each position, i.e. the risk score associated the specific position

    Args:
        authority (str): Authority generatng the data
        n_positions (int): Number of genetic positions to simulate.
        n_individuals (int): Number of individuals to simulate.
        precision (int): Decimal precision to use when quantifying beta values.

    Returns:
        data (dict): A dictionary representing the data our standard format.
                The keys should be strings representing the data IDs, and the values should be dictionaries with the following keys:
                    - "name": The name of the data (str).
                    - "description": A brief description of the data (str).
                    - "provider": The name of the data provider (str).
                    - "values": A list of values associated with the data.
                    - "type": The data type of the values (str).
                    - "format": The format of the values (str).
                    - "shape": A list representing the shape of the data (list of integers).
    """
    # This script generates the data for the risk score function

    N_POSITIONS = n_positions  # number of positions in each individual's array
    N_INDIVIDUALS = n_individuals  # number of individuals in the list
    PRECISION = precision

    # Generate individuals
    individuals = np.random.randint(0, 3, size=(N_INDIVIDUALS, N_POSITIONS))

    # Generate beta values
    betas = np.abs(np.random.normal(0, 1, size=N_POSITIONS))

    # Approximate beta values with integers with three decimal points precision
    betas_int = np.around(betas * (PRECISION * 10)).astype(int).tolist()

    # Compute individuals_int
    individuals_int = np.ravel(individuals).astype(int).tolist()

    # example usage
    data = [
        {
            "name": "Alleles",
            "description": f"Alleles of individuals from {authority['name']}",
            "provider": authority["name"],
            "values": individuals_int,
            "type": "int",
            "format": "u8",
            "shape": [N_POSITIONS, N_INDIVIDUALS],
        },
        {
            "name": "Beta",
            "description": f"Beta values of heart conditions from {authority['name']}",
            "provider": authority["name"],
            "values": betas_int,
            "type": "double",
            "precision": PRECISION,
            "format": "u8",
            "shape": [N_POSITIONS, 1],
        },
    ]
    return data
