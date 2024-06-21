from fastapi import status

from tests.factories import PostFactory


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
