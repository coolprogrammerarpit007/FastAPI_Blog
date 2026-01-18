from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,sessionmaker

MYSQL_DATABASE_URL = "mysql+pymysql://root@localhost:3307/blogs"

engine = create_engine(
    MYSQL_DATABASE_URL,
    
)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as db:
        yield db