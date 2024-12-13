from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Базовая схема пользователя (для общих свойств)
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: Optional[bool] = True

# Схема для создания пользователя
class UserCreate(UserBase):
    hashed_password: str

# Схема для обновления пользователя
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

# Схема ответа с данными пользователя
class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None  # Сделано необязательным

    class Config:
        from_attributes = True  # Отображение данных из ORM (SQLAlchemy)
