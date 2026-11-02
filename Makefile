COMPOSE ?= $(shell docker compose version >/dev/null 2>&1 && echo "docker compose" || echo "docker-compose")

.PHONY: dev prod down test lint format help

dev: ## Build and start all services in the foreground
	$(COMPOSE) up --build

prod: ## Build and start all services in detached mode
	$(COMPOSE) up -d --build

down: ## Stop and remove running containers
	$(COMPOSE) down

test: ## Run backend tests with pytest
	uv run --directory backend pytest

lint: ## Run code linters and checks
	uv run --directory backend ruff check
	uv run --directory backend ruff format --check
	sh -n db/init/*.sh
	git diff --check

format: ## Auto-fix lint issues and format code
	uv run --directory backend ruff check --fix
	uv run --directory backend ruff format

help: ## Show this help message
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z_-]+:.*## / {printf "  %-10s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
