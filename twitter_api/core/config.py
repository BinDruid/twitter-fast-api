from pathlib import Path
from typing import Any

from pydantic import PostgresDsn
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
    ROOT_DIR: Path = Path(__file__).parent.parent.parent
    BASE_DIR: Path = ROOT_DIR / 'twitter_api'


class Settings(BaseSettings):
    @property
    def PATHS(self) -> Paths:
        return Paths()

    ENVIRONMENT: Environment = 'dev'
    SECRET_KEY: str
    DEBUG: bool = True
    DB_URL: PostgresDsn
    ANALYTICS_HOST: str
    ANALYTICS_PORT: int
    PAGINATION_PER_PAGE: int = 20
    JWT_SECRET: str
    JWT_ALG: str = 'HS256'
    JWT_EXP: int = 86400  # Seconds

    @property
    def ANALYTICS_URL(self) -> str:
        return f'{self.ANALYTICS_HOST}:{str(self.ANALYTICS_PORT)}'

    class Config:
        env_file = '.env'


settings = Settings()

app_configs: dict[str, Any] = {
    'title': 'Twitter API',
    'description': 'Minimal twitter twitter_api built with FastAPI',
    'debug': settings.DEBUG,
    'root_path': '/api/v1',
    'swagger_ui_parameters': {'defaultModelsExpandDepth': -1},
}
