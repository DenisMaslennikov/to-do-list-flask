from uuid import UUID

from sqlalchemy.orm import Session

from app.models import User


def create_user_repo(
    session: Session,
    email: str,
    password: str,
    username: str | None = None,
    first_name: str | None = None,
    second_name: str | None = None,
    middle_name: str | None = None,
) -> User:
    """Создание нового пользователя в базе."""
    user = User(
        email=email,
        username=username,
        first_name=first_name,
        second_name=second_name,
        middle_name=middle_name,
    )
    user.password = password
    session.add(user)
    return user


def get_user_by_email_repo(session: Session, email: str) -> User | None:
    """Получение пользователя по email."""
    return session.query(User).filter(User.email == email).one_or_none()


def get_user_by_id_repo(session: Session, user_id: str | UUID) -> User | None:
    """Получение пользователя по id."""
    return session.query(User).get(user_id)


def partial_update_user_repo(session: Session, user: User, **kwargs) -> User:
    """Частичное обновление пользователя в базе."""
    for key, value in kwargs.items():
        setattr(user, key, value)
    return user


def update_user_repo(
    session: Session,
    user: User,
    email: str,
    password: str,
    username: str | None = None,
    first_name: str | None = None,
    second_name: str | None = None,
    middle_name: str | None = None,
):
    """Полное обновление информации о пользователе в базе."""
    user.password = password
    user.username = username
    user.first_name = first_name
    user.second_name = second_name
    user.middle_name = middle_name
    user.email = email
    return user


def delete_user_repo(session: Session, user: User) -> None:
    """Удаление пользователя из базы."""
    session.delete(user)
