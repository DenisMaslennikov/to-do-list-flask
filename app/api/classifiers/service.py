from app.api.classifiers.repo import get_task_status_list_repo
from app.models import TaskStatus
from app.tools.session import session_scope


def get_task_status_list() -> list[TaskStatus]:
    """Получение списка статусо задач."""
    with session_scope() as session:
        return get_task_status_list_repo(session)
