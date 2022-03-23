SHELL := /bin/bash

env_name = ainsley
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate


install:
	conda create -n ${env_name} python=3.8 -y

install-reqs:
	pip install --upgrade pip &&\
			pip install -r requirements.txt
	pre-commit install


