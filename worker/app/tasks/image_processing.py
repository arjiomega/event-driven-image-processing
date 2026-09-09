import time
from pathlib import Path

import cv2
import numpy as np

from app.celery_app import celery_app
from app.services.s3.dependencies import get_s3_service

EXTENSION_CONTENT_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}

PROCESSING_DELAY_SECONDS = 5


@celery_app.task(
    name="worker.tasks.image_processing.process_image",
    bind=True,
    max_retries=3,
)
def process_image(self, storage_key: str, bucket: str):
    s3 = get_s3_service()

    # download
    image_bytes = s3.download_object(storage_key, bucket_name=bucket)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError(f"Failed to decode image at storage_key={storage_key}")

    time.sleep(PROCESSING_DELAY_SECONDS)

    # --- your actual OpenCV processing goes here ---
    processed = cv2.GaussianBlur(src=img, ksize=(51, 51), sigmaX=0)  # placeholder

    h, w = processed.shape[:2]
    text = "PROCESSED"
    font = cv2.FONT_HERSHEY_SIMPLEX
    thickness = max(2, w // 200)

    font_scale = 1
    (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
    font_scale = (w * 0.8) / text_w

    (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
    x = (w - text_w) // 2
    y = (h + text_h) // 2  # roughly vertically centered

    cv2.putText(
        processed, text, (x, y), font, font_scale, (0, 0, 255), thickness, cv2.LINE_AA
    )

    extension = Path(storage_key).suffix.lower()
    content_type = EXTENSION_CONTENT_TYPES.get(extension, "image/jpeg")

    # encode + upload result
    success, buffer = cv2.imencode(extension, processed)
    if not success:
        raise ValueError("Failed to encode processed image")

    s3.upload_object(
        bucket_name="processed-output",
        storage_key=storage_key,
        data=buffer.tobytes(),
        content_type=content_type,
    )

    return {"output_key": storage_key, "status": "completed"}
