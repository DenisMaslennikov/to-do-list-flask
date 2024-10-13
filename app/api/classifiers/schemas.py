from flask_restx import Model, fields

task_status_read_schema = Model(
    "TaskStatusReadSchema",
    {
        "id": fields.Integer(description="Идентификатор статуса"),
        "name": fields.String(description="Наименование статуса"),
    },
)
