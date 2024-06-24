from typing import Annotated

from fastapi import Depends

from twitter_api.core import exceptions
from twitter_api.database import DbSession
from twitter_api.users.depends import get_user_by_name
from twitter_api.users.models import User

from .models import Post

AuthorByName = Annotated[User, Depends(get_user_by_name)]


async def get_post_by_id(post_id: int, db_session: DbSession) -> Post:
    post = db_session.query(Post).filter(Post.id == post_id).one_or_none()
    if post is None:
        raise exceptions.NotFound(detail=f'Post {post_id} not found')
    return post


PostByID = Annotated[Post, Depends(get_post_by_id)]


async def get_post_by_post_id_and_author(post_id: int, author: AuthorByName, db_session: DbSession) -> Post:
    author_post = db_session.query(Post).filter(Post.id == post_id, Post.author_id == author.id).one_or_none()
    if author_post is None:
        raise exceptions.NotFound(detail=f'Post {post_id} not found')
    return author_post


PostByAuthor = Annotated[Post, Depends(get_post_by_post_id_and_author)]
