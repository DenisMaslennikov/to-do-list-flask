def test_jwt_create(client, simple_user, user_password):
    """Проверка получения access и refresh токенов."""
    data = {
        "email": simple_user.email,
        "password": user_password,
    }
    response = client.post("/api/v1/users/jwt/create/", json=data)

    print(response.json)

    assert response.status_code == 200, "Код ответа отличается от ожидаемого"
    assert "access" in response.json, "В ответе не найден access токен"
    assert "refresh" in response.json, "В ответе не найден refresh токен"


def test_jwt_refresh(client, refresh_jwt_token):
    """Проверяет обновление access токена по рефреш токену."""
    data = {
        "refresh": refresh_jwt_token,
    }

    response = client.post("/api/v1/users/jwt/refresh/", json=data)

    print(response.json)

    assert response.status_code == 200, "Код ответа отличается от ожидаемого"
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

    assert response.status_code == 200, "Код ответа отличается от ожидаемого"
    assert response.json["access"] is True, "Access токен определен как невалидный"
    assert response.json["refresh"] is True, "Refresh токен определен как невалидный"
