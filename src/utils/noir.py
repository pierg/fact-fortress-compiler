from pathlib import Path
import os
from .my_io import save_dict_to_toml


def generate_noir_files(
    config: dict, data_signature: list[int], data_hash: list[int], circuit_path: Path
):
    generate_project(config, circuit_path)
    generate_input_file(config, data_signature, data_hash, circuit_path)
    generate_data_file(config, circuit_path)
    generate_main_file(config, circuit_path)


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


def generate_input_file(
    config: dict, data_signature: list[int], data_hash: list[int], circuit_path: Path
):
    # Save individuals and betas to a TOML file
    noir_data = {
        "public": {
            "keys": {
                "pub_key_x": config["keys"]["pub_key_x"],
                "pub_key_y": config["keys"]["pub_key_y"],
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
    if not os.path.exists(file_path):
        os.makedirs(file_path.parent)
    with open(str(file_path), "w") as f:
        data = config["data"]
        for key in data:
            d = data[key]
            f.write(
                "global {}_SIZE: Field = {};\n".format(key.upper(), len(d["values"]))
            )
            f.write(
                "global {}_SHAPE: [u8; {}] = {};\n".format(
                    key.upper(), len(d["shape"]), d["shape"]
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
    if not os.path.exists(file_path):
        os.makedirs(file_path.parent)
    with open(str(file_path), "w") as f:
        data = config["data"]
        f.write("use dep::std;\n\n")
        f.write("mod data;\n\n")
        f.write("fn concatenate(data: data::Data) -> [u8; data::DATA_SIZE]  {\n")
        f.write("    let mut result = [0; data::DATA_SIZE];\n")
        f.write("    let mut cur_i = 0;\n")

        for key, value in data.items():
            f.write(f"    // {value['description']}\n")
            f.write(f"    for i in 0..data::{key.upper()}_SIZE {{\n")
            f.write(f"        result[cur_i] = data.{key}[i] as u8;\n")
            f.write("        cur_i = cur_i + 1;\n")
            f.write("    }\n")
        f.write("    result\n")
        f.write("}\n")
        f.write("\n\n")
        f.write(
            """
fn compute_function(data: data::Data) -> u8  {
    // TODO
    // Implement the function on the data...

    result 
}

fn main(
    public : pub data::Public,
    private : data::Private,
    ){

    // concatenate all the data
    let data = concatenate(private.data);

    // compute sha256
    let mut digest256 = std::sha256::digest(data);

    // proof of provenance and data consistency
    constrain std::schnorr::verify_signature(
        public.keys.x, 
        public.keys.y, 
        private.provenance.signature, 
        digest256) == 1;

    // compute function on the authenticated data
    let result = compute_function(private.data);

    // check that the result is consistent with the public statement
    constrain result == public.statement.value

}
        """
        )

    print(f"File saved: {file_path}")
