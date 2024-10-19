from http import HTTPStatus

import pytest
from pytest_lazy_fixtures import lf

from app.models import Task
from tests.functions import check_task, task_dict


def test_create_task(client, db_session, faker, access_jwt_token_simple_user):
    """Проверяет создание новой задачи."""
    data = task_dict(db_session, faker)

    headers = {
        "Authorization": f"Bearer {access_jwt_token_simple_user}",
    }

    response = client.post("/api/v1/tasks/", json=data, headers=headers)
    assert response.status_code == HTTPStatus.CREATED
    task_from_db: Task = db_session.query(Task).filter(Task.id == response.json["id"]).first()
    check_task(task_from_db, data)


@pytest.mark.parametrize(
    ("results", "jwt_token"),
    [
        (lf("user_tasks"), lf("access_jwt_token_simple_user")),
        ([], lf("access_jwt_token_another_user")),
    ],
)
def test_get_task_list(client, db_session, jwt_token, results):
    """Проверяет получение списка задач для различных пользователей."""
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.get("/api/v1/tasks/", headers=headers)
    print(response.json)
    assert response.status_code == HTTPStatus.OK, "Получен код ответа отличный от ожидаемого"
    assert response.json["count"] == len(results), "Количество задач не совпадает с ожидаемым"


@pytest.mark.parametrize(
    ("jwt_token", "expected_status_code"),
    [
        (lf("access_jwt_token_simple_user"), HTTPStatus.OK),
        (lf("access_jwt_token_another_user"), HTTPStatus.FORBIDDEN),
    ],
)
def test_update_task(client, db_session, jwt_token, expected_status_code, user_task, faker):
    """Тест обновление задачи."""
    headers = {"Authorization": f"Bearer {jwt_token}"}
    data = task_dict(db_session, faker)
    response = client.put(f"/api/v1/tasks/{user_task.id}", headers=headers, json=data)
    print(response.json)
    assert response.status_code == expected_status_code, "Полученный статус код отличается от ожидаемого"

    db_session.refresh(user_task)
    check_task(user_task, data)
