from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:
    """Класс базового объекта для моделей."""

    @declared_attr
    def __table_args__(cls):
        if "__table_args__" not in cls.__dict__:
            cls.__table_args__ = {}
        cls.__table_args__["comment"] = cls.__doc__
        return cls.__table_args__
