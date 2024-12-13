# order_tasks.py
from celery_app.worker import celery_app  # Используем общий Celery инстанс
from app.models.order import Order
from app.core.database import SessionLocal


@celery_app.task
def process_order(order_id: int):
    """
    Задача для обработки заказа.
    """
    print(f"Processing order {order_id}")
    
    # Используем контекст сессии для корректного закрытия сессии
    try:
        db = SessionLocal()  # Создаём сессию для работы с БД

        # Получение заказа из базы данных
        order = Order.get_by_id(db, order_id)
        if not order:
            print(f"Order {order_id} not found")
            return
        
        # Логика обработки заказа
        print(f"Order {order_id} is being processed...")

        # Обновляем статус заказа
        Order.update_status(db, order_id, "completed")
        print(f"Order {order_id} processing completed.")

    except Exception as e:
        print(f"Error processing order {order_id}: {e}")
        # Здесь можно записать ошибку в лог или обновить статус заказа на "ошибка"
    finally:
        db.close()  # Закрываем сессию
