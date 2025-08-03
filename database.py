from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

#write path where database is stored
DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost:5432/Employee_Details"
#create async engine for high concurrency workloads
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=30, #no of connections in a pool
    max_overflow=10 #extra connections beyond pool size
    )
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

#start session
async def get_session():
    async with async_session() as session:
        yield session

#create table if not created
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)