from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.product import *
from app.models.product import Product
from app.core.database import get_db  # Импортируем асинхронную зависимость

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

# Зависимость для получения асинхронной сессии БД
# Используем асинхронную функцию get_db, которую вы уже создали в database.py

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_new_product(product_data: ProductCreate, db: AsyncSession = Depends(get_db)):
    """Создание нового продукта."""
    try:
        product = await Product.create(db=db, product_data=product_data)
        return product
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """Получение продукта по ID."""
    product = await Product.get_by_id(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.get("/", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
async def read_products(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """Получение списка продуктов с пагинацией."""
    return await Product.get_all(db=db, skip=skip, limit=limit)

@router.put("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def update_product(product_id: int, product_data: ProductBase, db: AsyncSession = Depends(get_db)):
    """Обновление информации о продукте."""
    product = await Product.update(db=db, product_id=product_id, product_data=product_data)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.delete("/{product_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """Удаление продукта."""
    success = await Product.delete(db=db, product_id=product_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return {"success": success}
