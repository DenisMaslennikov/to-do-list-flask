from alembic import command
from alembic.config import Config as AlembicConfig
from app import get_app
from config import DevelopmentConfig

app = get_app(DevelopmentConfig)

if __name__ == "__main__":
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", app.config.get("DATABASE_URI"))

    command.upgrade(alembic_cfg, "head")

    # Запуск сервера
    app.run(host="0.0.0.0", port=5000, use_debugger=True, use_reloader=True, passthrough_errors=True)
