# fact-fortress-circtuits

Python library facilitate the generation of Zero-Knowledge Proof circuits in [noir](https://noir-lang.org).

The library can compile circuits with various input data sizes and formats.

All the circuits compiled comes with a ZKP certifying the data proverance and consistency.

You can generate and verify proofs on the compiled circuits by navigating to the folder `circuits/YOU_CIRCUIT` and run:


```bash
nargo prove p
```

```bash
nargo prove p
```

This library has been used to generate valid circuit for [fact-fortress-dapp](https://github.com/pierg/fact-fortress-dapp)

# Installing

## System requirements
[noir](https://noir-lang.org)

[pdm](https://pdm.fming.dev/latest/)

[python 3.11](https://www.python.org)


## Install Dependencies

To install run:

```bash
pdm install
```


# Example

1. delete `circuits` and `configurations` folder
2. run `pdm run python src/main.py` to generate configurations and circuits from scratch
3. navigate to a circuit, i.e. `cd circuits/simple`
4. prove and verify the circuit by running `nargo prove p` and `nargo verify p`
