from utils.genhash import get_hash_simple
from utils.sign import sign
from utils.noir import generate_noir_files

import os
from shared import circuits_path


def generate_circuit(config: dict, data_hash: list[int], signature: tuple[str]):
    """
    Generates the circuit and the noir files for the given config.

    """

    noir_circuit_path = circuits_path / config["name"]
    if os.path.exists(noir_circuit_path):
        print(f"{noir_circuit_path} is not empty")
        return

    # Concatenate all data["values"] into one big list
    data_list = []
    for data in config["data"].values():
        data_list.extend(data["values"])

    # Compute hash only of individuals_int for simplicity (related to noir bug)
    data_hash_int, data_hash_hex = get_hash_simple(data_list)

    # Sign private_data
    data_signature = sign(
        "".join(data_hash_hex), config["authorities"]["auth_1"]["private_key"]
    )

    print("generating")
    generate_noir_files(
        config=config,
        data_hash=data_hash_int,
        data_signature=data_signature,
        circuit_path=noir_circuit_path,
    )
