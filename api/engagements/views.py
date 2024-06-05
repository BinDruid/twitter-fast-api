from fastapi import APIRouter, HTTPException
from starlette import status

from api.database import DbSession
from api.posts.depends import PostByID
from api.users.auth import CurrentUser

from . import services
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'User #{user.id} did not like post #{post.id}'
        )
    if like.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You did not like post #{post.id}')
    services.delete_like_for_post(db_session=db_session, like=like)
    return {'message': f'User #{user.id} disliked post #{post.id}'}
