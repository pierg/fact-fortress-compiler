from cli import gen_circuit
from generators import generate_risk, generate_simple, generate_variants


# Generate sample data
generate_simple("simple")
# generate_simple will produce the configuration file simple.json in the configurations folder
# Generate circuit
gen_circuit("simple")
# gen_circuit will produce the noir folder with all the files set up in the circuits folder
# you can generate proof or provenanance and data autenthicity
# by running 'nargo prove p'


generate_risk("risk")
gen_circuit("risk")


generate_variants("variants")
gen_circuit("variants")
