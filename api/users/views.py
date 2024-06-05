from fastapi import APIRouter, HTTPException
from starlette import status

from api.core.pagination import paginate
from api.database import DbSession

from .auth import CurrentUser, InvalidCredentialException
from .depends import FollowerByID, FollowingByID, UserByID
from .models import Followership, FollowerShipPayload, User, UserCreatePayload, UserDetail, UserList, UserLoginPayload

auth_router = APIRouter()
user_router = APIRouter()


@user_router.get('/profile/{user_id}/', response_model=UserDetail)
def get_user_profile(db_session: DbSession, user: UserByID):
    return user


@user_router.delete('/profile/{user_id}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(current_user: CurrentUser, db_session: DbSession, user: UserByID):
    if current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    db_session.delete(user)
    db_session.commit()
    return {'message': f'Deleted user {user.username}'}


@user_router.get('/{user_id}/followers/', response_model=UserList)
def get_user_followers(db_session: DbSession, user: UserByID, page: int = 1):
    subquery = db_session.query(Followership.follower_id).filter(Followership.following_id == user.id).subquery()
    followers = db_session.query(User).filter(User.id.in_(subquery))
    return paginate(items=followers, page=page)


@user_router.delete('/{user_id}/followers/{follower_user_id}/', status_code=status.HTTP_204_NO_CONTENT)
def remove_user_from_followers(
    current_user: CurrentUser, db_session: DbSession, user: UserByID, follower: FollowerByID
):
    if current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    db_session.delete(follower)
    db_session.commit()
    return {'message': f'User #{follower.follower_id} removed from followers'}


@user_router.get('/{user_id}/followings/', response_model=UserList)
def get_user_followings(db_session: DbSession, user: UserByID, page: int = 1):
    subquery = db_session.query(Followership.following_id).filter(Followership.follower_id == user.id).subquery()
    followings = db_session.query(User).filter(User.id.in_(subquery))
    return paginate(items=followings, page=page)


@user_router.post('/{user_id}/followings/', status_code=status.HTTP_201_CREATED)
def follow_user(current_user: CurrentUser, db_session: DbSession, user: UserByID, following: FollowerShipPayload):
    if current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    followership = Followership(follower_id=user.id, following_id=following.user_id)
    db_session.add(followership)
    db_session.commit()
    return {'message': f'User #{user.id} now is following user #{following.user_id}'}


@user_router.delete('/{user_id}/followings/{following_user_id}/', status_code=status.HTTP_204_NO_CONTENT)
def unfollow_user(current_user: CurrentUser, db_session: DbSession, user: UserByID, following: FollowingByID):
    if user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    db_session.delete(following)
    db_session.commit()
    return {'message': f'Unfollowed user #{following.following_id}'}


@auth_router.post('/', response_model=UserDetail, status_code=status.HTTP_201_CREATED)
def create_user(db_session: DbSession, payload: UserCreatePayload):
    user = User(email=payload.email, username=payload.username, password=payload.password)
    db_session.add(user)
    db_session.commit()
    return user


@auth_router.post('/login/')
def login_user(db_session: DbSession, payload: UserLoginPayload):
    user = db_session.query(User).filter(User.username == payload.username).one_or_none()
    if user is None:
        return InvalidCredentialException
    is_authenticated = user.check_password(payload.password)
    if not is_authenticated:
        return InvalidCredentialException
    return {'username': user.username, 'token': user.token}
