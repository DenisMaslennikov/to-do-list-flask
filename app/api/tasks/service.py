from app.api.tasks.repo import get_task_list_for_user_repo, create_task_repo, get_task_repo
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


def create_task(user_id: str, title: str, description: str, task_status_id: int) -> Task:
    """Создаёт задачу для пользователя."""
    with session_scope() as session:
        task = create_task_repo(
            session,
            user_id=user_id,
            title=title,
            description=description,
            task_status_id=task_status_id,
        )
        session.flush()
        task = get_task_repo(session, task_id=task.id, load_related=True)
        return task
