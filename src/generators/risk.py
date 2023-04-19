from utils.sign import gen_key_pairs
from utils.generate_configs import generate_configuration_json
import numpy as np
import codecs


def generate_risk(name: str):
    # This script generates the data for the risk score function

    N_POSITIONS = 3  # number of positions in each individual's array
    N_INDIVIDUALS = 2  # number of individuals in the list
    PRECISION = 1

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
            "description": "Alleles of individuals",
            "values": individuals_int,
            "type": "int",
            "format": "u8",
            "shape": [N_POSITIONS, N_INDIVIDUALS],
        },
        {
            "description": "Beta values",
            "values": betas_int,
            "type": "double",
            "precision": PRECISION,
            "format": "u8",
            "shape": [N_POSITIONS, 1],
        },
    ]

    # Generate key-pairs
    priv_key, pub_key = gen_key_pairs()

    # Convert the public key into its `x` and `y` points
    pub_key_bytes = codecs.decode(pub_key[2:], "hex_codec")
    pub_key_x = "0x" + "".join("{:02x}".format(x) for x in pub_key_bytes[0:32])
    pub_key_y = "0x" + "".join("{:02x}".format(x) for x in pub_key_bytes[32:64])

    generate_configuration_json(
        name=name,
        description="computes the average risk scores of a population",
        pub_key_x=pub_key_x,
        pub_key_y=pub_key_y,
        private_key=priv_key,
        statement=result,
        data=data,
    )
