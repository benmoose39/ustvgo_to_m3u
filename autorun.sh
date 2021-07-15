#!/bin/bash

cd $(dirname $0)/scripts/

echo "grabbing the links..."
python3 ustvgo_m3ugrabber.py

echo "done"
