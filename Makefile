SHELL=/bin/bash
PATH := .venv/bin:$(PATH)
export TEST?=./tests
export ENV?=dev

install:
	@( \
		if [ ! -d .venv ]; then python3 -m venv --copies .venv; fi; \
		source .venv/bin/activate; \
		pip install -qU pip; \
		pip install -r requirements.txt; \
	)

run-dev:
	@source .venv/bin/activate; \
	python Todo_automatico.py 

run:
	@( \
		if [ ! -d .venv ]; then python3 -m venv --copies .venv; fi; \
		source .venv/bin/activate; \
		python3 src/app/main.py; \
	)

autoflake:
	@autoflake . --check --recursive --remove-all-unused-imports --remove-unused-variables --exclude .venv;

black:
	@black . --check --exclude '.venv|build|target|dist|.cache|node_modules';

isort:
	@isort . --check-only;

lint: black isort autoflake

lint-fix:
	@black . --exclude '.venv|build|target|dist';
	@isort .;
	@autoflake . --in-place --recursive --exclude .venv --remove-all-unused-imports --remove-unused-variables;