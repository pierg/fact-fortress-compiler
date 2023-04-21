def unroll_and_compute(
    x: list[int], x_shape: tuple[int, int], y: list[int]
) -> list[int]:
    result = [0] * x_shape[1]
    for i in range(4):
        start = i * x_shape[0]
        end = start + x_shape[0]
        x_slice = x[start:end]
        result[i] = sum([x_slice[j] * y[j] for j in range(2)])
    return result


def average(x: list[int]) -> int:
    return sum(x) // 4


def risk_score_analysis(
    individuals: list[int],
    individuals_shape: tuple[int, int],
    beta_values: list[int],
) -> int:
    dot_products = unroll_and_compute(individuals, individuals_shape, beta_values)
    return average(dot_products)
