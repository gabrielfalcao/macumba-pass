test_layers:=unit functional smoke
export LOCALSTACK_ENABLED:=true
export AWS_PROFILE=localstack

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
