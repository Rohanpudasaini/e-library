from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.auth import get_current_user, login_for_access_token
from core.db import get_db
from core.exception import AUTHENTICATION_EXCEPTION
from models.user import User
from schema.user import (
    MessageResponse,
    PasswordUpdate,
    Token,
    UserCreate,
    UserSchema,
)

app = APIRouter()


@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    return login_for_access_token(form_data.username, form_data.password, db)


@app.get("/me")
def read_users_me(detail=Depends(get_current_user)):
    return detail


@app.get("/user", response_model=list[UserSchema] | UserSchema)
def get_user(id: UUID | None = None, db: Session = Depends(get_db)):
    return User.get(db=db, id=id)


@app.post("/user", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return User(**user.model_dump()).create(db=db)


@app.delete("/user")
def delete_user(data: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user: User = User.get(db=db, id=data["sub"])
    if user:
        _ = user.soft_delete(db=db)
        return MessageResponse(detail="User deleted successfully")
    return MessageResponse(detail="User not found")


@app.put("/user", response_model=UserSchema)
def change_password(
    password_data: PasswordUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user: User = User.get(db=db, id=current_user["sub"])
    if user:
        return user.update_password(
            old_password=password_data.old_password,
            new_password=password_data.new_password,
            db=db,
        )
    raise AUTHENTICATION_EXCEPTION
