from typing import Annotated

from fastapi import APIRouter, Depends

from app.services.s3.dependencies import get_s3_service
from app.services.s3.schemas import PresignedUploadRequest
from app.services.s3.service import S3Service

router = APIRouter(prefix="/media", tags=["media"])


@router.post(
    "/upload-url",
    # dependencies=[
    #     Depends(
    #         get_current_user,
    #     ),
    # ],
)
async def generate_presigned_upload_url(
    request: PresignedUploadRequest,
    s3_service: Annotated[
        S3Service,
        Depends(get_s3_service),
    ],
):

    object_path = f"raw-uploads/{request.filename}"

    presigned_url, storage_key = s3_service.generate_presigned_upload_url(
        storage_key=object_path,
    )

    return {
        "url": presigned_url,
        "storage_key": storage_key,
    }
