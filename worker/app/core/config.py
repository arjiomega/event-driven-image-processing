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
    celery_result_backend: str = Field(
        ...,
        validation_alias="CELERY_RESULT_BACKEND",
    )

    s3_bucket_name: str = Field(
        ...,
        validation_alias="S3_BUCKET_NAME",
    )
    s3_public_endpoint: str = Field(
        ...,
        validation_alias="S3_PUBLIC_ENDPOINT",
    )
    s3_access_key: str = Field(
        ...,
        validation_alias="S3_ACCESS_KEY",
    )
    s3_secret_key: str = Field(
        ...,
        validation_alias="S3_SECRET_KEY",
    )
    s3_region: str = Field(
        ...,
        validation_alias="S3_REGION",
    )
    s3_require_tls: bool = Field(
        ...,
        validation_alias="S3_REQUIRE_TLS",
    )
    is_proxy_required: bool = Field(
        ...,
        validation_alias="IS_PROXY_REQUIRED",
    )
    s3_internal_endpoint: str = Field(
        ...,
        validation_alias="S3_INTERNAL_ENDPOINT",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]
