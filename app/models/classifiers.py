from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import Task


class TaskStatus(Base):
    """Модель статуса задачи."""

    __tablename__ = "cl_task_status"
    id: Mapped[int] = mapped_column(primary_key=True, comment="Идентификатор")
    name: Mapped[str] = mapped_column(String(50), comment="Наименование статуса")

    tasks: Mapped[list["Task"]] = relationship(back_populates="task_status")
