from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

engine = create_async_engine( settings.DATABASE_URL )
SessionLocal = async_sessionmaker(bind=engine,class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()