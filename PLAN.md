# Hackathon Template Implementation Plan

This document details the tasks required to turn this repository into a ready-to-code hackathon backend and database monorepo template. Each task is self-contained with a dedicated title and description.

## Tasks

### Task 1: Database Application User Initialization and Permission Management
- **Title**: Create application database user via container entrypoint and manage permissions in dbmate migrations
- **Description**: Configure PostgreSQL container entrypoint (`/docker-entrypoint-initdb.d/01_create_app_user.sh`) to initialize a dedicated application user (`APP_USER`, `APP_PASSWORD`) using environment variables from `.env`. Configure `dbmate` in `docker-compose.yml` to run migrations using the administrative superuser (`POSTGRES_USER`). Add migration `db/migrations/01_grantUserPermissions.sql` to grant database connection, public schema usage, table CRUD, and default privileges to `APP_USER`. Move table creation migrations to subsequent versions (starting at `02_exampleMigration.sql`).
- **Status**: Done

### Task 2: Backend Scaffolding and Dependency Management
- **Title**: Initialize FastAPI application with modern dependency management
- **Description**: Configure the `backend/` directory using modern Python tooling (such as `uv` or `pyproject.toml`). Create `backend/app/main.py` with FastAPI initialization, structured application config reading from environment variables, and preconfigured `CORSMiddleware` (allowing cross-origin communication from local development clients). Remove `backend/.gitkeep`.
- **Status**: Done

### Task 3: Code Quality, Linting, and Automated Checks
- **Title**: Configure lightweight linting with Ruff and project check commands
- **Description**: Add `ruff` as a development dependency in the backend project (`pyproject.toml` or `uv`) for ultra-fast linting and code formatting. Define unified check commands (`ruff check .`, `ruff format --check .`, `sh -n db/init/*.sh`, and `git diff --check`). Update `AGENTS.md` validation instructions to reference these commands so agents and contributors automatically validate changes.
- **Status**: Done

### Task 4: Database Client and ORM Integration
- **Title**: Configure PostgreSQL connection and data models for application user
- **Description**: Set up an asynchronous database layer (using SQLModel or SQLAlchemy with `asyncpg`). Wire connection parameters so the application connects strictly as `APP_USER` via `DATABASE_URL` (without administrative superuser privileges). Define Python models corresponding to the `example_items` table and configure FastAPI dependency injection for database sessions. `DATABASE_URL` is used when set (Docker Compose), otherwise it is built from the root `.env` values (`APP_USER`, `APP_PASSWORD`, `POSTGRES_DB`, `POSTGRES_PORT`) with host `localhost`, which can be overridden with `POSTGRES_HOST`.
- **Status**: Done

### Task 5: Base API Endpoints and Healthcheck
- **Title**: Implement health check and sample CRUD endpoints
- **Description**: Add a `/health` endpoint that checks application and database connectivity. Implement basic CRUD endpoints under `/api/items` for querying and creating `example_items`. This serves as a working reference pattern for team members during the hackathon.
- **Status**: Done

### Task 6: Backend Containerization
- **Title**: Create backend Dockerfile and register service in Docker Compose
- **Description**: Add a `backend/Dockerfile` optimized for local development with auto-reload. Add the `backend` service definition to `docker-compose.yml`, configuring port mapping, environment variables from `.env`, and healthcheck dependencies on the `db` and `dbmate` services. Compose is the preferred way to run the backend, so set `DATABASE_URL` for the backend service from the `.env` values with host `db` (`postgresql+asyncpg://APP_USER:APP_PASSWORD@db:POSTGRES_PORT/POSTGRES_DB`, like dbmate's URL). Keep `APP_PASSWORD` URL-safe, since Compose does not escape it.
- **Status**: Done

### Task 7: Database Mock and Seed Data
- **Title**: Add database seed script for instant prototyping
- **Description**: Create a seed script or migration containing realistic placeholder data for `example_items`. This allows developers to test API endpoints and business logic immediately without having to manually insert test records.
- **Status**: Done

### Task 8: Task Runner and Developer Experience
- **Title**: Add Makefile for one-command workflows
- **Description**: Provide a `Makefile` with clear shorthand commands (such as `make dev`, `make db-up`, `make db-down`, `make migrate`, `make backend`, and `make lint`). This eliminates friction and saves time during quick iterations.
- **Status**: Done

### Task 9: Documentation and Hackathon Quickstart Guide
- **Title**: Write a comprehensive Quickstart guide in README.md
- **Description**: Update `README.md` with step-by-step onboarding instructions for the entire stack once fully built: prerequisites, setting up `.env`, running database services, starting the backend, and testing the API. Include troubleshooting tips for common hackathon issues.

### Task 10: Baseline README with Implemented Database Startup Instructions
- **Title**: Create placeholder README with startup instructions for implemented database services
- **Description**: Add a concise, placeholder `README.md` documenting exclusively what is currently implemented and working in the repository. Provide clear instructions for copying `.env.example` to `.env`, running `docker compose up -d` to initialize PostgreSQL and run dbmate migrations (including application user creation via the entrypoint script and permission setup via migration 01), and verifying database readiness. Avoid documenting unimplemented backend or frontend services until they are built.
