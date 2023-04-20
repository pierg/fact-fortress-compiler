from utils.generate_configs import generate_configuration_json
from utils.authorities import generate_authority


def generate_simple(name: str):
    authorities = []

    new_authority = generate_authority("Provider_A")

    authorities.append(new_authority)

    data_1 = [1, 2]
    data_2 = [3, 4]

    data = [
        {
            "name": "data_A_1",
            "description": "Sample data description 1",
            "provider": "Provider_A",
            "values": data_1,
            "type": "int",
            "format": "u8",
            "shape": [2, 1],
        },
        {
            "name": "data_A_2",
            "description": "Sample data description 2",
            "provider": "Provider_A",
            "values": data_2,
            "type": "double",
            "precision": 1,
            "format": "u8",
            "shape": [2, 1],
        },
    ]

    generate_configuration_json(
        name=name,
        description="simple example",
        authorities=authorities,
        statement=0,
        data=data,
    )
