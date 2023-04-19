# noir-zkp

Python library to create noir circuits 

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
