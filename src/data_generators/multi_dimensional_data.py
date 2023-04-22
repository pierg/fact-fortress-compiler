from utils.generate_configs import generate_configuration_file
import numpy as np
from utils.authorities import generate_authority


def generate_multi_dimensional_data(
    authority: dict,
    shape_1: int = 2,
    shape_2: int = 4,
    precision: int = 2,
) -> dict:
    """
    Generate synthetic example data for a given number of individuals.'
    The data generates contains:
        - data_1 counts for each genome position in each individual
        - data_2 values for each position, i.e. the function_1 associated the specific position

    Args:
        authority (str): Authority generatng the data
        n_positions (int): Number of example positions to simulate.
        n_individuals (int): Number of individuals to simulate.
        precision (int): Decimal precision to use when quantifying data_2 values.

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
    # This script generates the data for the function_1 function

    N_POSITIONS = shape_1  # number of positions in each individual's array
    N_INDIVIDUALS = shape_2  # number of individuals in the list
    PRECISION = precision

    # Generate individuals
    individuals = np.random.randint(0, 3, size=(N_INDIVIDUALS, N_POSITIONS))

    # Generate data_2 values
    data_2s = np.abs(np.random.normal(0, 1, size=N_POSITIONS))

    # Approximate data_2 values with integers with three decimal points precision
    data_2s_int = np.around(data_2s * (PRECISION * 10)).astype(int).tolist()

    # Compute individuals_int
    individuals_int = np.ravel(individuals).astype(int).tolist()

    # example usage
    data = {
        "d1": {
            "name": "Data_1",
            "description": f"Two-dimensional matrix from {authority['name']}",
            "provider": authority["name"],
            "values": individuals_int,
            "type": "int",
            "format": "u8",
            "shape": [N_POSITIONS, N_INDIVIDUALS],
        },
        "d2": {
            "name": "Data_2",
            "description": f"Vector of quantized double from {authority['name']}",
            "provider": authority["name"],
            "values": data_2s_int,
            "type": "double",
            "precision": PRECISION,
            "format": "u8",
            "shape": [N_POSITIONS, 1],
        },
    }
    return data
