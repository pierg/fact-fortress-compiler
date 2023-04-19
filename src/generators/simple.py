from utils.sign import gen_key_pairs
from utils.generate_configs import generate_configuration_json
import numpy as np
import codecs


def generate_simple(name: str):
    data_1 = [1, 2]
    data_2 = [3, 4]

    data = [
        {
            "description": "Sample data 1",
            "values": data_1,
            "type": "int",
            "format": "u8",
            "shape": [2, 1],
        },
        {
            "description": "Sample data 2",
            "values": data_2,
            "type": "double",
            "precision": 1,
            "format": "u8",
            "shape": [2, 1],
        },
    ]

    # Generate key-pairs
    priv_key, pub_key = gen_key_pairs()

    # Convert the public key into its `x` and `y` points
    pub_key_bytes = codecs.decode(pub_key[2:], "hex_codec")
    pub_key_x = "0x" + "".join("{:02x}".format(x) for x in pub_key_bytes[0:32])
    pub_key_y = "0x" + "".join("{:02x}".format(x) for x in pub_key_bytes[32:64])

    generate_configuration_json(
        name=name,
        description="simple example",
        pub_key_x=pub_key_x,
        pub_key_y=pub_key_y,
        private_key=priv_key,
        statement=0,
        data=data,
    )
