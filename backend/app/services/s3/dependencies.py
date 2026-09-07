from fastapi import Request

from .service import S3Service


def get_s3_service(request: Request) -> S3Service:
    return request.app.state.s3_service
