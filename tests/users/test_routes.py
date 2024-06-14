import pytest
from psycopg2 import IntegrityError
from twitter_api.users.models import User


def test_user_can_register_with_valid_register_info(session, client):
    url = '/auth/'
    payload = {'email': 'a.abharya@gmail.com', 'username': 'druid', 'password': '123456'}
    response = client.post(url, json=payload)
    assert response.status_code == 201

    new_user = session.query(User).filter(User.username == payload['username']).one_or_none()
    assert new_user is not None


def test_user_can_not_register_with_with_duplicate_username(session, client):
    url = '/auth/'
    payload = {'email': 'a.abharya@gmail.com', 'username': 'druid', 'password': '123456'}

    with pytest.raises(IntegrityError):
        client.post(url, json=payload)

    new_user = session.query(User).filter(User.username == payload['username']).one_or_none()
    assert new_user is None
