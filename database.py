from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker,create_async_engine
from sqlalchemy.orm import DeclarativeBase

MYSQL_DATABASE_URL = "mysql+aiomysql://root@localhost:3307/blogs"

engine = create_async_engine(
    MYSQL_DATABASE_URL,
    
)

AsyncSessionLocal = async_sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session