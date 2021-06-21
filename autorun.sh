#!/bin/bash

python3 -m pip install requests

cd scripts/

python3 ustvgo_m3ugrabber.py > ../ustvgo.m3
