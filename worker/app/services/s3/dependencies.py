from functools import lru_cache

from .service import S3Service


@lru_cache
def get_s3_service() -> S3Service:
    return S3Service()
