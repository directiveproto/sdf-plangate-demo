.PHONY: install run run-cloud run-interactive test record gif clean

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

run-cloud: install
	test -n "$$CLOUD_BASE_URL"
	test -n "$$CLOUD_API_KEY"
	PYTHONPATH=src SDF_MODE=cloud AUTO_CONFIRM=1 $(PYTHON) -m plangate_demo.main

run-interactive: install
	PYTHONPATH=src AUTO_CONFIRM=0 $(PYTHON) -m plangate_demo.main

test: install
	$(PYTHON) -m pytest -q

record: install
	mkdir -p docs
	asciinema rec --overwrite docs/plangate.cast --title "PlanGate demo: unsafe write blocked -> confirm -> continue" --idle-time-limit 1 --command "PYTHONPATH=src AUTO_CONFIRM=1 $(PYTHON) -m plangate_demo.main"

gif:
	test -f docs/plangate.cast
	docker run --rm -v "$(CURDIR):/data" ghcr.io/asciinema/agg:latest /data/docs/plangate.cast /data/docs/demo.gif

clean:
	rm -rf $(VENV) .pytest_cache __pycache__ src/plangate_demo/__pycache__ tests/__pycache__
