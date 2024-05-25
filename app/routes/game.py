from fastapi import APIRouter, Depends

from app.core.pagination import Params, paginate
from app.models import Tournament

router = APIRouter(prefix='/tournaments', tags=['tournaments'])


@router.get('/')
async def tournaments_list(params: Params = Depends()):
    return await paginate(Tournament.all(), params)


@router.post('/')
async def create_tournament():
    tournament = await Tournament.create(name='Another Tournament')
    return {'tournament': tournament.name}
