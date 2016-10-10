test:
	python -m unittest -v t 

bin/pip:
	virtualenv -p python3 .

install-dev: bin/pip
	$< install -r ./requirements.txt

install:
	python -m gauche_kernel.install --user $(user)
