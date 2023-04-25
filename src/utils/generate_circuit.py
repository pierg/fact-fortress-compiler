from pathlib import Path
from utils.genhash import get_hash_simple
from utils.sign import sign
from utils.noir import generate_noir_files

import os
from shared import circuits_path


def generate_circuit(config: dict, circuit_path: Path = circuits_path):
    """
    Generates the circuit and the noir files for the given config.

    """

    noir_circuit_path = circuit_path / config["name"]
    if os.path.exists(noir_circuit_path):
        print(f"{noir_circuit_path} is not empty")
        return

    print("generating")
    generate_noir_files(
        config=config,
        circuit_path=noir_circuit_path,
    )
