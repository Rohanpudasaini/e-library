import os
from functools import lru_cache
from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


@lru_cache
def get_env_path() -> Path:
    """Get environment file path with config mount support."""
    config_path = Path(os.environ.get("CONFIG_MOUNT_PATH", ".env"))
    return config_path if config_path.exists() else Path(".env")


class BaseSettings(PydanticBaseSettings):
    # Creating singleton instance of settings class
    log_exceptions: bool = False
    _instance = None

    def __init_subclass__(cls) -> None:
        cls._instance = None
        super().__init_subclass__()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def validate(cls, value):
        cls._instance = super().model_validate(value)
        return cls._instance

    model_config = SettingsConfigDict(
        env_file=str(get_env_path()),
        extra="ignore",
    )


class AuthTokenConfig(BaseSettings):
    user_access_token_expiry_minutes: int = 1440  # 24 hours
    secret_key: str
    refresh_secret_key: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    algorithm: str


class DBConfig(BaseSettings):
    database_url: PostgresDsn
    pool_size: int = 500
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 3600
    pool_pre_ping: bool = True


authconfig = AuthTokenConfig()  # type: ignore
db_config = DBConfig()  # type: ignore
