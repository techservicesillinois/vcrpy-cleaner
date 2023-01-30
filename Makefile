.PHONY: all test clean
VENV_PYTHON:=.test.venv/bin/python
TENV_PYTHON:=.integration.venv/bin/python

all: test

build:
	python setup.py bdist
	@touch $@

#TODO: Collapse 12 and 18 so make will not try to delete the venv, or add the venv to .PRECIOUS
.%.venv: setup.py
	rm -rf $@
	python -m venv $@
	$@/bin/python -m pip install -e .[$*]
	touch $@

test: .test.venv
	$(VENV_PYTHON) -m pytest

integration: .integration.venv
	$(TENV_PYTHON) -m mypy tests/integration/mypy_test.py

clean:
	rm -rf .install build dist .eggs
