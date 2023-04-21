from utils.my_io import save_dict_to_json

from shared import config_path


def generate_configuration_file(
    name: str,
    description: str,
    statement: int,
    authorities: list[dict],
    function: dict,
    data: list[dict],
):
    data_dict = {}
    for i, d in enumerate(data):
        data_dict[f"d{i+1}"] = d

    authorities_dict = {}
    for i, d in enumerate(authorities):
        authorities_dict[f"auth_{i+1}"] = d

    json_data = {
        "name": name,
        "description": description,
        "statement": statement,
        "authorities": authorities_dict,
        "function": function,
        "data": data_dict,
    }
    save_dict_to_json(json_data, config_path / (name + ".json"))
