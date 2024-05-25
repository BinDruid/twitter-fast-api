from fastapi import FastAPI
from .sample.routes import router as team_router
from .core.config import settings
from .db.config import register_db
from .lifetime import startup


def get_application() -> FastAPI:
    _app = FastAPI(
        title='fast_micro',
        description='',
        debug=settings.DEBUG,
    )
    _app.include_router(team_router)
    register_db(_app)
    _app.on_event('startup')(startup)

    return _app


app = get_application()
