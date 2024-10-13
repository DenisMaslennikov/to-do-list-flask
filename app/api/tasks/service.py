from datetime import datetime
from uuid import UUID

from werkzeug.exceptions import BadRequest, Forbidden

from app.api.tasks.repo import (
    create_task_repo,
    get_task_repo,
    get_task_list_for_user_repo,
    update_task_repo,
    delete_task_repo,
)
from app.models import Task
from app.tools.session import session_scope


def get_task_list_for_user(
    user_id: UUID,
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


def create_task(user_id: UUID, title: str, description: str, task_status_id: int, complete_before: datetime) -> Task:
    """Создаёт задачу для пользователя."""
    with session_scope() as session:
        task = create_task_repo(
            session,
            user_id=user_id,
            title=title,
            description=description,
            task_status_id=task_status_id,
            complete_before=complete_before,
        )
        session.flush()
        task = get_task_repo(session, task_id=task.id, load_related=True)
        return task


def get_task(user_id: UUID, task_id: UUID) -> Task:
    """Получение задачи по id."""
    with session_scope() as session:
        task = get_task_repo(session, task_id=task_id, load_related=True)
        if task is None:
            raise BadRequest("Задача не найдена")
        if task.user_id != user_id:
            raise Forbidden("Вы можете просматривать только свои задачи")
        return task


def update_task(
    user_id: UUID,
    task_id: UUID,
    title: str,
    description: str,
    task_status_id: int,
    complete_before: datetime,
    completed_at: datetime | None = None,
) -> Task:
    """Полное обновление задачи."""
    with session_scope() as session:
        task = get_task_repo(session, task_id=task_id, load_related=True)
        if task is None:
            raise BadRequest("Задача не найдена")
        if task.user_id != user_id:
            raise Forbidden("Вы можете редактировать только свои задачи")
        task = update_task_repo(
            session,
            task,
            title=title,
            description=description,
            task_status_id=task_status_id,
            complete_before=complete_before,
            completed_at=completed_at,
        )
        session.refresh(task)
        return task


def delete_task(user_id: UUID, task_id: UUID):
    """Удаление задачи по id."""
    with session_scope() as session:
        task = get_task_repo(session, task_id=task_id)
        if task is None:
            raise BadRequest("Задача не найдена")
        if task.user_id != user_id:
            raise Forbidden("Вы можете удалять только свои задачи")
        delete_task_repo(session, task)
