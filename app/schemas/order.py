from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Schema для элементов заказа (OrderItem)
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price_per_item: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int

    class Config:
        orm_mode = True

# Schema для заказа (Order)
class OrderBase(BaseModel):
    status: Optional[str] = "pending"

class OrderCreate(OrderBase):
    total_price: float
    items: List[OrderItemCreate]

class OrderResponse(OrderBase):
    id: int
    total_price: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
