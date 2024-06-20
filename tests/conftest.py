import pytest
from fastapi.testclient import TestClient
from twitter_api.database import Base, engine
from twitter_api.database.depends import get_db_session
from twitter_api.main import api

from .configs import Session
from .factories import FollowershipFactory, UserFactory


@pytest.fixture(scope='function')
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='function', autouse=True)
def session(db):
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture()
def test_api(session):
    api.dependency_overrides[get_db_session] = lambda: session
    return api


@pytest.fixture()
def client(test_api):
    base_url = 'http://localhost:8000/api/v1'
    yield TestClient(app=test_api, base_url=base_url)


@pytest.fixture(scope='function')
def test_user():
    return UserFactory(username='bindruid', email='abharya.dev@gmail.com')


@pytest.fixture(scope='function')
def user_as_follower(test_user):
    other_user = UserFactory()
    return FollowershipFactory(follower=test_user, following=other_user)


@pytest.fixture(scope='function')
def user_as_following(test_user):
    other_user = UserFactory()
    return FollowershipFactory(follower=other_user, following=test_user)
