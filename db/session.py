from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from config import DB_MANAGER, DB_PASSWORD, DB_HOST, DB_NAME, DB_USER, DB_PORT
from contextlib import contextmanager


def get_engine() -> Engine:
    
    if DB_MANAGER == "postgres":
        url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}\
        @{DB_HOST}/{DB_NAME}"
    elif DB_MANAGER == "mysql":
        url = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_PORT}"
    engine = create_engine(
        url        
    )

    return engine


def __get_session() -> Session:
    engine = get_engine()
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    return session


@contextmanager
def db_session():
    session = __get_session()
    yield session
    session.commit()
    session.close()
