import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from bot.config import settings
from bot.database import db
from bot.middlewares.db import DatabaseMiddleware
from bot.handlers import group_events, help_flow, admin

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    # Создание бота и диспетчера
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Подключение middleware
    dp.update.middleware(DatabaseMiddleware())
    
    # Регистрация роутеров
    dp.include_router(group_events.router)
    dp.include_router(help_flow.router)
    dp.include_router(admin.router)
    
    # Создание таблиц БД
    await db.create_tables()
    
    logger.info("Бот запущен")
    
    try:
        # Удаление вебхука и запуск polling
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")