from sqlalchemy.orm import Query

from src.database import DbSession
from src.users.models import User

from .depends import AuthorByName, PostByAuthor, PostByID
from .models import Mention, Post, PostPayload


def get_post_by_author(*, db_session: DbSession, author: AuthorByName) -> Query[Post]:
    author_posts = db_session.query(Post).filter(Post.author_id == author.id)
    return author_posts


def get_mentions_by_post(*, db_session: DbSession, post: PostByAuthor) -> Query[Post]:
    subquery = db_session.query(Mention.mention_id).filter(Mention.original_post_id == post.id).subquery()
    mentions = db_session.query(Post).filter(Post.id.in_(subquery))
    return mentions


def create_mention_for_post(*, db_session: DbSession, author: User, post: PostByAuthor, context: PostPayload) -> Post:
    new_mention = Post(content=context.content, author_id=author.id)
    db_session.add(new_mention)
    db_session.commit()
    mention_relation = Mention(original_post_id=post.id, mention_id=new_mention.id)
    db_session.add(mention_relation)
    db_session.commit()
    return new_mention


def get_quotes_by_post(*, db_session: DbSession, post: PostByAuthor) -> Query[Post]:
    subquery = db_session.query(Post.id).filter(Post.quoted_post_id == post.id).subquery()
    quotes = db_session.query(Post).filter(Post.id.in_(subquery))
    return quotes


def create_quote_for_post(*, db_session: DbSession, author: User, post: PostByAuthor, context: PostPayload) -> Post:
    new_quote = Post(content=context.content, author_id=author.id, quoted_post_id=post.id)
    db_session.add(new_quote)
    db_session.commit()
    return new_quote


def create_post_for_user(*, db_session: DbSession, author: User, context: PostPayload) -> Post:
    new_post = Post(content=context.content, author_id=author.id)
    db_session.add(new_post)
    db_session.commit()
    return new_post


def update_post_for_user(*, db_session: DbSession, post: PostByID, context: PostPayload) -> Post:
    post.content = context.content
    db_session.commit()
    return post


def delete_post_for_user(*, db_session: DbSession, post: PostByID) -> None:
    db_session.delete(post)
    db_session.commit()
