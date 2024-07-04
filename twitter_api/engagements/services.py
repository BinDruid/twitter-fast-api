import grpc
from sqlalchemy.orm import Session

from twitter_api.core.config import settings
from twitter_api.posts.models import Post
from twitter_api.users.models import User

from .grpc import post_views_pb2, post_views_pb2_grpc
from .models import Bookmark, Like


def count_total_views_for_post(*, post_id: int) -> int:
    with grpc.insecure_channel(settings.ANALYTICS_URL) as channel:
        stub = post_views_pb2_grpc.PostViewAnalyticsStub(channel)
        response = stub.GetViewCount(post_views_pb2.PostViewRequest(post_id=post_id))
    return response.post_view_count


def count_total_likes_for_post(*, db_session: Session, post: Post) -> int:
    total_likes = db_session.query(Like).filter(Like.post_id == post.id).count()
    return total_likes


def get_like_by_user_post(*, db_session: Session, user: User, post: Post) -> Like:
    like = db_session.query(Like).filter(Like.user_id == user.id, Like.post_id == post.id).one_or_none()
    return like


def create_like_for_post(*, db_session: Session, user: User, post: Post) -> None:
    new_like = Like(user_id=user.id, post_id=post.id)
    db_session.add(new_like)
    db_session.commit()


def delete_like_for_post(*, db_session: Session, like: Like) -> None:
    db_session.delete(like)
    db_session.commit()


def count_total_bookmarks_for_post(*, db_session: Session, post: Post) -> int:
    total_bookmarks = db_session.query(Bookmark).filter(Bookmark.post_id == post.id).count()
    return total_bookmarks


def get_bookmark_by_user_post(*, db_session: Session, user: User, post: Post) -> Bookmark:
    bookmark = db_session.query(Bookmark).filter(Bookmark.user_id == user.id, Bookmark.post_id == post.id).one_or_none()
    return bookmark


def create_bookmark_for_post(*, db_session: Session, user: User, post: Post) -> None:
    new_like = Bookmark(user_id=user.id, post_id=post.id)
    db_session.add(new_like)
    db_session.commit()


def delete_bookmark_for_post(*, db_session: Session, bookmark: Bookmark) -> None:
    db_session.delete(bookmark)
    db_session.commit()
