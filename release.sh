#!/usr/bin/env bash

rm -f -R ./dist/
./setup.py sdist bdist_wheel
python -m twine upload dist/*