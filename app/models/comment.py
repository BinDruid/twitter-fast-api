from __future__ import annotations

from tortoise import fields
from tortoise.models import Model

from app.database.mixin_models import TimeStampedModel


class Comment(TimeStampedModel, Model):
    id = fields.IntField(primary_key=True)
    post = fields.ForeignKeyField('models.Post', related_name='comments')
    author = fields.ForeignKeyField('models.User', related_name='comments')
    content = fields.TextField()

    def __str__(self):
        return f'{self.post}#{self.id}'
