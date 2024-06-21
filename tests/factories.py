from datetime import datetime

from factory import LazyFunction, SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyDateTime
from faker import Faker
from faker.providers import misc
from pytz import UTC
from twitter_api.posts.models import Post
from twitter_api.users.auth import hash_password
from twitter_api.users.models import Followership, User

from .configs import Session

fake = Faker()
fake.add_provider(misc)


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = 'flush'


class TimeStampBaseFactory(BaseFactory):
    created_at = FuzzyDateTime(datetime(2024, 1, 1, tzinfo=UTC))
    updated_at = FuzzyDateTime(datetime(2024, 1, 1, tzinfo=UTC))


class UserFactory(TimeStampBaseFactory, BaseFactory):
    username = fake.user_name()
    email = fake.email()
    password = LazyFunction(lambda: hash_password('test123'))

    class Meta:
        model = User


class FollowershipFactory(TimeStampBaseFactory, BaseFactory):
    following = SubFactory(UserFactory)
    follower = SubFactory(UserFactory)

    class Meta:
        model = Followership


class PostFactory(TimeStampBaseFactory, BaseFactory):
    author = SubFactory(UserFactory)
    content = 'sample tweet'

    class Meta:
        model = Post
