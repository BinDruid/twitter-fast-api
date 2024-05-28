from __future__ import annotations

from tortoise import fields
from tortoise.models import Model

from src.database.mixin_models import TimeStampedModel


class Like(TimeStampedModel, Model):
    id = fields.IntField(primary_key=True)
    post = fields.ForeignKeyField('models.Post', related_name='likes')
    author = fields.ForeignKeyField('models.User', related_name='likes')

    def __str__(self):
        return f'{self.post}#{self.id}'
