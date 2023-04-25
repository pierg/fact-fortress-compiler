def multi_dot_product_average(
    x: list[int],
    x_shape: tuple[int, int],
    y: list[int],
) -> dict[str, int]:
    result_dict = {"result": 0, "info": {"n_additions": 0, "n_multiplications": 0}}

    # Dot products
    x_shape = (int(x_shape[0]), int(x_shape[1]))
    result = [0] * int(x_shape[1])
    for i in range(x_shape[1]):
        start = i * x_shape[0]
        end = start + x_shape[0]
        x_slice = x[start:end]
        for j in range(x_shape[0]):
            # Count the number of additions and multiplications
            result[i] += x_slice[j] * y[j]
            result_dict["info"]["n_multiplications"] += 1
            result_dict["info"]["n_additions"] += 1

    # Average
    average = sum(result) // len(result)

    result_dict["info"]["n_additions"] += len(result) - 1
    result_dict["info"]["n_multiplications"] += 1

    result_dict["result"] = average

    return result_dict


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
