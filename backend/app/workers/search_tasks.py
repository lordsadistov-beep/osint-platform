from celery import Celery

from ..core.config import settings

celery_app = Celery("osint_platform", broker=settings.REDIS_URL, backend=settings.REDIS_URL)


@celery_app.task
def process_leak_import(file_path: str):
    pass
