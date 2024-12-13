from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, select
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from app.core.base import Base
from app.schemas.product import ProductCreate


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связь с заказами
    order_items = relationship("OrderItem", back_populates="product")

    @classmethod
    async def create(cls, db: AsyncSession, product_data: ProductCreate):
        """Создаёт продукт."""
        product = cls(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            is_available=product_data.is_available,
        )
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product

    @classmethod
    async def get_by_id(cls, db: AsyncSession, product_id: int):
        """Возвращает продукт по ID."""
        result = await db.execute(
            select(cls).filter(cls.id == product_id)
        )
        return result.scalars().first()

    @classmethod
    async def get_all(cls, db: AsyncSession, skip: int = 0, limit: int = 10):
        """Возвращает список продуктов с пагинацией."""
        result = await db.execute(
            select(cls).offset(skip).limit(limit)
        )
        return result.scalars().all()

    @classmethod
    async def update(cls, db: AsyncSession, product_id: int, product_data: ProductCreate):
        """Обновляет информацию о продукте."""
        result = await db.execute(
            select(cls).filter(cls.id == product_id)
        )
        product = result.scalars().first()
        if not product:
            return None
        product.name = product_data.name
        product.description = product_data.description
        product.price = product_data.price
        product.is_available = product_data.is_available
        await db.commit()
        await db.refresh(product)
        return product

    @classmethod
    async def delete(cls, db: AsyncSession, product_id: int) -> bool:
        """Удаляет продукт."""
        result = await db.execute(
            select(cls).filter(cls.id == product_id)
        )
        product = result.scalars().first()
        if not product:
            return False
        await db.delete(product)
        await db.commit()
        return True
