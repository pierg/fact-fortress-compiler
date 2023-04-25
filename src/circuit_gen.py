from pathlib import Path
from cli import gen_circuit
from py_functions.multi_dot_products import multi_dot_product_average
from data_generators.generic_data import generate_data
from src.shared import Aggregator, Functions
from shared import circuits_path
from utils.authorities import generate_authority
from utils.generate_configs import generate_configuration_file
from utils.sign_data import sign_data


def generate_circuit(
    name: str = "gen_circuit",
    d1_bits: int = 8,
    d1_shape: list[int] = [4, 3],
    d1_range: list[int] | None = [0, 10],
    d2_bits: int = 32,
    d2_shape: list[int] = [4, 3],
    d2_range: list[int] | None = [0, 8],
    path: Path = circuits_path,
):
    authority = generate_authority("Authority_A")

    if d1_range is None:
        d1_range = [0, 2**d1_bits]

    if d2_range is None:
        d2_range = [0, 2**d2_bits]

    data_format = {
        "d1": {
            "name": "Data_1",
            "provider": authority["name"],
            "type": "int",
            "bits": d1_bits,
            "shape": d1_shape,
            "range": d1_range,
        },
        "d2": {
            "name": "Data_2",
            "provider": authority["name"],
            "type": "int",
            "bits": d2_bits,
            "shape": d2_shape,
            "range": d2_range,
        },
    }

    data = generate_data(data_format)

    data_hash, signature = sign_data(authority, data)

    function = {
        "name": Functions.MULTIPLE_DOT_PRODUCT.value,
        "aggregator": Aggregator.AVERAGE.value,
    }

    result = multi_dot_product_average(
        x=data["d1"]["values"],
        x_shape=data["d1"]["shape"],
        y=data["d2"]["values"],
    )
    expected_result = result["result"]

    config_path = generate_configuration_file(
        name=name,
        description="Computes the average of dot-products between a two-dimensional matrix and a vector with a given precision, where the dot-product between each row of the matrix and the vector is computed and then averaged over all rows. The precision can be specified as the number of decimal places to include in the result.",
        authorities=[authority],
        data_hash=data_hash,
        signature=signature,
        statement=expected_result,
        data=data,
        function=function,
        info=result,
    )

    gen_circuit(config_path, path)

    return result
