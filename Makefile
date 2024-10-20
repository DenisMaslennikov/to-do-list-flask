CONTAINER_NAME = api

start: ## Запустить dev версию задач
	docker compose up --build

prod:
	docker compose -f docker-compose.prod.yml up --build

bash: ## Открыть оболочку bash в контейнере 'api'
	docker compose exec $(CONTAINER_NAME) bash

drop: ## Остановить и удалить контейнеры Docker
	docker compose down -v

lock: ## Обновить зависимости проекта с использованием poetry
	docker compose run --build --user=root --rm $(CONTAINER_NAME) poetry lock

migrations:  ## Создать миграции make migrations MSG="Добавить новую таблицу users"
	docker compose --env-file config/.env run --user=root --rm $(CONTAINER_NAME) python alembic_autogenerate.py "$(MSG)"

test: pytest

pytest: ## Выполняем тесты на pytest с запуском чистой базы и её удалением после тестов, для запуска определённых тестов: make pytest ARGS="--cov=app tests/test_migrations.py"
	docker compose -p to-do-list-flask-pytest -f docker-compose-pytest.yml run --build -e PYTHONPATH=./app --rm $(CONTAINER_NAME) pytest $(ARGS) && docker compose -p to-do-list-flask-pytest -f docker-compose-pytest.yml down -v || \
	( \
        docker compose -p to-do-list-flask-pytest -f docker-compose-pytest.yml down -v && exit 1 \
    )
