from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from bot.config import settings


class AdminMiddleware(BaseMiddleware):
    """Middleware для проверки прав администратора"""
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], 
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.from_user is None:
            await event.answer("❌ Ошибка: пользователь не найден")
            return
        
        if event.from_user.id not in settings.admin_ids_list:
            await event.answer("⛔ У вас нет прав администратора")
            return
        
        return await handler(event, data)