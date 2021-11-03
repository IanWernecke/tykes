#!/usr/bin/bash
poetry run black -l 120 tykes
# poetry run isort tykes
poetry run isort --profile black -l 120 tykes

