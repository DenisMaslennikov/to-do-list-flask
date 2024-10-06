from uuid import UUID

from flask import current_app
from flask_restx import abort
from sqlalchemy.exc import IntegrityError

from app.api.users.repo import (
    create_user_repo,
    delete_user_repo,
    get_user_by_email_repo,
    get_user_by_id_repo,
    partial_update_user_repo,
    update_user_repo,
)
from app.models import User
from app.tools.jwt import get_tokens_by_user_id, get_user_id_from_token, verify_token
from app.tools.session import session_scope


def create_user(
    email: str,
    password: str,
    username: str | None = None,
    first_name: str | None = None,
    second_name: str | None = None,
    middle_name: str | None = None,
) -> User:
    """Создание нового пользователя."""
    try:
        with session_scope() as session:
            return create_user_repo(
                session,
                email=email,
                password=password,
                username=username,
                first_name=first_name,
                second_name=second_name,
                middle_name=middle_name,
            )
    except (IntegrityError, ValueError):
        abort(400, "Некорректный email")


def get_tokens_by_email_and_password(email: str, password: str) -> dict[str, str]:
    """Получение access и refresh токенов по email и паролю."""
    with session_scope() as session:
        user = get_user_by_email_repo(session, email)
    if user is None or not user.check_password(password):
        abort(401, "Неверный логин или пароль")
    user_id = str(user.id)
    return get_tokens_by_user_id(user_id)


def verify_tokens(access: str | None = None, refresh: str | None = None) -> dict[str, bool]:
    """Валидирует переданные токены."""
    return {
        "access": verify_token(access, current_app.config["JWT_ACCESS_SECRET_KEY"]) if access else False,
        "refresh": verify_token(refresh, current_app.config["JWT_REFRESH_SECRET_KEY"]) if refresh else False,
    }


def refresh_tokens(refresh: str) -> dict[str, str]:
    """Обновляет токены по полученному refresh токену."""
    user_id = get_user_id_from_token(refresh, current_app.config["JWT_REFRESH_SECRET_KEY"])
    if user_id is None:
        abort(401, "Некорректный токен")
    return get_tokens_by_user_id(user_id)


def get_user_by_id(user_id: str | UUID) -> User | None:
    """Получение информации о пользователе по id."""
    with session_scope() as session:
        return get_user_by_id_repo(session, user_id)


def partial_update_user(user_id: str | UUID, **kwargs) -> User:
    """Частичное обновление информации о пользователе."""
    with session_scope() as session:
        user = get_user_by_id_repo(session, user_id)
        if user is None:
            abort(401, "Некорректный токен")
        return partial_update_user_repo(session, user, **kwargs)


def update_user(
    user_id: str | UUID,
    email: str,
    password: str,
    username: str | None = None,
    first_name: str | None = None,
    second_name: str | None = None,
    middle_name: str | None = None,
) -> User:
    """Полное обновление информации о пользователе."""
    with session_scope() as session:
        user = get_user_by_id_repo(session, user_id)
        if user is None:
            abort(401, "Некорректный токен")
        return update_user_repo(
            session,
            user=user,
            email=email,
            password=password,
            username=username,
            first_name=first_name,
            second_name=second_name,
            middle_name=middle_name,
        )


def delete_user(user_id: str | UUID) -> None:
    """Удаление пользователя."""
    with session_scope() as session:
        user = get_user_by_id_repo(session, user_id)
        if user is None:
            abort(401, "Некорректный токен")
        delete_user_repo(session, user)
