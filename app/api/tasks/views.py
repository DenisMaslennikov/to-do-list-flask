from flask_restx import Namespace, Resource

from app.api.tasks.schemas import task_filter_parser, task_list_schema, paginated_task_list_schema
from app.api.tasks.service import get_task_list_for_user
from app.models import Task
from app.tools.jwt import token_required

ns = Namespace("Задачи", "Апи задач")

ns.models[task_list_schema.name] = task_list_schema
ns.models[paginated_task_list_schema.name] = paginated_task_list_schema


@ns.route("")
class TaskListResource(Resource):
    """Получение списка задач, создание задачи."""

    method_decorators = [token_required]

    @ns.marshal_with(paginated_task_list_schema)
    @ns.expect(task_filter_parser)
    @ns.doc(security="jwt")
    def get(self, current_user_id: str) -> list[Task]:
        """Получение списка задач пользователя."""
        kwargs = task_filter_parser.parse_args()
        return get_task_list_for_user(user_id=current_user_id, **kwargs)

    def post(self, current_user_id: str) -> Task:
        """Создание новой задачи."""
        return create_task(user_id=current_user_id, **ns.payload)
