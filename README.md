# hack-tmp

Hackathon monorepo template with a Python FastAPI backend, PostgreSQL database with `dbmate` SQL migrations, and Docker Compose orchestration.

## Repository Layout

- `backend/` - FastAPI application managed with `uv` (`pyproject.toml`, `uv.lock`, `Dockerfile`). Application code lives in `backend/app/` and automated tests live in `backend/tests/`:
  - `main.py` - FastAPI app initialization, CORS middleware, and router registration
  - `config.py` - Environment-driven settings and database URL construction
  - `db.py` - Async SQLAlchemy engine and session dependency (`SessionDep`)
  - `models.py` - SQLAlchemy ORM models (`ExampleItem`)
  - `schemas.py` - Pydantic request/response schemas (`ItemCreate`, `ItemRead`)
  - `routers/` - API route modules (`health.py` for `/health` and `items.py` for `/api/items`)
  - `tests/` - `pytest` API test suite (`conftest.py`, `test_api.py`)
- `db/init/` - PostgreSQL container entrypoint scripts run on initial volume bootstrap (`01_create_app_user.sh`)
- `db/migrations/` - `dbmate` SQL migrations (`01_grantUserPermissions.sql`, `02_exampleMigration.sql`, `03_seedExampleItems.sql`)
- `frontend/` - Placeholder directory for the React Native client
- `docker-compose.yml` - PostgreSQL (`db`), one-shot migration runner (`dbmate`), and FastAPI (`backend`) services
- `Makefile` - Shorthand commands for running, migrating, formatting, and linting the project
- `.env.example` - Template for required local environment variables

## Prerequisites

- Docker with Docker Compose (`docker compose` v2 or standalone `docker-compose`)
- `make` (optional, for shorthand commands; the `Makefile` auto-detects `docker compose` or `docker-compose`)
- Python 3.13+ and [uv](https://docs.astral.sh/uv/) (optional, required only for running the backend or linter directly on the host)

## Quickstart

### 1. Configure Environment Variables

Copy the example environment file to `.env`:

```sh
cp .env.example .env
```

`.env` configures three groups of settings:

- **Ports**: `POSTGRES_PORT` (default `5432`) and `BACKEND_PORT` (default `8888` in `.env.example`)
- **Database admin credentials**: `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD` (used by PostgreSQL bootstrap and `dbmate` migrations)
- **Application database credentials**: `APP_USER` and `APP_PASSWORD` (used by the FastAPI backend so the app never connects as the database superuser)

### 2. Start the Full Stack in Docker (Recommended)

Build and start PostgreSQL, run migrations, and launch the FastAPI backend with auto-reload:

```sh
make dev
```

To run the stack detached in the background:

```sh
make up
```

On startup:

1. `db` initializes PostgreSQL and runs `db/init/01_create_app_user.sh` to create `APP_USER`.
2. `dbmate` waits for `db` to pass its health check and applies all pending migrations in `db/migrations/`.
3. `backend` waits for `db` and `dbmate`, then serves the API at `http://localhost:<BACKEND_PORT>` (for example `http://localhost:8888`).

To stop the containers:

```sh
make down
```

### 3. Run Database in Docker and Backend on the Host (Optional)

If you prefer running FastAPI directly on your machine while keeping PostgreSQL in Docker:

1. Start PostgreSQL and run migrations:

   ```sh
   make db-up
   ```

2. Sync dependencies and start the local FastAPI development server:

   ```sh
   uv sync --directory backend
   make backend
   ```

When `DATABASE_URL` is not set in the environment, `backend/app/config.py` builds the connection URL from the root `.env` variables using host `localhost` (overridable via `POSTGRES_HOST`). The local `fastapi dev` command serves the API on `http://localhost:8000` by default.

## Testing the API

Replace `8888` below with your `BACKEND_PORT` from `.env` (or `8000` when running `make backend` on the host).

- **Interactive Swagger UI**: `http://localhost:8888/docs`
- **Health check** (`GET /health`):

  ```sh
  curl http://localhost:8888/health
  ```

  Expected response:

  ```json
  {"status":"ok"}
  ```

- **List items** (`GET /api/items`, pre-populated by `03_seedExampleItems.sql`):

  ```sh
  curl http://localhost:8888/api/items
  ```

- **Create an item** (`POST /api/items`):

  ```sh
  curl -X POST http://localhost:8888/api/items \
    -H "Content-Type: application/json" \
    -d '{"name": "Fourth example item"}'
  ```

- **Run automated backend tests** (`pytest`):

  ```sh
  make test
  ```

## Common Commands

| Command | Description |
| --- | --- |
| `make dev` | Build and start all services in the foreground (`up --build`) |
| `make up` | Build and start all services in detached mode (`up -d --build`) |
| `make down` | Stop and remove running containers |
| `make db-up` | Start only `db` and run `dbmate` migrations in detached mode |
| `make db-down` | Stop running database and project containers |
| `make db-reset` | Wipe the database volume (`down -v`) and re-initialize `db` and `dbmate` |
| `make migrate` | Run pending `dbmate` migrations (`run --rm dbmate --wait up`) |
| `make backend` | Run FastAPI locally via `uv` using the root `.env` |
| `make test` | Run the backend `pytest` suite via `uv` |
| `make lint` | Run Ruff linter, Ruff format check, shell syntax check, and `git diff --check` |
| `make format` | Auto-fix lint issues and format Python code with Ruff |

## Database Migrations

SQL migrations live in `db/migrations/` and follow a two-digit prefix and camelCase naming convention (for example `04_addUsersTable.sql`). Each file contains `-- migrate:up` and `-- migrate:down` sections.

After adding a new migration file, apply it with:

```sh
make migrate
```

## Troubleshooting

- **`Set <VAR> in .env` error from Docker Compose**: Ensure `.env` exists in the repository root (`cp .env.example .env`) and all variables from `.env.example` are set.
- **Database authentication fails after changing `.env` credentials**: PostgreSQL entrypoint scripts in `/docker-entrypoint-initdb.d` (`db/init/01_create_app_user.sh`) only run when the data volume is first initialized. To re-initialize the local database volume from scratch (this deletes local database data), run:

  ```sh
  make db-reset
  ```

- **Special characters in database passwords**: `docker-compose.yml` interpolates `POSTGRES_PASSWORD` and `APP_PASSWORD` directly into `DATABASE_URL` strings without URL escaping. Keep passwords alphanumeric/URL-safe in `.env`.
- **`APP_USER` name mismatch in permissions migration**: `db/migrations/01_grantUserPermissions.sql` grants schema and table privileges to `app_user`. Keep `APP_USER=app_user` in `.env`, or update the migration if you rename the role.
- **Port already in use**: Update `POSTGRES_PORT` or `BACKEND_PORT` in `.env` to a free port and restart the stack with `make up`.
