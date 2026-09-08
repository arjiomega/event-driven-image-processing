from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

# celery_app.autodiscover_tasks(["app.tasks"], related_name="image_processing")
import app.tasks.image_processing  # noqa: F401
