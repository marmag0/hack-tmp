import os

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://app_user:password@localhost:5432/app_db",
)
