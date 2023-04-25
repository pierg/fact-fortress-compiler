#!/bin/bash

# Activate the Poetry environment
poetry shell

# Start the performance.py script
python3 ./src/performance.py > log.txt 2>&1 &

