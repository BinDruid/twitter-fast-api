from fastapi import APIRouter, HTTPException
from starlette import status

from src.core.pagination import paginate
from src.database.core import DbSession

from .auth import CurrentUser, InvalidCredentialException
from .models import Followership, FollowerShipPayload, User, UserCreatePayload, UserDetail, UserList, UserLoginPayload

auth_router = APIRouter()
user_router = APIRouter()


@user_router.get('/me/', response_model=UserDetail)
async def get_user_profile(user: CurrentUser, db_session: DbSession):
    user_profile = db_session.query(User).filter(User.id == user.id).one_or_none()
    if not user_profile:
        raise HTTPException(status_code=404, detail=f'User {user.username} not found')
    return user_profile


@user_router.delete('/me/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: CurrentUser, db_session: DbSession):
    user_profile = db_session.query(User).filter(User.id == user.id).one_or_none()
    if not user_profile:
        raise HTTPException(status_code=404, detail=f'User {user.username} not found')
    db_session.delete(user_profile)
    db_session.commit()
    return {'message': f'Deleted user {user.username}'}


@user_router.get('/me/followers/', response_model=UserList)
async def get_user_followers(user: CurrentUser, db_session: DbSession, page: int = 1):
    subquery = db_session.query(Followership.follower_id).filter(Followership.following_id == user.id).subquery()
    followers = db_session.query(User).filter(User.id.in_(subquery))
    return paginate(items=followers, page=page)


@user_router.delete('/me/followers/{follower_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def remove_user_from_followers(user: CurrentUser, db_session: DbSession, follower_id: int):
    follower = (
        db_session.query(Followership)
        .filter(Followership.follower_id == follower_id, Followership.following_id == user.id)
        .one_or_none()
    )
    if not follower:
        raise HTTPException(status_code=404, detail=f'User #{follower_id} not found')
    db_session.delete(follower)
    db_session.commit()
    return {'message': f'User #{follower_id} removed from followers'}


@user_router.get('/me/followings/', response_model=UserList)
def get_user_followings(user: CurrentUser, db_session: DbSession, page: int = 1):
    subquery = db_session.query(Followership.following_id).filter(Followership.follower_id == user.id).subquery()
    followings = db_session.query(User).filter(User.id.in_(subquery))
    return paginate(items=followings, page=page)


@user_router.post('/me/followings/', status_code=status.HTTP_201_CREATED)
async def follow_user(user: CurrentUser, db_session: DbSession, following: FollowerShipPayload):
    followership = Followership(follower_id=user.id, following_id=following.user_id)
    db_session.add(followership)
    db_session.commit()
    return {'message': f'user #{user.id} now is following user #{following.user_id}'}


@user_router.delete('/me/followings/{following_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_user(user: CurrentUser, db_session: DbSession, following_id: int):
    following = (
        db_session.query(Followership)
        .filter(Followership.following_id == following_id, Followership.follower_id == user.id)
        .one_or_none()
    )
    if not following:
        raise HTTPException(status_code=404, detail=f'User #{following_id} not found')
    db_session.delete(following)
    db_session.commit()
    return {'message': f'Unfollowed user #{following_id}'}


@auth_router.post('/', response_model=UserDetail, status_code=status.HTTP_201_CREATED)
async def create_user(db_session: DbSession, payload: UserCreatePayload):
    user = User(email=payload.email, username=payload.username, password=payload.password)
    db_session.add(user)
    db_session.commit()
    return user


@auth_router.post('/login/')
async def login_user(payload: UserLoginPayload, db_session: DbSession):
    user = db_session.query(User).filter(User.username == payload.username).one_or_none()
    if user is None:
        return InvalidCredentialException
    is_authenticated = user.check_password(payload.password)
    if not is_authenticated:
        return InvalidCredentialException
    return {'username': user.username, 'token': user.token}
