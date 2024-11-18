from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .models import Base


def create_session_factory(engine):
    return scoped_session(sessionmaker(bind=engine))

session_factory = None

def init_db(app):
    global session_factory
    engine = create_engine(app.config['DATABASE_URL'], echo=False, connect_args={"check_same_thread": False})
    
    session_factory = create_session_factory(engine)
    
    Base.metadata.bind = engine
    
    Base.metadata.create_all(engine)

def get_session():
    global session_factory
    return session_factory()