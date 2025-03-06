from datetime import datetime, time

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import  types

from core.states.set_time import SetTime
from .router import router
from core.DB.db import  db
from core.checksubscribe.checker import subscription_required





@router.message(Command("set_breakfast_time"))
@subscription_required
async def set_breakfast_time_command(message: types.Message, state: FSMContext):
    await state.set_state(SetTime.waiting_for_breakfast_time)
    await message.reply("Пожалуйста, введите желаемое время для напоминания о завтраке в формате ЧЧ:ММ (например, 07:30):")

@router.message(SetTime.waiting_for_breakfast_time)
async def breakfast_time_entered(message: types.Message, state: FSMContext):
    try:
        time_str = message.text
        breakfast_time = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        await message.reply("Неправильный формат времени. Пожалуйста, введите время в формате ЧЧ:ММ (например, 07:30).")
        return

    user_id = str(message.from_user.id)

    if db.eat_time_entered(user_id,  breakfast_time, "завтрак"):
        await message.reply(f"Время напоминания о завтраке установлено на {time_str}.")
    else:
        await message.reply("Пользователь не найден. Зарегистрируйтесь с помощью /register.")
    await state.set_state(state=None)

#Аналогичные функции для обеда и ужина
@router.message(Command("set_lunch_time"))
async def set_lunch_time_command(message: types.Message, state: FSMContext):
    await state.set_state(SetTime.waiting_for_lunch_time)
    await message.reply("Пожалуйста, введите желаемое время для напоминания об обеде в формате ЧЧ:ММ (например, 13:00):")


@router.message(SetTime.waiting_for_lunch_time)
async def lunch_time_entered(message: types.Message, state: FSMContext):
    try:
        time_str = message.text
        lunch_time = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        await message.reply("Неправильный формат времени. Пожалуйста, введите время в формате ЧЧ:ММ (например, 13:00).")
        return
    user_id = str(message.from_user.id)
    if db.eat_time_entered(user_id, lunch_time, "обед"):
        await message.reply(f"Время напоминания об обеде установлено на {time_str}.")
    else:
        await message.reply("Пользователь не найден. Зарегистрируйтесь с помощью /register.")
    await state.set_state(state=None)

@router.message(Command("set_dinner_time"))
async def set_dinner_time_command(message: types.Message, state: FSMContext):
    await state.set_state(SetTime.waiting_for_dinner_time)
    await message.reply("Пожалуйста, введите желаемое время для напоминания об ужине в формате ЧЧ:ММ (например, 19:00):")

@router.message(SetTime.waiting_for_dinner_time)
async def dinner_time_entered(message: types.Message, state: FSMContext):
    try:
        time_str = message.text
        dinner_time = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        await message.reply("Неправильный формат времени. Пожалуйста, введите время в формате ЧЧ:ММ (например, 19:00).")
        return

    user_id = str(message.from_user.id)

    if db.eat_time_entered(user_id, dinner_time, "ужин"):

        await message.reply(f"Время напоминания об ужине установлено на {time_str}.")
    else:
        await message.reply("Пользователь не найден. Зарегистрируйтесь с помощью /register.")
    await state.set_state(state=None)