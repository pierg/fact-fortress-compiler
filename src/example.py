from cli import gen_circuit
from data_generators import generate_risk_data
from bio_functions.risk_score_analysis import risk_score_analysis
from src.shared import Aggregator, Functions
from utils.authorities import generate_authority
from utils.generate_configs import generate_configuration_file
from utils.sign_data import sign_data


"""
Generate a new authority with a unique set of key-pairs, and returns the authority's details as a dictionary.
"""
authority = generate_authority("Hospital_A")


"""
Generate synthetic genetic data for a given number of individuals.'
The data generates contains:
    - allele counts for each genome position in each individual
    - beta values for each position, i.e. the risk score associated the specific position.
"""
genetic_data = generate_risk_data(
    authority=authority, n_positions=2, n_individuals=4, precision=2
)


"""
Computes the hash of concatenated values from a data dictionary, signs the hash using an authority's private key, and returns the resulting signature and data hash as a tuple.
"""
data_hash, signature = sign_data(authority, genetic_data)


"""
Choose the function to compute the risk score form ther library of functions and aggregators that are currently supported.
"""

function = {
    "name": Functions.MULTIPLE_DOT_PRODUCT.value,
    "aggregator": Aggregator.AVERAGE.value,
}

"""
Perform the risk score analysis in python so that we can compare the result with the one proved by the circuit in Zero Knowledge.
"""
expected_result = risk_score_analysis(
    individuals=genetic_data["d1"]["values"],
    individuals_shape=genetic_data["d1"]["shape"],
    beta_values=genetic_data["d2"]["values"],
)


"""
Generate a new configuration file in JSON format to programmatically create the circuit and saves it to the configuration folder.
"""
config_path = generate_configuration_file(
    name="risk_score_test",
    description="Computes the average risk scores for heart failure of a population",
    authorities=[authority],
    data_hash=data_hash,
    signature=signature,
    statement=expected_result,
    data=genetic_data,
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
