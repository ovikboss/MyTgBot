from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import  types

from .router import router
from core.states.registration import Registration
from core.DB.db import  db
from  core.DB.models import User
from core.checksubscribe.checker import subscription_required

@router.message(Command("register"))
async def register_command(message: types.Message, state: FSMContext):
    await state.set_state(Registration.waiting_for_name)
    await message.reply("Пожалуйста, введите ваше имя:")

@router.message(Registration.waiting_for_name)
async def name_entered(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Registration.waiting_for_login)
    await message.reply("Пожалуйста, введите ваш логин (никнейм):")

@router.message(Registration.waiting_for_login)
async def login_entered(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await state.set_state(Registration.waiting_for_current_weight)
    await message.reply("Пожалуйста, введите ваш текущий вес (в килограммах):")

@router.message(Registration.waiting_for_current_weight)
async def current_weight_entered(message: types.Message, state: FSMContext):
    try:
        current_weight = float(message.text)
        await state.update_data(current_weight=current_weight)
        await state.set_state(Registration.waiting_for_height)
        await message.reply("Пожалуйста, введите ваш рост (в сантиметрах):")
    except ValueError:
        await message.reply("Пожалуйста, введите корректное число для текущего веса.")
        await state.set_state(Registration.waiting_for_current_weight)  # Stay in the same state



@router.message(Registration.waiting_for_height)
async def height_entered(message: types.Message, state: FSMContext):
    try:
        height = float(message.text)
        await state.update_data(height=height)
        await state.set_state(Registration.waiting_for_age)
        await message.reply("Пожалуйста, введите ваш возраст (в годах):")
    except ValueError:
        await message.reply("Пожалуйста, введите корректное число для роста.")
        await state.set_state(Registration.waiting_for_height)

@router.message(Registration.waiting_for_age)
async def age_entered(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        await state.set_state(Registration.waiting_for_gender)
        await message.reply("Пожалуйста, введите ваш пол (мужской/женский):")
    except ValueError:
        await message.reply("Пожалуйста, введите корректное число для возраста.")
        await state.set_state(Registration.waiting_for_age)

@router.message(Registration.waiting_for_gender)
async def gender_entered(message: types.Message, state: FSMContext):
    gender = message.text.lower()
    if gender in ["мужской", "male"]:
        is_male = True
    elif gender in ["женский", "female"]:
        is_male = False
    else:
        await message.reply("Пожалуйста, введите 'мужской' или 'женский'.")
        await state.set_state(Registration.waiting_for_gender)
        return
    await state.update_data(is_male=is_male)
    await state.set_state(Registration.waiting_for_activity_level)
    await message.reply("Пожалуйста, выберите ваш уровень активности от 0 до 5:")

@router.message(Registration.waiting_for_activity_level)
async def activity_level_entered(message: types.Message, state: FSMContext):
    activity_level = message.text.lower()
    valid_activity_levels = 0 <= float(activity_level) <= 5
    if not  valid_activity_levels:
        await message.reply(f"Число должно быть в диапазоне от 0 до 5")
        await state.set_state(Registration.waiting_for_activity_level)
        return

    await state.update_data(activity_level=activity_level)
    data = await state.get_data()
    name = data.get('name')
    login = data.get('login')
    current_weight = data.get('current_weight')

    height = data.get('height')
    age = data.get('age')
    is_male = data.get('is_male')
    activity_level = data.get('activity_level')

    user_id = str(message.from_user.id)
    registration_success = db.register_user(user_id, name, login, current_weight, height, age, is_male,activity_level)

    if registration_success:
        await message.reply("Вы успешно зарегистрированы!")
    else:
        await message.reply("Ошибка при регистрации. Попробуйте еще раз.")

    await state.clear()