from fastapi import status
from twitter_api.users.models import User

from tests.factories import UserFactory


def test_user_can_register_with_valid_register_info(session, client):
    url = '/auth/'
    payload = {'email': 'a.abharya@gmail.com', 'username': 'druid', 'password': '123456'}
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    new_user = session.query(User).filter(User.username == payload['username']).one_or_none()
    assert new_user is not None


def test_user_can_not_register_with_with_duplicate_username(session, client):
    url = '/auth/'
    payload = {'email': 'duplicated_user@gmail.com', 'username': 'druid', 'password': '123456'}
    UserFactory(username=payload['username'])
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
