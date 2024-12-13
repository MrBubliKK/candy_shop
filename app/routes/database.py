from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from app.core.database import get_db

router = APIRouter(
    prefix="/database",
    tags=["database"]
)

# Роут для получения списка публичных таблиц
@router.get("/public-tables", summary="Получить список всех публичных таблиц", response_model=dict)
async def get_public_tables(db: AsyncSession = Depends(get_db)):
    query = text("""
        SELECT tablename
        FROM pg_catalog.pg_tables
        WHERE schemaname = 'public';
    """)
    try:
        result = await db.execute(query)
        tables = result.scalars().all()
        return {"public_tables": tables}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при выполнении запроса: {str(e)}"
        )

# Роут для получения количества таблиц
@router.get("/table-count", summary="Получить количество таблиц в публичной схеме", response_model=dict)
async def get_table_count(db: AsyncSession = Depends(get_db)):
    query = text("""
        SELECT COUNT(*) AS table_count
        FROM pg_catalog.pg_tables
        WHERE schemaname = 'public';
    """)
    try:
        result = await db.execute(query)
        count = result.scalar()
        return {"table_count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при выполнении запроса: {str(e)}"
        )

# Роут для создания таблицы products
@router.post("/create-products-table", summary="Создать таблицу products")
async def create_products_table(db: AsyncSession = Depends(get_db)):
    query = text("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            description TEXT,
            price FLOAT NOT NULL,
            is_available BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)
    try:
        await db.execute(query)
        await db.commit()
        return {"message": "Table 'products' created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании таблицы products: {str(e)}"
        )

# Роут для создания таблицы orders
@router.post("/create-orders-table", summary="Создать таблицу orders")
async def create_orders_table(db: AsyncSession = Depends(get_db)):
    query = text("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            status VARCHAR DEFAULT 'pending',
            total_price FLOAT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)
    try:
        await db.execute(query)
        await db.commit()
        return {"message": "Table 'orders' created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании таблицы orders: {str(e)}"
        )

# Роут для создания таблицы order_items
@router.post("/create-order-items-table", summary="Создать таблицу order_items")
async def create_order_items_table(db: AsyncSession = Depends(get_db)):
    query = text("""
        CREATE TABLE IF NOT EXISTS order_items (
            id SERIAL PRIMARY KEY,
            order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
            product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
            quantity INTEGER NOT NULL,
            price_per_item FLOAT NOT NULL
        );
    """)
    try:
        await db.execute(query)
        await db.commit()
        return {"message": "Table 'order_items' created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании таблицы order_items: {str(e)}"
        )

# Роут для создания таблицы users
@router.post("/create-users-table", summary="Создать таблицу users")
async def create_users_table(db: AsyncSession = Depends(get_db)):
    query = text("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR UNIQUE NOT NULL,
            email VARCHAR UNIQUE NOT NULL,
            hashed_password VARCHAR NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)
    try:
        await db.execute(query)
        await db.commit()
        return {"message": "Table 'users' created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании таблицы users: {str(e)}"
        )
        
# Роут для создания всех таблиц сразу
@router.post("/create-all-tables", summary="Создать все таблицы")
async def create_all_tables(db: AsyncSession = Depends(get_db)):
    queries = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR UNIQUE NOT NULL,
            email VARCHAR UNIQUE NOT NULL,
            hashed_password VARCHAR NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            description TEXT,
            price FLOAT NOT NULL,
            is_available BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            status VARCHAR DEFAULT 'pending',
            total_price FLOAT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS order_items (
            id SERIAL PRIMARY KEY,
            order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
            product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
            quantity INTEGER NOT NULL,
            price_per_item FLOAT NOT NULL
        );
        """
    ]

    try:
        for query in queries:
            await db.execute(text(query))
        await db.commit()
        return {"message": "All tables created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании таблиц: {str(e)}"
        )