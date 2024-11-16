import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.main.config.vars_config import settings

# SQLALCHEMY
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    echo=True,
    logging_name=logging.INFO,
)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db_async():
    db: AsyncSession = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def initialize_db():
    async with engine.begin() as conn:
        logging.info("Initializing database...")
        await conn.run_sync(Base.metadata.create_all)
        logging.info("Database has been successfully initialized!")
