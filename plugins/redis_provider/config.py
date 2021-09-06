

from typing import Optional

from pydantic import BaseSettings, validator


class Config(BaseSettings):
    redis_host: str
    redis_port: int
    redis_db: int = 0
    redis_password: Optional[str] = None
    redis_username: Optional[str] = None

    class Config:
        extra = "ignore"

    @validator("redis_db", pre=True)
    def replace_empty_str(cls, value):
        return value or 0
