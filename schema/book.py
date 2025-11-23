from uuid import UUID

from schema import SchemaBase


class CategoryCreateSchema(SchemaBase):
    name: str
    description: str | None


class CategoryResponse(CategoryCreateSchema):
    id: UUID


class TagCreateSchema(SchemaBase):
    name: str


class TagResponseSchema(TagCreateSchema):
    id: UUID


class EBookCreateSchema(SchemaBase):
    title: str
    author: str
    description: str
    file_url: str
    cover_image: str | None
    category_id: UUID


class TagSchema(SchemaBase):
    id: UUID
    name: str


class EbookTagSchema(SchemaBase):
    tag: TagSchema


class BookmarkSchema(SchemaBase):
    id: UUID
    page_number: int


class EBookSchema(EBookCreateSchema):
    id: UUID
    tags: list[EbookTagSchema] = []
    bookmarks: list[BookmarkSchema] = []
