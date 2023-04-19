import argparse
from shared import config_path
from utils.generate_circuit import generate_circuit
import json


def gen_circuit(file_name: str) -> int:
    file_path = config_path / (file_name + ".json")

    # Read from JSON and create dict
    with open(file_path) as f:
        configuration = json.load(f)

    generate_circuit(config=configuration)


def generate_cli(args: str) -> int:
    parser = argparse.ArgumentParser(prog="noir_zkp")
    parser.add_argument("file_name", type=str, help="File name of the configuration file")
    opts = parser.parse_args(args=args)

    file_path = config_path / (opts.file_name + ".json")

    gen_circuit(file_path)
