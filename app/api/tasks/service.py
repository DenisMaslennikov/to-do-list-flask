from datetime import datetime
from uuid import UUID

from werkzeug.exceptions import Forbidden

from app.api.tasks.repo import create_task_repo, get_task_list_for_user_repo, get_task_by_id_repo
from app.models import Task
from app.tools.session import session_scope


def get_task_list_for_user(
    user_id: str,
    title: str | None = None,
    task_status_id: int | None = None,
    sort_fields: str | None = None,
    sort_order: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> dict[str, list[Task] | int]:
    """Получение списка задач для конкретного пользователя."""
    with session_scope() as session:
        results, count = get_task_list_for_user_repo(
            session,
            user_id=user_id,
            title=title,
            task_status_id=task_status_id,
            sort_fields=sort_fields,
            sort_order=sort_order,
            limit=limit,
            offset=offset,
            load_related=True,
        )
        return {"results": results, "count": count}


def create_task(user_id: str, title: str, description: str, task_status_id: int, due_date: datetime) -> Task:
    """Создаёт задачу для пользователя."""
    with session_scope() as session:
        task = create_task_repo(
            session,
            user_id=user_id,
            title=title,
            description=description,
            task_status_id=task_status_id,
            due_date=due_date,
        )
        session.flush()
        task = get_task_by_id_repo(session, task_id=task.id, load_related=True)
        return task


def get_task_by_id(user_id: str, task_id: UUID) -> Task:
    """Получение задачи по id."""
    with session_scope() as session:
        task = get_task_by_id_repo(session, task_id=task_id, load_related=True)
        if task.user_id != UUID(user_id):
            raise Forbidden("Вы можете просматривать только свои задачи")
        return task
