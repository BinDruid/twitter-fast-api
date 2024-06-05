from typing import Annotated

from fastapi import Depends, HTTPException

from src.database.core import DbSession

from .models import User


async def get_user_by_name(username: str, db_session: DbSession) -> User:
    author = db_session.query(User).filter(User.username == username).one_or_none()
    if author is None:
        raise HTTPException(status_code=404, detail=f'User {username} not found')
    return author


UserByName = Annotated[User, Depends(get_user_by_name)]
