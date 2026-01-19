from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine
)
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
import logging
from bot.config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self, url: str):
        self.engine: AsyncEngine = create_async_engine(
            url,
            echo=False,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20
        )
        self.session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    async def create_tables(self):
        """Создать все таблицы"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Таблицы БД созданы")
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Получить сессию БД"""
        async with self.session_maker() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.error(f"Ошибка сессии БД: {e}")
                raise
            finally:
                await session.close()


db = Database(settings.DATABASE_URL)