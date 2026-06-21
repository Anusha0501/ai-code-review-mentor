from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ai-code-review-mentor"
    environment: str = "local"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/mentor"
    github_webhook_secret: str = "change-me"
    github_token: str = ""
    anthropic_api_key: str = ""
    langsmith_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
