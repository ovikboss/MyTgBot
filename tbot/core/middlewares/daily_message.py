from datetime import datetime
import logging
from aiogram import Bot
from core.DB.db import  db
from core.DB.models import FoodEntry

def calculate_total_calories(food_entries: list[FoodEntry]) -> float:
    """Calculates the total calories from a list of food entries."""
    total_calories = sum(entry.calories for entry in food_entries)
    return total_calories



async def send_daily_summary(bot):
    """Sends a daily summary to all registered users."""

    for user in db.get_show_daily():
        food_entries = db.get_today_food(user.id)
        total_calories = calculate_total_calories(food_entries)
        try:
            await bot.send_message(
                chat_id=user.id,
                text=f"Привет, {user.name}! Сегодня ты съел(а) {total_calories:.2f} ккал."
            )
        except Exception as e:
            logging.error(f"Failed to send daily summary to user {user.id}: {e}")



async def scheduler_job(bot: Bot):
    """Wrapper for the send_daily_summary function to be used with APScheduler."""
    await send_daily_summary(bot)