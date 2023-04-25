from pathlib import Path
import os

from circuit_functions_library.dot_product import generate_dot_product_multi
from shared import Aggregator, Functions
from .dictionary_tools import extract_data_labels_from_config
from .my_io import save_dict_to_json, save_dict_to_toml


def generate_noir_files(config: dict, circuit_path: Path):
    generate_project(config, circuit_path)
    generate_input_file(config, circuit_path)
    generate_data_file(config, circuit_path)
    generate_main_file(config, circuit_path)
    generate_info_file(config, circuit_path)


def generate_info_file(config: dict, circuit_path: Path):
    # extract relevant information
    function_name = config["name"]
    function_description = config["description"]
    data = []
    for data_key, data_value in config["data"].items():
        data.append(
            {
                "name": data_value["name"],
                "description": data_value["description"],
                "provider": data_value["provider"],
            }
        )

    # create output JSON object
    if "info" in config:
        output_data = {
            "function": {"name": function_name, "description": function_description},
            "info": config["info"],
        }
    else:
        output_data = {
            "function": {"name": function_name, "description": function_description},
            "data": data,
        }

    save_dict_to_json(output_data, circuit_path / "info.json")
    save_dict_to_json(config, circuit_path / "config.json")
    generate_prove_script(circuit_path)
    generate_verify_script(circuit_path)


def generate_prove_script(folder_path: Path):
    script = "#!/bin/bash\n"
    script += "nargo prove p\n"
    script += "if [ $? -eq 0 ]; then\n"
    script += '\techo "SUCCESS"\n'
    script += "else\n"
    script += '\techo "FAIL"\n'
    script += "fi\n"
    with open(str(folder_path / "prove.sh"), "w") as file:
        file.write(script)


def generate_verify_script(folder_path: Path):
    script = "#!/bin/bash\n"
    script += "nargo verify p\n"
    script += "if [ $? -eq 0 ]; then\n"
    script += '\techo "SUCCESS"\n'
    script += "else\n"
    script += '\techo "FAIL"\n'
    script += "fi\n"
    with open(str(folder_path / "verify.sh"), "w") as file:
        file.write(script)


def generate_project(config: dict, circuit_path: Path):
    if not os.path.exists(circuit_path):
        os.makedirs(circuit_path)
        os.makedirs(circuit_path / "src")
    file_path = circuit_path / "Nargo.toml"

    compiler_version = "0.4"
    authors = ""
    if "noir" in config:
        noir_config = config["noir"]
        if "version" in noir_config:
            compiler_version = noir_config["version"]
        else:
            compiler_version = "0.4"
        if "authors" in noir_config:
            authors = noir_config["authors"]
        else:
            authors = ""

    with open(str(file_path), "w") as f:
        f.write(
            f"""
[package]
authors = ["{authors}"]
compiler_version = "{compiler_version}"

[dependencies]
            """
        )


def generate_input_file(config: dict, circuit_path: Path):
    # Save individuals and data_2s to a TOML file
    noir_data = {
        "public": {
            "keys": {
                "pub_key_x": config["authorities"]["auth_1"]["pub_key_x"],
                "pub_key_y": config["authorities"]["auth_1"]["pub_key_y"],
            },
            "statement": {"value": config["statement"]},
        },
        "private": {
            "provenance": {
                "signature": config["signature"],
                "hash": config["data_hash"],
            },
            "data": {},
        },
    }

    for id, data in config["data"].items():
        noir_data["private"]["data"][id] = data["values"]

    comments = f"{config['description']}"

    save_dict_to_toml(noir_data, circuit_path / "Prover.toml", comments=comments)


