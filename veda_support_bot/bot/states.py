from aiogram.fsm.state import StatesGroup, State


class HelpFSM(StatesGroup):
    language = State()
    description = State()
    filial = State()