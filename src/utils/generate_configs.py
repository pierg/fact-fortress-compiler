from pathlib import Path
from utils.my_io import save_dict_to_json

from shared import config_path


def generate_configuration_file(
    name: str,
    description: str,
    data_hash: list[int],
    signature: list[str],
    statement: int,
    authorities: list[dict],
    function: dict,
    data: dict,
    info: dict | None,
    provenance: bool = True,
) -> Path:
    authorities_dict = {}
    for i, d in enumerate(authorities):
        authorities_dict[f"auth_{i+1}"] = d

    json_data = {
        "name": name,
        "description": description,
        "data_hash": data_hash,
        "signature": signature,
        "statement": statement,
        "authorities": authorities_dict,
        "function": function,
        "data": data,
        "info": info,
        "provenance": provenance,
    }
    return save_dict_to_json(json_data, config_path / (name + ".json"))
