from sqlalchemy import Column, Integer, String, Boolean, DateTime, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from app.core.base import Base
from app.schemas.user import UserCreate, UserUpdate

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    @classmethod
    async def create(cls, db: AsyncSession, user_data: UserCreate):
        """Создаёт пользователя."""
        user = cls(
            username=user_data.username,
            email=user_data.email,
            hashed_password=user_data.hashed_password,
            is_active=user_data.is_active,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @classmethod
    async def get_by_id(cls, db: AsyncSession, user_id: int):
        """Возвращает пользователя по ID."""
        result = await db.execute(
            select(cls).filter(cls.id == user_id)
        )
        return result.scalars().first()

    @classmethod
    async def get_all(cls, db: AsyncSession, skip: int = 0, limit: int = 10):
        """Возвращает список пользователей с пагинацией."""
        result = await db.execute(
            select(cls).offset(skip).limit(limit)
        )
        return result.scalars().all()

    @classmethod
    async def update(cls, db: AsyncSession, user_id: int, user_data: UserUpdate):
        """Обновляет данные пользователя."""
        result = await db.execute(
            select(cls).filter(cls.id == user_id)
        )
        user = result.scalars().first()
        if not user:
            return None
        user.username = user_data.username or user.username
        user.email = user_data.email or user.email
        user.is_active = user_data.is_active if user_data.is_active is not None else user.is_active
        await db.commit()
        await db.refresh(user)
        return user

    @classmethod
    async def delete(cls, db: AsyncSession, user_id: int) -> bool:
        """Удаляет пользователя."""
        result = await db.execute(
            select(cls).filter(cls.id == user_id)
        )
        user = result.scalars().first()
        if not user:
            return False
        await db.delete(user)
        await db.commit()
        return True
