#!/bin/bash

python3 -m pip install requests

cd scripts/

echo "grabbing the links..."
python3 ustvgo_m3ugrabber.py > ../ustvgo.m3

echo "done"
