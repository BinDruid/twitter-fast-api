from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from .logging import configure_sentry


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator:
    configure_sentry()
    yield
    # Shutdown
