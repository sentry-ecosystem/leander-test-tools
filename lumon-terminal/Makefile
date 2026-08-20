.DEFAULT_GOAL := help

.PHONY: help setup install run generate test

help:
	@printf "setup      Create .venv and install dependencies\n"
	@printf "run        Start the Lumon terminal on port 5001\n"
	@printf "generate   Send all demo incidents to Sentry\n"
	@printf "test       Run the test suite without sending events\n"

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements-dev.txt

install:
	.venv/bin/pip install -r requirements-dev.txt

run:
	.venv/bin/python app.py

generate:
	.venv/bin/python scripts/generate_incidents.py

test:
	SENTRY_DSN= .venv/bin/pytest -q
