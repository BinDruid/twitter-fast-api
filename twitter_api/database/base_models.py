from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.types import SecretStr
from sqlalchemy import Column, DateTime


class PydanticBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
        json_encoders={
            datetime: lambda v: v.strftime('%Y-%m-%dT%H:%M:%SZ') if v else None,
            SecretStr: lambda v: v.get_secret_value() if v else None,
        },
    )


class TimeStampedModel:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
