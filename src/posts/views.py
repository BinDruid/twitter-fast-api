from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from tortoise.exceptions import DoesNotExist

from src.core.pagination import Params, paginate
from src.users.auth import CurrentUser
from .models import Post, PostPydanticIn, PostPydanticOut

router = APIRouter()


@router.get('/')
async def list_user_posts(user: CurrentUser, params: Params = Depends()):
    user_posts = Post.all().filter(author_id=user['id'])
    return await paginate(user_posts, params)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostPydanticOut)
async def create_user_post(user: CurrentUser, post: PostPydanticIn):
    new_post = await Post.create(author_id=user['id'], content=post.content)
    return new_post


@router.patch('/{post_id}/', status_code=status.HTTP_206_PARTIAL_CONTENT, response_model=PostPydanticOut)
async def update_user_post(user: CurrentUser, post: PostPydanticIn, post_id: int):
    post_to_update = await Post.all().get_or_none(author_id=user['id'], id=post_id)
    if post_to_update is None:
        raise HTTPException(status_code=404, detail=f'Post {post_id} not found')
    post_to_update.content = post.content
    await post_to_update.save()
    return post_to_update


@router.delete('/{post_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_post(user: CurrentUser, post_id: int):
    deleted_count = await Post.all().filter(author_id=user['id'], id=post_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f'Post {post_id} not found')
    return {'message': f'Deleted post {post_id}'}
