#!/bin/bash

command -v python3 -m venv >/dev/null 2>&1 || { echo >&2 "Python 3.3 required. Install it and try again. Aborting"; exit 1; }

if [ ! -d "env" ]; then
    echo "No virtualenv. Creating one"
    python3 -m venv env
    source env/bin/activate
    # With a new venv, we want to force (without checking if it exists first) installing a venv pip
    # or else we'll end up with the system one.
    python get-pip.py $PIPARGS --force-reinstall
else
    echo "There's already an env. Activating it"
    source env/bin/activate
fi

command -v pip
if [ $? -ne 0 ]; then
    echo "pip not installed. Installing."
    python get-pip.py $PIPARGS
fi

echo "Installing pip requirements"
pip install $PIPARGS -r requirements.txt

echo "Bootstrapping complete!"
