from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Security
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError as JWTError
from sqlalchemy.orm import Session

from core.auth.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    create_refresh_token,
    pwd_context,
)
from core.exception import (
    AUTHENTICATION_EXCEPTION,
    AuthenticationError,
)
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.email == username, User.is_active)
    user = user.first()
    if not user or not pwd_context.verify(password, user.password):
        raise AUTHENTICATION_EXCEPTION
    return user


def login_for_access_token(username: str, password: str, db: Session):
    user = authenticate_user(username, password, db)
    access_token = create_access_token(data={"sub": str(user.id)})
    # Create refresh token
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    return access_token, refresh_token


#
def get_current_user(authorization: str = Security(oauth2_scheme)):
    """Extract user data from JWT token provided in Authorization header."""
    if not authorization:
        raise AuthenticationError("AuthenticationError", msg="Missing or invalid token")

    # Extract token
    try:
        payload = jwt.decode(authorization, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Expected to return user info, like role and permissions
    except JWTError:
        raise AuthenticationError("AuthenticationError", msg="Invalid or expired token")
