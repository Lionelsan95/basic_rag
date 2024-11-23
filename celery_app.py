from celery import Celery

# Configure Celery with Redis as the broker
celery_app = Celery(
    "basic_rag",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

# Task serialization settings
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)
