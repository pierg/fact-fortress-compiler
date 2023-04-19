from pathlib import Path
import os
from .my_io import save_dict_to_json, save_dict_to_toml


def generate_noir_files(config: dict, data_signature: list[int], data_hash: list[int], circuit_path: Path):
    generate_project(config, circuit_path)
    generate_input_file(config, data_signature, data_hash, circuit_path)
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
            {"name": data_value["name"], "description": data_value["description"], "provider": data_value["provider"]}
        )

    # create output JSON object
    output_data = {"function": {"name": function_name, "description": function_description}, "data": data}

    save_dict_to_json(output_data, circuit_path / "info.json")


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
authors = ["{compiler_version}"]
compiler_version = "{authors}"

[dependencies]
            """
        )


def generate_input_file(config: dict, data_signature: list[int], data_hash: list[int], circuit_path: Path):
    # Save individuals and betas to a TOML file
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
                "signature": data_signature,
                "hash": data_hash,
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
            f.write("global {}_SIZE: Field = {};\n".format(key.upper(), len(d["values"])))
            f.write("global {}_SHAPE: [u8; {}] = {};\n".format(key.upper(), len(d["shape"]), d["shape"]))
            if "precision" in d:
                f.write("global {}_PRECISION: u4 = {};\n".format(key.upper(), d["precision"]))
            f.write("\n")
        f.write("global DATA_SIZE: Field = {};\n".format(sum([len(data[key]["values"]) for key in data])))
        f.write("\n")
        f.write("struct Data {\n")
        for key in data:
            d = data[key]
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
        f.write("    value: u8,\n")
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


def generate_main_file(config: dict, circuit_path: Path):
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

fn main(
    public : pub data::Public,    // Data containing the expected result.
    private : data::Private,    // Data to be verified and processed.
    ){

    // Verify the authenticity and integrity of the private data.
    constrain verify_data_provenance(private.data, public.keys, private.provenance) == 1;

    // Perform some meaningful operations on the private data.
    let result = perform_computation_on_data(private.data);

    // Verify that the obtained result matches the value specified in the public statement.
    constrain result == public.statement.value;

}

        """
        )

    print(f"File saved: {file_path}")
