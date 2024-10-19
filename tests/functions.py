import datetime
import socket
import time
from uuid import UUID

from faker import Faker

from app.models import Task
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
