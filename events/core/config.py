from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    celery_broker_url: str = Field(
        ...,
        validation_alias="CELERY_BROKER_URL",
    )
    amqp_host: str = Field(
        ...,
        validation_alias="AMQP_HOST",
    )
    amqp_exchange: str = Field(
        ...,
        validation_alias="AMQP_EXCHANGE",
    )
    amqp_exchange_type: str = Field(
        ...,
        validation_alias="AMQP_EXCHANGE_TYPE",
    )
    amqp_queue: str = Field(
        ...,
        validation_alias="AMQP_QUEUE",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]
