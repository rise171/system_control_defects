from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Получаем параметры подключения из переменных окружения
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "project_spo")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

# Формируем URL для подключения к PostgreSQL
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создаем асинхронный движок для PostgreSQL
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Логирование SQL запросов
    pool_size=10,  # Размер пула соединений
    max_overflow=20,  # Максимальное количество соединений сверх pool_size
)

# Создаем фабрику сессий
make_session = async_sessionmaker(
    engine, 
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_session():
    async with make_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

class Base(DeclarativeBase):
    pass

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def check_connection():
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        print("PostgreSQL connection successful")
        return True
    except Exception as e:
        print(f"PostgreSQL connection failed: {e}")
        return False

"""engine = create_async_engine("sqlite+aiosqlite:///project_spo.db", echo=True)

make_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with make_session() as session:
        yield session

class Base(DeclarativeBase):
    pass

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await  conn.run_sync(Base.metadata.drop_all())"""