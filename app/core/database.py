from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.base import Base

from app.models.product import Product
from app.models.order import Order, OrderItem

# Используем асинхронный драйвер asyncpg
DATABASE_URL = settings.DATABASE_URL.replace("postgresql+psycopg2", "postgresql+asyncpg")

# Создание асинхронного подключения к базе данных
engine = create_async_engine(DATABASE_URL, echo=True)

# Асинхронная сессия
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Получение асинхронной сессии
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Импорт моделей внутри функции, чтобы избежать циклических импортов
def get_models():
    from app.models.product import Product
    from app.models.order import Order, OrderItem
    return Product, Order, OrderItem


