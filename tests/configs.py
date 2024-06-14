from sqlalchemy.orm import scoped_session, sessionmaker
from twitter_api.database import engine
from twitter_api.database.depends import get_db_session
from twitter_api.main import api

Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def db_session():
    session_class = Session
    session = session_class()
    yield session
    session.rollback()


api.dependency_overrides[get_db_session] = db_session


test_api = api
