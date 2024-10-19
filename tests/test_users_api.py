from http import HTTPStatus

from app.models import User


def test_jwt_create(client, simple_user, simple_user_password):
    """Проверка получения access и refresh токенов."""
    data = {
        "email": simple_user.email,
        "password": simple_user_password,
    }

    response = client.post("/api/v1/users/jwt/create/", json=data)
    print(response.json)

    assert response.status_code == HTTPStatus.OK, "Код ответа отличается от ожидаемого"
    assert "access" in response.json, "В ответе не найден access токен"
    assert "refresh" in response.json, "В ответе не найден refresh токен"


def test_jwt_refresh(client, refresh_jwt_token_simple_user):
    """Проверяет обновление access токена по рефреш токену."""
    data = {
        "refresh": refresh_jwt_token_simple_user,
    }

    response = client.post("/api/v1/users/jwt/refresh/", json=data)
    print(response.json)

    assert response.status_code == HTTPStatus.OK, "Код ответа отличается от ожидаемого"
    assert "access" in response.json, "В ответе не найден access токен"
    assert "refresh" in response.json, "В ответе не найден refresh токен"


def test_jwt_verify(client, refresh_jwt_token_simple_user, access_jwt_token_simple_user):
    """Проверяет обновление access токена по рефреш токену."""
    data = {
        "access": access_jwt_token_simple_user,
        "refresh": refresh_jwt_token_simple_user,
    }

    response = client.post("/api/v1/users/jwt/verify/", json=data)
    print(response.json)

    assert response.status_code == HTTPStatus.OK, "Код ответа отличается от ожидаемого"
    assert response.json["access"] is True, "Access токен определен как невалидный"
    assert response.json["refresh"] is True, "Refresh токен определен как невалидный"


def test_update_user_me(client, access_jwt_token_simple_user, faker, db_session):
    """Проверяет обновление текущего пользователя."""
    data = {
        "email": faker.email(),
        "username": faker.user_name(),
        "password": faker.password(),
        "first_name": faker.first_name(),
        "second_name": faker.last_name(),
        "middle_name": faker.middle_name(),
    }
    headers = {"Authorization": f"Bearer {access_jwt_token_simple_user}"}

    response = client.put("/api/v1/users/me/", json=data, headers=headers)
    print(response.json)

    assert response.status_code == HTTPStatus.OK, "Код ответа отличается от ожидаемого"

    user_from_db: User = db_session.query(User).filter(User.email == data["email"]).first()
    assert user_from_db is not None, "Пользователь не найден в базе данных по email"
    assert user_from_db.first_name == data["first_name"], "Имя пользователя не совпадает с переданным"
    assert user_from_db.second_name == data["second_name"], "Фамилия пользователя не совпадает с переданным"
    assert user_from_db.middle_name == data["middle_name"], "Отчество пользователя не совпадает с переданным"
    assert user_from_db.username == data["username"], "Username пользователя не совпадает с переданным"
    assert user_from_db.check_password(data["password"]), "Пароль пользователя не совпадает с переданным"


def test_delete_user_me(client, access_jwt_token_simple_user, db_session):
    """Проверяет удаление текущего пользователя."""
    headers = {"Authorization": f"Bearer {access_jwt_token_simple_user}"}
    response = client.delete("/api/v1/users/me/", headers=headers)
    if response.status_code != HTTPStatus.NO_CONTENT:
        print(response.json)

    assert response.status_code == HTTPStatus.NO_CONTENT, "Код ответа отличается от ожидаемого"
    assert db_session.query(User).count() == 0, "Количество пользователей в бд не соответствует ожидаемому"


def test_get_user_me(client, access_jwt_token_simple_user, simple_user):
    """Проверяет получение информации о текущем пользователе."""
    headers = {"Authorization": f"Bearer {access_jwt_token_simple_user}"}
    response = client.get("/api/v1/users/me/", headers=headers)
    print(response.json)

    assert response.status_code == HTTPStatus.OK, "Код ответа отличается от ожидаемого"
    assert simple_user.email == response.json["email"], "Email не соответствует"
    assert simple_user.username == response.json["username"], "Username не соответствует"
    assert simple_user.first_name == response.json["first_name"], "Имя не соответствует"
    assert simple_user.second_name == response.json["second_name"], "Фамилия не соответствует"
    assert simple_user.middle_name == response.json["middle_name"], "Отчество не соответствует"


