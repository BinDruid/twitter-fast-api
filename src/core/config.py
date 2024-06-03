from __future__ import annotations

from pathlib import Path

from pydantic import AnyHttpUrl, HttpUrl
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
    BASE_DIR: Path = ROOT_DIR / 'src'


class Settings(BaseSettings):
    @property
    def PATHS(self) -> Paths:
        return Paths()

    ENVIRONMENT: Environment = 'dev'
    SECRET_KEY: str = 'x!n5u!u==_n00rp%zu6o92ms82&3_-bqpe((4!%%zluxiq$!@b'
    DEBUG: bool = True
    SERVER_HOST: AnyHttpUrl = 'http://localhost:8000'  # type:ignore
    SENTRY_DSN: HttpUrl | None = None
    INSTALLED_APPS: [str] = ['src.users', 'src.posts', 'src.comments', 'src.likes']
    PAGINATION_PER_PAGE: int = 20
    JWT_SECRET: str = 'p-)w9@rq+xdr&chuco0fykbpjsnpq9&zj7k1i*y8$4#&)0pi1y'
    JWT_ALG: str = 'HS256'
    JWT_EXP: int = 86400  # Seconds
    DB_URL: str = ''

    class Config:
        env_file = '.env'


settings = Settings()
