from aiogram.fsm.state import State, StatesGroup

class SetTime(StatesGroup):
    waiting_for_breakfast_time = State()
    waiting_for_lunch_time = State()
    waiting_for_dinner_time = State()