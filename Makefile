test_layers:=unit smoke
export LOCALSTACK_ENABLED:=true
export AWS_PROFILE=personal
export DATA_DIR=/tmp/localstack/data
export MACUMBA_BUCKET_NAME=macumba-secrets

all: dev-local install tests

tests: unit functional

html-docs:
	cd docs && make html

install:
	pip install -t ./build/ .
	find build -type d -exec chmod 755 {} \;
	find build -type f -exec chmod 754 {} \;

reinstall:
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

package:
	aws s3 mb s3://macumba-lambda
	sam package --template-file=template.yaml --s3-bucket=macumba-lambda --output-template-file packaged-template.yaml


deploy: package
	sam deploy --template-file=packaged-template.yaml --stack-name=macumba-lambda-sandbox --capabilities CAPABILITY_IAM --parameter-overrides MacumbaBucketName=macumba-secrets
