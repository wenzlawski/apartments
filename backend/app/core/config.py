import logging
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    Field,
    PostgresDsn,
    computed_field,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]  # this is `backend/`
ROOT_DIR = BASE_DIR.parent  # this is project root

logger = logging.getLogger(__name__)

logger.info(f"{ROOT_DIR=}")


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env", env_ignore_empty=True, extra="ignore"
    )

    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_TEST_DB: str | None = None
    API_V1_STR: str = "/api/v1"
    ACTIVATE_SCHEDULER: bool = False
    KLEINANZEIGEN_USERNAME: str | None = Field(default=None)
    KLEINANZEIGEN_PASSWORD: str | None = Field(default=None)
    FAKER_LOCALE: str = "de_DE"
    FAKER_RANDOM_SEED: int | None = None
    FAKER_TEST_RANDOM_SEED: int = 0

    PROJECT_NAME: str

    @computed_field
    @property
    def POSTGRES_TEST_DB_effective(self) -> str:
        return self.POSTGRES_TEST_DB or f"{self.POSTGRES_DB}_test"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_TEST_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_TEST_DB_effective,
        )

    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    FRONTEND_HOST: str = "http://localhost:5173"
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    # You can still set this in your .env as a string (e.g. "DEBUG")
    LOG_LEVEL: str = "INFO"

    # Convert string level to logging constant
    @field_validator("LOG_LEVEL", mode="after")
    @classmethod
    def convert_log_level(cls, v: str) -> int:
        """Convert LOG_LEVEL string to a logging constant (e.g. logging.DEBUG)."""
        level = getattr(logging, v.upper(), None)
        if not isinstance(level, int):
            raise ValueError(f"Invalid log level: {v}")
        return level


settings = Settings()
