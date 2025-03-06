from aiogram import Bot, Dispatcher, types, F
import random
import asyncio
import logging

from core.checksubscribe.checker import subscription_required

from core.dispatcher.create_dp import dp
from core.DB.db import  db



async def get_recipe_for_meal(user_id: str, meal_type: str, calories:int) -> str:
    """Возвращает рецепт для конкретного приема пищи (нужно реализовать)."""
    recipe = db.get_recipe(meal_type = meal_type, calories = calories)
    user_subscribe = db.get_user_subscribe(user_id)
    await asyncio.sleep(0)
    if user_subscribe[0]:
        if recipe:
            return random.choice(recipe)
        else:
            return "К сожалению рецепта пока что нет"
    else:
        return "К сожаление у вас нет подписки"



@dp.callback_query(F.data.startswith("покажи рецепт:"))
async def show_recipe_callback(callback: types.CallbackQuery):
    """Обработчик нажатия на кнопку "Предложить рецепт"."""
    meal_type = callback.data.split(":")[1]
    calories = callback.data.split(":")[2]
    user_id = str(callback.from_user.id)

    recipe = await get_recipe_for_meal(user_id, meal_type, calories)
    await callback.message.answer(f"Вот рецепт на {meal_type}:\n{recipe}")
    await callback.answer()  # Убираем "часики"