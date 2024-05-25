from __future__ import annotations

from pathlib import Path

from pydantic import (
    AnyHttpUrl,
    HttpUrl,
    PostgresDsn,
)
from pydantic_settings import BaseSettings

try:
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        pass


class Environment(StrEnum):
    dev = 'dev'
    prod = 'prod'


class Paths:
    # fast_micro
    ROOT_DIR: Path = Path(__file__).parent.parent.parent
    BASE_DIR: Path = ROOT_DIR / 'app'


class Settings(BaseSettings):
    @property
    def PATHS(self) -> Paths:
        return Paths()

    ENVIRONMENT: Environment = 'dev'
    SECRET_KEY: str = 'x!n5u!u==_n00rp%zu6o92ms82&3_-bqpe((4!%%zluxiq$!@b'
    DEBUG: bool = False
    SERVER_HOST: AnyHttpUrl = 'http://localhost:8000'  # type:ignore
    SENTRY_DSN: HttpUrl | None = None
    PAGINATION_PER_PAGE: int = 20

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str = 'postgres'
    DB_PASS: str = 'postgres'
    DB_NAME: str = 'postgres'
    SES_ACCESS_KEY: str | None = None
    SES_SECRET_KEY: str | None = None
    SES_REGION: str | None = None
    DEFAULT_FROM_NAME: str | None = None
    INSTALLED_APPS: [str] = ['app.sample']

    class Config:
        env_file = '.env'


settings = Settings()
