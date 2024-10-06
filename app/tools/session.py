import contextlib

from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


@contextlib.contextmanager
def session_scope() -> Session:
    """Создание контекстного менеджера сессии и оборачивание её в транзакцию."""
    engine = create_engine(current_app.config["DATABASE_URI"])
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)

    with session_factory() as sess:
        try:
            yield sess
        except Exception as e:
            sess.rollback()
            raise e
        else:
            sess.commit()
        finally:
            sess.close()
