from datetime import datetime

from sqlalchemy import Column, DateTime


class TimeStampedModel:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
