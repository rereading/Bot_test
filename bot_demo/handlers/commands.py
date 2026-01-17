from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states import SupportRequest
import texts

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    print("START command received")
    try:
        await message.reply(texts.START_TEXT)
        print("Reply sent successfully")
    except Exception as e:
        print(f"Error sending reply: {e}")

@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.reply(texts.HELP_TEXT)

@router.message(Command("getsupp"))
async def getsupp_cmd(message: Message, state: FSMContext):
    await state.set_state(SupportRequest.problem)
    await message.reply(texts.ASK_PROBLEM)

@router.message(SupportRequest.problem)
async def get_problem(message: Message, state: FSMContext):
    await state.update_data(problem=message.text)
    await state.set_state(SupportRequest.details)
    await message.reply(texts.ASK_DETAILS)

@router.message(SupportRequest.details)
async def get_details(message: Message, state: FSMContext):
    data = await state.get_data()

    # пока просто лог
    print("NEW REQUEST")
    print("Problem:", data["problem"])
    print("Details:", message.text)

    await state.clear()
    await message.reply(texts.DONE_TEXT)
