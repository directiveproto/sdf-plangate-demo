.PHONY: install run run-interactive test clean

VENV=.venv
PY_BOOTSTRAP?=python3
PYTHON=$(VENV)/bin/python
PIP=$(PYTHON) -m pip

install:
	test -x $(PYTHON) || $(PY_BOOTSTRAP) -m venv $(VENV)
	$(PIP) install -U pip
	$(PIP) install -e .
	$(PIP) install pytest

run: install
	PYTHONPATH=src AUTO_CONFIRM=1 $(PYTHON) -m plangate_demo.main

run-interactive: install
	PYTHONPATH=src AUTO_CONFIRM=0 $(PYTHON) -m plangate_demo.main

test: install
	$(PYTHON) -m pytest -q

clean:
	rm -rf $(VENV) .pytest_cache __pycache__ src/plangate_demo/__pycache__ tests/__pycache__
