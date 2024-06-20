from sqlalchemy.orm import scoped_session, sessionmaker
from twitter_api.database import engine

Session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
