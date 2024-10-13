from uuid import UUID

from sqlalchemy.orm import Session, joinedload
from werkzeug.exceptions import BadRequest

from app.models import Task
from constants import MAX_AMOUNT_OF_TASKS


def get_task_list_for_user_repo(
    session: Session,
    user_id: str,
    title: str | None = None,
    task_status_id: int | None = None,
    sort_fields: str | None = None,
    sort_order: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    load_related: bool = False,
) -> tuple[list[Task], int]:
    """Получение списка задач из базы."""
    query = session.query(Task).filter(Task.user_id == user_id)

    if title is not None:
        query = query.filter(Task.title.icontains(title))
    if task_status_id is not None:
        query = query.filter(Task.task_status_id == task_status_id)

    if load_related:
        query = query.options(joinedload(Task.task_status))

    if sort_fields is not None:
        if hasattr(Task, sort_fields) and sort_fields in ["id", "title", "task_status_id"]:
            if sort_order.lower() == "desc":
                query = query.order_by(getattr(Task, sort_fields).desc())
            else:
                query = query.order_by(getattr(Task, sort_fields))
        else:
            raise BadRequest(f"{sort_fields} недопустимое поле для сортировки")

    count = query.count()

    if limit is not None and limit <= MAX_AMOUNT_OF_TASKS:
        query = query.limit(limit)
    else:
        query = query.limit(MAX_AMOUNT_OF_TASKS)
    if offset is not None:
        query = query.offset(offset)

    return query.all(), count


def create_task_repo(session: Session, user_id: str, title: str, description: str, task_status_id: int) -> Task:
    """Создает задачу для пользователя в базе."""
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        task_status_id=task_status_id,
    )
    session.add(task)
    return task


def get_task_repo(session: Session, task_id: str | UUID, load_related: bool = False) -> Task | None:
    """Получение задачи по id."""
    query = session.query(Task).filter(Task.id == task_id)
    if load_related:
        query = query.options(joinedload(Task.task_status))
    return query.first()
