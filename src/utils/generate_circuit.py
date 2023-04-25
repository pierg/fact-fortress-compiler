import json
from pathlib import Path
from utils.genhash import get_hash_simple
from utils.sign import sign
from utils.noir import generate_noir_files

import os
from shared import circuits_path


def generate_circuit(config_path: Path, circuits_folder: Path = circuits_path):
    """
    Generates the circuit and the noir files for the given config.
    """

    # Read from JSON and create dict
    with open(config_path) as f:
        configuration = json.load(f)

    noir_circuit_path = circuits_folder / configuration["name"]

    if os.path.exists(noir_circuit_path):
        print(f"{noir_circuit_path} circuit has already been generated")
        return

    generate_noir_files(
        config=configuration,
        circuit_path=noir_circuit_path,
    )
