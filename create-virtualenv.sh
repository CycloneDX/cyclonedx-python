#!/usr/bin/env bash
# Initializes a python virtual environment and installs dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt