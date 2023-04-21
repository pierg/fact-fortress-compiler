import numpy as np


def risk_score_analysis(
    individuals: list[int],
    individuals_shape: tuple[int, int],
    beta_values: list[int],
) -> int:
    """Computes the dot products between individuals and beta_values"""

    # Reshape individuals list to match the given shape
    individuals = np.reshape(individuals, individuals_shape)

    # Compute the dot product between individuals and beta_values
    dot_products = np.dot(individuals, beta_values)

    # Average of scores approximated to integer
    result = round(np.mean(dot_products))

    return result
