.PHONY: install test lint format run clean

install:
	pip install poetry
	poetry install

test:
	poetry run pytest tests/ -v --cov=src

lint:
	poetry run black --check src/ tests/
	poetry run flake8 src/ tests/
	poetry run mypy src/

format:
	poetry run black src/ tests/

run:
	poetry run python -m src.api.main

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache htmlcov dist build