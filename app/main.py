from fastapi import FastAPI

from .core.config import settings
from .database.config import register_db
from .lifetime import startup
from .routes.game import router as game_router


def get_application() -> FastAPI:
    _app = FastAPI(
        title='fast_micro',
        description='',
        debug=settings.DEBUG,
    )
    _app.include_router(game_router)
    register_db(_app)
    _app.on_event('startup')(startup)

    return _app


app = get_application()
