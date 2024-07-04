from fastapi import APIRouter, status

from twitter_api.core import exceptions
from twitter_api.database import DbSession
from twitter_api.posts.depends import PostByID
from twitter_api.users.depends import CurrentUser

from . import services

router = APIRouter()


@router.get('/statistics/{post_id}/', status_code=status.HTTP_200_OK)
def count_total_post_statistics(db_session: DbSession, post: PostByID):
    likes_count = services.count_total_likes_for_post(db_session=db_session, post=post)
    bookmarks_count = services.count_total_bookmarks_for_post(db_session=db_session, post=post)
    views_count = services.count_total_views_for_post(post_id=post.id)
    return {'views_count': views_count, 'likes_count': likes_count, 'bookmarks_count': bookmarks_count}


@router.get('/likes/{post_id}/', status_code=status.HTTP_200_OK)
def count_post_likes(db_session: DbSession, post: PostByID):
    likes_count = services.count_total_likes_for_post(db_session=db_session, post=post)
    return {'likes_count': likes_count}


@router.post('/likes/{post_id}/', status_code=status.HTTP_201_CREATED)
def like_post(user: CurrentUser, db_session: DbSession, post: PostByID):
    like = services.get_like_by_user_post(db_session=db_session, user=user, post=post)
    if like is not None:
        raise exceptions.BadRequest(detail=f'You have already like post #{post.id}')
    services.create_like_for_post(db_session=db_session, user=user, post=post)
    return {'message': f'User #{user.id} liked post #{post.id}'}


@router.delete('/likes/{post_id}/', status_code=status.HTTP_204_NO_CONTENT)
def dislike_post(user: CurrentUser, db_session: DbSession, post: PostByID):
    like = services.get_like_by_user_post(db_session=db_session, user=user, post=post)
    if like is None:
        raise exceptions.NotFound(detail=f'User #{user.id} did not liked post #{post.id}')
    if like.user_id != user.id:
        raise exceptions.NotFound(detail=f'You did not like post #{post.id}')
    services.delete_like_for_post(db_session=db_session, like=like)
    return {'message': f'User #{user.id} disliked post #{post.id}'}


@router.get('/bookmarks/{post_id}/', status_code=status.HTTP_200_OK)
def count_post_bookmarks(db_session: DbSession, post: PostByID):
    bookmarks_count = services.count_total_bookmarks_for_post(db_session=db_session, post=post)
    return {'bookmarks_count': bookmarks_count}


@router.post('/bookmarks/{post_id}/', status_code=status.HTTP_201_CREATED)
def bookmark_post(user: CurrentUser, db_session: DbSession, post: PostByID):
    bookmark = services.get_bookmark_by_user_post(db_session=db_session, user=user, post=post)
    if bookmark is not None:
        raise exceptions.BadRequest(detail=f'You have already bookmarked post #{post.id}')
    services.create_bookmark_for_post(db_session=db_session, user=user, post=post)
    return {'message': f'User #{user.id} bookmarked post #{post.id}'}


@router.delete('/bookmarks/{post_id}/', status_code=status.HTTP_204_NO_CONTENT)
def un_bookmark_post(user: CurrentUser, db_session: DbSession, post: PostByID):
    bookmark = services.get_bookmark_by_user_post(db_session=db_session, user=user, post=post)
    if bookmark is None:
        raise exceptions.NotFound(detail=f'User #{user.id} did not bookmark post #{post.id}')
    if bookmark.user_id != user.id:
        raise exceptions.NotFound(detail=f'You did not bookmark post #{post.id}')
    services.delete_bookmark_for_post(db_session=db_session, bookmark=bookmark)
    return {'message': f'User #{user.id} un-bookmark post #{post.id}'}


@router.get('/views/{post_id}/')
def get_count_of_post_views(post: PostByID):
    post_view_count = services.count_total_views_for_post(post_id=post.id)
    return {'post_id': post.id, 'view_count': post_view_count}
