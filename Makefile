.PHONY: install run run-interactive test clean

VENV=.venv
PY_BOOTSTRAP?=python3
PYTHON=$(VENV)/bin/python
PIP=$(PYTHON) -m pip

$(PYTHON):
	$(PY_BOOTSTRAP) -m venv $(VENV)
	$(PIP) install -U pip
	$(PIP) install -e .

install: $(PYTHON)

run: $(PYTHON)
	PYTHONPATH=src AUTO_CONFIRM=1 $(PYTHON) -m plangate_demo.main

run-interactive: $(PYTHON)
	PYTHONPATH=src AUTO_CONFIRM=0 $(PYTHON) -m plangate_demo.main

test: $(PYTHON)
	$(PYTHON) -m pytest -q

clean:
	rm -rf $(VENV) .pytest_cache __pycache__ src/plangate_demo/__pycache__ tests/__pycache__
