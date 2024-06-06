from api.database import DbSession
from fastapi import APIRouter, HTTPException
from starlette import status

from .models import View

router = APIRouter(prefix='/views', tags=['Post Views'])


@router.get('/{post_id}/', status_code=status.HTTP_200_OK)
def get_post_views(db_session: DbSession, post_id: int):
    post_view = db_session.query(View).filter(View.post_id == post_id).one_or_none()
    if post_view is None:
        return {'post_view_count': 0}
    return {'post_view_count': post_view.count}


@router.post('/{post_id}/', status_code=status.HTTP_201_CREATED)
def create_view_for_post(db_session: DbSession, post_id: int):
    post_view = db_session.query(View).filter(View.post_id == post_id).one_or_none()
    if post_view is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Can not create another view entry for post #{post_id}')
    new_post_view = View(post_id=post_id, count=0)
    db_session.add(new_post_view)
    db_session.commit()
    return {'message': f'Post #{post_id} was created'}


@router.patch('/{post_id}/', status_code=status.HTTP_206_PARTIAL_CONTENT)
def update_view_for_post(db_session: DbSession, post_id: int):
    post_view = db_session.query(View).filter(View.post_id == post_id).one_or_none()
    if post_view is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No view entry found for post #{post_id}')
    post_view.count = post_view.count + 1
    db_session.commit()
    return {'message': f'Post #{post_id} views updated'}
