from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from config import DB_PASSWORD, DB_HOST, DB_NAME, DB_USER
from contextlib import contextmanager


def get_engine() -> Engine:
    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}\
    @{DB_HOST}/{DB_NAME}"
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
