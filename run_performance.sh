#!/bin/bash

# Activate the Poetry environment
poetry shell

# Start the performance.py script
# python3 ./src/performance.py --bits 16 --rng 10 100 --step 50 > log.txt 2>&1 &
# python3 ./src/performance.py --bits 16 --rng 10 4000000000 --step 50 > log.txt 2>&1 &
python3 ./src/performance.py --bits 16 --rng 10 4000000000 --step 50 > log.txt 2>&1 &
