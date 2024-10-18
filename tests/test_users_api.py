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
    print(data)

    response = client.post("/api/v1/users/jwt/refresh/", json=data)

    print(response.json)

    assert response.status_code == 200, "Код ответа отличается от ожидаемого"
    assert "access" in response.json, "В ответе не найден access токен"
    assert "refresh" in response.json, "В ответе не найден refresh токен"
