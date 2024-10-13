from flask_restx import Namespace, Resource

from app.api.classifiers.schemas import task_status_read_schema
from app.api.classifiers.service import get_task_status_list

ns = Namespace("Справочники", "Апи справочников")

ns.models[task_status_read_schema.name] = task_status_read_schema


@ns.route("task_status/")
class TaskStatusListResource(Resource):
    """Класс для получения списка возможных статусов задач."""

    @ns.marshal_list_with(task_status_read_schema)
    def get(self):
        """Получение списка возможных статусов задач."""
        return get_task_status_list()
