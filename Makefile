.PHONY: help install run test format lint migrate superuser shell clean docker-up docker-down docker-build docker-logs

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements-dev.txt

run: ## Run development server
	python manage.py runserver

test: ## Run tests with coverage
	pytest

test-verbose: ## Run tests in verbose mode
	pytest -v

test-coverage: ## Run tests with coverage report
	pytest --cov=. --cov-report=html --cov-report=term-missing

format: ## Format code with black and isort
	black .
	isort .

lint: ## Run linting checks
	flake8 .
	black --check .
	isort --check-only .

migrate: ## Run database migrations
	python manage.py migrate

makemigrations: ## Create database migrations
	python manage.py makemigrations users books loans

superuser: ## Create a superuser
	python manage.py createsuperuser

shell: ## Open Django shell
	python manage.py shell

collectstatic: ## Collect static files
	python manage.py collectstatic --noinput

clean: ## Clean Python cache files
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf .coverage

docker-up: ## Start Docker containers
	docker-compose up -d

docker-down: ## Stop Docker containers
	docker-compose down

docker-build: ## Build Docker image
	docker-compose build

docker-logs: ## View Docker logs
	docker-compose logs -f

docker-shell: ## Open shell in Docker container
	docker-compose exec web bash

docker-migrate: ## Run migrations in Docker
	docker-compose exec web python manage.py migrate

docker-superuser: ## Create superuser in Docker
	docker-compose exec web python manage.py createsuperuser

docker-test: ## Run tests in Docker
	docker-compose exec web pytest

setup: install migrate ## Initial setup (install dependencies and run migrations)

