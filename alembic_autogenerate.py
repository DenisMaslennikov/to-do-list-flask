import sys

from alembic import command
from alembic.config import Config as AlembicConfig
from config import BaseConfig

if len(sys.argv) != 2:
    print("Использование: python alembic_autogenerate.py <сообщение>")
    sys.exit(1)

message = sys.argv[1]

# Убедитесь, что ваш путь к конфигурации Alembic (обычно это alembic.ini) правильно указан
alembic_cfg = AlembicConfig("alembic.ini")
alembic_cfg.set_main_option("sqlalchemy.url", BaseConfig.DATABASE_URI)

command.upgrade(alembic_cfg, "head")

# Создание новой ревизии с автогенерацией
command.revision(alembic_cfg, message=message, autogenerate=True)
