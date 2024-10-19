from http import HTTPStatus

from app.models import User


def test_jwt_create(client, simple_user, user_password):
    """Проверка получения access и refresh токенов."""
    data = {
        "email": simple_user.email,
        "password": user_password,
    }
    response = client.post("/api/v1/users/jwt/create/", json=data)

    print(response.json)

    assert response.status_code == HTTPStatus.OK, "Код ответа отличается от ожидаемого"
    assert "access" in response.json, "В ответе не найден access токен"
    assert "refresh" in response.json, "В ответе не найден refresh токен"


def test_jwt_refresh(client, refresh_jwt_token):
    """Проверяет обновление access токена по рефреш токену."""
    data = {
        "refresh": refresh_jwt_token,
    }

    response = client.post("/api/v1/users/jwt/refresh/", json=data)

    print(response.json)

    assert response.status_code == HTTPStatus.OK, "Код ответа отличается от ожидаемого"
    assert "access" in response.json, "В ответе не найден access токен"
    assert "refresh" in response.json, "В ответе не найден refresh токен"


def test_jwt_verify(client, refresh_jwt_token, access_jwt_token):
    """Проверяет обновление access токена по рефреш токену."""
    data = {
        "access": access_jwt_token,
        "refresh": refresh_jwt_token,
    }

    response = client.post("/api/v1/users/jwt/verify/", json=data)

    print(response.json)

    assert response.status_code == HTTPStatus.OK, "Код ответа отличается от ожидаемого"
    assert response.json["access"] is True, "Access токен определен как невалидный"
    assert response.json["refresh"] is True, "Refresh токен определен как невалидный"


def test_update_user_me(
    client,
    access_jwt_token,
    faker,
    db_session,
):
    """Проверяет обновление текущего пользователя."""
    data = {
        "email": faker.email(),
        "username": faker.user_name(),
        "password": faker.password(),
        "first_name": faker.first_name(),
        "second_name": faker.last_name(),
        "middle_name": faker.middle_name(),
    }
    headers = {"Authorization": f"Bearer {access_jwt_token}"}

    response = client.put(f"/api/v1/users/me/", json=data, headers=headers)

    print(response.json)
    db_session.expire_all()

    assert response.status_code == HTTPStatus.OK, "Код ответа отличается от ожидаемого"

    user_from_db: User = db_session.query(User).filter(User.email == data["email"]).first()
    assert user_from_db is not None, "Пользователь не найден в базе данных по email"
    assert user_from_db.first_name == data["first_name"], "Имя пользователя не совпадает с переданным"
    assert user_from_db.second_name == data["second_name"], "Фамилия пользователя не совпадает с переданным"
    assert user_from_db.middle_name == data["middle_name"], "Отчество пользователя не совпадает с переданным"
    assert user_from_db.username == data["username"], "Username пользователя не совпадает с переданным"
    assert user_from_db.check_password(data["password"]), "Пароль пользователя не совпадает с переданным"


def test_delete_user_me(client, access_jwt_token, db_session):
    """Проверяет удаление текущего пользователя."""
    headers = {"Authorization": f"Bearer {access_jwt_token}"}
    response = client.delete("/api/v1/users/me/", headers=headers)

    if response.status_code != HTTPStatus.NO_CONTENT:
        print(response.json)

    assert response.status_code == HTTPStatus.NO_CONTENT, "Код ответа отличается от ожидаемого"
    assert db_session.query(User).count() == 0, "Количество пользователей в бд не соответствует ожидаемому"


def test_get_user_me(client, access_jwt_token, simple_user):
    """Проверяет получение информации о текущем пользователе."""
    headers = {"Authorization": f"Bearer {access_jwt_token}"}
    response = client.get("/api/v1/users/me/", headers=headers)
    print(response.json)
    assert response.status_code == HTTPStatus.OK, "Код ответа отличается от ожидаемого"
    assert simple_user.email == response.json["email"], "Email не соответствует"
    assert simple_user.username == response.json["username"], "Username не соответствует"
    assert simple_user.first_name == response.json["first_name"], "Имя не соответствует"
    assert simple_user.second_name == response.json["second_name"], "Фамилия не соответствует"
    assert simple_user.middle_name == response.json["middle_name"], "Отчество не соответствует"
