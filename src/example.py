from cli import gen_circuit
from data_generators import generate_risk_data
from src.bio_functions.risk_score_analysis import risk_score_analysis
from src.utils.authorities import generate_authority
from src.utils.generate_configs import generate_configuration_file


"""
Generate a new authority with a unique set of key-pairs, and returns the authority's details as a dictionary.
"""
new_authority = generate_authority("Hospital_A")


"""
Generate synthetic genetic data for a given number of individuals.'
The data generates contains:
    - allele counts for each genome position in each individual
    - beta values for each position, i.e. the risk score associated the specific position.
"""
genetic_data = generate_risk_data(
    authority=new_authority, n_positions=2, n_individuals=4, precision=2
)


"""
Perform the risk score analysis in python so that we can compare the result with the one proved by the circuit in Zero Knowledge.
"""
expected_result = risk_score_analysis(
    individuals=genetic_data[0]["values"],
    individuals_shape=genetic_data[0]["shape"],
    beta_values=genetic_data[1]["values"],
)


"""
Generate a new configuration file in JSON format to programmatically create a circuit and saves it to the configuration folder.
"""
generate_configuration_file(
    name="risk_score",
    description="Computes the average risk scores for heart failure of a population",
    authorities=[new_authority],
    statement=expected_result,
    data=genetic_data,
    function=function,
)
