from cli import gen_circuit
from data_generators import generate_multi_dimensional_data
from py_functions.multi_dot_products import multi_dot_product_average
from src.shared import Aggregator, Functions
from utils.authorities import generate_authority
from utils.generate_configs import generate_configuration_file
from utils.sign_data import sign_data


"""
Generate a new authority with a unique set of key-pairs, and returns the authority's details as a dictionary.
"""
authority = generate_authority("Authority_B")
authority_b = generate_authority("Authority_C")


"""
Generate data of different shapes
"""
example_data = generate_multi_dimensional_data(
    authority=authority, shape_1=4, shape_2=8, precision=2
)


"""
Computes the hash of concatenated values from a data dictionary, signs the hash using an authority's private key, and returns the resulting signature and data hash as a tuple.
"""
data_hash, signature = sign_data(authority, example_data)


"""
Choose the function to apply on the data form ther library of functions and aggregators that are currently supported.
"""

function = {
    "name": Functions.MULTIPLE_DOT_PRODUCT.value,
    "aggregator": Aggregator.AVERAGE.value,
}

"""
Perform the function on the data in python so that we can compare the result with the one proved by the circuit in Zero Knowledge.
"""
expected_result = multi_dot_product_average(
    data_1=example_data["d1"]["values"],
    data_1_shape=example_data["d1"]["shape"],
    data_2_values=example_data["d2"]["values"],
)


"""
Generate a new configuration file in JSON format to programmatically create the circuit and saves it to the configuration folder.
"""
config_path = generate_configuration_file(
    name="sum_of_squares",
    description="Computes the sum of squares of a given list of numbers with a given precision, where each number in the list is squared and then summed up. The precision can be specified as the number of decimal places to include in the result.",
    authorities=[authority, authority_b],
    data_hash=data_hash,
    signature=signature,
    statement=expected_result,
    data=example_data,
    function=function,
)

"""
Generate the circuit! Given a configuration, this function will generate a folder all the structure and 'noir' files needed to generate the proof in Zero-Knowledge. 
The circuit compiles and generate valid proofs. Specifically it proofs:
    - Proof of Provenance
        - Checks that the data comes from the authority using Schnorr Signature
    - Proof of Data Consistency
        -  Checks that the data hash is valid using SHA256
    - Proof of Statement
        - Checks that the chosen function applied on the data results in the expected statement
"""

gen_circuit(config_path)


"""
Now navigate to the generated folder and run the following commands:

# PROVE
nargo prove p

# VERIFY
nargo verify p


Or simply execute the prove.sh and verify.sh scripts in the generated folder.

"""
