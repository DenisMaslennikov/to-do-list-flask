import re

# Регулярное выражение для проверки валидности email
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

# Регулярное выражение для проверки имени пользователя
USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+$")

# Максимально возможное количество задач для запроса на получение списка задач
MAX_AMOUNT_OF_TASKS_TO_DISPLAY = 1000

# Идентификатор статуса задачи "Не выполнено"
NOT_COMPLETED_TASK_STATUS_ID = 1
# Идентификатор статуса задачи "Выполнено"
COMPLETED_TASK_STATUS_ID = 2
