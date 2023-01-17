.PHONY: all test clean
VENV_PYTHON:=venv/bin/python

all: test

venv: setup.py
	rm -rf $@
	python -m venv $@

# Install package in develop mode
.install: setup.py venv
	$(VENV_PYTHON) -m pip install -e .[test]
	@touch $@

test: .install
	$(VENV_PYTHON) -m pytest

clean:
	rm -rf .install