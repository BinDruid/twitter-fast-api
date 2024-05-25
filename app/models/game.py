from __future__ import annotations

from tortoise import fields
from tortoise.models import Model

from app.database.mixin_models import TimeStampedModel


class Tournament(TimeStampedModel, Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()

    def __str__(self):
        return self.name


class Event(TimeStampedModel, Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()
    tournament = fields.ForeignKeyField('models.Tournament', related_name='events')
    participants = fields.ManyToManyField('models.Team', related_name='events', through='event_team')

    def __str__(self):
        return self.name


class Team(TimeStampedModel, Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()

    def __str__(self):
        return self.name
