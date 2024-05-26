from __future__ import annotations

from tortoise import fields
from tortoise.models import Model

from app.database.mixin_models import TimeStampedModel


class Post(TimeStampedModel, Model):
    id = fields.IntField(primary_key=True)
    author = fields.ForeignKeyField('models.User', related_name='posts')
    content = fields.TextField()

    def __str__(self):
        return f'{self.author}#{self.id}'
