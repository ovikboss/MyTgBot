from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import  types

from .registration import activity_level_entered
from .router import router
from core.DB.db import  db
from core.checksubscribe.checker import subscription_required

@router.message(Command("show_bmr"))
@subscription_required
async def command_bmr(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    bmr = db.get_data_bmr(user_id)
    if bmr:
        activity_level = db.get_activity_level(user_id)
        await message.reply(f"Ваш уровень базального метаболизма - {bmr:.2f} ккал\nКалорий с учетом вашей активности - {bmr * activity_level:.2f} ")
    else:
        await message.reply(f"Нужно зарегистрироваться")





