
virtualenv:
	virtualenv -p python3 .

install-dev:
	./bin/pip install -r ./requirements.txt
