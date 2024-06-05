from fastapi import APIRouter

from api.posts.views import router
from api.users.views import auth_router, user_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix='/auth', tags=['auth'])
api_router.include_router(user_router, prefix='/users', tags=['users'])
api_router.include_router(router, prefix='/posts', tags=['posts'])
