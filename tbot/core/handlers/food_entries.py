from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import  types

from .router import router
from core.states.addfood import AddFood
from core.DB.db import  db
from core.checksubscribe.checker import subscription_required



@router.message(Command("add_food"))
@subscription_required
async def add_food_command(message: types.Message, state: FSMContext):
    """Запускает процесс добавления записи о еде."""
    await state.set_state(AddFood.waiting_for_food_name)
    await message.reply("Как называется продукт?")

@router.message(AddFood.waiting_for_food_name)
async def food_name_entered(message: types.Message, state: FSMContext):
    """Обрабатывает ввод названия продукта."""
    await state.update_data(food_name=message.text)
    await state.set_state(AddFood.waiting_for_calories)
    await message.reply("Сколько калорий?")

@router.message(AddFood.waiting_for_calories)
async def calories_entered(message: types.Message, state: FSMContext):
    """Обрабатывает ввод количества калорий."""
    try:
        calories = int(message.text)
        if calories <= 0:
            await message.reply("Калории должны быть положительным числом.")
            return
    except ValueError:
        await message.reply("Пожалуйста, введи число.")
        return

    user_id = message.from_user.id
    data = await state.get_data()
    food_name = data["food_name"]

    db.add_food(user_id, food_name, calories)
    await state.clear()
    await message.reply(f"Добавлено: {food_name} - {calories} ккал")