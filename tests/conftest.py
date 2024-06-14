import pytest
from sqlalchemy_utils import create_database, database_exists, drop_database
from starlette.testclient import TestClient
from twitter_api.core.config import settings
from twitter_api.database import Base, engine

from .configs import Session, test_api
from .factories import UserFactory

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope='session')
def db():
    if database_exists(settings.DB_URL):
        drop_database(settings.DB_URL)

    if not database_exists(settings.DB_URL):
        create_database(settings.DB_URL)

    yield
    drop_database(settings.DB_URL)


@pytest.fixture(scope='function', autouse=True)
def session():
    session = Session()
    yield session
    session.rollback()


@pytest.fixture(scope='session')
def client():
    base_url = 'http://localhost:8000/api/v1'
    yield TestClient(app=test_api, base_url=base_url)


@pytest.fixture
def user():
    return UserFactory()
