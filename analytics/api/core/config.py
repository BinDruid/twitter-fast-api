from pathlib import Path
from typing import Any

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Paths:
    ROOT_DIR: Path = Path(__file__).parent.parent.parent
    BASE_DIR: Path = ROOT_DIR / 'api'


class Settings(BaseSettings):
    @property
    def PATHS(self) -> Paths:
        return Paths()

    DEBUG: bool = True
    DB_URL: PostgresDsn

    class Config:
        env_file = '.env'


settings = Settings()

app_configs: dict[str, Any] = {
    'title': 'Analytics API',
    'description': 'Analytics Service',
    'debug': settings.DEBUG,
    'root_path': '/api/v1',
    'swagger_ui_parameters': {'defaultModelsExpandDepth': -1},
}
