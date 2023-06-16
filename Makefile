.PHONY: all test clean lint static
VENV_PYTHON:=.test.venv/bin/python
SRCS_DIR:=src
TSCS_DIR:=tests
SRCS:=$(shell find $(SRCS_DIR) -name '*.py')
TSCS:=$(shell find $(TSCS_DIR) -name '*.py')

all: test

build:
	python setup.py bdist
	@touch $@

.%.venv: setup.py
	rm -rf $@
	python -m venv $@
	$@/bin/python -m pip install -e .[$*]
	touch $@

test: .test.venv
	$(VENV_PYTHON) -m pytest

lint: .test.venv .lint
.lint: $(SRCS) $(TSCS)
	$(VENV_PYTHON) -m flake8 $?
	touch $@

static: .test.venv .static
.static: $(SRCS) $(TSCS)
	$(VENV_PYTHON) -m mypy $^
	touch $@

autopep8: .test.venv .autopep8
.autopep8: $(SRCS) $(TSCS)
	$(VENV_PYTHON) -m autopep8 --in-place --max-line-length 80 $?

clean:
	rm -rf .install build dist .eggs
	rm -rf .lint .static
