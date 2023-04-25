from circuit_gen import generate_circuit
from shared import performance_path
import subprocess
import time

from src.utils.my_io import save_dict_to_json


def generate(bits=8, rng=[10, 100], step=10, path=performance_path):
    for i in range(rng[0], rng[1], step):
        generate_circuit(
            name="circuit_{}_{}_{}".format(bits, i, step),
            d1_bits=bits,
            d1_shape=[2, int(i / 2)],
            d2_bits=bits,
            d2_shape=[2, 1],
            path=path,
        )


if __name__ == "__main__":
    bits = 8
    rng = [10, 100]
    step = 10

    """Generate circuits"""
    generate(bits, rng, step, path=performance_path)

    """Store proving and verification times in a dictionary"""
    times = {}

    """Navigate to the directory where the circuits are stored"""
    for i in range(rng[0], rng[1], step):
        times[str(i)] = {}
        circuit_dir = performance_path / "circuit_{}_{}_{}".format(bits, i, step)
        """Generate the proof"""
        start_time = time.time()
        subprocess.run(["nargo", "prove", "p"], cwd=circuit_dir)
        end_time = time.time()
        proving_time = end_time - start_time

        """Verify the proof"""
        start_time = time.time()
        subprocess.run(["nargo", "verify", "p"], cwd=circuit_dir)
        end_time = time.time()
        verification_time = end_time - start_time

        times[str(i)] = {
            "proving_time": round(proving_time, 2),
            "verification_time": round(verification_time, 2),
        }
        print("Times Computed")
        print(times[str(i)])
        save_dict_to_json(times, file_path=performance_path / "times.json")
