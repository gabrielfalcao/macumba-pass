test_layers:=unit
export LOCALSTACK_ENABLED:=true
export AWS_PROFILE:=localstack
export DATA_DIR:=/tmp/localstack/data
export MACUMBA_BUCKET_NAME:=macumba-secrets
export LAMBDA_EXECUTOR:=local

all: dev-local install tests

tests: unit functional

html-docs:
	cd docs && make html

install:
	pip install -t ./build/ .
	chmod -R 777 ./build/

reinstall:
	pip install -U -t ./build/ .

dev-local:
	pip install -r development.txt

run:
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
	@echo 'removing ./build'
	@rm -rf build


localstack:
	localstack start

stop-localstack:
	@./wait-for-it.sh localhost:4572 -q -t 1 -- ps aux | grep -E 'localstack *start' | grep -v grep | awk '{print $$2}' | xargs kill

functional:
	@./wait-for-it.sh localhost:4572 -q -t 1 -- nosetests tests/functional

smoke:
	@python tests/smoke.py

ipython:
	ipython

bucket:
	AWS_PROFILE=personal aws s3 mb s3://macumba-lambda

package:
	AWS_PROFILE=personal sam package --template-file=template.yaml --s3-bucket=macumba-lambda --output-template-file packaged-template.yaml

deploy: package
	AWS_PROFILE=personal sam deploy --template-file=packaged-template.yaml --stack-name=macumba-lambda-sandbox --capabilities CAPABILITY_IAM

full-deploy: install deploy

force-redeploy: clean install deploy
