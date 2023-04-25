def unroll_and_compute(
    x: list[int], x_shape: tuple[int, int], y: list[int]
) -> list[int]:
    x_shape = (int(x_shape[0]), int(x_shape[1]))
    result = [0] * int(x_shape[1])
    for i in range(x_shape[1]):
        start = i * x_shape[0]
        end = start + x_shape[0]
        x_slice = x[start:end]
        result[i] = sum([x_slice[j] * y[j] for j in range(x_shape[0])])
    return result


def average(x: list[int]) -> int:
    return sum(x) // len(x)


def multi_dot_product_average(
    data_1: list[int],
    data_1_shape: tuple[int, int],
    data_2_values: list[int],
) -> int:
    dot_products = unroll_and_compute(data_1, data_1_shape, data_2_values)
    return int(average(dot_products))


# d1 = [
#     3,
#     6,
#     2,
#     5,
#     9,
#     5,
#     0,
#     2,
#     0,
#     6,
# ]
# d2 = [
#     0,
#     7,
# ]

# print(list(range(5 - 1)))
# print(multi_dot_product_average(d1, [2, 5], d2))
