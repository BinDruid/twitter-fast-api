from fastapi import APIRouter

from src.posts.views import router
from src.users.views import auth_router, user_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix='/auth', tags=['auth'])
api_router.include_router(user_router, prefix='/users', tags=['users'])
api_router.include_router(router, prefix='/posts', tags=['posts'])
