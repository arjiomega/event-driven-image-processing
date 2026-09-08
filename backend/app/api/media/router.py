from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.services.s3.dependencies import get_s3_service
from app.services.s3.schemas import PresignedDownloadRequest, PresignedUploadRequest
from app.services.s3.service import S3Service

router = APIRouter(prefix="/media", tags=["media"])


@router.post("/upload-url")
async def generate_presigned_upload_url(
    request: PresignedUploadRequest,
    s3_service: Annotated[
        S3Service,
        Depends(get_s3_service),
    ],
):

    object_path = f"{request.filename}"

    presigned_url, storage_key = s3_service.generate_presigned_upload_url(
        storage_key=object_path,
    )

    return {
        "url": presigned_url,
        "storage_key": storage_key,
    }


@router.post(
    "/download-url",
    status_code=status.HTTP_200_OK,
)
async def generate_presigned_download_url(
    request: PresignedDownloadRequest,
    s3_service: Annotated[
        S3Service,
        Depends(get_s3_service),
    ],
):
    presigned_url = s3_service.generate_presigned_download_url(
        bucket_name="processed-output",
        storage_key=request.filename,
    )

    if presigned_url is None:
        raise HTTPException(status_code=404, detail="Object not ready yet")

    return {
        "url": presigned_url,
    }
