from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.services.group_service import GroupService
from bot.middlewares.admin import AdminMiddleware
import logging

logger = logging.getLogger(__name__)
router = Router()
router.message.middleware(AdminMiddleware())


@router.message(Command("admin_set_premium"))
async def set_premium(message: Message, session: AsyncSession):
    """
    Установить премиум статус группы
    Формат: /admin_set_premium <group_id> <true/false>
    """
    assert message.text is not None  # Гарантировано командой
    try:
        args = message.text.split()
        if len(args) != 3:
            await message.answer(
                "⚠️ Формат: /admin_set_premium <group_id> <true/false>"
            )
            return
        
        group_id = int(args[1])
        is_premium = args[2].lower() == "true"
        
        success = await GroupService.set_premium(session, group_id, is_premium)
        
        if success:
            await message.answer(
                f"✅ Премиум статус для группы {group_id}: {is_premium}"
            )
        else:
            await message.answer(f"❌ Группа {group_id} не найдена")
            
    except ValueError:
        await message.answer("❌ Некорректный group_id")
    except Exception as e:
        logger.error(f"Ошибка установки премиум: {e}")
        await message.answer(f"❌ Ошибка: {e}")


@router.message(Command("admin_add_filial"))
async def add_filial(message: Message, session: AsyncSession):
    """
    Добавить филиал группе
    Формат: /admin_add_filial <group_id> <название>
    """
    assert message.text is not None  # Гарантировано командой
    try:
        args = message.text.split(maxsplit=2)
        if len(args) != 3:
            await message.answer(
                "⚠️ Формат: /admin_add_filial <group_id> <название>"
            )
            return
        
        group_id = int(args[1])
        filial_name = args[2]
        
        filial = await GroupService.add_filial(session, group_id, filial_name)
        
        if filial:
            await message.answer(
                f"✅ Филиал '{filial_name}' добавлен группе {group_id}"
            )
        else:
            await message.answer(f"❌ Группа {group_id} не найдена")
            
    except ValueError:
        await message.answer("❌ Некорректный group_id")
    except Exception as e:
        logger.error(f"Ошибка добавления филиала: {e}")
        await message.answer(f"❌ Ошибка: {e}")