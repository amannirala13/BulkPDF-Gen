#!/bin/bash

#Installing venv
python -m pip install virtualenv

#Creting virtual env as env
python -m venv env

echo
echo "----------------------------------------------------"
echo "	To activate the environment use the command:"
echo
echo "	-> source env/bin/activate"
echo
echo "	To deactivate the environment use the command:"
echo
echo "	-> deactivate"
echo "----------------------------------------------------"
