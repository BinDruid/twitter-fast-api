from fastapi import APIRouter, BackgroundTasks, HTTPException
from starlette import status

from twitter_api.core.pagination import paginate
from twitter_api.database import DbSession
from twitter_api.engagements import tasks
from twitter_api.users.depends import CurrentUser

from . import services
from .depends import AuthorByName, PostByAuthor, PostByID
from .models import PostDetail, PostDetailWithQuote, PostList, PostPayload, PostWithQuoteList

router = APIRouter()


@router.get('/{username}/', response_model=PostWithQuoteList)
async def list_user_posts_with_their_quoted(db_session: DbSession, author: AuthorByName, page: int = 1):
    author_posts = services.get_post_by_author(db_session=db_session, author=author)
    return paginate(items=author_posts, page=page)


@router.get('/{username}/{post_id}/', response_model=PostDetailWithQuote)
async def get_user_post_detail_with_its_quoted(post: PostByAuthor, worker: BackgroundTasks):
    worker.add_task(tasks.increase_post_view_count, post.id)
    return post


@router.get('/{username}/{post_id}/mentions/', response_model=PostList)
async def get_mentions_of_user_post(db_session: DbSession, post: PostByAuthor, page: int = 1):
    mentions = services.get_mentions_by_post(db_session=db_session, post=post)
    return paginate(items=mentions, page=page)


@router.post('/{username}/{post_id}/mentions/', status_code=status.HTTP_201_CREATED, response_model=PostDetail)
async def create_mention_on_post(
    user: CurrentUser, db_session: DbSession, post: PostByAuthor, worker: BackgroundTasks, payload: PostPayload
):
    new_mention = services.create_mention_for_post(db_session=db_session, author=user, post=post, context=payload)
    worker.add_task(tasks.create_post_view_count_entry, new_mention.id)
    return new_mention


@router.get('/{username}/{post_id}/quotes/', response_model=PostWithQuoteList)
async def get_quotes_for_user_post(db_session: DbSession, post: PostByAuthor, page: int = 1):
    quotes = services.get_quotes_by_post(db_session=db_session, post=post)
    return paginate(items=quotes, page=page)


@router.post('/{username}/{post_id}/quotes/', status_code=status.HTTP_201_CREATED, response_model=PostDetail)
async def create_quote_on_user_post(
    user: CurrentUser, db_session: DbSession, post: PostByAuthor, worker: BackgroundTasks, payload: PostPayload
):
    new_quote = services.create_quote_for_post(db_session=db_session, author=user, post=post, context=payload)
    worker.add_task(tasks.create_post_view_count_entry, new_quote.id)
    return new_quote


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostDetail)
async def create_user_post(user: CurrentUser, db_session: DbSession, worker: BackgroundTasks, payload: PostPayload):
    new_post = services.create_post_for_user(db_session=db_session, author=user, context=payload)
    worker.add_task(tasks.create_post_view_count_entry, new_post.id)
    return new_post


@router.patch('/{post_id}/', status_code=status.HTTP_206_PARTIAL_CONTENT, response_model=PostDetail)
async def update_user_post(user: CurrentUser, db_session: DbSession, post: PostByID, payload: PostPayload):
    if post.author_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You do not own post #{post.id}')
    updated_post = services.update_post_for_user(db_session=db_session, post=post, context=payload)
    return updated_post


@router.delete('/{post_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_post(user: CurrentUser, db_session: DbSession, post: PostByID, worker: BackgroundTasks):
    post_id = post.id
    if post.author_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You do not own post #{post_id}')
    services.delete_post_for_user(db_session=db_session, post=post)
    worker.add_task(tasks.delete_post_view_count_entry, post_id)
    return {'message': f'Deleted post {post_id}'}
