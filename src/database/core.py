from datetime import datetime
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel
from pydantic.types import SecretStr
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from src.core.config import settings


def get_db_session() -> Session:
    db_url = str(settings.DB_URL)
    engine = create_engine(db_url)
    session_class = sessionmaker(bind=engine)
    session = session_class()
    return session


DbSession = Annotated[Session, Depends(get_db_session)]

Base = declarative_base()


class PydanticBase(BaseModel):
    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        str_strip_whitespace = True

        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%dT%H:%M:%SZ') if v else None,
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }
