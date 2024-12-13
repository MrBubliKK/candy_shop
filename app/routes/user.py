from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import *
from app.models.user import User
from app.core.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Создание нового пользователя."""
    try:
        user = await User.create(db=db, user_data=user_data)
        return user
    except Exception as e:
        print("ERROR: ", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Получение пользователя по ID."""
    user = await User.get_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """Получение списка пользователей с пагинацией."""
    return await User.get_all(db=db, skip=skip, limit=limit)

@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    """Обновление данных пользователя."""
    user = await User.update(db=db, user_id=user_id, user_data=user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.delete("/{user_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Удаление пользователя."""
    success = await User.delete(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"success": success}
