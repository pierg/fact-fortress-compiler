from utils.genhash import get_hash_simple
from utils.sign import sign
from utils.noir import generate_noir_files


from shared import circuits_path


def generate_circuit(config: dict):
    """
    Generates the circuit and the noir files for the given config.

    """

    noir_circuit_path = circuits_path / config["name"]

    # Concatenate all data["values"] into one big list
    data_list = []
    for data in config["data"].values():
        data_list.extend(data["values"])

    # Compute hash only of individuals_int for simplicity (related to noir bug)
    data_hash_int, data_hash_hex = get_hash_simple(data_list)

    # Sign private_data
    data_signature = sign("".join(data_hash_hex), config["keys"]["private_key"])

    print("generating")
    generate_noir_files(
        config=config,
        data_hash=data_hash_int,
        data_signature=data_signature,
        circuit_path=noir_circuit_path,
    )


# Generate circuit
config = {
    "name": "circuit_test",
    "description": "Computes the risk score of a group of people",
    "data": {
        "d1": {
            "description": "Alleles of individuals",
            "values": [2, 1, 0, 1, 1, 0],
            "type": "int",
            "format": "u8",
            "shape": [2, 3],
        },
        "d2": {
            "description": "Risk factor",
            "values": [24, 55],
            "type": "double",
            "precision": 1,
            "format": "u8",
            "shape": [2, 1],
        },
    },
    "statement": 24,
    "keys": {
        "pub_key_x": "0x0",
        "pub_key_y": "0x0",
        "private_key": "0x0",
    },
}
generate_circuit(config=config)
