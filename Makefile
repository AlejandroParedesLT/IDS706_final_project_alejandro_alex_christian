# Install dependencies
install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

# Run tests in the backend folder
test:
	python -m pytest -vv backend/test_*.py

# Format Python code
format:
# black backend/*.py 
	black .

# Lint Python code
lint:
	ruff check backend/*.py 

# Lint Dockerfile
container-lint:
	docker run --rm -i hadolint/hadolint < backend/Dockerfile

# Refactor: Format and Lint together
refactor: format lint

# Deploy (placeholder)
deploy:
	# Add your deployment steps here

# Default target: Run all tasks
all: install lint test format deploy
