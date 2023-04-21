from utils.sign import gen_key_pairs
import codecs


def generate_authority(name: str) -> dict:
    """
    Generates a new authority with a unique set of key-pairs, and returns the authority's details as a dictionary.

    Args:
        name (str): The name of the authority.

    Returns:
        dict: A dictionary with the following keys:
            - "name": The name of the authority (str).
            - "pub_key_x": The x-coordinate of the authority's public key (hexadecimal string).
            - "pub_key_y": The y-coordinate of the authority's public key (hexadecimal string).
            - "private_key": The authority's private key (bytes object).
    """
    # Generate key-pairs
    priv_key, pub_key = gen_key_pairs()

    # Convert the public key into its `x` and `y` points
    pub_key_bytes = codecs.decode(pub_key[2:], "hex_codec")
    pub_key_x = "0x" + "".join("{:02x}".format(x) for x in pub_key_bytes[0:32])
    pub_key_y = "0x" + "".join("{:02x}".format(x) for x in pub_key_bytes[32:64])

    new_authority = {
        "name": name,
        "pub_key_x": pub_key_x,
        "pub_key_y": pub_key_y,
        "private_key": priv_key,
    }

    return new_authority
