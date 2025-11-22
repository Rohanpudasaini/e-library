from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base

if TYPE_CHECKING:
    from models.user import User, UserReadingSession


class EBook(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    author: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(500))
    file_url: Mapped[str] = mapped_column(String(500))
    cover_image: Mapped[str | None] = mapped_column(String(500))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship(back_populates="ebooks")
    tags: Mapped[list["EBookTag"]] = relationship(back_populates="ebook")

    bookmarks: Mapped[list["Bookmark"]] = relationship(back_populates="ebook")
    notes: Mapped[list["Note"]] = relationship(back_populates="ebook")
    sessions: Mapped[list["UserReadingSession"]] = relationship(back_populates="ebook")


class Category(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    ebooks: Mapped[list["EBook"]] = relationship(back_populates="category")


class Tag(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    ebook_tags: Mapped[list["EBookTag"]] = relationship(back_populates="tag")


class EBookTag(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ebook_id: Mapped[int] = mapped_column(ForeignKey("ebook.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id"))

    ebook: Mapped["EBook"] = relationship(back_populates="tags")
    tag: Mapped["Tag"] = relationship(back_populates="ebook_tags")


class Bookmark(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    ebook_id: Mapped[int] = mapped_column(ForeignKey("ebook.id"))
    page_number: Mapped[int] = mapped_column(Integer)
    user: Mapped["User"] = relationship(back_populates="bookmarks")
    ebook: Mapped["EBook"] = relationship(back_populates="bookmarks")


class Note(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    ebook_id: Mapped[int] = mapped_column(ForeignKey("ebook.id"))
    page_number: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(String(1000))

    user: Mapped["User"] = relationship(back_populates="notes")
    ebook: Mapped["EBook"] = relationship(back_populates="notes")
