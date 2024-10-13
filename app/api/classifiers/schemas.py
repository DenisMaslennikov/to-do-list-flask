from flask_restx import Model, fields

task_status = Model(
    "TaskStatus",
    {
        "id": fields.Integer(description="Идентификатор статуса"),
        "name": fields.String(description="Наименование статуса"),
    },
)
