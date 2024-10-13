from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from flask import current_app, request


def generate_token(user_id: str, secret_key: str, expired_delta: timedelta):
    """Генерирует access-токен для заданного user_id."""
    token = jwt.encode(
        {
            "user_id": user_id,
            "exp": datetime.now(UTC) + expired_delta,
        },
        secret_key,
        algorithm=current_app.config["JWT_ALGORITHM"],
    )
    return token


def token_required(function):
    """Декоратор для определения user_id из токена."""

    def wrapper(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            try:
                token = request.headers["Authorization"].split(" ")[1]
            except IndexError:
                pass

        if not token:
            return {"message": "Token not found in authorization header"}, 401

        try:
            data = jwt.decode(
                token,
                current_app.config["JWT_ACCESS_SECRET_KEY"],
                algorithms=current_app.config["JWT_ALGORITHM"],
            )
            current_user_id = UUID(data["user_id"])
        except jwt.ExpiredSignatureError:
            return {"message": "Token is expired"}, 401
        except jwt.InvalidTokenError:
            return {"message": "Token invalid"}, 401
        except KeyError:
            return {"message": "Wrong token, user_id not found"}, 401

        return function(*args, **kwargs, current_user_id=current_user_id)

    return wrapper


def verify_token(token: str, secret_key: str) -> bool:
    """Валидирует переданный токен."""
    try:
        jwt.decode(
            token,
            secret_key,
            algorithms=current_app.config["JWT_ALGORITHM"],
        )
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False


def get_tokens_by_user_id(user_id: str) -> dict[str, str]:
    """Генерирует access и refresh токены в зависимости от user_id."""
    return {
        "access": generate_token(
            user_id,
            current_app.config["JWT_ACCESS_SECRET_KEY"],
            current_app.config["JWT_ACCESS_EXPIRATION_DELTA"],
        ),
        "refresh": generate_token(
            user_id,
            current_app.config["JWT_REFRESH_SECRET_KEY"],
            current_app.config["JWT_REFRESH_EXPIRATION_DELTA"],
        ),
    }


def get_user_id_from_token(token: str, secret_key: str) -> str | None:
    """Получение user_id из токена."""
    try:
        data = jwt.decode(
            token,
            secret_key,
            algorithms=current_app.config["JWT_ALGORITHM"],
        )
        return data["user_id"]
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError, KeyError):
        return None
