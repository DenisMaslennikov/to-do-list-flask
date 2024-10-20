# API Задач
Небольшой проект для отработки навыков построения API с нуля на Flask-RESTx + SQLAlchemy. 
C последующим покрытием тестами и CI/CD посредством github action.

## Как запустить проект (dev версия)
- Для запуска требуется установленный docker compose
- Клонировать репозиторий 
```bash 
- git clone https://github.com/DenisMaslennikov/to-do-list-flask.git
```
- Настроить переменные окружения в папке **config** в файле **.env** используя в качестве шаблона файл **.env.template**
- Запустить контейнеры 
```bash 
docker compose up --build
```
- После запуска всех контейнеров документация Swagger будет доступна по ссылке  http://127.0.0.1:5000/api/apidocs/

