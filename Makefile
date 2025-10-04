# Fluxor Trading Platform Makefile
# Production deployment and development commands

.PHONY: help install dev test build deploy clean backup restore logs status

# Default target
help:
	@echo "Fluxor Trading Platform - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  make dev          - Start development environment"
	@echo "  make test         - Run all tests"
	@echo "  make lint         - Run linting and formatting"
	@echo "  make build        - Build all Docker images"
	@echo ""
	@echo "Production:"
	@echo "  make deploy       - Deploy to production"
	@echo "  make backup       - Create backup"
	@echo "  make restore      - Restore from backup"
	@echo ""
	@echo "Maintenance:"
	@echo "  make logs         - Show application logs"
	@echo "  make status       - Show service status"
	@echo "  make clean        - Clean up Docker resources"
	@echo "  make install      - Install dependencies"
	@echo ""

# Development
dev:
	@echo "🚀 Starting development environment..."
	docker-compose up -d
	@echo "✅ Development environment started"
	@echo "   Frontend: http://localhost:5173"
	@echo "   Dashboard: http://localhost:3001"
	@echo "   API: http://localhost:8000"

# Testing
test:
	@echo "🧪 Running tests..."
	@echo "Running Python tests..."
	cd fluxor_api && python manage.py test
	@echo "Running Frontend tests..."
	cd fluxor-frontend && npm test
	@echo "Running Dashboard tests..."
	cd fluxor-dashboard && npm test
	@echo "✅ All tests completed"

# Linting
lint:
	@echo "🔍 Running linting..."
	@echo "Linting Python code..."
	cd fluxor_api && flake8 . && black --check . && isort --check-only .
	@echo "Linting Frontend code..."
	cd fluxor-frontend && npm run lint
	@echo "Linting Dashboard code..."
	cd fluxor-dashboard && npm run lint
	@echo "✅ Linting completed"

# Build
build:
	@echo "🔨 Building Docker images..."
	docker-compose build --no-cache
	@echo "✅ Build completed"

# Production deployment
deploy:
	@echo "🚀 Deploying to production..."
	./deploy.sh
	@echo "✅ Deployment completed"

# Backup
backup:
	@echo "💾 Creating backup..."
	@mkdir -p backups
	@tar -czf backups/fluxor_backup_$(shell date +%Y%m%d_%H%M%S).tar.gz \
		--exclude='node_modules' \
		--exclude='.git' \
		--exclude='*.log' \
		--exclude='backups' \
		.
	@echo "✅ Backup created in backups/ directory"

# Restore (requires BACKUP_FILE variable)
restore:
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "❌ Please specify BACKUP_FILE=path/to/backup.tar.gz"; \
		exit 1; \
	fi
	@echo "🔄 Restoring from backup: $(BACKUP_FILE)"
	@tar -xzf $(BACKUP_FILE)
	@echo "✅ Restore completed"

# Logs
logs:
	@echo "📋 Showing application logs..."
	docker-compose -f docker-compose.prod.yml logs -f

# Status
status:
	@echo "📊 Service Status:"
	@docker-compose -f docker-compose.prod.yml ps
	@echo ""
	@echo "🔍 Health Checks:"
	@echo -n "API: "
	@curl -s -f http://localhost:8000/api/health/ > /dev/null && echo "✅ Healthy" || echo "❌ Unhealthy"
	@echo -n "Frontend: "
	@curl -s -f http://localhost:5173/ > /dev/null && echo "✅ Healthy" || echo "❌ Unhealthy"
	@echo -n "Dashboard: "
	@curl -s -f http://localhost:3001/ > /dev/null && echo "✅ Healthy" || echo "❌ Unhealthy"

# Clean
clean:
	@echo "🧹 Cleaning up Docker resources..."
	docker-compose down --volumes --remove-orphans
	docker system prune -f
	docker image prune -f
	@echo "✅ Cleanup completed"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	@echo "Installing Python dependencies..."
	cd fluxor_api && pip install -r requirements.txt
	@echo "Installing Frontend dependencies..."
	cd fluxor-frontend && npm install
	@echo "Installing Dashboard dependencies..."
	cd fluxor-dashboard && npm install
	@echo "✅ Dependencies installed"

# Database operations
migrate:
	@echo "🗄️ Running database migrations..."
	docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
	@echo "✅ Migrations completed"

collectstatic:
	@echo "📁 Collecting static files..."
	docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
	@echo "✅ Static files collected"

createsuperuser:
	@echo "👤 Creating superuser..."
	docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
	@echo "✅ Superuser created"

# Security
security-scan:
	@echo "🔒 Running security scan..."
	cd fluxor_api && bandit -r . -f json -o bandit-report.json
	cd fluxor_api && safety check --json --output safety-report.json
	@echo "✅ Security scan completed"

# Monitoring
monitor:
	@echo "📊 System monitoring..."
	@echo "Docker stats:"
	@docker stats --no-stream
	@echo ""
	@echo "Disk usage:"
	@df -h
	@echo ""
	@echo "Memory usage:"
	@free -h

# Quick commands
up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

# Production quick commands
prod-up:
	docker-compose -f docker-compose.prod.yml up -d

prod-down:
	docker-compose -f docker-compose.prod.yml down

prod-restart:
	docker-compose -f docker-compose.prod.yml restart

# Development helpers
shell:
	docker-compose exec web python manage.py shell

dbshell:
	docker-compose exec db psql -U fluxor -d fluxor_prod

redis-cli:
	docker-compose exec redis redis-cli
