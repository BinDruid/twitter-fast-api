from fastapi import APIRouter

from api.likes.views import router as like_router
from api.posts.views import router as post_router
from api.users.views import auth_router, user_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix='/auth', tags=['auth'])
api_router.include_router(user_router, prefix='/users', tags=['users'])
api_router.include_router(post_router, prefix='/posts', tags=['posts'])
api_router.include_router(like_router, prefix='/posts', tags=['likes'])
