from typing import Literal

from pydantic import BaseModel

CONTENT_TYPE_EXTENSIONS = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


class PresignedUploadRequest(BaseModel):
    filename: str
    content_type: Literal[
        "image/jpeg",
        "image/png",
        "image/webp",
    ]


class PresignedDownloadRequest(BaseModel):
    filename: str
