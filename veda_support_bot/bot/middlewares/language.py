"""
Middleware для автоматической установки языка из FSM
После выбора языка пользователем, он автоматически внедряется во все handlers
"""

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.fsm.context import FSMContext


class LanguageMiddleware(BaseMiddleware):
    """Middleware для автоматической установки языка из FSM"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Получаем state
        state: FSMContext | None = data.get("state")
        
        # Язык по умолчанию
        language = "ru"
        
        # Пытаемся получить язык из FSM
        if state:
            state_data = await state.get_data()
            language = state_data.get("language", "ru")
        
        # Внедряем язык в data для использования в handlers
        data["language"] = language
        
        return await handler(event, data)