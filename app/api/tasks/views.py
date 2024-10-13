from http import HTTPStatus
from uuid import UUID

from flask_restx import Namespace, Resource

from app.api.tasks.schemas import (
    paginated_task_list_schema,
    task_filter_parser,
    task_list_schema,
    task_read_schema,
    task_write_schema,
)
from app.api.tasks.service import create_task, get_task_list_for_user, get_task_by_id
from app.models import Task
from app.tools.jwt import token_required

ns = Namespace("Задачи", "Апи задач")

ns.models[task_list_schema.name] = task_list_schema
ns.models[paginated_task_list_schema.name] = paginated_task_list_schema
ns.models[task_write_schema.name] = task_write_schema
ns.models[task_read_schema.name] = task_read_schema


@ns.route("")
class TaskListResource(Resource):
    """Получение списка задач, создание задачи."""

    method_decorators = [token_required]

    @ns.marshal_with(paginated_task_list_schema)
    @ns.expect(task_filter_parser)
    @ns.doc(security="jwt")
    def get(self, current_user_id: UUID) -> dict[str, list[Task] | int]:
        """Получение списка задач пользователя."""
        kwargs = task_filter_parser.parse_args()
        return get_task_list_for_user(user_id=current_user_id, **kwargs)

    @ns.expect(task_write_schema)
    @ns.marshal_with(task_read_schema, code=HTTPStatus.CREATED)
    @ns.doc(security="jwt")
    def post(self, current_user_id: UUID) -> tuple[Task, int]:
        """Создание новой задачи."""
        return create_task(user_id=current_user_id, **ns.payload), HTTPStatus.CREATED


@ns.route("<uuid:task_id>")
class TaskResource(Resource):
    """Работа с конкретной задачей, получение, обновление, удаление."""

    method_decorators = [token_required]

    @ns.marshal_with(task_read_schema)
    @ns.doc(security="jwt")
    def get(self, current_user_id: UUID, task_id: UUID) -> Task:
        """Получение задачи по id."""
        return get_task_by_id(user_id=current_user_id, task_id=task_id)

    @ns.expect(task_write_schema)
    @ns.marshal_with(task_read_schema)
    @ns.doc(security="jwt")
    def put(self, current_user_id: UUID, task_id: UUID) -> Task:
        """Полное обновление задачи."""
        return uodate_task(user_id=current_user_id, task_id=task_id, **ns.payload)
