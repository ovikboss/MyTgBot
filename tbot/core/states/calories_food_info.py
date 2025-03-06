from aiogram.fsm.state import State, StatesGroup

class CaloriesInfo(StatesGroup):
    waiting_for_food_name = State()
    waiting_for_weight = State()