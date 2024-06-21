from twitter_api.users import services
from twitter_api.users.models import Followership, FollowerShipPayload, User, UserCreatePayload

from tests.factories import UserFactory


def test_get_user_by_email_for_existing_user(session, test_user):
    user = services.get_user_by_email(db_session=session, email=test_user.email)
    assert user


def test_get_user_by_email_for_non_existing_user(session):
    user = services.get_user_by_email(db_session=session, email='none@gmail.com')
    assert user is None


def test_get_user_by_username_for_existing_user(session, test_user):
    user = services.get_user_by_username(db_session=session, username=test_user.username)
    assert user


def test_get_user_by_username_for_non_existing_user(session):
    user = services.get_user_by_username(db_session=session, username='none')
    assert user is None


def test_delete_user(session, test_user):
    services.delete_user(db_session=session, user=test_user)
    user_exists = session.query(session.query(User).filter(User.id == test_user.id).exists()).scalar()
    assert user_exists is False


def test_get_followers_by_user(session, user_as_following):
    user = user_as_following.following
    follower = user_as_following.follower
    followers = services.get_followers_by_user(db_session=session, user=user)
    follower_exists = session.query(followers.filter(User.id == follower.id).exists()).scalar()
    assert follower_exists


def test_get_following_by_user(session, user_as_follower):
    user = user_as_follower.follower
    following = user_as_follower.following
    followings = services.get_followings_by_user(db_session=session, user=user)
    following_exists = session.query(followings.filter(User.id == following.id).exists()).scalar()
    assert following_exists


def test_remove_user_from_followers(session, user_as_following):
    user = user_as_following.following
    follower_user = user_as_following.follower
    services.remove_user_from_followers(db_session=session, follower=user_as_following)
    followership_exists = session.query(
        session.query(Followership)
        .filter(Followership.following_id == user.id, Followership.follower_id == follower_user.id)
        .exists()
    ).scalar()
    assert followership_exists is False


def test_follow_user(session, test_user):
    following_user = UserFactory()
    services.follow_user(db_session=session, user=test_user, following=FollowerShipPayload(user_id=following_user.id))
    followership_exists = session.query(
        session.query(Followership)
        .filter(Followership.following_id == following_user.id, Followership.follower_id == test_user.id)
        .exists()
    ).scalar()
    assert followership_exists


def test_unfollow_user(session, user_as_follower):
    user = user_as_follower.follower
    following_user = user_as_follower.following
    services.unfollow_user(db_session=session, following=user_as_follower)
    followership_exists = session.query(
        session.query(Followership)
        .filter(Followership.following_id == following_user.id, Followership.follower_id == user.id)
        .exists()
    ).scalar()
    assert followership_exists is False


def test_create_new_user(session):
    payload = UserCreatePayload(username='ali', email='a.abharya@gmail.com', password='123456')
    new_user = services.create_user(db_session=session, context=payload)
    user_exists = session.query(
        session.query(User).filter(User.username == payload.username, User.email == payload.email).exists()
    ).scalar()
    assert new_user
    assert user_exists
