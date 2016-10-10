test: bin/python
	python -m unittest -v t 

bin/pip:
	virtualenv -p python3 .

install-dev: bin/pip
	$< install -r ./requirements.txt

install: bin/python
	$< -m jupyter_gauche.install --user $(user)

upload: bin/python
	$< setup.py sdist upload -v

register: bin/python
	$< setup.py register
