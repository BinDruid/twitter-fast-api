from fastapi import status

from tests.factories import UserFactory


def test_anyone_can_register_with_valid_register_info(client):
    url = '/auth/'
    payload = {'email': 'druid@gmail.com', 'username': 'druid', 'password': '123456'}
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_201_CREATED


def test_anyone_can_not_register_with_with_duplicate_username(client):
    url = '/auth/'
    payload = {'email': 'user@gmail.com', 'username': 'druid', 'password': '123456'}
    UserFactory(username=payload['username'])
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_anyone_can_not_register_with_with_duplicate_email(client):
    url = '/auth/'
    payload = {'email': 'user@gmail.com', 'username': 'druid', 'password': '123456'}
    UserFactory(email=payload['email'])
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_anyone_can_get_token_when_login_successfully(client):
    sample_user = UserFactory()
    url = '/auth/login/'
    payload = {'username': sample_user.username, 'password': 'test123'}
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.json()


def test_anyone_can_do_not_get_token_with_invalid_credentials(client):
    sample_user = UserFactory()
    url = '/auth/login/'
    payload = {'username': sample_user.username, 'password': 'invalid_pass'}
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'token' not in response.json()


def test_anyone_can_view_existing_user_profile(client, auth_user):
    url = f'/users/profile/{auth_user.id}/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_anyone_can_not_view_non_existing_user_profile(client):
    url = '/users/profile/100000/'
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_authenticated_user_can_delete_their_profile(client, auth_user, auth_header):
    url = f'/users/profile/{auth_user.id}/'
    response = client.delete(url, headers=auth_header)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_authenticated_user_can_not_delete_other_user_profile(client, auth_user, auth_header):
    other_user = UserFactory()
    url = f'/users/profile/{other_user.id}/'
    response = client.delete(url, headers=auth_header)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_non_authenticated_user_can_not_delete_other_user_profile(client):
    other_user = UserFactory()
    url = f'/users/profile/{other_user.id}/'
    response = client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_anyone_can_view_user_followers(client, user_as_follower):
    url = f'/users/{user_as_follower.following.id}/followers/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_anyone_can_not_view_non_existing_user_followers(client):
    url = '/users/10000/followers/'
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_anyone_can_view_user_followings(client, user_as_following):
    url = f'/users/{user_as_following.follower.id}/followings/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_anyone_can_not_view_non_existing_user_followings(client):
    url = '/users/10000/followings/'
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_authenticated_user_can_remove_another_user_from_their_followers(client, user_as_following, auth_header):
    user = user_as_following.following
    url = f'/users/{user.id}/followers/{user_as_following.follower.id}/'
    response = client.delete(url, headers=auth_header)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_authenticated_user_can_only_remove_their_followers(client, user_as_follower):
    user = user_as_follower.follower
    headers = {'Authorization': f'Bearer {user.token}'}
    url = f'/users/{user_as_follower.following.id}/followers/{user.id}/'
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_authenticated_user_can_not_remove_non_existing_followership(client, auth_user, auth_header):
    other_user = UserFactory()
    url = f'/users/{auth_user.id}/followers/{other_user.id}/'
    response = client.delete(url, headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_authenticated_user_can_follow_another_user(client, auth_user, auth_header):
    other_user = UserFactory()
    payload = {'user_id': other_user.id}
    url = f'/users/{auth_user.id}/followings/'
    response = client.post(url, headers=auth_header, json=payload)
    assert response.status_code == status.HTTP_201_CREATED


def test_authenticated_user_can_not_follow_another_user_on_behalf_of_other_user(client, auth_user, auth_header):
    other_user = UserFactory()
    payload = {'user_id': auth_user.id}
    url = f'/users/{other_user.id}/followings/'
    response = client.post(url, headers=auth_header, json=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_authenticated_user_can_not_follow_themselves(client, auth_user, auth_header):
    payload = {'user_id': auth_user.id}
    url = f'/users/{auth_user.id}/followings/'
    response = client.post(url, headers=auth_header, json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_authenticated_user_can_unfollow_another_user(client, user_as_follower, auth_header):
    user = user_as_follower.follower
    url = f'/users/{user.id}/followings/{user_as_follower.following.id}/'
    response = client.delete(url, headers=auth_header)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_authenticated_user_can_not_unfollow_another_user_on_behalf_of_other_user(
    client, user_as_following, auth_header
):
    user = user_as_following.following
    url = f'/users/{user_as_following.follower.id}/followings/{user.id}/'
    response = client.delete(url, headers=auth_header)
    assert response.status_code == status.HTTP_403_FORBIDDEN
