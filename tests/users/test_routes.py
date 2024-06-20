from fastapi import status
from twitter_api.users.models import User

from tests.factories import FollowershipFactory, UserFactory


def test_anyone_can_register_with_valid_register_info(session, client):
    url = '/auth/'
    payload = {'email': 'druid@gmail.com', 'username': 'druid', 'password': '123456'}
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    new_user = session.query(User).filter(User.username == payload['username']).one_or_none()
    assert new_user is not None


def test_anyone_can_not_register_with_with_duplicate_username(session, client):
    url = '/auth/'
    payload = {'email': 'user@gmail.com', 'username': 'druid', 'password': '123456'}
    UserFactory(username=payload['username'])
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_anyone_can_not_register_with_with_duplicate_email(session, client):
    url = '/auth/'
    payload = {'email': 'user@gmail.com', 'username': 'druid', 'password': '123456'}
    UserFactory(email=payload['email'])
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_anyone_can_get_token_when_login_successfully(session, client):
    sample_user = UserFactory()
    url = '/auth/login/'
    payload = {'username': sample_user.username, 'password': 'test123'}
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.json()


def test_anyone_can_do_not_get_token_with_invalid_credentials(session, client):
    sample_user = UserFactory()
    url = '/auth/login/'
    payload = {'username': sample_user.username, 'password': 'invalid_pass'}
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'token' not in response.json()


def test_anyone_can_view_existing_user_profile(session, client):
    sample_user = UserFactory()
    url = f'/users/profile/{sample_user.id}/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    returned_user = response.json()
    assert returned_user['id'] == sample_user.id


def test_anyone_can_not_view_non_existing_user_profile(session, client):
    url = '/users/profile/100000/'
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_authenticated_user_can_delete_their_profile(session, client, user):
    headers = {'Authorization': f'Bearer {user.token}'}
    url = f'/users/profile/{user.id}/'
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_authenticated_user_can_not_delete_other_user_profile(session, client, user):
    sample_user = UserFactory()
    headers = {'Authorization': f'Bearer {user.token}'}
    url = f'/users/profile/{sample_user.id}/'
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_non_authenticated_user_can_not_delete_other_user_profile(session, client):
    sample_user = UserFactory()
    url = f'/users/profile/{sample_user.id}/'
    response = client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_anyone_can_view_user_followers(session, client, user):
    sample_user = UserFactory()
    FollowershipFactory(follower=user, following=sample_user)
    url = f'/users/{sample_user.id}/followers/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_anyone_can_not_view_non_existing_user_followers(session, client):
    url = '/users/10000/followers/'
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_anyone_can_view_user_followings(session, client, user):
    sample_user = UserFactory()
    FollowershipFactory(follower=sample_user, following=user)
    url = f'/users/{sample_user.id}/followings/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_anyone_can_not_view_non_existing_user_followings(session, client):
    url = '/users/10000/followings/'
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_authenticated_user_can_remove_another_user_from_their_followers(session, client, user):
    sample_user = UserFactory()
    FollowershipFactory(follower=sample_user, following=user)
    headers = {'Authorization': f'Bearer {user.token}'}
    url = f'/users/{user.id}/followers/{sample_user.id}/'
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_authenticated_user_can_only_remove_their_followers(session, client, user):
    sample_user = UserFactory()
    FollowershipFactory(follower=user, following=sample_user)
    headers = {'Authorization': f'Bearer {user.token}'}
    url = f'/users/{sample_user.id}/followers/{user.id}/'
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_authenticated_user_can_not_remove_non_existing_followership(session, client, user):
    sample_user = UserFactory()
    headers = {'Authorization': f'Bearer {user.token}'}
    url = f'/users/{user.id}/followers/{sample_user.id}/'
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
