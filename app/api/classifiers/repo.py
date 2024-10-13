from sqlalchemy.orm import Session

from app.models import TaskStatus


def get_task_status_list_repo(session: Session) -> list[TaskStatus]:
    """Получение списка статусов задач из базы."""
    return session.query(TaskStatus).all()
