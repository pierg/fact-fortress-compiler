from utils.generate_circuit import generate_circuit
from utils.config_generator import general_config_generator
from shared import performance_path, results_path
import subprocess
import time
import argparse
import os
import json
import platform
from src.utils.my_io import save_dict_to_json

if platform.system() == "Darwin":
    platform_use = "mac"
elif platform.system() == "Linux":
    platform_use = "linux"
else:
    platform_use = "unknown"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script description")
    parser.add_argument("--bits", type=int, default=16, help="Number of bits")
    parser.add_argument(
        "--rng", type=int, nargs=2, default=[10, 65500], help="Range of values"
    )
    parser.add_argument("--step", type=int, default=50, help="Step size")
    args = parser.parse_args()

    bits = args.bits
    rng = args.rng
    step = args.step

    times_file_path = results_path / f"times-{platform_use}.json"

    # Check if the file exists
    if os.path.exists(performance_path / times_file_path):
        # If the file exists, load it as a dictionary
        with open(performance_path / times_file_path, "r") as f:
            times = json.load(f)
    else:
        # If the file doesn't exist, create a new dictionary
        times = {}

    machine_platform = f"{platform_use}"

    """Navigate to the directory where the circuits are stored"""
    for i in range(rng[0], rng[1], step):
        if str(i) in times:
            if machine_platform in times[str(i)]:
                print(
                    f"Performance for {str(i)} on {machine_platform} already computed"
                )
                continue

        """Generate circuit"""
        config_path = general_config_generator(
            name="circuit_{}_{}_{}".format(bits, i, step),
            d1_bits=bits,
            d1_shape=[2, int(i / 2)],
            d2_bits=bits,
            d2_shape=[2, 1],
            provenance=False,
        )
        generate_circuit(config_path, performance_path)

        """Evaluate circuit"""
        times[str(i)] = {machine_platform: {}}
        time_info = times[str(i)][machine_platform]
        circuit_dir = performance_path / "circuit_{}_{}_{}".format(bits, i, step)

        with open(circuit_dir / "info.json", "r") as f:
            info = json.load(f)
            time_info["info"] = info["info"]["info"]

        print("Generating proof...")
        """Generate the proof"""
        start_time = time.time()
        subprocess.run(["nargo", "prove", "p"], cwd=circuit_dir)
        end_time = time.time()
        proving_time = end_time - start_time
        print(f"Proof generated in {round(proving_time, 2)} seconds")

        print("Verifying proof...")
        """Verify the proof"""
        start_time = time.time()
        subprocess.run(["nargo", "verify", "p"], cwd=circuit_dir)
        end_time = time.time()
        verification_time = end_time - start_time
        print(f"Proof verified in {round(verification_time, 2)} seconds")

        time_info["proving_time"] = round(proving_time, 2)
        time_info["verification_time"] = round(verification_time, 2)
        time_info["proof_size"] = os.path.getsize(circuit_dir / "proofs" / "p.proof")

        save_dict_to_json(times, file_path=times_file_path)
