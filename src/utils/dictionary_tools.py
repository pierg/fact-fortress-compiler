def extract_data_labels_from_config(input_dict) -> list[str]:
    if "data" in input_dict:
        return list(input_dict["data"].keys())
    else:
        return []
