all: lint build install test

lint:
	poetry run black -l 120 tykes
	poetry run isort --profile black -l 120 tykes

build:
	poetry build

install:
	poetry install 

test:
	poetry run pytest tests/
