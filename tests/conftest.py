from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from twitter_api.database import Base, engine
from twitter_api.database.depends import get_db_session
from twitter_api.main import api
from twitter_api.users.auth import generate_token

from .configs import Session
from .factories import BookmarkFactory, FollowershipFactory, LikeFactory, MentionFactory, PostFactory, UserFactory


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
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


@pytest.fixture()
def test_user():
    return UserFactory(username='bindruid', email='abharya.dev@gmail.com')


@pytest.fixture()
def auth_header(test_user):
    return {'Authorization': f'Bearer {generate_token(user=test_user)}'}


@pytest.fixture()
def user_as_follower(test_user):
    other_user = UserFactory()
    return FollowershipFactory(follower=test_user, following=other_user)


@pytest.fixture()
def user_as_following(test_user):
    other_user = UserFactory()
    return FollowershipFactory(follower=other_user, following=test_user)


@pytest.fixture()
def test_post(test_user):
    return PostFactory(author=test_user)


@pytest.fixture()
def post_with_quote(test_user):
    quoted_post = PostFactory(author=test_user)
    return PostFactory(author=test_user, quoted_post=quoted_post)


@pytest.fixture()
def post_with_mention(test_user):
    post = PostFactory(author=test_user)
    mention = PostFactory(author=test_user)
    return MentionFactory(mention=mention, original_post=post)


@pytest.fixture()
def liked_post(test_user):
    post = PostFactory(author=test_user)
    LikeFactory(user=test_user, post=post)
    return post


@pytest.fixture()
def bookmarked_post(test_user):
    post = PostFactory(author=test_user)
    BookmarkFactory(user=test_user, post=post)
    return post


@pytest.fixture()
def mocked_view_analytics_service():
    with patch('twitter_api.engagements.services.count_total_views_for_post') as views_analytics_service:
        views_analytics_service.return_value = 1
        yield