def generate_data_file(config: dict, circuit_path: Path):
    file_path = circuit_path / "src" / "data.nr"
    if not os.path.exists(file_path.parent):
        os.makedirs(file_path.parent)
    with open(str(file_path), "w") as f:
        data = config["data"]
        for key in data:
            d = data[key]
            f.write(
                "global {}_SIZE: Field = {};\n".format(key.upper(), len(d["values"]))
            )
            f.write(
                "global {}_SHAPE_0: {} = {};\n".format(
                    key.upper(), d["format"], d["shape"][0]
                )
            )
            f.write(
                "global {}_SHAPE_1: {} = {};\n".format(
                    key.upper(), d["format"], d["shape"][1]
                )
            )
            if "precision" in d:
                f.write(
                    "global {}_PRECISION: u4 = {};\n".format(
                        key.upper(), d["precision"]
                    )
                )
            f.write("\n")
        f.write(
            "global DATA_SIZE: Field = {};\n".format(
                sum([len(data[key]["values"]) for key in data])
            )
        )
        f.write("\n")
        f.write("struct Data {\n")
        D1_TYPE = 8
        for key in data:
            d = data[key]
            D1_TYPE = int(d["format"][1:])
            f.write("    // {}\n".format(d["description"]))
            f.write("    {}: [{}; {}],\n".format(key, d["format"], len(d["values"])))
        f.write("}\n")
        f.write("\n")
        f.write("struct Public{\n")
        f.write("    keys: Keys,\n")
        f.write("    statement: Statement\n")
        f.write("}\n")
        f.write("\n")
        f.write("struct Keys {\n")
        f.write("    pub_key_x: Field,\n")
        f.write("    pub_key_y: Field,\n")
        f.write("}\n")
        f.write("\n")
        f.write("struct Statement {\n")
        f.write(f"    value: u{2*int(D1_TYPE)},\n")
        f.write("}\n")
        f.write("\n")
        f.write("struct Private {\n")
        f.write("    provenance: Provenance,\n")
        f.write("    data: Data,\n")
        f.write("}\n")
        f.write("\n")
        f.write("struct Provenance {\n")
        f.write("    signature: [u8; 64],\n")
        f.write("    hash: [u8; 32],\n")
        f.write("}\n")

    print(f"File saved: {file_path}")


def generate_verify_data_provenance(config: dict) -> str:
    """
    Generate the Rust code for verifying the authenticity and integrity of data using the Schnorr signature scheme.

    Args:
        config (dict): The configuration dictionary containing the required parameters.

    Returns:
        str: The Rust code as a string.
    """
    code = """
// Verify the authenticity and integrity of the data by concatenating it, 
// computing its SHA256 hash, and verifying its Schnorr signature using the 
// public keys and the signature from the provenance.
fn verify_data_provenance(
    data: data::Data,    // The data to be verified.
    keys: data::Keys,    // The public keys to be used for the verification.
    provenance: data::Provenance    // The provenance object containing the signature to be verified.
) -> Field  {
    // Concatenate all the data.
    let flat_data = concatenate(data);

    // Compute the SHA256 hash of the concatenated data.
    let mut digest256 = std::sha256::digest(flat_data);

    // Verify the Schnorr signature of the hash using the public keys and the signature from the provenance.
    std::schnorr::verify_signature(
        keys.pub_key_x, 
        keys.pub_key_y, 
        provenance.signature, 
        digest256)
}
"""
    return code


def generate_concatenate(config: dict) -> str:
    result = "// Concatenates the data into a byte array of size `DATA_SIZE`.\n"
    result += "// This function returns the concatenated byte array.\n"
    result += "mod data;\n\n"
    result += "fn concatenate(data: data::Data) -> [u8; data::DATA_SIZE]  {\n"
    result += "    let mut result = [0; data::DATA_SIZE];\n"
    result += "    let mut cur_i = 0;\n"
    for key, value in config["data"].items():
        result += f"    // {value['description']}\n"
        result += f"    // Copy the contents of {key} into the byte array.\n"
        result += f"    for i in 0..data::{key.upper()}_SIZE {{\n"
        result += f"        result[cur_i] = data.{key}[i] as u8;\n"
        result += "        cur_i = cur_i + 1;\n"
        result += "    }\n"
    result += "    result\n"
    result += "}\n"
    return result


def generate_main(config: dict) -> str:
    result = (
        "// Verify the authenticity and integrity of the data by concatenating it, \n"
    )
    result += (
        "// computing its SHA256 hash, and verifying its Schnorr signature using the \n"
    )
    result += "// public keys and the signature from the provenance.\n"
    result += "fn verify_data_provenance(\n"
    result += "    data: data::Data,    // The data to be verified.\n"
    result += (
        "    keys: data::Keys,    // The public keys to be used for the verification.\n"
    )
    result += "    provenance: data::Provenance    // The provenance object containing the signature to be verified.\n"
    result += ") -> Field  {\n"
    result += "    // Concatenate all the data.\n"
    result += "    let flat_data = concatenate(data);\n"
    result += "    // Compute the SHA256 hash of the concatenated data.\n"
    result += "    let mut digest256 = std::sha256::digest(flat_data);\n"
    result += "    // Verify the Schnorr signature of the hash using the public keys and the signature from the provenance.\n"
    result += "    std::schnorr::verify_signature(keys.pub_key_x, keys.pub_key_y, provenance.signature, digest256)\n"
    result += "}\n\n"


