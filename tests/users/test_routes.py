from fastapi import status
from twitter_api.users.models import User

from tests.factories import UserFactory


def test_user_can_register_with_valid_register_info(session, client):
    url = '/auth/'
    payload = {'email': 'druid@gmail.com', 'username': 'druid', 'password': '123456'}
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    new_user = session.query(User).filter(User.username == payload['username']).one_or_none()
    assert new_user is not None


def test_user_can_not_register_with_with_duplicate_username(session, client):
    url = '/auth/'
    payload = {'email': 'user@gmail.com', 'username': 'druid', 'password': '123456'}
    UserFactory(username=payload['username'])
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_user_can_not_register_with_with_duplicate_email(session, client):
    url = '/auth/'
    payload = {'email': 'user@gmail.com', 'username': 'druid', 'password': '123456'}
    UserFactory(email=payload['email'])
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_user_can_get_token_when_login_successfully(session, client):
    sample_user = UserFactory()
    url = '/auth/login/'
    payload = {'username': sample_user.username, 'password': 'test123'}
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.json()


def test_user_can_do_not_get_token_with_invalid_credentials(session, client):
    sample_user = UserFactory()
    url = '/auth/login/'
    payload = {'username': sample_user.username, 'password': 'invalid_pass'}
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'token' not in response.json()


def test_user_can_view_existing_user_profile(session, client):
    sample_user = UserFactory()
    url = f'/users/profile/{sample_user.id}'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    returned_user = response.json()
    assert returned_user['id'] == sample_user.id


def test_user_can_not_view_non_existing_user_profile(session, client):
    url = '/users/profile/100000/'
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
