from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from contextlib import contextmanager

from core.config import settings



def get_engine() -> Engine:
    
    engine = create_engine(
        settings.DB_URL,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_recycle=settings.DB_POOL_RECYCLE,
        pool_pre_ping=True,
        echo=(settings.ENV == "development")
    )
    return engine


def __get_session() -> Session:
    engine = get_engine()
    SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Session = scoped_session(SessionFactory)
    session = Session()
    return session


@contextmanager
def db_session():
    session = __get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()