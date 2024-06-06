from fastapi import APIRouter

from twitter_api.engagements.views import router as engagement_router
from twitter_api.posts.views import router as post_router
from twitter_api.users.views import auth_router, user_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix='/auth', tags=['Authentication'])
api_router.include_router(user_router, prefix='/users', tags=['Users'])
api_router.include_router(post_router, prefix='/posts', tags=['Posts'])
api_router.include_router(engagement_router, prefix='/engagements', tags=['Engagements'])
