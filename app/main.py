from fastapi import FastAPI
from app.routes import database, product, order, user

app = FastAPI()

# Подключение маршрутов
app.include_router(product.router, prefix="/products", tags=["products"])
app.include_router(order.router, prefix="/orders", tags=["orders"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(database.router, prefix="/database", tags=["database"])
