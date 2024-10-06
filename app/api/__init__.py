from flask_restx import Api

from app.api.tasks import ns as tasks_ns
from app.api.users import ns as users_ns

authorizations = {
    "jwt": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token",
    }
}

api = Api(
    title="API заметок",
    version="1.0",
    description="Апи для заметок на все случаи жизни",
    doc="/api/apidocs/",
    prefix="/api/v1",
    authorizations=authorizations,
)

api.add_namespace(users_ns, path="/users/")
api.add_namespace(tasks_ns, path="/tasks/")
