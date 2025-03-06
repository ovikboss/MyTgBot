from aiogram.fsm.state import State, StatesGroup



class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_login = State()
    waiting_for_current_weight = State()
    waiting_for_height = State()  # Added height
    waiting_for_age = State()     # Added age
    waiting_for_gender = State()  # Added gender
    waiting_for_activity_level = State() # Added activity level