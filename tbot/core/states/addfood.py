from aiogram.fsm.state import State, StatesGroup

class AddFood(StatesGroup):
    waiting_for_food_name = State()
    waiting_for_calories = State()
