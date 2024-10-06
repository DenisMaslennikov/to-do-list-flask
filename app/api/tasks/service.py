from app.api.tasks.repo import get_task_list_for_user_repo
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
            user_id,
            title,
            task_status_id,
            sort_fields,
            sort_order,
            limit,
            offset,
        )
        return {"results": results, "count": count}
