from fastapi import status

from tests.factories import BookmarkFactory, LikeFactory, PostFactory, UserFactory


def test_anyone_can_view_statistics_for_a_post(client, test_post, mocked_view_analytics_service):
    url = f'/engagements/statistics/{test_post.id}/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_no_one_can_view_statistics_for_a_non_existing_post(client, mocked_view_analytics_service):
    url = '/engagements/statistics/1000/'
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_anyone_can_view_count_of_views_for_a_post(client, test_post, mocked_view_analytics_service):
    url = f'/engagements/views/{test_post.id}/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_no_one_can_view_count_of_views_for_a_non_existing_post(client, mocked_view_analytics_service):
    url = '/engagements/views/1000/'
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_anyone_can_view_like_counts_for_a_post(client, liked_post):
    url = f'/engagements/likes/{liked_post.id}/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_no_one_can_view_like_counts_for_a_non_existing_post(client):
    url = '/engagements/likes/1000/'
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_authenticated_user_can_like_a_post(client, test_user, auth_header, test_post):
    url = f'/engagements/likes/{test_post.id}/'
    response = client.post(url, headers=auth_header)
    assert response.status_code == status.HTTP_201_CREATED


def test_authenticated_user_can_not_like_a_post_which_already_has_liked(client, test_user, auth_header, liked_post):
    url = f'/engagements/likes/{liked_post.id}/'
    response = client.post(url, headers=auth_header)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_unauthenticated_user_can_not_like_a_post(client, test_post):
    url = f'/engagements/likes/{test_post.id}/'
    response = client.post(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authenticated_user_can_dislike_a_post_they_liked(client, test_user, auth_header, liked_post):
    url = f'/engagements/likes/{liked_post.id}/'
    response = client.delete(url, headers=auth_header)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_authenticated_user_can_not_dislike_a_post_they_did_not_like(client, test_user, auth_header, test_post):
    url = f'/engagements/likes/{test_post.id}/'
    response = client.delete(url, headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_authenticated_user_can_not_dislike_a_post_on_behalf_of_other_user(client, test_user, auth_header):
    other_user = UserFactory()
    other_user_post = PostFactory(author=other_user)
    LikeFactory(user=other_user, post=other_user_post)
    url = f'/engagements/likes/{other_user_post.id}/'
    response = client.delete(url, headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_authenticated_user_can_not_dislike_a_non_existing_post(client, test_user, auth_header):
    url = '/engagements/likes/1000/'
    response = client.delete(url, headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_unauthenticated_user_can_not_dislike_a_post(client, liked_post):
    url = f'/engagements/likes/{liked_post.id}/'
    response = client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_anyone_can_view_bookmark_counts_for_a_post(client, bookmarked_post):
    url = f'/engagements/bookmarks/{bookmarked_post.id}/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_no_one_can_view_bookmark_counts_for_a_non_existing_post(client):
    url = '/engagements/bookmarks/1000/'
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_authenticated_user_can_bookmark_a_post(client, test_user, auth_header, test_post):
    url = f'/engagements/bookmarks/{test_post.id}/'
    response = client.post(url, headers=auth_header)
    assert response.status_code == status.HTTP_201_CREATED


def test_authenticated_user_can_not_bookmark_a_post_which_already_has_bookmarked(
    client, test_user, auth_header, bookmarked_post
):
    url = f'/engagements/bookmarks/{bookmarked_post.id}/'
    response = client.post(url, headers=auth_header)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_unauthenticated_user_can_not_bookmark_a_post(client, test_post):
    url = f'/engagements/bookmarks/{test_post.id}/'
    response = client.post(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authenticated_user_can_un_bookmark_a_post_they_bookmarked(client, test_user, auth_header, bookmarked_post):
    url = f'/engagements/bookmarks/{bookmarked_post.id}/'
    response = client.delete(url, headers=auth_header)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_authenticated_user_can_not_un_bookmark_a_post_they_did_not_bookmark(client, test_user, auth_header, test_post):
    url = f'/engagements/bookmarks/{test_post.id}/'
    response = client.delete(url, headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_authenticated_user_can_not_un_bookmark_a_post_on_behalf_of_other_user(client, test_user, auth_header):
    other_user = UserFactory()
    other_user_post = PostFactory(author=other_user)
    BookmarkFactory(user=other_user, post=other_user_post)
    url = f'/engagements/bookmarks/{other_user_post.id}/'
    response = client.delete(url, headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_authenticated_user_can_not_un_bookmark_a_non_existing_post(client, test_user, auth_header):
    url = '/engagements/bookmarks/1000/'
    response = client.delete(url, headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_unauthenticated_user_can_not_un_bookmark_a_post(client, bookmarked_post):
    url = f'/engagements/bookmarks/{bookmarked_post.id}/'
    response = client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
