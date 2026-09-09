import io
from datetime import timedelta

from minio import Minio, S3Error
from pydantic import BaseModel
from urllib3 import ProxyManager

from app.core.config import get_settings

from .exceptions import S3ObjectDoesntExistException

settings = get_settings()


class S3ServiceSettings(BaseModel):
    S3_BUCKET_NAME: str = settings.s3_bucket_name
    S3_ENDPOINT: str = settings.s3_public_endpoint
    S3_ACCESS_KEY: str = settings.s3_access_key
    S3_SECRET_KEY: str = settings.s3_secret_key
    S3_REGION: str = settings.s3_region
    S3_REQUIRE_TLS: bool = settings.s3_require_tls
    IS_PROXY_REQUIRED: bool = settings.is_proxy_required
    S3_INTERNAL_URL: str = settings.s3_internal_endpoint


class S3Service:
    def __init__(
        self,
        storage_configuration: S3ServiceSettings | None = None,
    ):
        self.storage_configuration = (
            storage_configuration
            if storage_configuration is not None
            else S3ServiceSettings()
        )

        self.minio_client = Minio(
            self.storage_configuration.S3_ENDPOINT,
            access_key=self.storage_configuration.S3_ACCESS_KEY,
            secret_key=self.storage_configuration.S3_SECRET_KEY,
            region=self.storage_configuration.S3_REGION,
            secure=self.storage_configuration.S3_REQUIRE_TLS,
            http_client=ProxyManager(self.storage_configuration.S3_INTERNAL_URL)
            if self.storage_configuration.IS_PROXY_REQUIRED
            else None,
        )

    def __validate_object_existance(
        self,
        s3_object_path: str,
        bucket_name: str | None = None,
    ) -> None:
        bucket_name = (
            bucket_name if bucket_name else self.storage_configuration.S3_BUCKET_NAME
        )
        try:
            self.minio_client.stat_object(bucket_name, s3_object_path)
        except S3Error as e:
            if e.code == "NoSuchKey":
                raise S3ObjectDoesntExistException(
                    f"The S3 object with path='{s3_object_path}' does not exist in the bucket."
                ) from e
            raise

    def remove_digital_object(self, s3_object_path: str) -> None:

        self.__validate_object_existance(s3_object_path=s3_object_path)
        self.minio_client.remove_object(
            self.storage_configuration.S3_BUCKET_NAME, s3_object_path
        )

    def generate_presigned_download_url(
        self,
        storage_key: str,
        expiration_minutes: int = 60,
    ) -> str:
        self.__validate_object_existance(s3_object_path=storage_key)

        try:
            return self.minio_client.presigned_get_object(
                bucket_name=self.storage_configuration.S3_BUCKET_NAME,
                object_name=storage_key,
                expires=timedelta(minutes=expiration_minutes),
            )
        except Exception as e:
            raise RuntimeError(f"Failed to generate download link: {e!s}") from e

    def generate_presigned_upload_url(
        self, storage_key: str, expiration_minutes: int = 360
    ) -> tuple[str, str]:

        try:
            presigned_url = self.minio_client.presigned_put_object(
                bucket_name=self.storage_configuration.S3_BUCKET_NAME,
                object_name=storage_key,
                expires=timedelta(minutes=expiration_minutes),
            )
            return presigned_url, storage_key
        except Exception as e:
            raise RuntimeError(f"Failed to generate pre-signed URL: {e!s}") from e

    def download_object(
        self,
        storage_key: str,
        bucket_name: str | None = None,
    ) -> bytes:
        bucket_name = (
            bucket_name if bucket_name else self.storage_configuration.S3_BUCKET_NAME
        )

        self.__validate_object_existance(
            s3_object_path=storage_key,
            bucket_name=bucket_name,
        )
        response = None
        try:
            response = self.minio_client.get_object(
                bucket_name,
                storage_key,
            )
            return response.read()
        except S3Error as e:
            raise RuntimeError(f"Failed to download object: {e!s}") from e
        finally:
            if response is not None:
                response.close()
                response.release_conn()

    def upload_object(
        self,
        storage_key: str,
        data: bytes,
        bucket_name: str | None = None,
        content_type: str = "application/octet-stream",
    ) -> str:
        bucket_name = (
            bucket_name if bucket_name else self.storage_configuration.S3_BUCKET_NAME
        )
        try:
            self.minio_client.put_object(
                bucket_name=bucket_name,
                object_name=storage_key,
                data=io.BytesIO(data),
                length=len(data),
                content_type=content_type,
            )
            return storage_key
        except S3Error as e:
            raise RuntimeError(f"Failed to upload object: {e!s}") from e
