.PHONY: all test clean
VENV_PYTHON:=venv/bin/python
TENV_PYTHON:=test_venv/bin/python

all: test

build:
	python setup.py bdist
	@touch $@

venv: setup.py
	rm -rf $@
	python -m venv $@

test_venv: setup.py
	rm -rf $@
	python -m venv $@

# Install package in develop mode
.install: setup.py venv
	$(VENV_PYTHON) -m pip install -e .[test]
	@touch $@

test: .install
	$(VENV_PYTHON) -m pytest

.test_deps: test_venv
	$(TENV_PYTHON) -m pip install -e . mypy vcrpy

integration: .test_deps
	$(TENV_PYTHON) -m mypy tests/integration/mypy_test.py

clean:
	rm -rf .install build dist .eggs