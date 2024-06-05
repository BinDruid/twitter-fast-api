from fastapi import APIRouter

from api.engagements.views import router as engagement_router
from api.posts.views import router as post_router
from api.users.views import auth_router, user_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix='/auth', tags=['auth'])
api_router.include_router(user_router, prefix='/users', tags=['users'])
api_router.include_router(post_router, prefix='/posts', tags=['posts'])
api_router.include_router(engagement_router, prefix='/engagements', tags=['engagements'])
