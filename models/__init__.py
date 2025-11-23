from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, and_, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, Session, declarative_base, mapped_column

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

    @declared_attr
    def deleted_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            nullable=True,
            default=None,
            deferred=True,
            deferred_raiseload=True,
            deferred_group="timestamps",
        )

    @declared_attr
    def is_deleted(cls) -> Mapped[bool]:
        return mapped_column(
            Boolean,
            default=False,
            nullable=False,
            deferred=True,
            deferred_raiseload=True,
            deferred_group="status",
        )

    @declared_attr
    def is_active(cls) -> Mapped[bool]:
        return mapped_column(
            Boolean,
            default=True,
            nullable=False,
            deferred=True,
            deferred_raiseload=True,
            deferred_group="status",
        )

    def create(self, db):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self

    def update(self, db):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self

    def soft_delete(self, db: Session):
        self.is_deleted = True
        self.deleted_at = datetime.now(tz=timezone.utc)
        self.is_active = False  # Optional: You can choose to deactivate it
        return self.update(db)

    def hard_delete(self, db: Session):
        db.delete(self)
        db.commit()

    @classmethod
    def get(cls, db, id=None):
        if id is None:
            return (
                db.query(cls)
                .filter(and_(cls.is_deleted.is_(False), cls.is_active))
                .all()
            )
        return (
            db.query(cls)
            .filter(and_(cls.id == id, cls.is_deleted.is_(False), cls.is_active))
            .first()
        )


def load_models():
    base_dir = BASE_DIR / "models"
    for file in base_dir.glob("*.py"):
        if file.name != "__init__.py" and not file.name.startswith("_"):
            module_name = f"models.{file.stem}"
            __import__(module_name)


load_models()
