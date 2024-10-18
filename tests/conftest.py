import pytest
from faker import Faker
from flask.testing import FlaskClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import create_database, database_exists, drop_database

from alembic import command
from alembic.config import Config as AlembicConfig
from app import get_app
from app.models import User
from app.tools.jwt import generate_token
from config import TestingConfig
from tests.functions import wait_for_port


@pytest.fixture
def alembic_engine(migrations_test_container):
    """Используется pytest-alembic."""
    pg_alembic_uri = (
        f"postgresql+psycopg2://"
        f"{TestingConfig.DATABASE_USER}:"
        f"{TestingConfig.DATABASE_PASSWORD}@"
        f"{TestingConfig.DATABASE_HOST_MIGRATIONS_TESTS}:"
        f"{TestingConfig.DATABASE_PORT}/"
        f"{TestingConfig.DATABASE_NAME}"
    )
    if database_exists(pg_alembic_uri):
        drop_database(pg_alembic_uri)
    # Создание тестовой базы данных
    create_database(pg_alembic_uri)
    return create_engine(pg_alembic_uri)


@pytest.fixture(scope="session")
def migrations_test_container():
    """Для тестирования миграций alembic."""
    wait_for_port(TestingConfig.DATABASE_HOST_MIGRATIONS_TESTS, TestingConfig.DATABASE_PORT)


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
    # Применяем миграции
    try:
        command.upgrade(alembic_cfg, "head")  # Выполнение миграций
    except Exception as e:
        print(f"Error during Alembic migration: {e}")
        raise e


@pytest.fixture(scope="session")
def engine(app, migrations):
    """Создает engine SQLAlchemy для взаимодействия с базой."""
    uri = app.config.get("DATABASE_URI")
    engine = create_engine(uri)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(engine):
    """Создает и возвращает сессию базы данных для тестирования."""
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function", autouse=True)
def mock_session(mocker, db_session):
    """Патчит сессию подменяя её фикстурой."""
    mocker.patch("app.api.users.service.session_scope", return_value=db_session)
    mocker.patch("app.api.tasks.service.session_scope", return_value=db_session)
    mocker.patch("app.api.classifiers.service.session_scope", return_value=db_session)


@pytest.fixture
def faker() -> Faker:
    """Фейкер для генерации данных."""
    return Faker("ru_RU")


@pytest.fixture
def client(app) -> FlaskClient:
    """Клиент для тестирования апи."""
    with app.app_context():
        with app.test_client() as client:
            yield client


@pytest.fixture
def user_password(faker) -> str:
    """Генерирует пароль пользователя."""
    return faker.password()


@pytest.fixture
def simple_user(db_session, faker, user_password) -> User:
    """Обычный пользователь."""
    email = faker.email()
    user = User(
        email=email,
        first_name=faker.first_name(),
        second_name=faker.last_name(),
        middle_name=faker.middle_name(),
        username=faker.user_name(),
    )
    user.password = user_password
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def refresh_jwt_token(simple_user, app):
    return generate_token(
        str(simple_user.id), app.config["JWT_REFRESH_SECRET_KEY"], app.config["JWT_REFRESH_EXPIRATION_DELTA"]
    )


@pytest.fixture
def access_jwt_token(simple_user, app):
    return generate_token(
        str(simple_user.id), app.config["JWT_ACCESS_SECRET_KEY"], app.config["JWT_ACCESS_EXPIRATION_DELTA"]
    )
