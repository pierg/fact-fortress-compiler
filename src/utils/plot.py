import json
import matplotlib.pyplot as plt
from pathlib import Path
from src.shared import results_path
import numpy as np


def create_performance_graph(input_path: Path, output_path_folder: Path):
    with open(str(input_path)) as f:
        data = json.load(f)

    proving_times = []
    verification_times = []
    n_additions = []
    n_multiplications = []
    n_operations = []
    data_sizes = []
    folder_ids = []

    for element in data:
        proving_times.append(data[element]["mac"]["proving_time"])
        verification_times.append(data[element]["mac"]["verification_time"])
        n_additions.append(data[element]["mac"]["info"]["n_additions"])
        n_multiplications.append(data[element]["mac"]["info"]["n_multiplications"])
        n_operations.append(
            data[element]["mac"]["info"]["n_additions"]
            + data[element]["mac"]["info"]["n_multiplications"]
        )
        folder_ids.append(element)
        data_size = (int(element) * 2) * 2 + 2
        data_sizes.append(data_size)

    plt.plot(data_sizes, proving_times, label="proving_time")
    plt.plot(data_sizes, verification_times, label="verification_time")

    # Compute differences between adjacent values of proving_time and verification_time
    proving_time_diffs = np.abs(np.diff(proving_times))
    verification_time_diffs = np.abs(np.diff(verification_times))

    # Compute threshold for detecting abrupt spikes
    proving_time_threshold = np.mean(proving_time_diffs) + 1
    verification_time_threshold = np.mean(verification_time_diffs) + 1

    # Find indices of abrupt spikes
    proving_time_spikes = np.where(proving_time_diffs > proving_time_threshold)[0] + 1
    verification_time_spikes = (
        np.where(verification_time_diffs > verification_time_threshold)[0] + 1
    )

    # Common spikes, common elements between proving_time_spikes and verification_time_spikes
    spikes = list(set(proving_time_spikes).intersection(verification_time_spikes))
    print(proving_time_spikes)
    print(verification_time_spikes)
    print(spikes)
    print([folder_ids[s] for s in spikes])

    # Indexes in data_sizes where

    # Plot vertical lines at indices of abrupt spikes
    for idx in spikes:
        plt.axvline(x=data_sizes[idx], color="r", linestyle="--")

    plt.xlabel("data size (# of 16 bits integers)")
    plt.ylabel("time (sec)")
    plt.legend()
    plt.savefig(output_path_folder / "plot_with_spikes.pdf")


create_performance_graph(results_path / "times-mac.json", results_path)
