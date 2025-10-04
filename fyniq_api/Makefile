# Fluxor Trading API Makefile
# ============================

.PHONY: help install test lint format security clean dev deploy backup docs

# Default help target
help: ## Show this help message
	@echo "Fluxor Trading API - Development Commands"
	@echo "========================================"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Environment Setup
install: ## Install all dependencies
	pip install -r requirements-dev.txt
	npm install --prefix ./src  # If frontend exists
	pre-commit install

install-prod: ## Install production dependencies only
	pip install -r requirements.txt

venv: ## Create virtual environment
	python -m venv venv
	@echo "Activate with: source venv/bin/activate"

# Development
dev: ## Start development servers
	@echo "Starting development environment..."
	docker-compose -f docker-compose.yml up -d db redis
	python manage.py migrate
	python manage.py runserver &
	celery -A fluxor_api worker -l info &
	celery -A fluxor_api beat -l info &

dev-stop: ## Stop development servers
	@echo "Stopping development environment..."
	docker-compose -f docker-compose.yml down
	pkill -f "python manage.py runserver" || true
	pkill -f "celery -A fluxor_api worker" || true
	pkill -f "celery -A fluxor_api beat" || true

# Database Operations
migrate: ## Run database migrations
	python manage.py migrate

makemigrations: ## Create new migrations
	python manage.py makemigrations

reset-db: ## Reset database (WARNING: destroys data)
	python manage.py flush --no-input
	python manage.py migrate
	python manage.py loaddata initial_data.json

superuser: ## Create superuser
	python manage.py createsuperuser

# Testing
test: ## Run all tests
	pytest --cov=. --cov-report=html --cov-report=term-missing -v

test-fast: ## Run tests without coverage
	pytest -x -v --tb=short

test-unit: ## Run unit tests only
	pytest -m "unit" -v

test-integration: ## Run integration tests only
	pytest -m "integration" -v

test-api: ## Run API tests only
	pytest -m "api" -v

test-websocket: ## Run WebSocket tests only
	pytest -m "websocket" -v

test-trading: ## Run trading-specific tests
	pytest -m "trading" -v

test-watch: ## Run tests in watch mode
	pytest-watch -- --tb=short

# Code Quality
lint: ## Run all linting tools
	flake8 .
	black --check .
	isort --check-only .
	mypy .

format: ## Format code
	black .
	isort .

format-check: ## Check code formatting
	black --check .
	isort --check-only .

# Security
security: ## Run security checks
	bandit -r . -x tests/
	safety check
	pip-audit
	semgrep --config=auto .

security-fix: ## Fix security vulnerabilities
	pip-audit --fix

# Performance
profile: ## Profile application performance
	python manage.py runprofileserver

benchmark: ## Run performance benchmarks
	pytest --benchmark-only

load-test: ## Run load tests
	locust -f tests/load_tests/locustfile.py --host=http://localhost:8000

# Monitoring
health-check: ## Check system health
	curl -f http://localhost:8000/api/health/ || exit 1

logs: ## View application logs
	tail -f logs/django.log

logs-celery: ## View Celery logs
	tail -f logs/celery.log

# Docker Operations
docker-build: ## Build Docker images
	docker-compose build

docker-up: ## Start Docker services
	docker-compose up -d

docker-down: ## Stop Docker services
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

docker-shell: ## Open shell in web container
	docker-compose exec web bash

# Data Management
backup: ## Backup database
	@mkdir -p backups
	pg_dump $(DB_NAME) > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Database backed up to backups/"

restore: ## Restore database from backup (specify BACKUP_FILE)
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "Please specify BACKUP_FILE: make restore BACKUP_FILE=backup.sql"; \
		exit 1; \
	fi
	psql $(DB_NAME) < $(BACKUP_FILE)

fixtures: ## Create test fixtures
	python manage.py dumpdata --indent=2 accounts trades > fixtures/test_data.json

load-fixtures: ## Load test fixtures
	python manage.py loaddata fixtures/test_data.json

# Documentation
docs: ## Build documentation
	cd docs && sphinx-build -b html . _build/html
	@echo "Documentation available at docs/_build/html/index.html"

docs-serve: ## Serve documentation locally
	cd docs/_build/html && python -m http.server 8080

docs-clean: ## Clean documentation build
	rm -rf docs/_build

# Deployment
deploy-staging: ## Deploy to staging
	@echo "Deploying to staging..."
	git push staging main
	# Add staging deployment commands

deploy-prod: ## Deploy to production (requires confirmation)
	@echo "Are you sure you want to deploy to production? [y/N]"
	@read -r REPLY; \
	if [ "$$REPLY" = "y" ] || [ "$$REPLY" = "Y" ]; then \
		echo "Deploying to production..."; \
		git push production main; \
	else \
		echo "Deployment cancelled."; \
	fi

# Environment Management
env-check: ## Check environment variables
	@echo "Checking required environment variables..."
	@python -c "from decouple import config; print('✓ Environment configured')" 2>/dev/null || \
		echo "✗ Environment not properly configured. Copy .env.example to .env"

env-example: ## Create .env from example
	cp .env.example .env
	@echo "Created .env from example. Please edit with your values."

# Cleanup
clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage htmlcov/ .pytest_cache/
	rm -rf dist/ build/

clean-all: clean ## Clean everything including venv
	rm -rf venv/
	rm -rf node_modules/
	docker system prune -f

# Trading Specific Commands
update-prices: ## Update cryptocurrency prices
	python manage.py shell -c "from market_data.tasks import update_market_data; update_market_data()"

check-exchanges: ## Check exchange connectivity
	python manage.py shell -c "from core.health_checks import HealthCheckService; print(HealthCheckService().check_exchanges())"

run-strategies: ## Run trading strategies
	python manage.py shell -c "from trading_engine.tasks import run_trading_strategies; run_trading_strategies()"

# API Testing
api-test: ## Test API endpoints
	python test_api.py

api-docs: ## Generate API documentation
	python manage.py spectacular --file schema.yml
	@echo "OpenAPI schema generated: schema.yml"

# Monitoring Setup
setup-monitoring: ## Setup monitoring tools
	@echo "Setting up monitoring..."
	# Add monitoring setup commands

# Development Database
dev-data: ## Load development data
	python manage.py loaddata fixtures/dev_data.json
	@echo "Development data loaded"

# Quick Commands
quick-test: ## Quick test run (fast tests only)
	pytest tests/unit/ -v --tb=short

quick-lint: ## Quick lint (essential checks only)
	flake8 --select=E9,F63,F7,F82 .
	black --check . --fast

serve: ## Start development server
	python manage.py runserver

shell: ## Open Django shell
	python manage.py shell_plus --ipython

# Git Hooks
pre-commit-all: ## Run pre-commit on all files
	pre-commit run --all-files

# Status
status: ## Show project status
	@echo "Fluxor Trading API Status"
	@echo "========================"
	@echo "Python version: $$(python --version)"
	@echo "Django version: $$(python -c 'import django; print(django.get_version())')"
	@echo "Database status: $$(python manage.py migrate --check 2>/dev/null && echo '✓ Up to date' || echo '✗ Migrations needed')"
	@echo "Redis status: $$(redis-cli ping 2>/dev/null || echo 'Not running')"
	@echo "Environment: $$(python -c 'from django.conf import settings; print(\"Development\" if settings.DEBUG else \"Production\")')"