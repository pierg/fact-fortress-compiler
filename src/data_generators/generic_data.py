import numpy as np


def generate_data(input_dict: dict):
    """
    Given a dictionary of input data, this function generates a dictionary of output data
    with additional information, such as a description of the data and randomly generated
    values within a specified range.

    Parameters:
    input_dict (dict): A dictionary containing information about the input data.

    Returns:
    dict: A dictionary containing information about the output data.

    Example:
    input_dict = {
        "d1": {
            "name": "Data_1",
            "provider": "Provider_A",
            "type": "int",
            "bits": 8,
            "shape": [4, 3],
            "range": [0, 10],
        },
        "d2": {
            "name": "Data_2",
            "provider": "Provider_A",
            "type": "double",
            "bits": 32,
            "shape": [3, 1],
            "range": [0, 800],
            "precision": 2,
        },
    }

    output_dict = process_data(input_dict)

    print(output_dict)

    Output:
    {
        "d1": {
            "name": "Data_1",
            "description": "Two-dimensional matrix with shape [4, 3]",
            "provider": "Provider_A",
            "values": [2, 4, 7, 2, 4, 8, 4, 0, 4, 5, 9, 3],
            "type": "int",
            "format": "u8",
            "shape": [4, 3],
        },
        "d2": {
            "name": "Data_2",
            "description": "Vector of quantized double of 3 elements",
            "provider": "Provider_A",
            "values": [472, 284, 589],
            "type": "double",
            "precision": 2,
            "format": "u32",
            "shape": [3, 1],
        },
    }
    """

    output_dict = {}

    for key, value in input_dict.items():
        output_dict[key] = {}

        output_dict[key]["name"] = value["name"]
        output_dict[key]["provider"] = value["provider"]
        output_dict[key]["type"] = value["type"]
        output_dict[key]["shape"] = value["shape"]

        if "precision" in value:
            output_dict[key]["precision"] = value["precision"]

        output_dict[key]["format"] = f"u{value['bits']}"

        # Process the range and values fields
        range_start, range_end = map(int, value["range"])

        num_elements = 1

        for dim in value["shape"]:
            num_elements *= dim

        num_elements = int(num_elements)

        if "precision" in value:
            # Generates random integers between (value["range"][0] * value["precision"] * 10) and ( value["range"][1] * value["precision"] * 10)
            output_dict[key]["values"] = (
                np.random.randint(
                    range_start * value["precision"] * 10,
                    (range_end) * value["precision"] * 10,
                    size=num_elements,
                )
                / value["precision"]
            ).tolist()
        else:
            # Generates random integers between value["range"][0] and value["range"][1]
            output_dict[key]["values"] = np.random.randint(
                range_start, range_end, size=num_elements
            ).tolist()

        # Generate the description field based on the data type and shape
        if len(value["shape"]) == 1:
            output_dict[key][
                "description"
            ] = f"Vector of quantized {value['type']} of {value['shape'][0]} elements"
        else:
            output_dict[key][
                "description"
            ] = f"Two-dimensional matrix with shape {value['shape']}"

    return output_dict
