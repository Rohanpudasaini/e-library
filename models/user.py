from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid_extensions import uuid7

from core.auth.security import get_password_hash, verify_password
from core.exception import AUTHENTICATION_EXCEPTION
from models import Base

if TYPE_CHECKING:
    from models.book import Bookmark, EBook, Note


class User(Base):
    id: Mapped[UUID] = mapped_column(default=uuid7, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str | None] = mapped_column(String(255))
    profile: Mapped["UserProfile"] = relationship(back_populates="user", uselist=False)
    bookmarks: Mapped[list["Bookmark"]] = relationship(back_populates="user")
    notes: Mapped[list["Note"]] = relationship(back_populates="user")
    reading_sessions: Mapped[list["UserReadingSession"]] = relationship(
        back_populates="user"
    )

    def create(self, db):
        self.password = get_password_hash(self.password)
        return super().create(db)

    def update_password(self, old_password: str, new_password: str, db):
        if not verify_password(old_password, self.password):
            raise AUTHENTICATION_EXCEPTION
        self.password = get_password_hash(new_password)
        return super().update(db)


class UserProfile(Base):
    id: Mapped[UUID] = mapped_column(default=uuid7, primary_key=True, index=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), unique=True)
    dark_mode: Mapped[bool] = mapped_column(Boolean, default=False)
    preferences: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    user: Mapped["User"] = relationship(back_populates="profile")


class UserReadingSession(Base):
    id: Mapped[UUID] = mapped_column(default=uuid7, primary_key=True, index=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    ebook_id: Mapped[UUID] = mapped_column(ForeignKey("ebook.id"))
    last_page: Mapped[int] = mapped_column(Integer)

    user: Mapped["User"] = relationship(back_populates="reading_sessions")
    ebook: Mapped["EBook"] = relationship(back_populates="sessions")
