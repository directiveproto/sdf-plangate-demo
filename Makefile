.PHONY: install run run-interactive test

install:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -e .

run:
	AUTO_CONFIRM=1 python -m plangate_demo.main

run-interactive:
	AUTO_CONFIRM=0 python -m plangate_demo.main

test:
	python -m pytest -q
