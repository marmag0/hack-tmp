FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev

COPY . .

CMD ["fastapi", "dev", "--host", "0.0.0.0"]
