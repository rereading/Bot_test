from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(lambda m: m.entities and any(e.type == "mention" for e in m.entities))
async def on_mention(message: Message):
    await message.reply(
        "Меня позвали 👀\n"
        "Используйте /getsupp чтобы создать обращение."
    )
