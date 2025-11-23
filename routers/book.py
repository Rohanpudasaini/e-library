from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.auth.auth import get_current_user
from core.db import get_db
from core.exception import NotFound
from models.book import Bookmark, Category, EBook, EBookTag, Tag
from schema.book import (
    CategoryCreateSchema,
    CategoryResponse,
    EBookCreateSchema,
    EBookSchema,
    TagCreateSchema,
    TagResponseSchema,
)

app = APIRouter()


@app.get("/categories", response_model=list[CategoryResponse] | CategoryResponse)
def get_categories(id: UUID | None = None, db: Session = Depends(get_db)):
    return Category.get(db=db, id=id)


@app.post("/categories", response_model=CategoryResponse)
def create_category(category: CategoryCreateSchema, db: Session = Depends(get_db)):
    return Category(**category.model_dump()).create(db=db)


@app.get("/tags", response_model=list[TagResponseSchema] | TagResponseSchema)
def get_tags(id: UUID | None = None, db: Session = Depends(get_db)):
    return Tag.get(db=db, id=id)


@app.post("/tags", response_model=TagResponseSchema)
def create_tag(tag: TagCreateSchema, db: Session = Depends(get_db)):
    return Tag(**tag.model_dump()).create(db=db)


@app.get("/ebooks", response_model=list[EBookSchema] | EBookSchema)
def get_ebooks(id: UUID | None = None, db: Session = Depends(get_db)):
    return EBook.get(db=db, id=id)


@app.post("/ebooks", response_model=EBookSchema)
def create_ebook(ebook: EBookCreateSchema, db: Session = Depends(get_db)):
    return EBook(**ebook.model_dump()).create(db=db)


@app.put("/ebooks/tags/{ebook_id}", response_model=EBookSchema)
def add_tags_to_ebook(
    ebook_id: UUID,
    tag_ids: list[UUID],
    db: Session = Depends(get_db),
):
    book = EBook.get(db=db, id=ebook_id)
    if not book:
        raise NotFound(msg=f"EBook with id {ebook_id} not found")
    tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
    if len(tags) != len(tag_ids):
        missing_ids = set(tag_ids) - {tag.id for tag in tags}
        raise NotFound(msg=f"Tags not found: {missing_ids}")
    for tag in tags:
        _ = EBookTag(ebook_id=ebook_id, tag_id=tag.id).create(db=db)
    print(book.tags[0].tag.name)
    return book


@app.get("/user/bookmarks", response_model=list[EBookSchema])
def get_my_bookmarks(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = current_user["sub"]
    book = db.query(EBook).join(EBook.bookmarks).filter_by(user_id=user_id).all()
    return book


@app.post("/user/bookmarks/{ebook_id}", response_model=EBookSchema)
def add_bookmark(
    ebook_id: UUID,
    page_number: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = current_user["sub"]
    ebook = EBook.get(db=db, id=ebook_id)
    if not ebook:
        raise NotFound(msg=f"EBook with id {ebook_id} not found")
    bookmark = (
        db.query(ebook.bookmarks)
        .filter_by(user_id=user_id, page_number=page_number)
        .first()
    )
    if bookmark:
        return ebook
    _ = ebook.bookmarks.append(
        Bookmark(user_id=user_id, ebook_id=ebook_id, page_number=page_number)
    )
    db.commit()
    db.refresh(ebook)
    return ebook
