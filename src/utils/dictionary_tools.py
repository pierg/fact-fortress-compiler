def extract_data_labels_from_config(input_dict):
    if "data" in input_dict:
        return set(input_dict["data"].keys())
    else:
        return set()
