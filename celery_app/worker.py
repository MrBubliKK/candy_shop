from celery import Celery
from app.core.config import settings  # Импортируйте экземпляр settings

# Инициализация Celery
celery_app = Celery(
    "candy_shop",  # Название приложения
    broker=settings.REDIS_URL,  # Брокер (например, Redis)
    backend=settings.REDIS_URL,  # Бэкенд для хранения результатов задач
)

# Настройки Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",  # Укажите ваш часовой пояс
    enable_utc=True,
)

# Автоматическое обнаружение задач
celery_app.autodiscover_tasks(["app.tasks"])  # Укажите путь к вашим задачам
