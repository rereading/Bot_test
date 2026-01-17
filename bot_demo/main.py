import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from settings import BOT_TOKEN
from handlers import commands, mentions

async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(commands.router)
    dp.include_router(mentions.router)

    await bot.set_my_commands([
        BotCommand(command="start", description="Описание и приветствие"),
        BotCommand(command="help", description="Как пользоваться ботом"),
        BotCommand(command="getsupp", description="Создать обращение"),
    ])

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
