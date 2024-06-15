from datetime import datetime

from factory import LazyFunction, Sequence
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyDateTime
from faker import Faker
from faker.providers import misc
from pytz import UTC
from twitter_api.users.models import User, hash_password

from .configs import Session

fake = Faker()
fake.add_provider(misc)


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = 'flush'


class TimeStampBaseFactory(BaseFactory):
    created_at = FuzzyDateTime(datetime(2020, 1, 1, tzinfo=UTC))
    updated_at = FuzzyDateTime(datetime(2020, 1, 1, tzinfo=UTC))


class UserFactory(TimeStampBaseFactory, BaseFactory):
    username = fake.user_name()
    email = Sequence(lambda n: f'user{n}@example.com')
    password = LazyFunction(lambda: hash_password('test123').decode('utf-8'))

    class Meta:
        model = User
