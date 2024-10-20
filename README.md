# API Задач
Небольшой проект для отработки навыков построения API с нуля на Flask-RESTx + SQLAlchemy. 
C последующим покрытием тестами и CI/CD посредством github action.

## Как запустить проект 
- Для запуска требуется установленный docker compose

## Development версия
- Клонировать репозиторий 
```bash 
git clone https://github.com/DenisMaslennikov/to-do-list-flask.git
```
- Настроить переменные окружения в папке **config** в файле **.env** используя в качестве шаблона файл **.env.template** в тойже папке.
- Запустить контейнеры. 
```bash 
docker compose up --build
```
- После запуска всех контейнеров документация Swagger будет доступна по ссылке  http://127.0.0.1:5000/api/apidocs/

## Запуск тестов
- Клонировать репозиторий 
```bash 
git clone https://github.com/DenisMaslennikov/to-do-list-flask.git
```
- Настроить переменные окружения в папке **config** в файле **.env** используя в качестве шаблона файл **.env.template** в тойже папке.
- Запустить тесты командой 
```bash
docker compose -p to-do-list-flask-pytest -f docker-compose-pytest.yml run --build -e PYTHONPATH=./app --rm api pytest
```
- После тестов можно удалить все созданные контейнеры
```bash
docker compose -p to-do-list-flask-pytest -f docker-compose-pytest.yml down -v
```

## Запуск production версии
- Скопировать из репозитория файл **docker-compose.prod.yml**
- Настроить переменные окружения в папке **config** в файле **.env** используя в качестве шаблона файл **.env.template** из папки **config** репозитория.
- Запустить контейнеры. 
```bash 
docker compose -f docker-compose.prod.yml up --build
```
