from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session, sessionmaker

from .configs import engine


def get_db_session() -> Session:
    session_class = sessionmaker(bind=engine)
    session = session_class()
    return session


DbSession = Annotated[Session, Depends(get_db_session)]
