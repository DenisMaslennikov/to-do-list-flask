from app.models import User
from app.tools.session import session_scope


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
