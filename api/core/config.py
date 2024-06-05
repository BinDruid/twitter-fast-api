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
    BASE_DIR: Path = ROOT_DIR / 'api'


class Settings(BaseSettings):
    @property
    def PATHS(self) -> Paths:
        return Paths()

    ENVIRONMENT: Environment = 'dev'
    SECRET_KEY: str
    DEBUG: bool = True
    DB_URL: PostgresDsn
    PAGINATION_PER_PAGE: int = 20
    JWT_SECRET: str
    JWT_ALG: str = 'HS256'
    JWT_EXP: int = 86400  # Seconds

    class Config:
        env_file = '.env'


settings = Settings()

app_configs: dict[str, Any] = {
    'title': 'Twitter API',
    'description': 'Minimal twitter api built with FastAPI',
    'debug': settings.DEBUG,
    'root_path': '/api/v1',
}
