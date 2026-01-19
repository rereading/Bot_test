from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from bot.database import db


class DatabaseMiddleware(BaseMiddleware):
    """Middleware для внедрения сессии БД"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async for session in db.get_session():
            data["session"] = session
            return await handler(event, data)