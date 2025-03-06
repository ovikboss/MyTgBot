from datetime import datetime
import logging
from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.DB.db import  db
from core.DB.models import FoodEntry

async def send_daily_breakfast(bot, meal_type, percent, user_id):
    """Sends a daily summary to all registered users."""
    builder = InlineKeyboardBuilder()
    user = db.get_user(user_id)
    bmr = db.get_data_bmr(user_id)
    activity_level = db.get_activity_level(user_id)
    builder.button(text="Предложить рецепт", callback_data=f"покажи рецепт:{meal_type}:{round(bmr * percent * activity_level,2)}")
    keyboard = builder.as_markup()
    try:
        res = "завтракать" if meal_type == "завтрак" else  "обедать" if meal_type == "обед" else "ужинать"
        if user.daily_message: 
                await bot.send_message(
                chat_id=user_id,
                text=f"Привет, {user.name}! Время {res}! "
                     f"Желательно съесть {bmr * percent * activity_level:.2f} ккал.",
                reply_markup=keyboard,)
    except Exception as e:
        logging.error(f"Failed to send daily summary to user {user_id}: {e}")



async def send_meal_reminder(bot: Bot, meal_type: str, percent: float, user_id):
    """Wrapper for the send_daily_summary function to be used with APScheduler."""
    await send_daily_breakfast(bot, meal_type, percent, user_id)