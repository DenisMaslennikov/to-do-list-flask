from flask_restx import Model, fields
from flask_restx.reqparse import Argument, RequestParser

task_list_schema = Model(
    "TaskListSchema",
    {
        "id": fields.String(description="Идентификатор задачи"),
        "title": fields.String(description="Заголовок задачи"),
        "task_status": fields.String(description="Статус задачи"),
    },
)

paginated_task_list_schema = Model(
    "PaginatedTaskListSchema",
    {
        "count": fields.Integer(description="Количество записей всего"),
        "results": fields.List(fields.Nested(task_list_schema), description="Список задач"),
    },
)

task_filter_parser = RequestParser()
task_filter_parser.add_argument(Argument(name="title", type=str, help="Поиск по заголовку"))
task_filter_parser.add_argument(Argument(name="task_status_id", type=int, help="Фильтр по id статуса"))
task_filter_parser.add_argument(Argument(name="sort_fields", type=str, help="Поле для сортировки"))
task_filter_parser.add_argument(
    Argument(
        name="sort_order",
        type=str,
        choices=["asc", "desc"],
        help="Порядок сортировки",
    )
)
task_filter_parser.add_argument(Argument(name="limit", type=int, help="Максимальное кол-во записей"))
task_filter_parser.add_argument(Argument(name="offset", type=int, help="Смещение"))

task_write_schema = Model(
    "TaskWriteSchema",
    {
        "id": fields.String(description="Идентификатор задачи"),
        "title": fields.String(description="Заголовок задачи"),
        "description": fields.String(description="Описание задачи"),
        "task_status": fields.String(description="Статус задачи"),
    },
)
