SHELL=/bin/bash

env_name = ainsley

install-kernel:
	conda create -n ${env_name} python=3.8 -y
	python -m ipykernel install --user --name ${env_name} --display-name "${env_name}"

install-conda:
	make install-kernel

install-reqs:
	pip install -r requirements.txt
	
	

