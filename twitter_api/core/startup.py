from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
    yield
    # Shutdown
