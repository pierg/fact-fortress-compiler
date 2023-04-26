import json
from pathlib import Path
import matplotlib.pyplot as plt

from src.shared import results_path


def create_performance_graph(input_path: Path, output_path_folder: Path):
    with open(str(input_path)) as f:
        data = json.load(f)

    proving_times = []
    verification_times = []
    n_additions = []
    n_multiplications = []
    n_operations = []
    data_sizes = []

    for element in data:
        proving_times.append(data[element]["mac"]["proving_time"])
        verification_times.append(data[element]["mac"]["verification_time"])
        n_additions.append(data[element]["mac"]["info"]["n_additions"])
        n_multiplications.append(data[element]["mac"]["info"]["n_multiplications"])
        n_operations.append(
            data[element]["mac"]["info"]["n_additions"]
            + data[element]["mac"]["info"]["n_multiplications"]
        )
        data_size = (int(element) * 2) * 2 + 2
        data_sizes.append(data_size)

    # create plot 1
    plt.plot(data_sizes, proving_times, label="proving_time")
    plt.plot(data_sizes, verification_times, label="verification_time")
    plt.xlabel("data size (total number of elements in data vectors)")
    plt.ylabel("time")
    plt.legend()
    plt.savefig(output_path_folder / "plot_1.pdf")
    plt.clf()

    # create plot 2
    plt.plot(data_sizes, n_additions, label="n_additions")
    plt.plot(data_sizes, n_multiplications, label="n_multiplications")
    plt.plot(data_sizes, n_operations, label="n_operations")
    plt.xlabel("data size (total number of elements in data vectors)")
    plt.ylabel("n arithmetic elements")
    plt.legend()
    plt.savefig(output_path_folder / "plot_2.pdf")
    plt.clf()


create_performance_graph(results_path / "times-mac.json", results_path)
