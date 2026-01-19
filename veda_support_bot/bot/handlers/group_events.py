from aiogram import Router, F
from aiogram.types import ChatMemberUpdated
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore
from bot.services.group_service import GroupService
import logging

logger = logging.getLogger(__name__)
router = Router()


@router.chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=IS_NOT_MEMBER >> IS_MEMBER
    )
)
async def on_bot_added(event: ChatMemberUpdated, session: AsyncSession):
    """Обработчик добавления бота в группу"""
    assert event.bot is not None  # Убеждаемся, что бот инициализирован
    
    if not event.new_chat_member.user.is_bot:
        return
    
    try:
        group, created = await GroupService.get_or_create_group(
            session,
            event.chat.id,
            event.chat.title or "Неизвестная группа"
        )
        
        welcome_text = (
            "👋 <b>Добро пожаловать!</b>\n\n"
            "Я бот технической поддержки компании VedaVector.\n\n"
            "<b>Как создать заявку:</b>\n"
            "1. Напишите команду /help\n"
            "2. Выберите язык\n"
            "3. Опишите вашу проблему\n\n"
            "⚠️ <i>Пожалуйста, заполняйте заявку максимально подробно</i>"
        )
        
        msg = await event.bot.send_message(
            event.chat.id,
            welcome_text,
            parse_mode="HTML"
        )
        
        # Закрепляем сообщение (может не быть прав)
        try:
            await event.bot.pin_chat_message(event.chat.id, msg.message_id)
        except Exception as e:
            logger.warning(f"Не удалось закрепить сообщение: {e}")
        
        logger.info(f"Бот добавлен в группу: {event.chat.title} ({event.chat.id})")
        
    except Exception as e:
        logger.error(f"Ошибка при добавлении бота в группу: {e}")