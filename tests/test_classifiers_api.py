from http import HTTPStatus

from app.models import TaskStatus


def test_classifier_task_status_api(client, db_session):
    """Проверяет апи классификатора статусов задач."""
    response = client.get("/api/v1/classifiers/task_status/")
    print(response.json)

    classifier_records_count = db_session.query(TaskStatus).count()
    assert response.status_code == HTTPStatus.OK, "Получен код ответа отличный от ожидаемого"
    assert len(response.json) == classifier_records_count, "Количество записей в ответе и в базе данных не совпадает"
