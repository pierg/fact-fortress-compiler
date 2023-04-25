from circuit_gen import generate_circuit
from shared import performance_path
import subprocess
import time

# import psutil
import os
import json
import platform
from src.utils.my_io import save_dict_to_json

if platform.system() == "Darwin":
    platform_use = "mac"
elif platform.system() == "Linux":
    platform_use = "linux"
else:
    platfplatform_useorm = "unknown"


# mem_size = psutil.virtual_memory().total


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
    rng = [4, 100]
    step = 4

    """Generate circuits"""
    generate(bits, rng, step, path=performance_path)

    """Store proving and verification times in a dictionary"""

    file_path = performance_path / "times.json"

    # Check if the file exists
    if os.path.exists(performance_path / file_path):
        # If the file exists, load it as a dictionary
        with open(performance_path / file_path, "r") as f:
            times = json.load(f)
    else:
        # If the file doesn't exist, create a new dictionary
        times = {}

    signature = f"{platform_use}"

    print(times)

    """Navigate to the directory where the circuits are stored"""
    for i in range(rng[0], rng[1], step):
        if str(i) in times:
            if signature in times[str(i)]:
                continue
        times[str(i)] = {signature: {}}
        time_info = times[str(i)][signature]
        circuit_dir = performance_path / "circuit_{}_{}_{}".format(bits, i, step)

        with open(circuit_dir / "info.json", "r") as f:
            info = json.load(f)
            time_info["n_multiplications"] = info["n_multiplications"]
            time_info["n_additions"] = info["n_additions"]

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

        time_info["proving_time"] = round(proving_time, 2)
        time_info["verification_time"] = round(proving_time, 2)

        print("Times Computed")
        print(time_info)
        save_dict_to_json(times, file_path=performance_path / "times.json")
