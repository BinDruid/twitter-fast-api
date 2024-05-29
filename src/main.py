from fastapi import FastAPI

from src.core.config import settings
from src.core.middleware import ExceptionMiddleware
from src.core.startup import startup
from src.database.config import register_db
from src.routes import api_router


def get_application() -> FastAPI:
    app = FastAPI(
        title='fast_micro',
        description='',
        debug=settings.DEBUG,
        root_path='/api/v1',
    )
    app.include_router(api_router)
    register_db(app)
    app.on_event('startup')(startup)

    return app


api = get_application()

api.add_middleware(ExceptionMiddleware)
