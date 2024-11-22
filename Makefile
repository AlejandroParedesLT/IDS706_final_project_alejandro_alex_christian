install:
	pip install -r requirements.txt
format:
	black *.py
lint:
	ruff check *.py ./lib/*.py
test:
	python -m pytest -vv --nbval -cov=mylib -cov=main test_main.py



all: install format test lint run_cli