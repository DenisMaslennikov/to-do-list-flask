FROM python:3.12

ENV TZ=Europe/Moscow \
  # python:
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  # poetry:
  POETRY_VERSION=1.8.3 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
  # Установка менеджера пакетов `poetry`:
  # https://github.com/python-poetry/poetry
  && curl -sSL 'https://install.python-poetry.org' | python - \
  && poetry --version

WORKDIR /src

# Копировать только requirements, чтобы кэшировать их в слое docker
COPY ./poetry.lock ./pyproject.toml /src/

RUN --mount=type=cache,target="$POETRY_CACHE_DIR" \
  poetry version \
  && poetry run pip install -U pip \
  && poetry install --no-interaction --no-ansi

# Ставим wait-for-it https://github.com/vishnubob/wait-for-it
COPY ./docker/utils/wait-for-it.sh /wait-for-it.sh

COPY ./docker/utils/entrypoint.sh /docker-entrypoint.sh

# Установка соответствующих разрешений:
RUN chmod +x '/wait-for-it.sh' \
  && chmod +x '/docker-entrypoint.sh' \
  # Замена разделителя строк CRLF на LF для пользователей Windows:
  && sed -i 's/\r$//g' '/docker-entrypoint.sh' \
  && sed -i 's/\r$//g' '/wait-for-it.sh'

ENTRYPOINT ["/docker-entrypoint.sh"]
