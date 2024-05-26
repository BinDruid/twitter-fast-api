from fastapi import APIRouter, Depends

from app.core.pagination import Params, paginate
from app.models import User

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/')
async def users_list(params: Params = Depends()):
    return await paginate(User.all(), params)
