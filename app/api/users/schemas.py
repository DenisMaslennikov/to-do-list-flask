from flask_restx import Model, fields

user_create_schema = Model(
    "UserCreateSchema",
    {
        "email": fields.String(required=True, example="email@example.com", description="Email"),
        "username": fields.String(required=False, example="You_username", description="Username"),
        "password": fields.String(required=True, example="You_password", description="Пароль"),
        "first_name": fields.String(required=False, example="John", description="Имя"),
        "second_name": fields.String(required=False, example="Doe", description="Фамилия"),
        "middle_name": fields.String(required=False, example="Blankovich", description="Отчество"),
    },
)

user_partial_update_schema = Model(
    "UserPartialUpdateSchema",
    {
        "email": fields.String(required=False, example="email@example.com", description="Email"),
        "username": fields.String(required=False, example="You_username", description="Username"),
        "password": fields.String(required=False, example="You_password", description="Пароль"),
        "first_name": fields.String(required=False, example="John", description="Имя"),
        "second_name": fields.String(required=False, example="Doe", description="Фамилия"),
        "middle_name": fields.String(required=False, example="Blankovich", description="Отчество"),
    },
)

user_update_schema = Model(
    "UserUpdateSchema",
    {
        "email": fields.String(required=True, example="email@example.com", description="Email"),
        "username": fields.String(required=True, example="You_username", description="Username"),
        "password": fields.String(required=True, example="You_password", description="Пароль"),
        "first_name": fields.String(required=True, example="John", description="Имя"),
        "second_name": fields.String(required=True, example="Doe", description="Фамилия"),
        "middle_name": fields.String(required=True, example="Blankovich", description="Отчество"),
    },
)

user_read_schema = Model(
    "UserReadSchema",
    {
        "email": fields.String(required=True, example="email@example.com", description="Email"),
        "username": fields.String(required=False, example="You_username", description="Username"),
        "first_name": fields.String(required=False, example="John", description="First Name"),
        "second_name": fields.String(required=False, example="Doe", description="Second Name"),
        "middle_name": fields.String(required=False, example="Blankovich", description="Middle Name"),
    },
)

login_schema = Model(
    "LoginSchema",
    {
        "email": fields.String(required=True, example="email@example.com", description="Email"),
        "password": fields.String(required=True, example="You_password", description="Пароль"),
    },
)

tokens_schema = Model(
    "TokensSchema",
    {
        "access": fields.String(required=False, description="Access Token"),
        "refresh": fields.String(required=False, description="Refresh token"),
    },
)

token_verify_schema = Model(
    "TokenVerifySchema",
    {
        "access": fields.Boolean(required=False, description="Access token verify"),
        "refresh": fields.Boolean(required=False, description="Refresh token verify"),
    },
)

refresh_token_schema = Model(
    "RefreshTokenSchema",
    {
        "refresh": fields.String(required=True, description="Refresh token"),
    },
)
