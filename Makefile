test_layers:=unit smoke
export LOCALSTACK_ENABLED:=true
export AWS_PROFILE=localstack
export DATA_DIR=/tmp/localstack/data
export MACUMBA_BUCKET_NAME=macumba-secrets

all: dev-local install tests

tests: unit functional

html-docs:
	cd docs && make html

install:
	pip install -U -t ./build/ .

dev-local:
	pip install -r development.txt

run: install
	sam local start-api

docs: dev-local html-docs
	open docs/build/html/index.html

release: install
	@rm -rf dist/*
	@./.release
	@make pypi

pypi:
	@python setup.py build sdist
	@twine upload dist/*.tar.gz

.PHONY: docs $(test_layers)


$(test_layers):
	nosetests tests/$@

clean:
	@find . -name '*.pyc' -delete

localstack:
	localstack start

stop-localstack:
	@./wait-for-it.sh localhost:4572 -q -t 1 -- ps aux | grep -E 'localstack *start' | grep -v grep | awk '{print $$2}' | xargs kill

functional:
	@nohup localstack start >>localstack.log 2>&1 &
	@./wait-for-it.sh localhost:4572 -q -t 1 -- nosetests tests/functional

ipython:
	ipython
