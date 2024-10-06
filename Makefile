CONTAINER_NAME = api

start: ## Запустить dev версию задачь
	docker compose up --build

bash: ## Открыть оболочку bash в контейнере 'api'
	docker compose exec $(CONTAINER_NAME) bash

drop: ## Остановить и удалить контейнеры Docker
	docker compose down -v

lock: ## Обновить зависимости проекта с использованием poetry
	docker compose run --build --user=root --rm $(CONTAINER_NAME) poetry lock

migrations:  ## Создать миграции make migrations MSG="Добавить новую таблицу users"
	docker compose --env-file config/.env run --user=root --rm $(CONTAINER_NAME) python alembic_autogenerate.py "$(MSG)"
