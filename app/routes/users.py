from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.exceptions import HTTPException

from app.core.pagination import Params, paginate
from app.models import User
from app.models.users import UserPydanticIn, UserPydanticOut, hash_password

router = APIRouter(prefix='/users', tags=['users'])


class Status(BaseModel):
    message: str


@router.get('/')
async def users_list(params: Params = Depends()):
    return await paginate(User.all(), params)


@router.post('/')
async def create_user(user: UserPydanticIn):
    hashed_password = hash_password(user.password).decode('utf-8')
    user = await User.create(email=user.email, password=hashed_password)
    return {'user_id': user.id}


@router.get('/{user_id}', response_model=UserPydanticOut)
async def delete_user(user_id: int):
    user = await User.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f'User {user_id} not found')
    return await UserPydanticOut.from_tortoise_orm(user)


@router.delete('/{user_id}', response_model=Status)
async def delete_user(user_id: int):
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f'User {user_id} not found')
    return Status(message=f'Deleted user {user_id}')
