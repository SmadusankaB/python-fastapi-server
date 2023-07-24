from celery import Celery
from server.config import settings

# Create celery instance to send task
# and run celery workers
celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include="server.jobs.tasks",
)
