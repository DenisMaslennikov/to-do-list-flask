from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import TaskStatus, User


class Task(Base):
    """Модель задачи."""

    __tablename__ = "tasks"
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        comment="Идентификатор",
    )
    title: Mapped[str] = mapped_column(String(255), comment="Заголовок задачи", index=True)
    description: Mapped[str] = mapped_column(comment="Описание задачи")
    task_status_id: Mapped[int] = mapped_column(
        ForeignKey("cl_task_status.id", ondelete="RESTRICT"),
        comment="Идентификатор статуса",
        index=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        comment="Идентификатор пользователя",
        index=True,
    )

    user: Mapped["User"] = relationship(back_populates="tasks")
    status: Mapped["TaskStatus"] = relationship(back_populates="tasks")

    @validates("title")
    def validate_title(self, key: str, title: str) -> str:
        """Валидация заголовка задачи."""
        if len(title) > 255:
            raise ValueError("Длинна заголовка задачи не может превышать 255 символов")
        if len(title) < 5:
            raise ValueError("Длинна заголовка задачи не может быть меньше 5 символов")
        return title
