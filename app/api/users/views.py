from flask_restx import Namespace, Resource

from app.api.users.schemas import (
    login_schema,
    refresh_token_schema,
    token_verify_schema,
    tokens_schema,
    user_create_schema,
    user_partial_update_schema,
    user_read_schema,
    user_update_schema,
)
from app.api.users.service import (
    create_user,
    delete_user,
    get_tokens_by_email_and_password,
    get_user_by_id,
    partial_update_user,
    refresh_tokens,
    update_user,
    verify_tokens,
)
from app.models import User
from app.tools.jwt import token_required

ns = Namespace("Пользователи", "Апи пользователей")

ns.models[user_create_schema.name] = user_create_schema
ns.models[user_read_schema.name] = user_read_schema
ns.models[login_schema.name] = login_schema
ns.models[tokens_schema.name] = tokens_schema
ns.models[token_verify_schema.name] = token_verify_schema
ns.models[refresh_token_schema.name] = refresh_token_schema
ns.models[user_partial_update_schema.name] = user_partial_update_schema
ns.models[user_update_schema.name] = user_update_schema


@ns.route("register/")
class RegisterResource(Resource):
    """Регистрация нового пользователя."""

    @ns.expect(user_create_schema, validate=True)
    @ns.marshal_with(user_read_schema, code=201, description="User Created")
    @ns.response(400, "If email is incorrect")
    def post(self) -> tuple[User, int]:
        """Создание нового пользователя."""
        return create_user(**ns.payload), 201


@ns.route("jwt/create/")
class JWTCreateResource(Resource):
    """Класс для создания jwt токена."""

    @ns.expect(login_schema, validate=True)
    @ns.marshal_with(tokens_schema)
    def post(self) -> tuple[dict[str, str], int]:
        """Получение access и refresh токенов по логину/паролю."""
        return get_tokens_by_email_and_password(**ns.payload), 200


@ns.route("jwt/verify/")
class JWTVerifyResource(Resource):
    """Валидация токенов."""

    @ns.expect(tokens_schema)
    @ns.marshal_with(token_verify_schema)
    def post(self) -> tuple[dict[str, bool], int]:
        """Валидация access и refresh токенов."""
        return verify_tokens(**ns.payload), 200


@ns.route("jwt/refresh/")
class JWTRefreshResource(Resource):
    """Обновление токенов по refresh токену."""

    @ns.expect(refresh_token_schema)
    @ns.marshal_with(tokens_schema)
    def post(self) -> tuple[dict[str, str], int]:
        """Получение access и refresh токенов по refresh токену."""
        return refresh_tokens(**ns.payload), 200


@ns.route("me/")
class MeResource(Resource):
    """Работа с учетной записью пользователя."""

    method_decorators = [token_required]

    @ns.doc(security="jwt")
    @ns.marshal_with(user_read_schema)
    def get(self, current_user_id: str) -> tuple[User, int]:
        """Получение информации о текущем пользователе."""
        return get_user_by_id(current_user_id), 200

    @ns.marshal_with(user_read_schema)
    @ns.expect(user_partial_update_schema, validate=True)
    @ns.doc(security="jwt")
    def patch(self, current_user_id: str) -> tuple[User, int]:
        """Частичное обновление информации о пользователе."""
        return partial_update_user(current_user_id, **ns.payload), 200

    @ns.marshal_with(user_read_schema)
    @ns.expect(user_update_schema, validate=True)
    @ns.doc(security="jwt")
    def put(self, current_user_id: str) -> tuple[User, int]:
        """Полное обновление пользователя."""
        return update_user(current_user_id, **ns.payload), 200

    @ns.doc(security="jwt")
    @ns.response(204, "No Content")
    def delete(self, current_user_id: str) -> tuple[None, int]:
        """Удаление пользователя."""
        delete_user(current_user_id)
        return None, 204
