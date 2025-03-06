from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import  types
import requests
from googletrans import Translator
import json

from .router import router
from core.states.calories_food_info import CaloriesInfo
from core.checksubscribe.checker import subscription_required

def info_food(text_to_translate):
    translator = Translator()
    translated = translator.translate(text_to_translate, src='ru', dest='en')
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    query = translated.text
    response = requests.get(api_url + query, headers={'X-Api-Key': 'rkztpii013JMUL2O4ONcTA==GTDQbAkSU2Q0xT6b'})
    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)
        total_kcal = 0
        total_fat = 0
        total_protein = 0
        total_carbohydrates = 0
        for elem in data["items"]:
            print(elem)
            total_kcal += int(elem["calories"])
            total_fat += int(elem["fat_total_g"])
            total_protein += int(elem["protein_g"])
            total_carbohydrates += int(elem["carbohydrates_total_g"])
        return total_kcal,total_fat,total_protein,total_carbohydrates
    else:
        print("Error:", response.status_code, response.text)

@router.message(Command("food_info"))
@subscription_required
async def add_food_command(message: types.Message, state: FSMContext):
    """Запускает процесс добавления записи о еде."""
    await state.set_state(CaloriesInfo.waiting_for_food_name)
    await message.reply("Как называется продукт?")

@router.message(CaloriesInfo.waiting_for_food_name)
async def food_name_entered(message: types.Message, state: FSMContext):
    """Обрабатывает ввод названия продукта."""
    await state.update_data(food_name=message.text)
    await state.set_state(CaloriesInfo.waiting_for_weight)
    await message.reply("Сколько грамм?")

@router.message(CaloriesInfo.waiting_for_weight)
async def calories_entered(message: types.Message, state: FSMContext):
    """Обрабатывает ввод количества калорий."""
    try:
        grams = int(message.text)
        if grams <= 0:
            await message.reply("Вес должны быть положительным числом.")
            return
    except ValueError:
        await message.reply("Пожалуйста, введи число.")
        return

    user_id = message.from_user.id
    data = await state.get_data()
    food_name = data["food_name"]
    calories = info_food(f"{grams} грамм {food_name}")
    print(calories)
    if calories != (0,0,0,0):
        await state.clear()
        await message.reply(f"В : {food_name} - {calories[0]} ккал \nбелок: {calories[2]} \nжиров: {calories[1]}  \nуглеводов: {calories[3]}")
    else:
        await state.clear()
        await message.reply(f"Такого продукта нет в базе")