from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from app.core.database import Base  # Импортируем Base из app/core/database.py
from app.models.order import Order, OrderItem  # Импортируем модели
from app.models.product import Product  # Импортируем модель Product

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Устанавливаем target_metadata, чтобы Alembic знал, какие метаданные использовать
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Здесь используем обычный create_engine, а не create_async_engine, так как Alembic не поддерживает асинхронные соединения
    engine = create_engine(config.get_main_option("sqlalchemy.url"))

    with engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Выбор режима (offline или online)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
