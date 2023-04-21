from utils.genhash import get_hash_simple
from utils.sign import sign


def sign_data(authority: dict, data_dict: dict) -> tuple[list[int], list[str]]:
    # Concatenate all data["values"] into one big list
    data_list = []
    for data in data_dict.values():
        data_list.extend(data["values"])

    # Compute hash only of individuals_int for simplicity (related to noir bug)
    data_hash_int, data_hash_hex = get_hash_simple(data_list)

    # Sign private_data
    data_signature = sign("".join(data_hash_hex), authority["private_key"])

    return data_hash_int, data_signature
