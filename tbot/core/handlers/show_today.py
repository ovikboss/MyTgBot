from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import  types

from .router import router
from core.DB.db import  db
from core.checksubscribe.checker import subscription_required

@router.message(Command("show_today"))
@subscription_required
async def show_today_command(message: types.Message):
    """Показывает записи о еде за сегодня."""
    user_id = message.from_user.id
    today_entries = db.get_today_food(user_id)
    if today_entries:
        text = "Сегодня ты ел(а):\n"
        total_calories = 0
        for entry in today_entries:
            text += (
                f"- {entry.name}: {entry.calories} ккал ({entry.timestamp.strftime('%H:%M')})\n"
            )
            total_calories += entry.calories
        text += f"\nВсего калорий сегодня: {total_calories}"
        await message.reply(text)
    else:
        await message.reply("Сегодня ты еще ничего не ел(а).")