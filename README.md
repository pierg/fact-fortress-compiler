# Fact Fortress Compiler
<p align="center">
  <img src="./docs/logo-compiler-500.png" alt="Fact Fortress Logo" width="400"/>
</p>

This repository contains the code for a Python library that facilitates the generation of Zero-Knowledge Proof circuits in [noir](https://noir-lang.org) with various input data sizes and formats. The circuits compiled come with a ZKP certifying the data provenance and proof of statement.


The library provides clear and abstract APIs that allow users to specify the data format, the function to be performed by the circuit, and the authority that provided the data. It compiles down from Python API to JSON configuration file and ultimately parses the JSON and compiles the fully functioning circuit in Noir.


<p align="center">
  <img src="./docs/compiler-500.png" alt="Circuits Compilation Process" width="700"/>
</p>


This tool aims to increase adoption of zero-knowledge proof (ZKP) frameworks by providing user-friendly interfaces and higher-level abstractions to abstract away the low-level details of arithmetic circuits. It enables easier implementation of ZKP protocols in real-world applications, making it possible for developers with limited experience to implement functions.

Once the circuit is generated, the user can navigate to the generated folder and immediately prove and verify the compiled circuit, without any additional modification on the DSL source code.

To generate and verify proofs on the compiled circuits, navigate to the folder `circuits/YOUR_CIRCUIT` and run:

```bash
nargo prove p
```

```bash
nargo prove p
```


## What is Fact Fortress

Fact Fortress is a blockchain-based framework that uses zero-knowledge proofs for trustworthy and private fact-checking. It ensures trustworthy data handling and computation by using proofs of data provenance and auditable data access policies. The solution democratizes circuit construction and deployment with a circuit compiler that supports various data formats and source authentication, and facilitates on-chain verification. This preserves sensitive data privacy while ensuring accountability and transparency in data handling and computation. It achieves this by enabling on-chain verification of computation and data provenance without revealing any information about the data itself.


Our framework provides a comprehensive solution that covers the entire process from circuit generation to proof generation, while facilitating collaboration among data analysts, data providers, external verifiers, and policy auditors.



<p align="center">
  <img src="./docs/end-to-end-500.png" alt="Fact Fortress Overview" width="350"/>
</p>



For more information, check out our website at: [https://pierg.github.io/fact-fortress-web/](https://pierg.github.io/fact-fortress-web/).


# Installing and Compiling Circuits

## System requirements
[noir](https://noir-lang.org)

[poetry](https://python-poetry.org)

[python 3.11](https://www.python.org)


## Install Dependencies

To install run:

```bash
poetry install
```

Clone, install and run backend

```bash
git clone https://github.com/pierg/fact-fortress-dapp
```

```bash
pnpm instll
```

```bash
pnpm backend
```


# Example

*Makesure that you have the back-end running (to access sign, hash functions)*

Complete running example: `src/example.py`

Generate a new authority with a unique set of key-pairs, and returns the authority's details as a dictionary.

```python
authority = generate_authority("Authority_A")
```


Generate data of different shapes
```python
example_data = generate_risk_data(
    authority=authority, shape_1=2, shape_2=4, precision=2
)
```


Computes the hash of concatenated values from a data dictionary, signs the hash using an authority's private key, and returns the resulting signature and data hash as a tuple.

```python
data_hash, signature = sign_data(authority, example_data)
```


Choose the function to compute the function_1 form ther library of functions and aggregators that are currently supported.

```python
function = {
    "name": Functions.MULTIPLE_DOT_PRODUCT.value,
    "aggregator": Aggregator.AVERAGE.value,
}
```


Perform the function on the data in python so that we can compare the result with the one proved by the circuit in Zero Knowledge.

```python
expected_result = multi_dot_product_average(
    data_1=example_data["d1"]["values"],
    data_1_shape=example_data["d1"]["shape"],
    data_2_values=example_data["d2"]["values"],
)["result"]

```


Generate a new configuration file in JSON format to programmatically create the circuit and saves it to the configuration folder.

```python
config_path = generate_configuration_file(
    name="average_dot_products",
    description="Computes the average of dot-products between a two-dimensional matrix and a vector with a given precision, where the dot-product between each row of the matrix and the vector is computed and then averaged over all rows. The precision can be specified as the number of decimal places to include in the result.",
    authorities=[authority],
    data_hash=data_hash,
    signature=signature,
    statement=expected_result,
    data=example_data,
    function=function,
)
```


Generate the circuit! Given a configuration, this function will generate a folder all the structure and 'noir' files needed to generate the proof in Zero-Knowledge. 
The circuit compiles and generate valid proofs. Specifically it proofs:
    - Proof of Provenance
        - Checks that the data comes from the authority using Schnorr Signature
    - Proof of Data Consistency
        -  Checks that the data hash is valid using SHA256
    - Proof of Statement
        - Checks that the chosen function applied on the data results in the expected statement


```python
gen_circuit(config_path)
```

Now navigate to the generated folder and run the following commands:

### GENERATE PROOF

```bash
nargo prove p
```

### VERIFY PROOF

```bash
nargo verify p
```

Or simply execute the `prove.sh` and `verify.sh` scripts in the generated folder.
