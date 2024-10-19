from http import HTTPStatus

import pytest
from pytest_lazy_fixtures import lf
from sqlalchemy import func

from app.models import Task, TaskStatus
from constants import COMPLETED_TASK_STATUS_ID


def test_create_task(client, db_session, faker, access_jwt_token_simple_user):
    """Проверяет создание новой задачи."""
    CHANCE_TO_OPTIONAL_DATA = 30
    task_status_id: int = db_session.query(TaskStatus).order_by(func.random()).first().id
    data = {
        "title": faker.text(max_nb_chars=255),
        "description": faker.text(max_nb_chars=500),
        "task_status_id": task_status_id,
    }

    if faker.random_int(1, 100) <= CHANCE_TO_OPTIONAL_DATA:
        data["complete_before"] = faker.date_time().replace(microsecond=0)

    if task_status_id == COMPLETED_TASK_STATUS_ID:
        if data.get("complete_before") is None:
            data["completed_at"] = faker.date_time().replace(microsecond=0)
        else:
            data["completed_at"] = faker.date_time_between(end_date=data["complete_before"]).replace(microsecond=0)

    headers = {
        "Authorization": f"Bearer {access_jwt_token_simple_user}",
    }

    response = client.post("/api/v1/tasks/", json=data, headers=headers)
    assert response.status_code == HTTPStatus.CREATED
    task_from_db: Task = db_session.query(Task).filter(Task.id == response.json["id"]).first()
    assert task_from_db is not None, "Задача не найдена в бд"
    assert task_from_db.task_status_id == data["task_status_id"], "Статус задачи не совпадает"
    assert task_from_db.title == data["title"], "Заголовок задачи не совпадает"
    assert task_from_db.description == data["description"], "Описание задачи не совпадает"
    if data.get("complete_before") is not None:
        assert task_from_db.complete_before == data["complete_before"], "Срок выполнения задачи не совпадает"
    if data.get("complete_at") is not None:
        assert task_from_db.completed_at == data["completed_at"], "Время выполнения задачи не совпадает"


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
    assert response.json["count"] == len(results), "Количество задач не совпадает"
