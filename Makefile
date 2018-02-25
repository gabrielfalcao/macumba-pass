test_layers:=unit functional

tests: unit functional

html-docs:
	cd docs && make html

run:
	pip install -t . -r requirements.txt
	sam local start-api

docs: html-docs
	open docs/build/html/index.html

release:
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


smoke:
	curl -H GET http://localhost:3000/