def generate_main(config: dict) -> str:
    result = (
        "// Verify the authenticity and integrity of the data by concatenating it, \n"
    )
    result += (
        "// computing its SHA256 hash, and verifying its Schnorr signature using the \n"
    )
    result += "// public keys and the signature from the provenance.\n"
    result += "fn verify_data_provenance(\n"
    result += "    data: data::Data,    // The data to be verified.\n"
    result += (
        "    keys: data::Keys,    // The public keys to be used for the verification.\n"
    )
    result += "    provenance: data::Provenance    // The provenance object containing the signature to be verified.\n"
    result += ") -> Field  {\n"
    result += "    // Concatenate all the data.\n"
    result += "    let flat_data = concatenate(data);\n"
    result += "    // Compute the SHA256 hash of the concatenated data.\n"
    result += "    let mut digest256 = std::sha256::digest(flat_data);\n"
    result += "    // Verify the Schnorr signature of the hash using the public keys and the signature from the provenance.\n"
    result += "    std::schnorr::verify_signature(keys.pub_key_x, keys.pub_key_y, provenance.signature, digest256)\n"
    result += "}\n\n"


def compose_main_file(config: dict, circuit_path: Path):
    function_string = ""
    if "function" in config:
        # add funtion to the main file
        function_name = config["function"]["name"]
        if function_name == Functions.MULTIPLE_DOT_PRODUCT.value:
            aggregator_name = config["function"]["aggregator"]
            if aggregator_name == Aggregator.AVERAGE.value:
                d_labels = extract_data_labels_from_config(config)
                if len(d_labels) != 2:
                    raise ValueError(
                        f"Aggregator {aggregator_name} requires exactly 2 data labels."
                    )
                function_string = generate_dot_product_multi(
                    d_labels[0].upper(),
                    config["data"][d_labels[0]],
                    d_labels[1].upper(),
                    config["data"][d_labels[1]],
                    aggregator=Aggregator.AVERAGE,
                )
            elif aggregator_name == Aggregator.SUM.value:
                pass
        else:
            raise ValueError(f"Function {function_name} not supported.")

    file_path = circuit_path / "src" / "main.nr"
    if not os.path.exists(file_path.parent):
        os.makedirs(file_path.parent)
    with open(str(file_path), "w") as f:
        data = config["data"]
        f.write("use dep::std;\n")
        f.write("mod data;\n\n")
        f.write("// Concatenates the data into a byte array of size `DATA_SIZE`.")
        f.write("// This function returns the concatenated byte array.")
        f.write("mod data;\n\n")
        f.write("fn concatenate(data: data::Data) -> [u8; data::DATA_SIZE]  {\n")
        f.write("    let mut result = [0; data::DATA_SIZE];\n")
        f.write("    let mut cur_i = 0;\n")

        for key, value in data.items():
            f.write(f"    // {value['description']}\n")
            f.write(f"    // Copy the contents of {key} into the byte array.\n")
            f.write(f"    for i in 0..data::{key.upper()}_SIZE {{\n")
            f.write(f"        result[cur_i] = data.{key}[i] as u8;\n")
            f.write("        cur_i = cur_i + 1;\n")
            f.write("    }\n")
        f.write("    result\n")
        f.write("}\n")
        f.write("\n\n")
        f.write(
            """
// Verify the authenticity and integrity of the data by concatenating it, 
// computing its SHA256 hash, and verifying its Schnorr signature using the 
// public keys and the signature from the provenance.
fn verify_data_provenance(
    data: data::Data,    // The data to be verified.
    keys: data::Keys,    // The public keys to be used for the verification.
    provenance: data::Provenance    // The provenance object containing the signature to be verified.
) -> Field  {
    // Concatenate all the data.
    let flat_data = concatenate(data);

    // Compute the SHA256 hash of the concatenated data.
    let mut digest256 = std::sha256::digest(flat_data);

    // Verify the Schnorr signature of the hash using the public keys and the signature from the provenance.
    std::schnorr::verify_signature(
        keys.pub_key_x, 
        keys.pub_key_y, 
        provenance.signature, 
        digest256)
}
"""
        )
        if function_string == "":
            f.write(
                """

// Perform some meaningful operations on the data and return the result.
fn perform_computation_on_data(data: data::Data) -> u8  {
    // TODO: Implement the actual computation on the data.

    // Dummy implementation that returns zero.
    let mut result = data.d1[0];
    """
            )
            f.write(f"    result = {config['statement']};")
            f.write(
                """

    result as u8
    }
    """
            )
        else:
            f.write(function_string)
        f.write(
            """


fn main(
    public : pub data::Public,    // Data containing the expected result.
    private : data::Private,    // Data to be verified and processed.
    ) -> pub u16{

    // Verify the authenticity and integrity of the private data.
    constrain verify_data_provenance(private.data, public.keys, private.provenance) == 1;

    // Perform some meaningful operations on the private data.
    let result = perform_computation_on_data(private.data);

    // Verify that the obtained result matches the value specified in the public statement.
    constrain result == public.statement.value;

    // Return result, for debugging
    result

}

        """
        )

    print(f"File saved: {file_path}")


