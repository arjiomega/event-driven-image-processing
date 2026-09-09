from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "worker",
    broker=settings.celery_broker_url,
)

celery_app.conf.update(
    task_ignore_result=True,
)

import app.tasks.image_processing  # noqa: F401
