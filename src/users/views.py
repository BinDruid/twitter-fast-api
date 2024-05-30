from typing import Annotated

from fastapi import APIRouter, Body
from starlette import status
from starlette.exceptions import HTTPException
from tortoise.exceptions import DoesNotExist

from .auth import CurrentUser, InvalidCredentialException
from .models import User, UserPydanticIn, UserPydanticOut, hash_password

auth_router = APIRouter()
user_router = APIRouter()


@user_router.get('/profile/', response_model=UserPydanticOut)
async def get_user_profile(user: CurrentUser):
    user_profile = await User.get(id=user['id'])
    if not user_profile:
        raise HTTPException(status_code=404, detail=f"User {user['email']} not found")
    return user_profile


@user_router.delete('/profile/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: CurrentUser):
    deleted_count = await User.filter(id=user['id']).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user['email']} not found")
    return {'message': f"Deleted user {user['id']}"}


@auth_router.post('/', response_model=UserPydanticOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserPydanticIn):
    hashed_password = hash_password(user.password).decode('utf-8')
    user = await User.create(email=user.email, password=hashed_password)
    return user


@auth_router.post('/login/')
async def login_user(email: Annotated[str, Body()], password: Annotated[str, Body()]):
    try:
        user = await User.get(email=email)
    except DoesNotExist:
        return InvalidCredentialException
    is_authenticated = user.check_password(password)
    if not is_authenticated:
        return InvalidCredentialException
    return {'email': user.email, 'token': user.token}
