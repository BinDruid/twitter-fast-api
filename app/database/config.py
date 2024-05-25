from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import settings

TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': settings.DB_HOST,
                'port': settings.DB_PORT,
                'user': settings.DB_USER,
                'password': settings.DB_PASS,
                'database': settings.DB_NAME,
            },
        },
    },
    'apps': {
        'models': {
            'models': ['app.models.game'] + ['aerich.models'],
            'default_connection': 'default',
        }
    },
    'use_tz': False,
    'timezone': 'UTC',
}


def register_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True,
    )
