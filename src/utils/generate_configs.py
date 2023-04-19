import json

from utils.my_io import save_dict_to_json

from shared import config_path


def generate_configuration_json(
    name: str, description: str, pub_key_x: str, pub_key_y: str, private_key: str, statement: int, data: list
):
    data_dict = {}
    for i, d in enumerate(data):
        data_dict[f"d{i+1}"] = d

    json_data = {
        "name": name,
        "description": description,
        "keys": {"pub_key_x": pub_key_x, "pub_key_y": pub_key_y, "private_key": private_key},
        "statement": statement,
        "data": data_dict,
    }
    save_dict_to_json(json_data, config_path / (name + ".json"))
