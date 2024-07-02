from fastapi import status

from tests.factories import PostFactory, UserFactory


def test_authenticated_user_can_make_a_post(client, auth_header):
    payload = {'content': 'test'}
    url = '/posts/'
    response = client.post(url, json=payload, headers=auth_header)
    assert response.status_code == status.HTTP_201_CREATED


def test_unauthenticated_user_can_not_make_a_post(client):
    payload = {'content': 'test'}
    url = '/posts/'
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authenticated_user_can_update_a_post(client, test_post, auth_header):
    payload = {'content': 'test'}
    url = f'/posts/{test_post.id}'
    response = client.patch(url, json=payload, headers=auth_header)
    assert response.status_code == status.HTTP_206_PARTIAL_CONTENT


def test_authenticated_user_can_not_update_a_post_he_has_not_written(client, test_post, auth_header):
    other_user = UserFactory()
    other_user_post = PostFactory(author=other_user)
    payload = {'content': 'test'}
    url = f'/posts/{other_user_post.id}'
    response = client.patch(url, json=payload, headers=auth_header)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_authenticated_user_can_delete_his_post(client, test_post, auth_header):
    url = f'/posts/{test_post.id}'
    response = client.delete(url, headers=auth_header)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_authenticated_user_can_not_delete_a_post_he_has_not_written(client, test_post, auth_header):
    other_user = UserFactory()
    other_user_post = PostFactory(author=other_user)
    url = f'/posts/{other_user_post.id}'
    response = client.delete(url, headers=auth_header)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_anyone_can_view_list_of_post_of_an_existing_user(client, test_user):
    PostFactory.create_batch(size=5, author=test_user)
    url = f'/posts/{test_user.username}/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_anyone_can_not_view_list_of_post_of_a_non_existing_user(client):
    url = '/posts/none/'
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_anyone_can_view_detail_of_post_with_its_quoted_post(client, test_user, post_with_quote):
    url = f'/posts/{test_user.username}/{post_with_quote.id}'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['quoted_post']


def test_anyone_can_view_all_mentions_of_a_post(client, test_user, post_with_mention):
    url = f'/posts/{test_user.username}/{post_with_mention.original_post.id}/mentions'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_unauthenticated_user_can_not_mention_on_a_post(client, test_user, test_post):
    payload = {'content': 'test'}
    url = f'/posts/{test_user.username}/{test_post.id}/mentions'
    response = client.post(url, json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authenticated_user_can_mention_on_a_post(client, test_user, auth_header, test_post):
    payload = {'content': 'test'}
    url = f'/posts/{test_user.username}/{test_post.id}/mentions'
    response = client.post(url, json=payload, headers=auth_header)
    assert response.status_code == status.HTTP_201_CREATED
