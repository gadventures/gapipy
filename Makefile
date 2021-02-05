.PHONY: clean-pyc clean-build docs clean

VERSION := $(shell python setup.py --version)

all: version help

version:
	@echo " gapipy.__version__ == $(VERSION)"
	@echo

help:
	@echo " Make targets"
	@echo
	@echo " * clean-build - remove build artifacts"
	@echo " * clean-pyc   - remove Python file artifacts"
	@echo " * coverage    - check code coverage quickly with the default Python"
	@echo " * dist        - package"
	@echo " * docs        - generate Sphinx HTML documentation, including API docs"
	@echo " * help        - print this help doc"
	@echo " * lint        - check style with flake8"
	@echo " * release     - package and upload a release"
	@echo " * test        - run tests quickly with the default Python"
	@echo

clean: clean-build clean-pyc
	@rm -fr htmlcov/

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

lint:
	@flake8 gapipy tests

test:
	@python setup.py test

coverage:
	@coverage run --source gapipy setup.py test
	@coverage report -m
	@coverage html
	@open htmlcov/index.html

test-coverage: test coverage

docs:
	@rm -f docs/gapipy.rst
	@rm -f docs/modules.rst
	@sphinx-apidoc -o docs/ gapipy
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	@open docs/_build/html/index.html

release: clean
	@python setup.py -q sdist
	@twine upload dist/gapipy-$(VERSION).tar.gz

dist: clean
	@python setup.py -q sdist
	@ls -l dist
	@twine check dist/gapipy-${VERSION}.tar.gz
