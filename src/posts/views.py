from fastapi import APIRouter, HTTPException
from starlette import status

from src.core.pagination import paginate
from src.database import DbSession
from src.users.auth import CurrentUser
from src.users.models import User

from .models import Post, PostDetail, PostList, PostPayload

router = APIRouter()


@router.get('/{username}/', response_model=PostList)
async def list_user_posts(user: CurrentUser, db_session: DbSession, username: str, page: int = 1):
    author = db_session.query(User).filter(User.username == username).one_or_none()
    if author is None:
        raise HTTPException(status_code=404, detail=f'User {username} not found')
    author_posts = db_session.query(Post).filter(Post.author_id == author.id)
    return paginate(items=author_posts, page=page)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostDetail)
async def create_user_post(user: CurrentUser, db_session: DbSession, payload: PostPayload):
    post = Post(content=payload.content, author_id=user.id)
    db_session.add(post)
    db_session.commit()
    return post


@router.patch('/{post_id}/', status_code=status.HTTP_206_PARTIAL_CONTENT, response_model=PostDetail)
async def update_user_post(user: CurrentUser, db_session: DbSession, post_id: int, payload: PostPayload):
    post_to_update = db_session.query(Post).filter(Post.id == post_id, Post.author_id == user.id).one_or_none()
    if post_to_update is None:
        raise HTTPException(status_code=404, detail=f'Post {post_id} not found')
    post_to_update.content = payload.content
    db_session.commit()
    return post_to_update


@router.delete('/{post_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_post(user: CurrentUser, db_session: DbSession, post_id: int):
    user_post = db_session.query(Post).filter(Post.id == post_id, Post.author_id == user.id).one_or_none()
    if not user_post:
        raise HTTPException(status_code=404, detail=f'Post {post_id} not found')
    db_session.delete(user_post)
    db_session.commit()
    return {'message': f'Deleted post {post_id}'}
