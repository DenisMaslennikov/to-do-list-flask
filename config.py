import os
from datetime import timedelta
from pathlib import Path


class BaseConfig(object):
    """Базовая конфигурация."""

    DEBUG: bool = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    ROOT_PATH = Path(__file__).parent

    # region База данных
    DATABASE_HOST = os.environ.get("POSTGRES_HOST")
    DATABASE_PORT = os.environ.get("POSTGRES_PORT")
    DATABASE_NAME = os.environ.get("POSTGRES_DB")
    DATABASE_USER = os.environ.get("POSTGRES_USER")
    DATABASE_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    JWT_ACCESS_SECRET_KEY = os.environ.get("JWT_ACCESS_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY")
    DATABASE_URI: str = (
        f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    )
    # endregion

    PROPAGATE_EXCEPTIONS = True
    JWT_ALGORITHM = "HS256"
    JWT_REFRESH_EXPIRATION_DELTA = timedelta(days=7)
    JWT_ACCESS_EXPIRATION_DELTA = timedelta(minutes=5)


class ProductionConfig(BaseConfig):
    """Продакшен конфигурация."""

    pass


class DevelopmentConfig(BaseConfig):
    """Конфигурация разработки."""

    LOG_LEVEL = "DEBUG"
    JWT_ACCESS_EXPIRATION_DELTA = timedelta(days=1)


class TestingConfig(BaseConfig):
    """Конфигурация для тестов."""

    DATABASE_HOST_MIGRATIONS_TESTS = "db2test"
    DATABASE_HOST_TESTS = "db1test"
