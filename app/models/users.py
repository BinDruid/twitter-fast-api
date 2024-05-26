from __future__ import annotations

from tortoise import fields
from tortoise.models import Model

from app.database.mixin_models import TimeStampedModel


class User(TimeStampedModel, Model):
    id = fields.IntField(primary_key=True)
    first_name = fields.CharField(max_length=32)
    last_name = fields.CharField(max_length=32)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