def test_partial_update_user_me(
    client, access_jwt_token_simple_user, faker, db_session, simple_user, simple_user_password
):
    """Проверяет частичное обновление текущего пользователя."""
    CHANCE_TO_CHANGE_DATA = 30
    data = {}
    old_data = {
        "email": simple_user.email,
        "username": simple_user.username,
        "first_name": simple_user.first_name,
        "second_name": simple_user.second_name,
        "middle_name": simple_user.middle_name,
    }
    if faker.random_int(1, 100) <= CHANCE_TO_CHANGE_DATA:
        data["email"] = faker.email()
    if faker.random_int(1, 100) <= CHANCE_TO_CHANGE_DATA:
        data["username"] = faker.user_name()
    if faker.random_int(1, 100) <= CHANCE_TO_CHANGE_DATA:
        data["password"] = faker.password()
    if faker.random_int(1, 100) <= CHANCE_TO_CHANGE_DATA:
        data["first_name"] = faker.first_name()
    if faker.random_int(1, 100) <= CHANCE_TO_CHANGE_DATA:
        data["second_name"] = faker.last_name()
    if faker.random_int(1, 100) <= CHANCE_TO_CHANGE_DATA:
        data["middle_name"] = faker.middle_name()

    headers = {"Authorization": f"Bearer {access_jwt_token_simple_user}"}

    response = client.patch("/api/v1/users/me/", json=data, headers=headers)
    print(response.json)

    assert response.status_code == HTTPStatus.OK, "Код ответа отличается от ожидаемого"

    db_session.refresh(simple_user)
    if data.get("email") is not None:
        assert simple_user.email == data["email"], "Email пользователя не соответствует"
    else:
        assert simple_user.email == old_data["email"], "Email пользователя не передавался но был изменен"
    if data.get("first_name") is not None:
        assert simple_user.first_name == data["first_name"], "Имя пользователя не совпадает с переданным"
    else:
        assert simple_user.first_name == old_data["first_name"], "Имя пользователя не передавалось но было изменено"
    if data.get("second_name") is not None:
        assert simple_user.second_name == data["second_name"], "Фамилия пользователя не совпадает с переданным"
    else:
        assert (
            simple_user.second_name == old_data["second_name"]
        ), "Фамилия пользователя не передавалась но была изменена"
    if data.get("middle_name") is not None:
        assert simple_user.middle_name == data["middle_name"], "Отчество пользователя не совпадает с переданным"
    else:
        assert simple_user.middle_name == old_data["middle_name"], "Отчество не передавалось но было изменено"
    if data.get("username") is not None:
        assert simple_user.username == data["username"], "Username пользователя не совпадает с переданным"
    else:
        assert simple_user.username == old_data["username"], "Username не передавался но был изменен"
    if data.get("password") is not None:
        assert simple_user.check_password(data["password"]), "Пароль пользователя не совпадает с переданным"
    else:
        assert simple_user.check_password(simple_user_password), "Пароль не передавался но был изменен"


def test_create_user(client, faker, db_session):
    """Проверяет создание нового пользователя."""
    data = {
        "email": faker.email(),
        "username": faker.user_name(),
        "password": faker.password(),
        "first_name": faker.first_name(),
        "second_name": faker.last_name(),
        "middle_name": faker.middle_name(),
    }

    response = client.post("/api/v1/users/register/", json=data)
    print(response.json)

    assert response.status_code == HTTPStatus.CREATED, "Код ответа отличается от ожидаемого"

    user_from_db: User = db_session.query(User).filter(User.email == data["email"]).first()
    assert user_from_db is not None, "Пользователь не найден в базе данных по email"
    assert user_from_db.first_name == data["first_name"], "Имя пользователя не совпадает с переданным"
    assert user_from_db.second_name == data["second_name"], "Фамилия пользователя не совпадает с переданным"
    assert user_from_db.middle_name == data["middle_name"], "Отчество пользователя не совпадает с переданным"
    assert user_from_db.username == data["username"], "Username пользователя не совпадает с переданным"
    assert user_from_db.check_password(data["password"]), "Пароль пользователя не совпадает с переданным"
