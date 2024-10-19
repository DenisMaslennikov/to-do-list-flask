import datetime
import socket
import time
from uuid import UUID

from faker import Faker
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Task, TaskStatus
from constants import COMPLETED_TASK_STATUS_ID


def wait_for_port(host, port, timeout=60):
    """Ожидание открытия порта на указанном хосте."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(1)
    return False


def create_test_task(task_status_id: int, user_id: UUID, faker: Faker) -> Task:
    """Создает новую задачу."""
    CHANCE_TO_UPDATE = 10
    CHANCE_TO_DEADLINE = 30
    completed_at = None

    if task_status_id == COMPLETED_TASK_STATUS_ID:
        completed_at = faker.date_time()
    created_at = faker.date_time()
    updated_at = None
    if faker.random_int(1, 100) <= CHANCE_TO_UPDATE:
        updated_at = faker.date_time_between(start_date=created_at, end_date=datetime.datetime.today())
    complete_before = None
    if faker.random_int(1, 100) <= CHANCE_TO_DEADLINE:
        complete_before = faker.date_time()
    task = Task(
        title=faker.text(max_nb_chars=255),
        description=faker.text(max_nb_chars=2000),
        task_status_id=task_status_id,
        completed_at=completed_at,
        created_at=created_at,
        updated_at=updated_at,
        user_id=user_id,
        complete_before=complete_before,
    )
    return task


def task_dict(db_session: Session, faker: Faker) -> dict[str, str | datetime.datetime]:
    """Генерирует словарь с задачей для использования в put и post запросах."""
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
    return data


def check_task(task_from_db: Task, data: dict[str, str | datetime.datetime]) -> None:
    """Проверяет соответствие задачи из DB и словаря с данными в случае несовпадения поднимает AssertationError."""
    assert task_from_db is not None, "Задача не найдена в бд"
    if "task_status_id" in data:
        assert task_from_db.task_status_id == data["task_status_id"], "Статус задачи не совпадает"
    elif "task_status" in data:
        assert task_from_db.task_status_id == data["task_status"]["id"], "Статус задачи не совпадает"
    assert task_from_db.title == data["title"], "Заголовок задачи не совпадает"
    assert task_from_db.description == data["description"], "Описание задачи не совпадает"
    if "complete_before" in data:
        if isinstance(data["complete_before"], str):
            data["complete_before"] = datetime.datetime.fromisoformat(data["complete_before"])
        assert task_from_db.complete_before == data["complete_before"], "Срок выполнения задачи не совпадает"
    if "complete_at" in data:
        if isinstance(data["complete_at"], str):
            data["complete_at"] = datetime.datetime.fromisoformat(data["complete_at"])
        assert task_from_db.completed_at == data["completed_at"], "Время выполнения задачи не совпадает"
    if "created_at" in data:
        if isinstance(data["created_at"], str):
            data["created_at"] = datetime.datetime.fromisoformat(data["created_at"])
        assert task_from_db.created_at == data["created_at"], "Дата создания не совпадает"
    if "updated_at" in data:
        if isinstance(data["created_at"], str):
            data["updated_at"] = datetime.datetime.fromisoformat(data["updated_at"])
        assert task_from_db.updated_at == data["updated_at"], "Дата обновления не совпадает"
