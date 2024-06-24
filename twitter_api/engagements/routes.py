import grpc
from fastapi import APIRouter, status

from twitter_api.core import exceptions
from twitter_api.core.config import settings
from twitter_api.database import DbSession
from twitter_api.posts.depends import PostByID
from twitter_api.users.depends import CurrentUser

from . import services
from .grpc import post_views_pb2, post_views_pb2_grpc
from .models import Like

router = APIRouter()


@router.post('/likes/{post_id}/', status_code=status.HTTP_201_CREATED)
def like_post(user: CurrentUser, db_session: DbSession, post: PostByID):
    services.create_like_for_post(db_session=db_session, user=user, post=post)
    return {'message': f'User #{user.id} liked post #{post.id}'}


@router.delete('/likes/{post_id}/', status_code=status.HTTP_204_NO_CONTENT)
def dislike_post(user: CurrentUser, db_session: DbSession, post: PostByID):
    like = db_session.query(Like).filter(Like.user_id == user.id, Like.post_id == post.id).one_or_none()
    if like is None:
        raise exceptions.NotFound(detail=f'User #{user.id} did not like post #{post.id}')
    if like.user_id != user.id:
        raise exceptions.NotFound(detail=f'You did not like post #{post.id}')
    services.delete_like_for_post(db_session=db_session, like=like)
    return {'message': f'User #{user.id} disliked post #{post.id}'}


@router.get('/views/{post_id}/')
def get_count_of_post_views(post_id: int):
    with grpc.insecure_channel(settings.ANALYTICS_URL) as channel:
        stub = post_views_pb2_grpc.PostViewAnalyticsStub(channel)
        response = stub.GetViewCount(post_views_pb2.PostViewRequest(post_id=post_id))
    return {'post_id': response.post_id, 'view_count': response.post_view_count}
