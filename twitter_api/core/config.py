from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import ConfigDict, PostgresDsn
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    LOCAL = 'LOCAL'
    TEST = 'TEST'
    STAGING = 'STAGING'
    PRODUCTION = 'PRODUCTION'

    @property
    def is_debug(self):
        return self in (self.LOCAL, self.STAGING, self.TEST)

    @property
    def is_testing(self):
        return self == self.TEST

    @property
    def is_deployed(self) -> bool:
        return self in (self.STAGING, self.PRODUCTION)


class Paths:
    ROOT_DIR: Path = Path(__file__).parent.parent.parent
    BASE_DIR: Path = ROOT_DIR / 'twitter_api'


class Settings(BaseSettings):
    model_config = ConfigDict(env_file='.env')

    @property
    def PATHS(self) -> Paths:
        return Paths()

    ENVIRONMENT: Environment
    SECRET_KEY: str
    SENTRY_ENABLED: bool
    SENTRY_DSN: str
    DEBUG: bool = True
    DB_URL: PostgresDsn
    CORS_ORIGINS: list[str] = ['*']
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str] = ['*']
    ANALYTICS_HOST: str
    ANALYTICS_PORT: int
    PAGINATION_PER_PAGE: int = 20
    JWT_SECRET: str
    JWT_ALG: str = 'HS256'
    JWT_EXP: int = 86400  # Seconds

    @property
    def ANALYTICS_URL(self) -> str:
        return f'{self.ANALYTICS_HOST}:{str(self.ANALYTICS_PORT)}'


settings = Settings()

app_configs: dict[str, Any] = {
    'title': 'Twitter API',
    'description': 'Minimal twitter twitter_api built with FastAPI',
    'debug': settings.DEBUG,
    'root_path': '/api/v1',
    'swagger_ui_parameters': {'defaultModelsExpandDepth': -1},
}
