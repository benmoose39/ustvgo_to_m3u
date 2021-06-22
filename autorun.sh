#!/bin/bash

python3 -m pip install requests

cd $(dirname $0)/scripts/

echo "grabbing the links..."
python3 ustvgo_m3ugrabber.py > ../ustvgo.m3u

echo "done"
