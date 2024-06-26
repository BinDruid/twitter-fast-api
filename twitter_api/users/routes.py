from fastapi import APIRouter, status

from twitter_api.core import exceptions
from twitter_api.core.pagination import paginate
from twitter_api.database import DbSession

from . import services
from .auth import check_password, generate_token
from .depends import CurrentUser, FollowerByID, FollowingByID, UserByID
from .models import FollowerShipPayload, User, UserCreatePayload, UserDetail, UserList, UserLoginPayload

auth_router = APIRouter()
user_router = APIRouter()


@user_router.get('/profile/{user_id}/', response_model=UserDetail)
def get_user_profile(db_session: DbSession, user: UserByID):
    return user


@user_router.delete('/profile/{user_id}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(current_user: CurrentUser, db_session: DbSession, user: UserByID):
    if current_user.id != user.id:
        raise exceptions.PermissionDenied
    services.delete_user(db_session=db_session, user=user)
    return {'message': f'Deleted user {user.username}'}


@user_router.get('/{user_id}/followers/', response_model=UserList)
def get_user_followers(db_session: DbSession, user: UserByID, page: int = 1):
    followers = services.get_followers_by_user(db_session=db_session, user=user)
    return paginate(items=followers, page=page)


@user_router.delete('/{user_id}/followers/{follower_user_id}/', status_code=status.HTTP_204_NO_CONTENT)
def remove_user_from_followers(
    current_user: CurrentUser, db_session: DbSession, user: UserByID, follower: FollowerByID
):
    if current_user.id != user.id:
        raise exceptions.PermissionDenied
    services.remove_user_from_followers(db_session=db_session, follower=follower)
    return {'message': f'User #{follower.follower_id} removed from followers'}


@user_router.get('/{user_id}/followings/', response_model=UserList)
def get_user_followings(db_session: DbSession, user: UserByID, page: int = 1):
    followings = services.get_followings_by_user(db_session=db_session, user=user)
    return paginate(items=followings, page=page)


@user_router.post('/{user_id}/followings/', status_code=status.HTTP_201_CREATED)
def follow_user(current_user: CurrentUser, db_session: DbSession, user: UserByID, following: FollowerShipPayload):
    if current_user.id != user.id:
        raise exceptions.PermissionDenied
    if user.id == following.user_id:
        raise exceptions.BadRequest(detail='User can not follow themselves')
    services.follow_user(db_session=db_session, user=user, following_id=following.user_id)
    return {'message': f'User #{user.id} now is following user #{following.user_id}'}


@user_router.delete('/{user_id}/followings/{following_user_id}/', status_code=status.HTTP_204_NO_CONTENT)
def unfollow_user(current_user: CurrentUser, db_session: DbSession, user: UserByID, following: FollowingByID):
    if current_user.id != user.id:
        raise exceptions.PermissionDenied
    services.unfollow_user(db_session=db_session, following=following)
    return {'message': f'Unfollowed user #{following.following_id}'}


@auth_router.post('/', response_model=UserDetail, status_code=status.HTTP_201_CREATED)
def create_user(db_session: DbSession, payload: UserCreatePayload):
    email_already_exist = services.get_user_by_username(db_session=db_session, username=payload.username)
    username_already_exist = services.get_user_by_email(db_session=db_session, email=payload.email)
    if email_already_exist or username_already_exist:
        raise exceptions.BadRequest(detail='User already exists')
    new_user = services.create_user(
        db_session=db_session, username=payload.username, email=payload.email, password=payload.password
    )
    return new_user


@auth_router.post('/login/')
def login_user(db_session: DbSession, payload: UserLoginPayload):
    user = db_session.query(User).filter(User.username == payload.username).one_or_none()
    if user is None:
        raise exceptions.NotAuthenticated
    is_authenticated = check_password(user=user, password=payload.password)
    if not is_authenticated:
        raise exceptions.NotAuthenticated
    token = generate_token(user=user)
    return {'username': user.username, 'token': token}
