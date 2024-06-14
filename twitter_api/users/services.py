from sqlalchemy.orm import Query, Session

from .depends import FollowerByID, FollowingByID
from .models import Followership, FollowerShipPayload, User, UserCreatePayload


def get_user_by_email(*, db_session: Session, email: str):
    user = db_session.query(User.email == email).one_or_none()
    return user


def get_user_by_username(*, db_session: Session, username: str):
    user = db_session.query(User.username == username).one_or_none()
    return user


def delete_user(*, db_session: Session, user: User) -> None:
    db_session.delete(user)
    db_session.commit()


def get_followers_by_user(*, db_session: Session, user: User) -> Query[User]:
    subquery = db_session.query(Followership.follower_id).filter(Followership.following_id == user.id).subquery()
    followers = db_session.query(User).filter(User.id.in_(subquery))
    return followers


def remove_user_from_followers(*, db_session: Session, follower: FollowerByID) -> None:
    db_session.delete(follower)
    db_session.commit()


def get_followings_by_user(*, db_session: Session, user: User) -> Query[User]:
    subquery = db_session.query(Followership.following_id).filter(Followership.follower_id == user.id).subquery()
    followings = db_session.query(User).filter(User.id.in_(subquery))
    return followings


def follow_user(*, db_session: Session, user: User, following: FollowerShipPayload) -> None:
    followership = Followership(follower_id=user.id, following_id=following.user_id)
    db_session.add(followership)
    db_session.commit()


def unfollow_user(*, db_session: Session, following: FollowingByID) -> None:
    db_session.delete(following)
    db_session.commit()


def create_user(*, db_session: Session, context: UserCreatePayload):
    user = User(email=context.email, username=context.username, password=context.password)
    db_session.add(user)
    db_session.commit()
    return user
