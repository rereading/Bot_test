from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, InaccessibleMessage
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from bot.states import HelpFSM
from bot.keyboards.language import language_keyboard
from bot.keyboards.filials import filials_keyboard
from bot.services.group_service import GroupService
from bot.services.pyrus_service import pyrus_service
from bot.config import settings
import logging

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("help"))
async def start_help(message: Message, state: FSMContext):
    """Начало создания заявки"""
    if message.chat.type == "private":
        await message.answer(
            "⚠️ Эта команда работает только в групповых чатах"
        )
        return
    
    await state.set_state(HelpFSM.language)
    await message.answer(
        "🌐 <b>Выберите язык / Tilni tanlang / Choose language:</b>",
        reply_markup=language_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "cancel")
async def cancel_help(call: CallbackQuery, state: FSMContext):
    """Отмена создания заявки"""
    if call.message is None or isinstance(call.message, InaccessibleMessage):
        return
    await state.clear()
    await call.message.delete()
    await call.answer("❌ Создание заявки отменено")


@router.callback_query(HelpFSM.language, F.data.startswith("lang_"))
async def choose_language(
    call: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    """Выбор языка"""
    if call.message is None or isinstance(call.message, InaccessibleMessage) or call.data is None:
        return
    language = call.data.split("_")[1]
    await state.update_data(language=language)
    
    lang_messages = {
        "ru": "📝 Опишите вашу проблему подробно:",
        "uz": "📝 Muammoingizni batafsil tasvirlab bering:",
        "en": "📝 Describe your problem in detail:"
    }
    
    await call.message.edit_text(
        lang_messages.get(language, lang_messages["ru"])
    )
    await state.set_state(HelpFSM.description)
    await call.answer()


@router.message(HelpFSM.description, F.text)
async def get_description(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    """Получение описания проблемы"""
    assert message.text is not None  # Гарантировано фильтром F.text
    description = message.text.strip()
    
    # Валидация
    if len(description) < 10:
        await message.answer(
            "⚠️ Описание слишком короткое. Пожалуйста, опишите проблему подробнее."
        )
        return
    
    if len(description) > settings.MAX_DESCRIPTION_LENGTH:
        await message.answer(
            f"⚠️ Описание слишком длинное (максимум {settings.MAX_DESCRIPTION_LENGTH} символов)"
        )
        return
    
    await state.update_data(description=description)
    
    # Удаляем сообщение пользователя для конфиденциальности
    try:
        await message.delete()
    except Exception as e:
        logger.warning(f"Не удалось удалить сообщение: {e}")
    
    # Проверяем наличие филиалов
    group = await GroupService.get_group(session, message.chat.id)
    
    if not group:
        await message.answer("❌ Ошибка: группа не найдена в базе данных")
        await state.clear()
        return
    
    if group.has_filials:
        filials = await GroupService.get_filials(session, message.chat.id)
        
        if filials:
            await message.answer(
                "🏢 Выберите филиал:",
                reply_markup=filials_keyboard(filials)
            )
            await state.set_state(HelpFSM.filial)
        else:
            await send_to_pyrus(message.bot, message.chat.id, state, session, group)
    else:
        await send_to_pyrus(message.bot, message.chat.id, state, session, group)


@router.callback_query(HelpFSM.filial, F.data.startswith("filial_"))
async def choose_filial(
    call: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    """Выбор филиала"""
    if call.message is None or isinstance(call.message, InaccessibleMessage) or call.data is None:
        return
    filial_id = int(call.data.split("_")[1])
    
    # Получаем филиал
    from bot.models.filial import Filial
    from sqlalchemy import select
    
    result = await session.execute(
        select(Filial).where(Filial.id == filial_id)
    )
    filial = result.scalar_one_or_none()
    
    if not filial:
        await call.answer("❌ Филиал не найден")
        return
    
    await state.update_data(filial=filial.name)
    
    # Получаем группу
    group = await GroupService.get_group(session, call.message.chat.id)
    
    await call.message.delete()
    await send_to_pyrus(call.bot, call.message.chat.id, state, session, group)
    await call.answer()


async def send_to_pyrus(
    bot,
    chat_id: int,
    state: FSMContext,
    session: AsyncSession,
    group
):
    """Отправка заявки в Pyrus"""
    data = await state.get_data()
    
    # Формируем данные для Pyrus
    pyrus_data = {
        "description": data["description"],
        "language": data["language"],
        "group_name": group.group_name,
        "is_premium": group.is_premium,
        "filial": data.get("filial")
    }
    
    # Создаем задачу
    task_id = await pyrus_service.create_task(pyrus_data)
    
    if task_id:
        success_messages = {
            "ru": (
                "✅ <b>Заявка успешно создана!</b>\n\n"
                f"Номер заявки: <code>{task_id}</code>\n"
                "Мы свяжемся с вами в ближайшее время."
            ),
            "uz": (
                "✅ <b>Murojaat muvaffaqiyatli yaratildi!</b>\n\n"
                f"Murojaat raqami: <code>{task_id}</code>\n"
                "Yaqin orada siz bilan bog'lanamiz."
            ),
            "en": (
                "✅ <b>Request created successfully!</b>\n\n"
                f"Request ID: <code>{task_id}</code>\n"
                "We will contact you soon."
            )
        }
        
        msg_text = success_messages.get(data["language"], success_messages["ru"])
        await bot.send_message(chat_id, msg_text, parse_mode="HTML")
    else:
        await bot.send_message(
            chat_id,
            "❌ Произошла ошибка при создании заявки. Попробуйте позже."
        )
    
    await state.clear()