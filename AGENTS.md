# AGENTS.md

## Project overview

- Project brief: we are creating `[complete here]`.
- Planned stack: React Native for the frontend, Python with FastAPI for the backend, PostgreSQL for the database, and Docker with Docker Compose.
- Development environment: VS Code on macOS, Windows, and Linux. `.gitignore` should cover generated artifacts from the stack and development environments, as well as local secret files.

## Working rules

- **Simplicity is the key**: Keep things simple. Do not generate boilerplate, overengineered abstractions, or premature complexity. Write minimal, clean, and direct code that solves the task directly.
- Always use classic dashes (`-`) rather than em dashes in code, comments, documentation, commit messages, and responses.
- Follow the repository's existing code structure, formatting, commenting, and documentation style. Read nearby files before editing and use established tooling when available.
- Never delete comments written by the user. If a comment conflicts with a requested change, point out the conflict and ask the user how to resolve it. The only exception is a TODO comment addressed by your changes, which may be removed when replaced with the corresponding implementation.
- Add code comments only when needed. Keep them simple, straightforward, and idiomatic, without excessive formatting. Avoid decorative, obvious, or boilerplate comments.
- Make only changes needed to complete the requested task. Report unrelated errors or improvement opportunities instead of fixing them without being asked.
- Inspect the working tree before editing and preserve unrelated or pre-existing changes.
- Challenge unclear requirements or assumptions. Ask the user for clarification before implementing an ambiguous decision rather than inventing behavior, architecture, or scope. Continue independent work that does not depend on the answer.
- Validate that changes are correct and do not break related behavior. Review the final diff, run relevant available checks, and report their results and any checks that could not be run. Use `[complete here]` for validation.
- Use `.gitkeep` to include otherwise empty directories in Git. Remove a directory's `.gitkeep` once it contains other tracked files.

## Code style and formatting conventions

- **Core philosophy**: Simplicity and readability. Every line, comment, and configuration entry must have a clear purpose. Avoid boilerplate, speculative features, or redundant helpers.
- **Dashes**: Always use classic ASCII dashes (`-`) rather than em dashes or en dashes.
- **Whitespace and line breaks**:
  - Use blank lines purposefully to separate logical units, not randomly.
  - SQL migrations (`db/migrations/`):
    - File naming follows a two-digit prefix and camelCase name (e.g. `01_grantUserPermissions.sql`, `02_exampleMigration.sql`).
    - Add a blank line immediately after `-- migrate:up` and `-- migrate:down`.
    - Group distinct logical blocks with a single blank line (e.g. between `DO $$ ... $$;` blocks, `GRANT` statements, and `ALTER DEFAULT PRIVILEGES`).
    - Separate the end of the `migrate:up` section from the `-- migrate:down` header with two blank lines.
  - Shell scripts (`db/init/`):
    - Use POSIX shell (`#!/bin/sh`) with `set -e`.
    - Place a single blank line after the shebang and after `set -e`.
    - Keep scripts concise, minimal, and idiomatic without wrapper bloat.
  - Environment files (`.env`, `.env.example`):
    - Logically group related variables (such as network ports, administrative database credentials, and application credentials).
    - Separate variable groups with a single blank line.
    - Avoid noisy inline comments; let variable names remain self-explanatory.
  - Docker Compose (`docker-compose.yml`):
    - Use strict 2-space indentation for hierarchy.
    - Separate service definitions with a single blank line.
    - Format multi-line array arguments with clean line breaks (such as healthcheck `test`).
    - Use the `${VAR:?Set VAR in .env}` pattern for required environment variables.
    - Preserve section comments that indicate extension points (e.g. `# other services can go here`).
- **Comments**:
  - Add comments only when the intent is not self-evident from the code or when marking extension points.
  - Never write decorative, redundant, or boilerplate comments that merely restate what the code does.

## Architecture and repository layout

- `frontend/` contains the React Native application. It currently has only a `.gitkeep` placeholder.
- `backend/` contains the Python FastAPI application, managed with uv (`pyproject.toml` and `uv.lock`). `main.py` creates the app and `config.py` reads settings from environment variables.
- `db/init/` contains database initialization scripts executed on initial PostgreSQL container bootstrap (such as creating the application user).
- `db/migrations/` contains dbmate SQL migrations, with both `migrate:up` and `migrate:down` sections in each file. Schema snapshot generation is disabled (no `db/schema.sql`).
- `docker-compose.yml` defines the PostgreSQL database and the one-shot dbmate migration service.
- `.env` holds local environment values and is ignored by Git. `.env.example` documents the variables required by Docker Compose.
- `README.md` is the top-level project documentation.

## Validation

- Run `git diff --check` after changes and inspect changed and newly created files for unintended edits.
- For documentation changes, check grammar, Markdown structure, and affected links or table-of-contents anchors.
- For ignore-rule changes, check representative ignored and tracked paths with `git check-ignore`.
- For code or Docker changes, run the relevant configured formatting, build, test, and configuration checks, including checks for affected callers or services. Add or update regression tests when behavior changes warrant them.

## Secrets and local files

- Never commit real credentials, tokens, private keys, or populated secret files. Use placeholders in tracked examples and documentation.
- Keep secrets out of logs, command output, and shared VS Code configuration. `.gitignore` is not a substitute for reviewing files before staging.
- Store local secret values in `.env`. Keep `.env.example` tracked with the required variable names and placeholder values only, never real secrets.
