from sqlalchemy.orm import scoped_session, sessionmaker
from twitter_api.database import engine
from twitter_api.engagements.models import Bookmark, Like
from twitter_api.posts.models import Mention, Post
from twitter_api.users.models import Followership, User

Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def db_session():
    session_class = Session
    session = session_class()
    yield session
    session.rollback()


def clean_tables(session):
    session.query(User).delete()
    session.query(Followership).delete()
    session.query(Post).delete()
    session.query(Mention).delete()
    session.query(Like).delete()
    session.query(Bookmark).delete()
    session.commit()
