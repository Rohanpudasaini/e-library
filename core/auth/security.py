import datetime

import bcrypt
import jwt

from config import auth_config

# from src.lib.config import auth_config

# Generate a secure key using: openssl rand -hex 32
SECRET_KEY = auth_config.secret_key
REFRESH_SECRET_KEY = auth_config.refresh_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = auth_config.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = auth_config.refresh_token_expire_minutes


class CryptContext:
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    def hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


pwd_context = CryptContext()


def verify_password(plain_password, hashed_password):
    # if plain_password == hashed_password:
    #     return True
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_refresh_token(
    data: dict,
    expires_delta: datetime.timedelta = datetime.timedelta(
        minutes=REFRESH_TOKEN_EXPIRE_MINUTES
    ),
):
    to_encode = data.copy()
    expire = datetime.datetime.now(tz=datetime.timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
