from aiogram.fsm.state import StatesGroup, State

class SupportRequest(StatesGroup):
    problem = State()
    details = State()
