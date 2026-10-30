COMPOSE ?= $(shell docker compose version >/dev/null 2>&1 && echo "docker compose" || echo "docker-compose")

.PHONY: dev up down db-up db-down migrate backend lint format

dev:
	$(COMPOSE) up --build

up:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

db-up:
	$(COMPOSE) up -d db dbmate

db-down:
	$(COMPOSE) down

migrate:
	$(COMPOSE) run --rm dbmate --wait up

backend:
	uv run --directory backend --env-file ../.env fastapi dev

lint:
	uv run --directory backend ruff check
	uv run --directory backend ruff format --check
	sh -n db/init/*.sh
	git diff --check

format:
	uv run --directory backend ruff check --fix
	uv run --directory backend ruff format
