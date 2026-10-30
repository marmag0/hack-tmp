from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy import URL


class DatabaseSettings(BaseSettings):
    postgres_host: str = "localhost"
    postgres_port: int
    postgres_db: str
    app_user: str
    app_password: str

    @property
    def url(self) -> str:
        return URL.create(
            "postgresql+asyncpg",
            username=self.app_user,
            password=self.app_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        ).render_as_string(hide_password=False)


class Settings(BaseSettings):
    cors_origins: list[str] = ["*"]

    # Docker Compose sets DATABASE_URL, otherwise it is built from the root .env values
    database_url: str = Field(default_factory=lambda: DatabaseSettings().url)


settings = Settings()