def generate_main_file(config: dict, circuit_path: Path):
    function_string = ""
    if "function" in config:
        # add funtion to the main file
        function_name = config["function"]["name"]
        if function_name == Functions.MULTIPLE_DOT_PRODUCT.value:
            aggregator_name = config["function"]["aggregator"]
            if aggregator_name == Aggregator.AVERAGE.value:
                d_labels = extract_data_labels_from_config(config)
                if len(d_labels) != 2:
                    raise ValueError(
                        f"Aggregator {aggregator_name} requires exactly 2 data labels."
                    )
                function_string = generate_dot_product_multi(
                    d_labels[0].upper(),
                    config["data"][d_labels[0]],
                    d_labels[1].upper(),
                    config["data"][d_labels[1]],
                    aggregator=Aggregator.AVERAGE,
                )
            elif aggregator_name == Aggregator.SUM.value:
                pass
        else:
            raise ValueError(f"Function {function_name} not supported.")

    file_path = circuit_path / "src" / "main.nr"
    if not os.path.exists(file_path.parent):
        os.makedirs(file_path.parent)
    with open(str(file_path), "w") as f:
        data = config["data"]
        f.write("use dep::std;\n")
        f.write("mod data;\n\n")

        if config["provenance"]:
            f.write("// Concatenates the data into a byte array of size `DATA_SIZE`.")
            f.write("// This function returns the concatenated byte array.")
            f.write("mod data;\n\n")
            f.write("fn concatenate(data: data::Data) -> [u8; data::DATA_SIZE]  {\n")
            f.write("    let mut result = [0; data::DATA_SIZE];\n")
            f.write("    let mut cur_i = 0;\n")

            for key, value in data.items():
                f.write(f"    // {value['description']}\n")
                f.write(f"    // Copy the contents of {key} into the byte array.\n")
                f.write(f"    for i in 0..data::{key.upper()}_SIZE {{\n")
                f.write(f"        result[cur_i] = data.{key}[i] as u8;\n")
                f.write("        cur_i = cur_i + 1;\n")
                f.write("    }\n")
            f.write("    result\n")
            f.write("}\n")
            f.write("\n\n")
            f.write(
                """
// Verify the authenticity and integrity of the data by concatenating it, 
// computing its SHA256 hash, and verifying its Schnorr signature using the 
// public keys and the signature from the provenance.
fn verify_data_provenance(
    data: data::Data,    // The data to be verified.
    keys: data::Keys,    // The public keys to be used for the verification.
    provenance: data::Provenance    // The provenance object containing the signature to be verified.
) -> Field  {
    // Concatenate all the data.
    let flat_data = concatenate(data);

    // Compute the SHA256 hash of the concatenated data.
    let mut digest256 = std::sha256::digest(flat_data);

    // Verify the Schnorr signature of the hash using the public keys and the signature from the provenance.
    std::schnorr::verify_signature(
        keys.pub_key_x, 
        keys.pub_key_y, 
        provenance.signature, 
        digest256)
}
"""
            )
        if function_string == "":
            f.write(
                """

// Perform some meaningful operations on the data and return the result.
fn perform_computation_on_data(data: data::Data) -> u8  {
    // TODO: Implement the actual computation on the data.

    // Dummy implementation that returns zero.
    let mut result = data.d1[0];
    """
            )
            f.write(f"    result = {config['statement']};")
            f.write(
                """

    result as u8
    }
    """
            )
        else:
            f.write(function_string)

        D1_TYPE = 16
        for key in data:
            d = data[key]
            D1_TYPE = int(d["format"][1:])

        f.write(f"\n\nfn main(\n")
        f.write(
            f"    public : pub data::Public,    // Data containing the expected result.\n"
        )
        f.write(
            f"    private : data::Private,    // Data to be verified and processed.\n"
        )
        f.write(f"    ) -> pub u{2*int(D1_TYPE)}{{\n")
        if config["provenance"]:
            f.write(
                """

    // Verify the authenticity and integrity of the private data.
    constrain verify_data_provenance(private.data, public.keys, private.provenance) == 1;

    // Perform some meaningful operations on the private data.
    let result = perform_computation_on_data(private.data);

    // Verify that the obtained result matches the value specified in the public statement.
    constrain result == public.statement.value;

    // Return result, for debugging
    result

}

        """
            )
        else:
            f.write(
                """

    // Perform some meaningful operations on the private data.
    let result = perform_computation_on_data(private.data);

    // Verify that the obtained result matches the value specified in the public statement.
    constrain result == public.statement.value;

    // Return result, for debugging
    result

}

        """
            )

    print(f"File saved: {file_path}")
