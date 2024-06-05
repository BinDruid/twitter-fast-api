from sqlalchemy.orm import Session

from api.posts.models import Post
from api.users.models import User

from .models import Like


def create_like_for_post(*, db_session: Session, user: User, post: Post) -> None:
    new_like = Like(user_id=user.id, post_id=post.id)
    db_session.add(new_like)
    db_session.commit()


def delete_like_for_post(*, db_session: Session, like: Like) -> None:
    db_session.delete(like)
    db_session.commit()
