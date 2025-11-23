from uuid import UUID

from pydantic import EmailStr

from schema import SchemaBase


class Token(SchemaBase):
    access_token: str
    refresh_token: str


class MessageResponse(SchemaBase):
    detail: str


class UserSchema(SchemaBase):
    id: UUID
    email: EmailStr
    full_name: str | None


class UserCreate(SchemaBase):
    email: EmailStr
    password: str
    full_name: str | None


class PasswordUpdate(SchemaBase):
    old_password: str
    new_password: str
