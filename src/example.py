from utils.generate_circuit import generate_circuit
from data_generators import generate_multi_dimensional_data
from py_functions.multi_dot_products import multi_dot_product_average
from src.shared import Aggregator, Functions
from utils.authorities import generate_authority
from utils.generate_configs import generate_configuration_file
from utils.sign_data import sign_data


"""
Generate a new authority with a unique set of key-pairs, and returns the authority's details as a dictionary.
"""
authority = generate_authority("Authority_A")


"""
Generate data of different shapes
"""
example_data = generate_multi_dimensional_data(
    authority=authority, shape_1=2, shape_2=4, precision=2
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
computation_output = multi_dot_product_average(
    x=example_data["d1"]["values"],
    x_shape=example_data["d1"]["shape"],
    y=example_data["d2"]["values"],
)
expected_result, info = computation_output["result"], computation_output["info"]


"""
Generate a new configuration file in JSON format to programmatically create the circuit and saves it to the configuration folder.
"""
config_path = generate_configuration_file(
    name="average_dot_products",
    description="Computes the average of dot-products between a two-dimensional matrix and a vector with a given precision, where the dot-product between each row of the matrix and the vector is computed and then averaged over all rows. The precision can be specified as the number of decimal places to include in the result.",
    authorities=[authority],
    data_hash=data_hash,
    signature=signature,
    statement=expected_result,
    data=example_data,
    function=function,
    info=info,
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

generate_circuit(config_path)


"""
Now navigate to the generated folder and run the following commands:

# PROVE
nargo prove p

# VERIFY
nargo verify p


Or simply execute the prove.sh and verify.sh scripts in the generated folder.

"""
