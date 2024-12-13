from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, select
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from app.core.base import Base
from app.models.product import Product
from app.schemas.order import OrderCreate


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pending")  # Статус заказа: pending, completed, canceled
    total_price = Column(Float, nullable=False)  # Общая стоимость заказа
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Время создания
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # Время обновления

    # Связь с элементами заказа
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    @classmethod
    async def create(cls, db: AsyncSession, order_data: OrderCreate):
        """Создаёт заказ с элементами заказа."""
        total_price = sum(item.quantity * item.price_per_item for item in order_data.items)
        order = cls(status=order_data.status, total_price=total_price)
        db.add(order)
        await db.commit()
        await db.refresh(order)

        for item in order_data.items:
            product = await db.get(Product, item.product_id)
            if not product:
                raise ValueError(f"Product with id {item.product_id} not found")
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_per_item=item.price_per_item,
            )
            db.add(order_item)

        await db.commit()
        await db.refresh(order)
        return order

    @classmethod
    async def get_by_id(cls, db: AsyncSession, order_id: int):
        """Возвращает заказ по ID."""
        result = await db.execute(
            select(cls).filter(cls.id == order_id)
        )
        return result.scalars().first()

    @classmethod
    async def get_all(cls, db: AsyncSession, skip: int = 0, limit: int = 10):
        """Возвращает список заказов с пагинацией."""
        result = await db.execute(
            select(cls).offset(skip).limit(limit)
        )
        return result.scalars().all()

    @classmethod
    async def update_status(cls, db: AsyncSession, order_id: int, status: str):
        """Обновляет статус заказа."""
        result = await db.execute(
            select(cls).filter(cls.id == order_id)
        )
        order = result.scalars().first()
        if not order:
            return None
        order.status = status
        await db.commit()
        await db.refresh(order)
        return order

    @classmethod
    async def delete(cls, db: AsyncSession, order_id: int) -> bool:
        """Удаляет заказ."""
        result = await db.execute(
            select(cls).filter(cls.id == order_id)
        )
        order = result.scalars().first()
        if not order:
            return False
        await db.delete(order)
        await db.commit()
        return True


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))  # Ссылка на заказ
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))  # Ссылка на продукт
    quantity = Column(Integer, nullable=False)  # Количество продукта в заказе
    price_per_item = Column(Float, nullable=False)  # Цена за единицу продукта

    # Связь с заказом и продуктом
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
