from fastapi import APIRouter, HTTPException
from starlette import status

from src.database.core import DbSession

from .auth import CurrentUser, InvalidCredentialException
from .models import User, UserDetail, UserPayload, hash_password

auth_router = APIRouter()
user_router = APIRouter()


@user_router.get('/profile/', response_model=UserDetail)
async def get_user_profile(user: CurrentUser, db_session: DbSession):
    user_profile = db_session.query(User).filter(User.id == user['id']).one_or_none()
    if not user_profile:
        raise HTTPException(status_code=404, detail=f"User {user['email']} not found")
    return user_profile


@user_router.delete('/profile/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: CurrentUser, db_session: DbSession):
    user_profile = db_session.query(User).filter(User.id == user['id']).one_or_none()
    if not user_profile:
        raise HTTPException(status_code=404, detail=f"User {user['email']} not found")
    db_session.delete(user_profile)
    db_session.commit()
    return {'message': f"Deleted user {user['id']}"}


@auth_router.post('/', response_model=UserDetail, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserPayload, db_session: DbSession):
    hashed_password = hash_password(payload.password).decode('utf-8')
    user = User(email=payload.email, password=hashed_password)
    db_session.add(user)
    db_session.commit()
    return user


@auth_router.post('/login/')
async def login_user(payload: UserPayload, db_session: DbSession):
    user = db_session.query(User).filter(User.email == payload.email).one_or_none()
    if user is None:
        return InvalidCredentialException
    is_authenticated = user.check_password(payload.password)
    if not is_authenticated:
        return InvalidCredentialException
    return {'email': user.email, 'token': user.token}
