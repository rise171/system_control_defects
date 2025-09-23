from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine("sqlite+aiosqlite:///project_spo.db", echo=True)
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
        await  conn.run_sync(Base.metadata.drop_all())