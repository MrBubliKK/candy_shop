import os

class Settings:
    def __init__(self):
        # Инициализируем атрибуты с помощью self
        self.DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:1234@localhost:5432/candy_shop")
        self.REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", self.REDIS_URL)
        self.CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", self.REDIS_URL)

# Инициализация конфигурации
settings = Settings()
