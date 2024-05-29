from fastapi import APIRouter, Depends

from src.core.pagination import Params, paginate

from .models import Post

router = APIRouter()


@router.get('/')
async def posts_list(params: Params = Depends()):
    return await paginate(Post.all(), params)
