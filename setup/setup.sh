#!/bin/bash

python -m venv venv
venv\Scripts\activate
pip install jupyter notebook
ipython kernel install --user --name=venv
pip install -r final-project-dataviz/requirements.txt
jupyter notebook