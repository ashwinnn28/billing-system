from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    app_version: str
    debug: bool

    host: str
    port: int

    database_url: str

    secret_key: str = "billing-secret-key"
    access_token_expire_minutes: int = 60

    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    email_from: str
    admin_email: str = "admin@test.com"
    admin_password: str = "admin123"

    @field_validator("*", mode="before")
    def strip_whitespace(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()