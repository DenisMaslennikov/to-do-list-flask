import pytest
import sqlalchemy
from sqlalchemy_utils import create_database, database_exists, drop_database

from alembic import command
from alembic.config import Config as AlembicConfig
from app import get_app
from config import TestingConfig
from tests.functions import wait_for_port


@pytest.fixture
def alembic_engine(migrations_test_container):
    """Используется pytest-alembic."""
    pg_alembic_uri = (
        f"postgresql+psycopg2://"
        f"{TestingConfig.DATABASE_USER}:"
        f"{TestingConfig.DATABASE_PASSWORD}@"
        f"{TestingConfig.DATABASE_HOST_ALEMBIC_TESTS}:"
        f"{TestingConfig.DATABASE_PORT}/"
        f"{TestingConfig.DATABASE_NAME}"
    )
    if database_exists(pg_alembic_uri):
        drop_database(pg_alembic_uri)
    # Создание тестовой базы данных
    create_database(pg_alembic_uri)
    return sqlalchemy.create_engine(pg_alembic_uri)


@pytest.fixture(scope="session")
def migrations_test_container():
    """Для тестирования миграций alembic."""
    wait_for_port(TestingConfig.DATABASE_HOST_ALEMBIC_TESTS, TestingConfig.DATABASE_PORT)


@pytest.fixture(scope="session")
def database_test_container():
    """Для тестирования."""
    if not wait_for_port(TestingConfig.DATABASE_HOST_TESTS, TestingConfig.DATABASE_PORT):
        pytest.exit(f"Exiting: Failed to connect to {TestingConfig.DATABASE_HOST_TESTS} container.")


@pytest.fixture(scope="session")
def app(database_test_container):
    """Приложение фласк для тестирования."""
    app = get_app(TestingConfig)
    app.config["DATABASE_URI"] = (
        f"postgresql+psycopg2://"
        f"{TestingConfig.DATABASE_USER}:"
        f"{TestingConfig.DATABASE_PASSWORD}@"
        f"{TestingConfig.DATABASE_HOST_TESTS}:"
        f"{TestingConfig.DATABASE_PORT}/"
        f"{TestingConfig.DATABASE_NAME}"
    )
    return app


@pytest.fixture(scope="session")
def create_db(app):
    """Создание тестовой базы данных."""
    uri = app.config.get("DATABASE_URI")
    print(f"{app.config.get('DATABASE_URI')=}")
    if database_exists(uri):
        drop_database(uri)

    # Создание тестовой базы данных
    create_database(uri)

    yield

    # Удаление тестовой базы данных
    if database_exists(uri):
        drop_database(uri)


@pytest.fixture(scope="session")
def migrations(app, create_db):
    """Запуск миграций Alembic."""
    uri = app.config.get("DATABASE_URI")

    # Запуск миграций Alembic
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", uri)

    print(f"Starting Alembic migrations on {uri}")

    # Ручная проверка параметров конфигурации
    # for key in alembic_cfg.get_section("alembic"):
    #     print(f"Alembic config {key}: {alembic_cfg.get_section_option('alembic', key)}")

    # Применяем миграции
    try:
        command.upgrade(alembic_cfg, "head")  # Выполнение миграций
    except Exception as e:
        print(f"Error during Alembic migration: {e}")
