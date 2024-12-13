from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.order import *
from app.models.order import Order
from app.core.database import get_db  # Импортируем асинхронную зависимость

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

# Зависимость для получения асинхронной сессии БД
# Используем асинхронную функцию get_db, которую вы уже создали в database.py

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate, db: AsyncSession = Depends(get_db)):
    """Создание нового заказа."""
    try:
        order = await Order.create(db=db, order_data=order_data)
        return order
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def read_order(order_id: int, db: AsyncSession = Depends(get_db)):
    """Получение заказа по ID."""
    order = await Order.get_by_id(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

@router.get("/", response_model=list[OrderResponse], status_code=status.HTTP_200_OK)
async def read_orders(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """Получение списка заказов с пагинацией."""
    return await Order.get_all(db=db, skip=skip, limit=limit)

@router.put("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def update_order(order_id: int, status: str, db: AsyncSession = Depends(get_db)):
    """Обновление статуса заказа."""
    order = await Order.update_status(db=db, order_id=order_id, status=status)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

@router.delete("/{order_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    """Удаление заказа."""
    success = await Order.delete(db=db, order_id=order_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return {"success": success}
