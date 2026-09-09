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


class DownloanLinkSchemaOut(BaseModel):
    download_link: str


class UploadTestFileSchemaOut(BaseModel):
    s3_object_path: str


class DownloadTestFileSchemaOut(BaseModel):
    downloaded_file_path: str


class UploadUrlSchemaOut(BaseModel):
    url: str
    s3_object_path: str


class MessageResponseSchemaOut(BaseModel):
    message: str
