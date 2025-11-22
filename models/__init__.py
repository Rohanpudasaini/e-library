from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from config import BASE_DIR

initial_base = declarative_base()


# class Base(initial_base):
class Base(initial_base):
    __abstract__ = True

    # Generate __tablename__ automatically
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            deferred=True,
            deferred_raiseload=True,
            deferred_group="timestamps",
        )

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            deferred=True,
            deferred_raiseload=True,
            deferred_group="timestamps",
        )


def load_models():
    base_dir = BASE_DIR / "models"
    for file in base_dir.glob("*.py"):
        if file.name != "__init__.py" and not file.name.startswith("_"):
            module_name = f"models.{file.stem}"
            __import__(module_name)


load_models()
